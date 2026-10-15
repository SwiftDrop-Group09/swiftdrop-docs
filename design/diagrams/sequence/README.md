# Sequence Diagrams

> **Status:** Draft  
> **Last Updated:** October 2026

This document contains sequence diagrams for the critical workflows in the SwiftDrop system. Each diagram shows the interaction between actors, services, and infrastructure components for a specific use case.

---

## 1. User Authentication — Google OIDC Login

This sequence shows how a user authenticates through Google OIDC and receives application-specific JWTs from the Identity API.

```mermaid
sequenceDiagram
    actor User
    participant SPA as React SPA
    participant Gateway as API Gateway
    participant Identity as Identity API
    participant Google as Google OIDC
    participant DB as Identity DB

    User->>SPA: Click "Sign in with Google"
    SPA->>Google: Redirect to Google consent screen
    Google->>User: Show consent prompt
    User->>Google: Grant consent
    Google->>SPA: Authorization code (redirect)

    SPA->>Gateway: POST /api/auth/google {code}
    Gateway->>Identity: Forward request

    Identity->>Google: Exchange code for tokens
    Google-->>Identity: ID token + access token

    Identity->>Identity: Validate ID token (signature, issuer, audience)
    Identity->>DB: Find or create user by provider_subject
    DB-->>Identity: User record

    Identity->>DB: Create refresh session
    Identity->>Identity: Generate application JWT (user_id, roles, exp)

    Identity-->>Gateway: {access_token, refresh_token, expires_in}
    Gateway-->>SPA: {access_token, refresh_token, expires_in}
    SPA->>SPA: Store tokens, update auth state
    SPA-->>User: Redirect to dashboard
```

---

## 2. JWT Token Refresh

This sequence shows how the React SPA refreshes an expired JWT without requiring the user to re-authenticate with Google.

```mermaid
sequenceDiagram
    actor User
    participant SPA as React SPA
    participant Gateway as API Gateway
    participant Identity as Identity API
    participant DB as Identity DB

    Note over SPA: Access token expired

    SPA->>Gateway: POST /api/auth/refresh {refresh_token}
    Gateway->>Identity: Forward request

    Identity->>DB: Lookup refresh session by token hash
    DB-->>Identity: Session (valid, not expired, not revoked)

    Identity->>DB: Revoke current refresh session
    Identity->>DB: Create new refresh session (rotation)
    Identity->>Identity: Generate new application JWT

    Identity-->>Gateway: {access_token, refresh_token, expires_in}
    Gateway-->>SPA: {access_token, refresh_token, expires_in}
    SPA->>SPA: Replace stored tokens
```

---

## 3. Parcel Booking Flow

This sequence shows the end-to-end flow when a customer creates a new parcel booking, including fee estimation, idempotency, and event publishing via the transactional outbox.

```mermaid
sequenceDiagram
    actor Customer
    participant SPA as React SPA
    participant Gateway as API Gateway
    participant Delivery as Delivery Ops API
    participant DB as Delivery DB
    participant Relay as Outbox Relay
    participant Broker as RabbitMQ

    Customer->>SPA: Fill booking form (addresses, parcel details)

    Note over SPA,Delivery: Step 1: Fee Estimation
    SPA->>Gateway: POST /api/bookings/estimate {size, weight, zone}
    Gateway->>Delivery: Forward
    Delivery->>DB: Lookup pricing tier for zone + size
    DB-->>Delivery: Pricing tier
    Delivery->>Delivery: Calculate fee (base + weight + distance)
    Delivery-->>Gateway: {estimated_fee, breakdown}
    Gateway-->>SPA: {estimated_fee, breakdown}
    SPA-->>Customer: Display fee estimate

    Customer->>SPA: Confirm booking

    Note over SPA,Delivery: Step 2: Create Booking (idempotent)
    SPA->>Gateway: POST /api/bookings {details, Idempotency-Key: abc-123}
    Gateway->>Delivery: Forward

    Delivery->>DB: Check idempotency key "abc-123"
    DB-->>Delivery: Key not found (new request)

    Delivery->>DB: BEGIN TRANSACTION
    Delivery->>DB: INSERT parcel (status: Pending)
    Delivery->>DB: INSERT price_snapshot
    Delivery->>DB: INSERT idempotency_key
    Delivery->>DB: INSERT outbox_message (ParcelBooked event)
    Delivery->>DB: COMMIT

    Delivery-->>Gateway: 201 Created {parcel_id, status, fee}
    Gateway-->>SPA: 201 Created {parcel_id, status, fee}
    SPA-->>Customer: Booking confirmation

    Note over Relay,Broker: Step 3: Async Event Publishing
    Relay->>DB: Poll unpublished outbox messages
    DB-->>Relay: ParcelBooked event
    Relay->>Broker: Publish ParcelBooked
    Relay->>DB: Mark message as published
```

---

## 4. Courier Assignment and Delivery Lifecycle

This sequence shows how a dispatcher assigns a courier and the courier completes the delivery with proof upload.

```mermaid
sequenceDiagram
    actor Dispatcher
    actor Courier
    participant SPA as React SPA
    participant Gateway as API Gateway
    participant Delivery as Delivery Ops API
    participant DB as Delivery DB
    participant Broker as RabbitMQ

    Note over Dispatcher: View unassigned parcels
    Dispatcher->>SPA: Open dispatch dashboard
    SPA->>Gateway: GET /api/dispatch/unassigned
    Gateway->>Delivery: Forward
    Delivery->>DB: Query parcels (status: Confirmed)
    Delivery-->>SPA: List of unassigned parcels

    Note over Dispatcher: Assign courier
    Dispatcher->>SPA: Select courier, confirm assignment
    SPA->>Gateway: POST /api/dispatch/assign {parcel_id, courier_id}
    Gateway->>Delivery: Forward
    Delivery->>DB: BEGIN TRANSACTION
    Delivery->>DB: INSERT assignment
    Delivery->>DB: UPDATE parcel status → Assigned
    Delivery->>DB: INSERT booking_history
    Delivery->>DB: INSERT outbox_message (CourierAssigned)
    Delivery->>DB: COMMIT
    Delivery-->>SPA: 200 OK {assignment_id}

    Note over Courier: Pickup parcel
    Courier->>SPA: Tap "Picked Up"
    SPA->>Gateway: PUT /api/parcels/{id}/status {status: PickedUp}
    Gateway->>Delivery: Forward
    Delivery->>DB: UPDATE parcel status → PickedUp
    Delivery->>DB: INSERT outbox_message (ParcelPickedUp)
    Delivery-->>SPA: 200 OK

    Note over Courier: Complete delivery
    Courier->>SPA: Tap "Delivered" + upload photo
    SPA->>Gateway: POST /api/parcels/{id}/proof {photo}
    Gateway->>Delivery: Forward
    Delivery->>DB: INSERT proof_metadata
    Delivery->>DB: UPDATE parcel status → Delivered
    Delivery->>DB: INSERT outbox_message (ParcelDelivered)
    Delivery-->>SPA: 200 OK

    Broker-->>Broker: Events distributed to subscribers
```

---

## 5. Merchant Order Submission via API

This sequence shows how an external merchant system submits a delivery order using API key authentication.

```mermaid
sequenceDiagram
    participant MerchantSys as Merchant System
    participant Gateway as API Gateway
    participant Merchant as Merchant API
    participant DB as Merchant DB
    participant Delivery as Delivery Ops API
    participant DelDB as Delivery DB

    MerchantSys->>Gateway: POST /api/merchant-orders<br/>X-API-Key: swd_live_abc123<br/>{order details}
    Gateway->>Merchant: Forward

    Merchant->>DB: Validate API key hash + scopes
    DB-->>Merchant: Key valid, business_id resolved

    Merchant->>DB: INSERT inbox_job (status: Received)
    Merchant->>Merchant: Validate order payload

    Merchant->>Delivery: gRPC CreateBooking(order, service_jwt)
    Delivery->>Delivery: Validate service JWT via JWKS
    Delivery->>DelDB: INSERT parcel + price_snapshot + outbox_message
    Delivery-->>Merchant: BookingResponse {parcel_id, status, fee}

    Merchant->>DB: UPDATE inbox_job (status: Processed, parcel_id)

    Merchant-->>Gateway: 201 Created {order_id, parcel_id, status}
    Gateway-->>MerchantSys: 201 Created {order_id, parcel_id, status}
```

---

## 6. Webhook Delivery to Merchant

This sequence shows how delivery status events are propagated to merchant webhook endpoints with retry logic.

```mermaid
sequenceDiagram
    participant Delivery as Delivery Ops API
    participant DB as Delivery DB
    participant Relay as Outbox Relay
    participant Broker as RabbitMQ
    participant Worker as Background Worker
    participant MerchantAPI as Merchant API
    participant MerDB as Merchant DB
    participant Webhook as Merchant Webhook URL

    Note over Delivery: Parcel status changes to "Delivered"
    Delivery->>DB: INSERT outbox_message (ParcelDelivered)

    Relay->>DB: Poll unpublished messages
    Relay->>Broker: Publish ParcelDelivered event
    Broker->>Worker: Consume ParcelDelivered

    Worker->>MerchantAPI: Get webhook subscriptions for event
    MerchantAPI->>MerDB: Query active subscriptions
    MerDB-->>MerchantAPI: Subscription list
    MerchantAPI-->>Worker: [{url, secret_hash}]

    Worker->>Worker: Build payload + HMAC-SHA256 signature

    Worker->>Webhook: POST {event, data}<br/>X-SwiftDrop-Signature: sha256=...

    alt Success (2xx)
        Webhook-->>Worker: 200 OK
        Worker->>MerDB: INSERT delivery_attempt (status: 200)
    else Failure (5xx / timeout)
        Webhook-->>Worker: 500 Error
        Worker->>MerDB: INSERT delivery_attempt (status: 500)
        Worker->>Worker: Schedule retry (exponential backoff)
        Note over Worker: Retry 1: 30s, 2: 2min, 3: 10min, 4: 1h, 5: 6h
    end
```

---

## References

- [Architecture Diagram](../architecture/architecture.md)
- [Integration Design](../../../integration/integration-design.md)
- [Authentication](../../../security/authentication.md)
- [Merchant Webhooks](../../../integration/merchant-webhooks.md)
- [Data Architecture](../../../architecture/data-architecture.md)
