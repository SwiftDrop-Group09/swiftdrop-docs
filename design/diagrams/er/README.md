# Entity Relationship Diagrams

> **Status:** Draft  
> **Last Updated:** October 2026

This document contains the Entity Relationship (ER) diagrams for all four SwiftDrop databases and protected proof storage. Each database is owned exclusively by its corresponding bounded context, following the [database-per-service](../../architecture/data-architecture.md) pattern.

---

## 1. Identity Database

The Identity database stores user accounts, roles, external identity provider links, refresh sessions, and audit records.

```mermaid
erDiagram
    users {
        uuid id PK
        varchar email UK
        varchar password_hash
        varchar name
        varchar phone
        boolean is_active
        timestamp created_at
        timestamp updated_at
    }

    roles {
        uuid id PK
        varchar name UK
    }

    user_roles {
        uuid user_id FK
        uuid role_id FK
    }

    external_identities {
        uuid id PK
        uuid user_id FK
        varchar provider
        varchar provider_subject
        timestamp linked_at
    }

    refresh_sessions {
        uuid id PK
        uuid user_id FK
        varchar token_hash
        varchar ip_address
        varchar user_agent
        timestamp created_at
        timestamp expires_at
        boolean revoked
    }

    audit_logs {
        uuid id PK
        uuid user_id FK
        varchar action
        varchar resource
        varchar detail
        varchar ip_address
        timestamp timestamp
    }

    users ||--o{ user_roles : "has"
    roles ||--o{ user_roles : "assigned to"
    users ||--o{ external_identities : "linked via"
    users ||--o{ refresh_sessions : "maintains"
    users ||--o{ audit_logs : "generates"
```

### Key Relationships

- A **user** can have multiple **roles** (many-to-many via `user_roles`).
- A **user** can have multiple **external identities** (e.g., Google, future providers).
- A **user** can have multiple active **refresh sessions** across devices.
- All significant actions generate **audit log** entries.

---

## 2. Delivery Database

The Delivery database stores the core business data for parcel booking, courier assignment, delivery tracking, pricing, and the transactional outbox.

```mermaid
erDiagram
    parcels {
        uuid id PK
        uuid customer_id
        varchar status
        varchar size_category
        decimal weight_kg
        varchar pickup_address
        varchar pickup_contact
        varchar dropoff_address
        varchar dropoff_contact
        uuid zone_id FK
        varchar notes
        timestamp created_at
        timestamp updated_at
    }

    assignments {
        uuid id PK
        uuid parcel_id FK
        uuid courier_id
        varchar status
        timestamp assigned_at
        timestamp picked_up_at
        timestamp delivered_at
    }

    price_snapshots {
        uuid id PK
        uuid parcel_id FK
        uuid zone_id
        decimal base_fee
        decimal weight_fee
        decimal distance_fee
        decimal total
        timestamp calculated_at
    }

    booking_history {
        uuid id PK
        uuid parcel_id FK
        varchar from_status
        varchar to_status
        uuid changed_by
        varchar change_reason
        timestamp timestamp
    }

    idempotency_keys {
        varchar key PK
        uuid parcel_id FK
        timestamp created_at
    }

    outbox_messages {
        uuid id PK
        varchar event_type
        jsonb payload
        timestamp created_at
        timestamp published_at
    }

    proof_metadata {
        uuid id PK
        uuid parcel_id FK
        varchar type
        varchar storage_ref
        timestamp uploaded_at
        uuid uploaded_by
    }

    delivery_zones {
        uuid id PK
        varchar name UK
        varchar description
        jsonb boundaries
        boolean is_active
    }

    pricing_tiers {
        uuid id PK
        uuid zone_id FK
        varchar size_category
        decimal base_rate
        decimal per_kg_rate
        boolean is_active
    }

    parcels ||--o{ assignments : "assigned via"
    parcels ||--|| price_snapshots : "priced at"
    parcels ||--o{ booking_history : "history of"
    parcels ||--o| idempotency_keys : "deduplicated by"
    parcels ||--o| proof_metadata : "proven by"
    delivery_zones ||--o{ parcels : "located in"
    delivery_zones ||--o{ pricing_tiers : "priced by"
```

### Key Relationships

- A **parcel** is the central entity, linked to assignments, pricing, history, and proof.
- Each **parcel** has exactly one **price snapshot** captured at booking time.
- **Assignments** track the courier lifecycle for a parcel (assigned → picked up → delivered).
- **Booking history** records every status transition for audit purposes.
- **Outbox messages** are independent of parcels — they relay domain events to RabbitMQ.
- **Delivery zones** and **pricing tiers** are admin-managed configuration data.

### Parcel Status Lifecycle

```mermaid
stateDiagram-v2
    [*] --> Pending : Booking created
    Pending --> Confirmed : Fee accepted
    Confirmed --> Assigned : Courier assigned
    Assigned --> PickedUp : Courier picks up
    PickedUp --> InTransit : In delivery
    InTransit --> Delivered : Proof uploaded
    InTransit --> Failed : Delivery failed
    Failed --> Assigned : Reassigned
    Delivered --> [*]
```

---

## 3. Merchant Database

The Merchant database stores merchant business profiles, API credentials, webhook configurations, and delivery attempt tracking.

```mermaid
erDiagram
    businesses {
        uuid id PK
        uuid user_id
        varchar business_name
        varchar contact_email
        varchar contact_phone
        varchar status
        timestamp registered_at
        timestamp approved_at
        uuid approved_by
    }

    api_keys {
        uuid id PK
        uuid business_id FK
        varchar key_hash
        varchar key_prefix
        varchar scopes
        boolean is_active
        timestamp created_at
        timestamp revoked_at
    }

    webhook_subscriptions {
        uuid id PK
        uuid business_id FK
        varchar url
        varchar events
        varchar secret_hash
        boolean is_active
        timestamp created_at
    }

    encrypted_secrets {
        uuid id PK
        uuid business_id FK
        bytea encrypted_value
        integer key_version
        timestamp created_at
    }

    inbox_jobs {
        uuid id PK
        uuid business_id FK
        jsonb order_payload
        varchar status
        varchar error_message
        timestamp received_at
        timestamp processed_at
    }

    delivery_attempts {
        uuid id PK
        uuid subscription_id FK
        varchar event_id
        integer attempt_number
        integer status_code
        varchar response_body
        timestamp attempted_at
        timestamp next_retry_at
    }

    businesses ||--o{ api_keys : "authenticates with"
    businesses ||--o{ webhook_subscriptions : "subscribes via"
    businesses ||--o{ encrypted_secrets : "secured by"
    businesses ||--o{ inbox_jobs : "receives orders as"
    webhook_subscriptions ||--o{ delivery_attempts : "delivered through"
```

### Key Relationships

- A **business** (merchant) is the root entity, owning API keys, webhook subscriptions, and secrets.
- **API keys** are stored as hashed values; only the prefix is readable after creation.
- **Webhook subscriptions** define which events trigger notifications to which URLs.
- **Delivery attempts** track each webhook POST, including response codes for retry logic.
- **Inbox jobs** represent inbound merchant orders queued for processing.
- **Encrypted secrets** store HMAC signing keys for webhook payload verification.

### Merchant Status Lifecycle

```mermaid
stateDiagram-v2
    [*] --> Pending : Registration submitted
    Pending --> Approved : Admin approves
    Pending --> Rejected : Admin rejects
    Approved --> Suspended : Admin suspends
    Suspended --> Approved : Admin reactivates
    Rejected --> [*]
```

---

## 4. Notification Database (Worker Host)

The Notification database is owned by the Notification Consumer component running in the .NET Worker host. It records consumed notification events, scheduled alerts (Email and mock SMS), and transmission audit logs.

```mermaid
erDiagram
    inbox_messages {
        uuid id PK
        varchar event_id UK
        varchar event_type
        jsonb payload
        timestamp received_at
        timestamp processed_at
    }

    notification_jobs {
        uuid id PK
        varchar recipient
        varchar channel
        varchar template_id
        jsonb template_data
        varchar status
        timestamp created_at
        timestamp scheduled_at
    }

    delivery_attempts {
        uuid id PK
        uuid job_id FK
        int attempt_number
        varchar status
        varchar error_message
        varchar provider_response
        timestamp attempted_at
    }

    notification_logs {
        uuid id PK
        uuid job_id FK
        varchar recipient
        varchar channel
        varchar status
        timestamp sent_at
    }

    notification_jobs ||--o{ delivery_attempts : "tracked by"
    notification_jobs ||--o| notification_logs : "records"
```

### Key Responsibilities
- **Inbox Pattern (`inbox_messages`):** Ensures idempotent consumption of notification domain events emitted by Delivery and Merchant services via RabbitMQ.
- **Dispatch Jobs (`notification_jobs`):** Manages asynchronous customer notifications (e.g., booking confirmation, courier arrival) across Email and SMS channels.
- **Reliability (`delivery_attempts`):** Logs delivery status and backoff attempts if third-party notification providers fail.

---

## 5. Protected Proof Storage

Protected Proof Storage is an encrypted object store (MinIO in local development / AWS S3 in cloud deployments) managed with access control exclusively mediated by the Delivery Operations API.

```mermaid
flowchart LR
    CourierApp["Courier Device"] -->|Upload Signature / Photo| DeliveryAPI["Delivery Operations API"]
    DeliveryAPI -->|Commit storage reference| DeliveryDB[("Delivery DB\nproof_metadata")]
    DeliveryAPI -->|Write encrypted binary| ProofBucket[("Protected Proof Bucket\nMinIO / S3")]
    CustomerApp["Customer / Dispatcher"] -->|Request Proof View| DeliveryAPI
    DeliveryAPI -.->|Issue 15-min pre-signed URL| ProofBucket
```

- **Authorized Access:** Direct public access to the storage bucket is permanently disabled.
- **Short-Lived URLs:** Viewing proofs requires requesting a pre-signed, time-limited URL (15-minute expiration) generated by the Delivery Operations API following resource ownership authorization.

---

## References

- [Data Architecture](../../../architecture/data-architecture.md)
- [Service Catalog](../../../architecture/service-catalog.md)
- [Architecture Diagram](../architecture/architecture.md)
