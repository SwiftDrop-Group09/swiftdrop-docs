# gRPC Services Specification

> **Status:** Draft  
> **Version:** 1.0  
> **Last Updated:** October 2026  

---

## 1. Overview

While external clients communicate via REST, GraphQL, and WebSockets through the YARP Gateway, internal microservices utilize **gRPC over HTTP/2** with Protocol Buffers v3 for synchronous, strongly-typed, low-latency inter-service RPC.

```mermaid
flowchart LR
    subgraph SvcDelivery["Delivery Service"]
        DelApp["Delivery Domain Logic"]
        DelClient["Identity gRPC Client"]
    end

    subgraph SvcMerchant["Merchant Service"]
        MerchApp["Merchant Domain Logic"]
        MerchClient["Delivery gRPC Client"]
    end

    subgraph SvcIdentity["Identity Service"]
        IdGrpc["Identity gRPC Server<br/>(:5101)"]
    end

    subgraph SvcDeliveryServer["Delivery Operations"]
        DelGrpc["Delivery gRPC Server<br/>(:5102)"]
    end

    DelClient -->|mTLS / HTTP/2<br/>ValidateToken(), GetUserSummary()| IdGrpc
    MerchClient -->|mTLS / HTTP/2<br/>ValidateCourierCapacity()| DelGrpc
```

### 1.1. Why gRPC for Internal Communication?
- **High Performance:** Binary serialization via Protobuf v3 is ~5-8x faster and ~60% smaller than JSON over HTTP/1.1.
- **Contract-First Development:** `.proto` IDL files generate strongly-typed C# client and server stubs at build time, preventing runtime schema mismatches.
- **Multiplexing:** Single persistent TCP connection per service pair handles concurrent RPC calls without head-of-line blocking.
- **Deadlines & Cancellation:** Native propagation of timeouts and cancellation tokens through `CancellationToken`.

---

## 2. Protobuf Service Definitions

### 2.1. Identity gRPC Contract (`identity.proto`)

Used by Delivery Operations and Merchant Integration services to validate user claims and enrich manifests with user profile summaries.

```protobuf
syntax = "proto3";

package swiftdrop.identity.v1;

option csharp_namespace = "SwiftDrop.Identity.Grpc";

// ----------------------------------------------------
// Service Definition
// ----------------------------------------------------

service IdentityInternalService {
  // Validates an active JWT token and extracts authorized user claims
  rpc ValidateToken (ValidateTokenRequest) returns (ValidateTokenResponse);

  // Retrieves basic user profile summary for manifest generation
  rpc GetUserSummary (GetUserSummaryRequest) returns (GetUserSummaryResponse);

  // Batch query to resolve multiple user IDs in a single network round-trip
  rpc BatchGetUsers (BatchGetUsersRequest) returns (BatchGetUsersResponse);
}

// ----------------------------------------------------
// Request & Response Messages
// ----------------------------------------------------

message ValidateTokenRequest {
  string token = 1;
}

message ValidateTokenResponse {
  bool is_valid = 1;
  string user_id = 2;
  string email = 3;
  string role = 4;
  repeated string permissions = 5;
  int64 expires_at_unix = 6;
  string error_message = 7;
}

message GetUserSummaryRequest {
  string user_id = 1;
}

message GetUserSummaryResponse {
  string user_id = 1;
  string full_name = 2;
  string email = 3;
  string phone_number = 4;
  string role = 5;
  bool is_active = 6;
}

message BatchGetUsersRequest {
  repeated string user_ids = 1;
}

message BatchGetUsersResponse {
  map<string, GetUserSummaryResponse> users = 1;
}
```

---

### 2.2. Delivery Operations gRPC Contract (`delivery.proto`)

Used by the Merchant Integration service to verify courier capacity and schedule automated pickups for bulk consignments.

```protobuf
syntax = "proto3";

package swiftdrop.delivery.v1;

option csharp_namespace = "SwiftDrop.Delivery.Grpc";

// ----------------------------------------------------
// Service Definition
// ----------------------------------------------------

service DeliveryInternalService {
  // Checks if a designated courier or zone has capacity for additional parcels
  rpc CheckZoneCapacity (CheckZoneCapacityRequest) returns (CheckZoneCapacityResponse);

  // Synchronously registers an internal parcel reservation for bulk merchant orders
  rpc ReserveParcelSlot (ReserveParcelSlotRequest) returns (ReserveParcelSlotResponse);

  // Queries current delivery execution state
  rpc GetDeliveryStatus (GetDeliveryStatusRequest) returns (GetDeliveryStatusResponse);
}

// ----------------------------------------------------
// Messages
// ----------------------------------------------------

message CheckZoneCapacityRequest {
  string postal_code = 1;
  string province = 2;
  int32 required_parcel_slots = 3;
}

message CheckZoneCapacityResponse {
  bool has_capacity = 1;
  int32 available_couriers_count = 2;
  int32 estimated_pickup_window_minutes = 3;
}

message ReserveParcelSlotRequest {
  string merchant_id = 1;
  string batch_reference = 2;
  int32 parcel_count = 3;
  double total_weight_kg = 4;
}

message ReserveParcelSlotResponse {
  bool success = 1;
  string reservation_id = 2;
  int64 expires_at_unix = 3;
  string rejection_reason = 4;
}

message GetDeliveryStatusRequest {
  string tracking_number = 1;
}

message GetDeliveryStatusResponse {
  string tracking_number = 1;
  string status = 2;
  string assigned_courier_id = 3;
  string assigned_courier_name = 4;
  int64 last_updated_unix = 5;
}
```

---

### 2.3. Merchant gRPC Contract (`merchant.proto`)

Used by the Gateway and Delivery service to validate merchant credentials, enterprise credit limits, and subscription quotas.

```protobuf
syntax = "proto3";

package swiftdrop.merchant.v1;

option csharp_namespace = "SwiftDrop.Merchant.Grpc";

// ----------------------------------------------------
// Service Definition
// ----------------------------------------------------

service MerchantInternalService {
  // Validates API Key and retrieves associated merchant account context
  rpc ValidateApiKey (ValidateApiKeyRequest) returns (ValidateApiKeyResponse);

  // Checks merchant account status, credit limit, and daily quota
  rpc CheckMerchantQuota (CheckMerchantQuotaRequest) returns (CheckMerchantQuotaResponse);
}

// ----------------------------------------------------
// Messages
// ----------------------------------------------------

message ValidateApiKeyRequest {
  string api_key = 1;
}

message ValidateApiKeyResponse {
  bool is_valid = 1;
  string merchant_id = 2;
  string business_name = 3;
  string tier = 4; // "Starter", "Growth", "Enterprise"
  bool is_active = 5;
  string error_message = 6;
}

message CheckMerchantQuotaRequest {
  string merchant_id = 1;
  int32 parcel_count = 2;
}

message CheckMerchantQuotaResponse {
  bool is_allowed = 1;
  int32 remaining_daily_quota = 2;
  double available_credit_limit = 3;
  string rejection_reason = 4;
}
```

---

## 3. Security & Transport Configuration

### 3.1. Mutual TLS (mTLS) in Production
All internal gRPC communication occurs within the private virtual network or Kubernetes cluster. In production environments:
- Microservices authenticate one another using **x509 client certificates** issued by an internal Certificate Authority (Vault / cert-manager).
- HTTP/2 with ALPN (`h2`) is enforced on gRPC ports (5101–5103).

### 3.2. Channel Configuration in C# (.NET 8)

```csharp
// Program.cs - Delivery Operations Service registering Identity gRPC Client
builder.Services.AddGrpcClient<IdentityInternalService.IdentityInternalServiceClient>(o =>
{
    o.Address = new Uri(builder.Configuration["GrpcServices:IdentityUrl"] ?? "http://identity-service:5101");
})
.ConfigureChannel(options =>
{
    options.HttpHandler = new SocketsHttpHandler
    {
        EnableMultipleHttp2Connections = true,
        KeepAlivePingDelay = TimeSpan.FromSeconds(30),
        KeepAlivePingTimeout = TimeSpan.FromSeconds(5)
    };
    options.MaxReceiveMessageSize = 4 * 1024 * 1024; // 4MB
});
```

---

## 4. gRPC Status Codes & Error Handling

All gRPC services return standard gRPC status codes according to Google Cloud RPC specification:

| gRPC Status Code | Numeric | Trigger Scenario in SwiftDrop |
|---|---|---|
| `OK` | 0 | RPC executed successfully |
| `INVALID_ARGUMENT` | 3 | Missing required field, malformed ID format |
| `NOT_FOUND` | 5 | User ID, merchant ID, or tracking number does not exist |
| `ALREADY_EXISTS` | 6 | Attempted to reserve an existing reservation reference |
| `PERMISSION_DENIED` | 7 | Merchant account suspended or inactive |
| `RESOURCE_EXHAUSTED` | 8 | Merchant daily parcel quota or zone courier capacity exceeded |
| `DEADLINE_EXCEEDED` | 4 | Downstream database query or service timeout exceeded |
| `UNAVAILABLE` | 14 | Upstream microservice restarting or network partition |
