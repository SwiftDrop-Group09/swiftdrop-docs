# Live Demonstration & Viva Presentation Plan

> **Course:** Enterprise Application Development (EAD)  
> **Duration:** 15 Minutes Live Demo + 10 Minutes Panel Q&A  
> **Target Audience:** Academic Evaluation Panel  
> **Format:** Live Environment Demonstration (Docker Compose / Local Cluster)  

---

## 1. Presentation Structure & Time Allocation

| Segment | Duration | Presenter | Primary Topic / Focus | Key Visual / Screen |
|---|:---:|---|---|---|
| **1. Architectural Intro** | 2 mins | Member 1 (Lead) | Problem Statement, C4 Container Topology, ADR Rationale | Slide Deck: C4 Architecture Diagram |
| **2. Customer Journey** | 3 mins | Member 8 & 3 | Google OIDC Sign-In, Parcel Booking, Dynamic Pricing | Web Portal: Customer Booking Wizard |
| **3. Dispatcher Operations** | 3 mins | Member 4 & 8 | Courier Fleet Allocation, Capacity Constraints, Status Sync | Web Portal: Dispatcher Operations Map |
| **4. Courier Execution & PoD** | 3 mins | Member 7 & 4 | Mobile Web Manifest, Live GPS Telemetry, Digital PoD Upload | Mobile View: Courier Manifest & Signature Pad |
| **5. Merchant & Webhooks** | 2 mins | Member 5 & 6 | API Key Auth, Bulk Ingestion, Outbound Webhook Delivery | Postman / Webhook.site live inspector |
| **6. Resilience & Wrap-up** | 2 mins | Member 9 & 10 | Transactional Outbox, RabbitMQ recovery, Test Coverage | Terminal: RabbitMQ UI & Coverlet Report |
| **7. Panel Q&A / Viva** | 10 mins | Full Team | Technical defense of design decisions | Architectural documentation & source code |

---

## 2. Detailed Live Demonstration Script

### Scenario 1: Customer Authentication & Parcel Booking (02:00 – 05:00)
1. **Action:** Open Web Portal (`http://localhost:3000`). Click "Sign in with Google".
2. **System Behavior:** Browser exchanges Google OIDC token at `POST /api/v1/auth/google`. Identity Service validates signature, creates Customer record, and returns RS256 JWT access token (15-minute TTL).
3. **Action:** Navigate to "Book Parcel". Enter Colombo pickup, Kadawatha destination, 2.5kg package, "Express Delivery", and flag "Fragile".
4. **System Behavior:** Client displays real-time pricing breakdown (Base: 450 + Weight: 150 + Express: 200 = 800 LKR). On clicking "Confirm Booking", `POST /api/v1/parcels` commits parcel record and generates tracking number `TRK-202610-A9B8C7`.
5. **Architectural Highlight:** The `ParcelBooked` domain event is committed inside the database transaction via the Transactional Outbox table (zero message loss).

---

### Scenario 2: Dispatcher Control Room & Real-Time Assignment (05:00 – 08:00)
1. **Action:** Switch to Dispatcher account on the Operations Portal.
2. **System Behavior:** Real-time dashboard queries GraphQL endpoint `dispatcherDashboard` retrieving pending parcels and available on-duty couriers.
3. **Action:** Click on pending parcel `TRK-202610-A9B8C7`. Select Courier "Nuwan Fernando" and click "Assign Courier".
4. **System Behavior:** `POST /api/v1/deliveries/assign` validates courier capacity (max 10 active parcels). Courier assignment succeeds; status transitions to `Assigned`.
5. **Architectural Highlight:** Status transition emits `DeliveryAssigned` event over RabbitMQ, synchronizing the customer tracking timeline via Server-Sent Events.

---

### Scenario 3: Courier Mobile Execution, GPS Streaming & PoD (08:00 – 11:00)
1. **Action:** Switch browser to mobile viewport (iPhone 14 frame) representing the Courier Web App.
2. **System Behavior:** Courier views active delivery manifest. Courier clicks "Accept & Pickup".
3. **Action:** Courier status updates to `PickedUp`, then `InTransit`. Courier turns on "Live Tracking".
4. **System Behavior:** Mobile client streams GPS coordinate frames over WebSocket (`wss://api.swiftdrop.io/hubs/delivery`). Dispatcher map and public tracking customer map update smoothly in real time without page refreshing.
5. **Action:** Courier clicks "Complete Delivery". Captures customer signature on touchscreen canvas and uploads camera package photo.
6. **System Behavior:** Multipart `POST /api/v1/deliveries/{id}/pod` uploads assets to MinIO object storage. Status changes to `Delivered`.

---

### Scenario 4: Merchant Bulk Ingestion & Webhook Delivery (11:00 – 13:00)
1. **Action:** Open Postman or terminal. Send bulk order POST request to `http://localhost:5000/api/v1/merchant/parcels/bulk` with `X-API-Key: sk_live_...` containing 10 orders.
2. **System Behavior:** Gateway authenticates API key via salted SHA-256 hash. Returns `202 Accepted` with 10 generated tracking numbers.
3. **Action:** Open `webhook.site` browser tab displaying the merchant's simulated endpoint.
4. **System Behavior:** Show the `delivery.completed` webhook arriving at the merchant endpoint, signed with `X-SwiftDrop-Signature` header matching HMAC-SHA256.
5. **Fault Injection Demo:** Temporarily kill the mock receiver to demonstrate the Webhook Worker automatically scheduling exponential backoff retries.

---

### Scenario 5: Architectural Resilience & Quality Gate Evidence (13:00 – 15:00)
1. **Action:** Open RabbitMQ management console (`http://localhost:15672`).
2. **Demonstration:** Show active topic exchanges, queues, and Dead Letter Queues (DLQ).
3. **Action:** Open terminal and run `dotnet test`.
4. **System Behavior:** 21 automated unit and Testcontainers integration tests pass green with Coverlet reporting **82.4% line coverage**.

---

## 3. Anticipated Panel Q&A Defense & Justifications

| Expected Question from Panel | Architectural Defense / Rationale |
|---|---|
| **Why Database-per-Service instead of a single shared database?** | Independent deployability, complete schema autonomy, and preventing cross-domain tight coupling. A failure or schema lock in the Delivery DB never impacts Identity or Merchant operations. |
| **How do you guarantee consistency without 2-phase commits (2PC)?** | 2PC introduces blocking and single-point-of-failure risks in cloud microservices. SwiftDrop uses the **Transactional Outbox Pattern** with RabbitMQ to achieve guaranteed eventual consistency and at-least-once message delivery. |
| **Why use YARP instead of Ocelot or Kong?** | YARP is engineered by Microsoft on top of .NET 8 Kestrel, offering superior throughput, minimal memory footprint, native ASP.NET Core middleware integration, and zero overhead for C# teams. |
| **How is sensitive customer PII protected?** | Column-level AES-256 encryption at rest for phone numbers and street addresses, Serilog log redaction filters, TLS 1.3 in transit, and short-lived pre-signed URLs for PoD signatures. |

---

## 4. Fallback Contingency Plan

In the event of hardware, network, or venue technical difficulties during the presentation:
- **Local Fallback:** All services and databases run 100% locally on localhost via Docker Compose without requiring external internet (mock Google OIDC tokens are pre-seeded).
- **Video Fallback:** A pre-recorded 1080p full-length walkthrough video is stored locally on USB and laptop desktop (`artifacts/demo_backup.mp4`).
- **Data Fallback:** Seed data script (`seed-data.sh`) can reset and populate test parcels, couriers, and merchants in 10 seconds.
