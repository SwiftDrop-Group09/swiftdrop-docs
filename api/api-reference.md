# API Reference Architecture & Inventory

> **Status:** Draft  
> **Version:** 1.0  
> **Last Updated:** October 2026  

---

## 1. Overview

The SwiftDrop platform exposes a multi-protocol API surface tailored to diverse consumer personas: web/mobile single-page applications, merchant enterprise backends, mobile courier applications, and internal microservices. All external client traffic routes through a unified **YARP (Yet Another Reverse Proxy)** API Gateway, ensuring centralized authentication, rate limiting, TLS termination, and observability.

```mermaid
flowchart TD
    subgraph Clients["Client Layer"]
        SPA["Customer & Merchant Web (React/Vite)"]
        Mobile["Courier Mobile App (Flutter/MAUI)"]
        MerchantBackend["Merchant ERP/Store Backend"]
        Dispatcher["Dispatcher Operations Dashboard"]
    end

    subgraph Gateway["YARP API Gateway (:5000)"]
        AuthFilter["JWT / API Key Validation"]
        RateLimit["Rate Limiting & Throttling"]
        Router["Route Dispatcher & Path Rewriter"]
    end

    subgraph Services["Microservices Cluster"]
        Identity["Identity API (:5001)<br/>REST (ASP.NET Core)"]
        Delivery["Delivery API (:5002)<br/>REST + GraphQL + SSE"]
        Merchant["Merchant API (:5003)<br/>REST (ASP.NET Core)"]
        Realtime["Real-time Tracking Hub (:5004)<br/>WebSocket / SSE"]
    end

    subgraph InternalRPC["Internal gRPC Mesh (HTTP/2 mTLS)"]
        IdentityGRPC["Identity gRPC (:5101)"]
        DeliveryGRPC["Delivery gRPC (:5102)"]
        MerchantGRPC["Merchant gRPC (:5103)"]
    end

    SPA -->|HTTPS / REST / GraphQL| Gateway
    Mobile -->|HTTPS / REST| Gateway
    MerchantBackend -->|HTTPS / REST + API Key| Gateway
    Dispatcher -->|HTTPS / REST + SSE| Gateway
    Mobile -.->|WebSocket / SSE| Realtime

    Router -->|HTTP / REST| Identity
    Router -->|HTTP / REST / GraphQL| Delivery
    Router -->|HTTP / REST| Merchant
    Router -->|HTTP / SSE| Realtime

    Delivery -.->|gRPC| IdentityGRPC
    Merchant -.->|gRPC| DeliveryGRPC
    Merchant -.->|gRPC| IdentityGRPC
```

---

## 2. Base URLs & Environment Endpoints

| Environment | Base URL | YARP Gateway Host | Health Check Endpoint |
|---|---|---|---|
| **Local Development** | `http://localhost:5000` | `gateway.swiftdrop.local` | `http://localhost:5000/health` |
| **Docker Compose** | `http://gateway:80` | `swiftdrop-gateway` | `http://gateway:80/health` |
| **Staging** | `https://staging-api.swiftdrop.io` | `alb.staging.swiftdrop.internal` | `https://staging-api.swiftdrop.io/health` |
| **Production** | `https://api.swiftdrop.io` | `alb.prod.swiftdrop.internal` | `https://api.swiftdrop.io/health` |

---

## 3. Protocol Matrix & Selection Guidelines

| Protocol | Primary Use Case | Primary Consumers | Transport & Port | Serialization | Specification Link |
|---|---|---|---|---|---|
| **REST (JSON)** | CRUD operations, standard transactional interactions, merchant integration | Web SPAs, Mobile Apps, Merchant Systems | HTTPS (Port 443 / 5000) | JSON (camelCase) | [REST API Specification](./rest-api.md) |
| **GraphQL** | Multi-entity dashboards, composite tracking views, client-controlled fetching | Customer Portal, Dispatcher Dashboard | HTTPS POST `/graphql` | JSON | [GraphQL API Specification](./graphql-api.md) |
| **gRPC** | High-throughput, low-latency inter-service synchronous calls | Microservices (Internal) | HTTP/2 Cleartext / mTLS (Ports 5101–5103) | Protocol Buffers v3 | [gRPC Services Specification](./grpc-services.md) |
| **WebSocket** | Bidirectional courier GPS streaming, driver location updates | Courier Mobile App, Dispatcher Live Map | WSS (Port 443 / 5004) | JSON Text Frames | [WebSocket Protocol](./websocket-protocol.md) |
| **Server-Sent Events (SSE)** | Unidirectional parcel status updates, tracking timeline feeds | Customer Web Tracking, Merchant Live Feed | HTTPS (Port 443 / 5002) | `text/event-stream` (JSON) | [Real-Time Tracking Integration](../integration/realtime-tracking.md) |

---

## 4. Service Endpoint Inventory

### 4.1. Identity Service (`http://identity-service:8080` / Gateway Prefix: `/api/v1/auth`, `/api/v1/users`)

| Method | Endpoint | Description | Auth Required | Roles Permitted |
|---|---|---|---|---|
| `POST` | `/api/v1/auth/google` | Exchange Google OIDC ID token for JWT key pair | No | Public |
| `POST` | `/api/v1/auth/refresh` | Rotate expired access token using refresh token | No (Bearer) | Public / Refresh |
| `POST` | `/api/v1/auth/logout` | Revoke active refresh token and invalidate session | Yes | Any Authenticated |
| `GET` | `/api/v1/users/me` | Fetch authenticated user's profile and roles | Yes | Any Authenticated |
| `PUT` | `/api/v1/users/me` | Update authenticated user's contact information | Yes | Any Authenticated |
| `GET` | `/api/v1/users` | List platform users with pagination & role filtering | Yes | `Admin` |
| `PUT` | `/api/v1/users/{id}/role` | Assign or modify role assignment for a user | Yes | `Admin` |

### 4.2. Delivery Operations Service (`http://delivery-service:8080` / Gateway Prefix: `/api/v1/parcels`, `/api/v1/deliveries`, `/api/v1/couriers`)

| Method | Endpoint | Description | Auth Required | Roles Permitted |
|---|---|---|---|---|
| `POST` | `/api/v1/parcels` | Book a new standard or express parcel | Yes | `Customer`, `Merchant`, `Admin` |
| `GET` | `/api/v1/parcels/{id}` | Retrieve comprehensive parcel details | Yes | Owner, `Dispatcher`, `Admin` |
| `GET` | `/api/v1/parcels/track/{trackingNumber}` | Public tracking status and timeline history | No | Public |
| `GET` | `/api/v1/parcels` | Query parcels with status, date, and customer filters | Yes | `Dispatcher`, `Admin` |
| `PUT` | `/api/v1/parcels/{id}/cancel` | Cancel an unassigned or pending parcel | Yes | Owner, `Dispatcher`, `Admin` |
| `POST` | `/api/v1/deliveries/assign` | Assign courier to parcel (manual or auto) | Yes | `Dispatcher`, `Admin` |
| `PUT` | `/api/v1/deliveries/{id}/status` | Advance delivery state (InTransit, Delivered, Failed) | Yes | `Courier`, `Dispatcher` |
| `POST` | `/api/v1/deliveries/{id}/pod` | Submit Proof of Delivery (Signature + Photo) | Yes | `Courier` |
| `GET` | `/api/v1/couriers/available` | List couriers currently on-duty and within capacity | Yes | `Dispatcher`, `Admin` |
| `PUT` | `/api/v1/couriers/status` | Update courier duty status (`OnDuty`, `OffDuty`) | Yes | `Courier` |
| `GET` | `/api/v1/deliveries/courier/{courierId}/active` | Retrieve active delivery manifest for a courier | Yes | Assigned `Courier`, `Dispatcher` |

### 4.3. Merchant Integration Service (`http://merchant-service:8080` / Gateway Prefix: `/api/v1/merchants`, `/api/v1/merchant`)

| Method | Endpoint | Description | Auth Required | Roles Permitted |
|---|---|---|---|---|
| `POST` | `/api/v1/merchants/register` | Register new merchant business account | Yes | Authenticated User |
| `GET` | `/api/v1/merchants/me` | Fetch merchant profile, approval status, and quota | Yes | `Merchant` |
| `PUT` | `/api/v1/merchants/{id}/status` | Approve, suspend, or reject merchant onboarding | Yes | `Admin` |
| `POST` | `/api/v1/merchants/api-keys` | Generate a new merchant API key | Yes | `Merchant` |
| `DELETE` | `/api/v1/merchants/api-keys/{keyId}` | Revoke an existing API key | Yes | `Merchant` |
| `POST` | `/api/v1/merchant/parcels/bulk` | Bulk parcel creation endpoint (max 100/batch) | API Key / Bearer | `Merchant` |
| `GET` | `/api/v1/merchant/parcels` | List all parcels initiated by merchant | API Key / Bearer | `Merchant` |
| `POST` | `/api/v1/merchant/webhooks` | Register or update merchant webhook endpoint | API Key / Bearer | `Merchant` |
| `GET` | `/api/v1/merchant/webhooks` | Retrieve registered webhook endpoints (masked secret) | API Key / Bearer | `Merchant` |
| `POST` | `/api/v1/merchant/webhooks/{id}/test` | Trigger mock test ping to merchant endpoint | API Key / Bearer | `Merchant` |

---

## 5. Common Standards & Cross-Cutting Conventions

### 5.1. Authentication Headers

SwiftDrop supports dual authentication schemes depending on the caller:

1. **User / Interactive Sessions (JWT Bearer Token):**
   ```http
   Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
   ```
2. **Merchant Automated Systems (API Key):**
   ```http
   X-API-Key: [REDACTED_STRIPE_KEY]...
   ```

### 5.2. Distributed Tracing & Correlation

Every incoming request is tagged with a correlation identifier at the YARP Gateway. If the caller provides one, it is preserved; otherwise, a UUIDv4 is generated. All services must propagate this header across HTTP, gRPC, and RabbitMQ message headers.

```http
X-Correlation-ID: 7a8f5b40-9a2e-4b68-98e3-3e7284b3e811
```

### 5.3. Standard Error Response (RFC 7807 ProblemDetails)

All error responses return HTTP status codes >= 400 and adhere strictly to the IETF RFC 7807 `application/problem+json` specification:

```json
{
  "type": "https://api.swiftdrop.io/errors/validation-failed",
  "title": "One or more validation errors occurred.",
  "status": 400,
  "detail": "The parcel payload contains invalid address coordinates.",
  "instance": "/api/v1/parcels",
  "correlationId": "7a8f5b40-9a2e-4b68-98e3-3e7284b3e811",
  "errors": {
    "recipientAddress.postalCode": [
      "Postal code '00000' is invalid for destination province 'Western'."
    ],
    "weightKg": [
      "Parcel weight must be greater than 0.10 kg."
    ]
  }
}
```

### 5.4. Pagination Conventions

List endpoints accept standard offset-pagination query parameters and return uniform metadata:

**Query Parameters:**
- `page`: Page index (1-based, default: `1`)
- `pageSize`: Number of items per page (default: `20`, max: `100`)
- `sortBy`: Field name to sort by (default: `createdAt`)
- `sortOrder`: `asc` or `desc` (default: `desc`)

**Response Envelope:**
```json
{
  "items": [ ... ],
  "pagination": {
    "currentPage": 1,
    "pageSize": 20,
    "totalCount": 142,
    "totalPages": 8,
    "hasNext": true,
    "hasPrevious": false
  }
}
```

### 5.5. Rate Limiting Headers

YARP implements sliding-window rate limiting per IP address, user ID, or Merchant API Key. When evaluated, the response contains standard rate-limiting headers:

```http
X-RateLimit-Limit: 120
X-RateLimit-Remaining: 114
X-RateLimit-Reset: 1729036800
```

When exceeded, the server returns HTTP status `429 Too Many Requests`:

```http
HTTP/1.1 429 Too Many Requests
Retry-After: 30
Content-Type: application/problem+json

{
  "type": "https://api.swiftdrop.io/errors/rate-limit-exceeded",
  "title": "Rate limit quota exceeded.",
  "status": 429,
  "detail": "You have exceeded your tier allowance of 120 requests/minute. Retry in 30 seconds."
}
```

---

## 6. Detailed API Specifications

Detailed schema definitions, parameters, and code snippets are partitioned across dedicated specification guides:

- **[REST API Reference](./rest-api.md)** — Comprehensive request/response JSON contracts for Identity, Delivery Operations, and Merchant APIs.
- **[GraphQL API Reference](./graphql-api.md)** — GraphQL SDL schema, queries, mutations, and complexity rules.
- **[gRPC Services Reference](./grpc-services.md)** — Protobuf v3 contracts, RPC procedures, and inter-service channels.
- **[WebSocket Protocol Reference](./websocket-protocol.md)** — Live courier GPS protocol, framing, and topic subscription contracts.
