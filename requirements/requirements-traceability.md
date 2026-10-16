# Requirements Traceability

> Status: Proposed baseline 2.0 · All runtime implementation/test evidence pending

[SRS](srs.md) defines **32 functional + 20 non-functional = 52 requirements**. This matrix is generated from [traceability.json](traceability.json); operation IDs resolve only through the [REST catalog](../api/rest-api.md). Suggested roles are not individual allocations. Every primary case is drafted in the [test catalog](../testing/test-cases.md); none is recorded implemented/executed/passing.

| Requirement | Capability | Operation IDs / verification | Event | Client/UI | Suggested role | Test | Evidence |
|---|---|---|---|---|---|---|---|
| FR-C01 | Customer registration | Register, Login, Refresh, Logout | None (no status side effect) | React Customer + Flutter Customer | SEC/UI | TC-C01 | Pending |
| FR-C02 | Google OIDC login | GoogleLogin, LinkGoogle | None (no status side effect) | React Customer + Flutter Customer | SEC/UI | TC-C02 | Pending |
| FR-C03 | Profile management | GetProfile, UpdateProfile | None (no status side effect) | React Customer + Flutter Customer | SEC/UI | TC-C03 | Pending |
| FR-C04 | Create parcel booking | CreateParcel | StatusChanged | React Customer + Flutter Customer | DEL/UI | TC-C04 | Pending |
| FR-C05 | Fee estimation | EstimateFee | None (no status side effect) | React Customer + Flutter Customer | DEL/UI | TC-C05 | Pending |
| FR-C06 | Real-time parcel tracking | PublicTrack, GetParcel, ParcelEvents | StatusChanged | React Customer + Flutter Customer | DEL/UI | TC-C06 | Pending |
| FR-C07 | Delivery history | ListParcels | None (no status side effect) | React Customer + Flutter Customer | DEL/UI | TC-C07 | Pending |
| FR-C08 | Download receipt | DownloadReceipt | None (no status side effect) | React Customer + Flutter Customer | DEL/UI | TC-C08 | Pending |
| FR-M01 | Merchant registration | RegisterMerchant | None (no status side effect) | React Merchant / external merchant system | MER/UI | TC-M01 | Pending |
| FR-M02 | Admin approval workflow | SetMerchantStatus | None (no status side effect) | React Merchant / external merchant system | MER/UI | TC-M02 | Pending |
| FR-M03 | API key management | CreateApiKey, ListApiKeys, RevokeApiKey | None (no status side effect) | React Merchant / external merchant system | MER/UI | TC-M03 | Pending |
| FR-M04 | Submit order via API | SubmitMerchantOrder | StatusChanged | React Merchant / external merchant system | MER/UI | TC-M04 | Pending |
| FR-M05 | Webhook subscription | CreateWebhook, ListWebhooks, DeleteWebhook, ListWebhookAttempts, ReplayWebhook | StatusChanged | React Merchant / external merchant system | MER/UI | TC-M05 | Pending |
| FR-M06 | Merchant dashboard | MerchantDashboard, ListMerchantOrders | None (no status side effect) | React Merchant / external merchant system | MER/UI | TC-M06 | Pending |
| FR-M07 | Order status tracking | GetMerchantOrder | StatusChanged | React Merchant / external merchant system | MER/UI | TC-M07 | Pending |
| FR-R01 | View assigned deliveries | CourierAssignments | None (no status side effect) | React Courier + Flutter Courier | DEL/UI | TC-R01 | Pending |
| FR-R02 | Update parcel status | UpdateDeliveryStatus | StatusChanged | React Courier + Flutter Courier | DEL/UI | TC-R02 | Pending |
| FR-R03 | Upload proof of delivery | CompleteDeliveryWithProof | StatusChanged | React Courier + Flutter Courier | DEL/UI | TC-R03 | Pending |
| FR-R04 | Report failed delivery | UpdateDeliveryStatus | StatusChanged | React Courier + Flutter Courier | DEL/UI | TC-R04 | Pending |
| FR-R05 | View delivery history | CourierHistory | None (no status side effect) | React Courier + Flutter Courier | DEL/UI | TC-R05 | Pending |
| FR-D01 | View unassigned parcels | ListParcels | None (no status side effect) | React Dispatcher | DEL/UI | TC-D01 | Pending |
| FR-D02 | Assign courier to parcel | AssignCourier | StatusChanged | React Dispatcher | DEL/UI | TC-D02 | Pending |
| FR-D03 | Monitor courier workload | CourierWorkload | None (no status side effect) | React Dispatcher | DEL/UI | TC-D03 | Pending |
| FR-D04 | Reassign delivery | AssignCourier | StatusChanged | React Dispatcher | DEL/UI | TC-D04 | Pending |
| FR-D05 | View delivery zone summary | ZoneSummary | None (no status side effect) | React Dispatcher | DEL/UI | TC-D05 | Pending |
| FR-A01 | User management | ListUsers, CreateUser, UpdateUser, DeactivateUser | None (no status side effect) | React Admin | SEC/UI | TC-A01 | Pending |
| FR-A02 | Role assignment | SetRoles | None (no status side effect) | React Admin | SEC/UI | TC-A02 | Pending |
| FR-A03 | Merchant approval/rejection | ListMerchants, SetMerchantStatus | None (no status side effect) | React Admin | API/UI | TC-A03 | Pending |
| FR-A04 | Configure delivery zones | ListZones, CreateZone, UpdateZone | None (no status side effect) | React Admin | API/UI | TC-A04 | Pending |
| FR-A05 | Configure pricing tiers | ListPricing, CreatePricing, UpdatePricing | None (no status side effect) | React Admin | API/UI | TC-A05 | Pending |
| FR-A06 | View system reports | DeliveryReport | None (no status side effect) | React Admin | API/UI | TC-A06 | Pending |
| FR-A07 | View audit logs | ListAudit | None (no status side effect) | React Admin | SEC/UI | TC-A07 | Pending |
| NFR-01 | API responses must return within 500 ms at the 95th percentile under normal load. | Cross-cutting acceptance scenario | None / cross-cutting | Cross-cutting / see acceptance scenario | Delivery/Identity | TC-N01 | Pending |
| NFR-02 | Real-time tracking updates must be delivered to subscribed clients within 2 seconds of a status change. | Cross-cutting acceptance scenario | StatusChanged | Cross-cutting / see acceptance scenario | Delivery/MSG | TC-N02 | Pending |
| NFR-03 | The system must support at least 50 concurrent users for demonstration purposes. | Cross-cutting acceptance scenario | None / cross-cutting | Cross-cutting / see acceptance scenario | QA/OPS | TC-N03 | Pending |
| NFR-04 | All external API communication must use HTTPS (TLS 1.2+). | Cross-cutting acceptance scenario | None / cross-cutting | Cross-cutting / see acceptance scenario | SEC/OPS | TC-N04 | Pending |
| NFR-05 | User authentication must use Google OIDC with application-issued JWTs (expiry ≤ 15 minutes). | Cross-cutting acceptance scenario | None / cross-cutting | Cross-cutting / see acceptance scenario | SEC | TC-N05 | Pending |
| NFR-06 | Merchant API keys must be stored as hashed values; raw keys are shown only at creation time. | Cross-cutting acceptance scenario | None / cross-cutting | Cross-cutting / see acceptance scenario | SEC/MER | TC-N06 | Pending |
| NFR-07 | Webhook payloads must be signed with HMAC-SHA256 using per-merchant secrets. | Cross-cutting acceptance scenario | StatusChanged | Cross-cutting / see acceptance scenario | SEC/MER | TC-N07 | Pending |
| NFR-08 | Role-based access control must be enforced on every API endpoint. | Cross-cutting acceptance scenario | None / cross-cutting | Cross-cutting / see acceptance scenario | SEC | TC-N08 | Pending |
| NFR-09 | Merchant secrets and sensitive configuration must be encrypted at rest. | Cross-cutting acceptance scenario | None / cross-cutting | Cross-cutting / see acceptance scenario | SEC/OPS | TC-N09 | Pending |
| NFR-10 | Booking operations must be idempotent using client-generated idempotency keys. | Cross-cutting acceptance scenario | StatusChanged | Cross-cutting / see acceptance scenario | DEL/MER | TC-N10 | Pending |
| NFR-11 | Events must be published reliably using a transactional outbox pattern, preventing message loss. | Cross-cutting acceptance scenario | StatusChanged | Cross-cutting / see acceptance scenario | DEL/MSG | TC-N11 | Pending |
| NFR-12 | Webhook delivery must retry failed attempts with exponential backoff (one initial attempt plus five retries, per the webhook policy). | Cross-cutting acceptance scenario | StatusChanged | Cross-cutting / see acceptance scenario | MER/MSG | TC-N12 | Pending |
| NFR-13 | Failed webhook attempts must be logged and available for manual inspection and replay. | Cross-cutting acceptance scenario | StatusChanged | Cross-cutting / see acceptance scenario | MER/QA | TC-N13 | Pending |
| NFR-14 | Each backend service must own its own PostgreSQL database with no shared schemas. | Cross-cutting acceptance scenario | None / cross-cutting | Cross-cutting / see acceptance scenario | ARCH/OPS | TC-N14 | Pending |
| NFR-15 | Services must communicate asynchronously for non-blocking operations via RabbitMQ. | Cross-cutting acceptance scenario | StatusChanged | Cross-cutting / see acceptance scenario | MSG | TC-N15 | Pending |
| NFR-16 | Services must be independently deployable as Docker containers. | Cross-cutting acceptance scenario | None / cross-cutting | Cross-cutting / see acceptance scenario | OPS | TC-N16 | Pending |
| NFR-17 | The codebase must maintain ≥ 80% unit test coverage for business logic. | Cross-cutting acceptance scenario | None / cross-cutting | Cross-cutting / see acceptance scenario | QA | TC-N17 | Pending |
| NFR-18 | The web application must be responsive across mobile (320px+), tablet and desktop viewports, including the public tracking page. | Cross-cutting acceptance scenario | None / cross-cutting | Cross-cutting / see acceptance scenario | UI/QA | TC-N18 | Pending |
| NFR-19 | Error responses must return meaningful messages with appropriate HTTP status codes. | Cross-cutting acceptance scenario | None / cross-cutting | Cross-cutting / see acceptance scenario | API/QA | TC-N19 | Pending |
| NFR-20 | The mobile application must support Android devices (API level 26+). | Cross-cutting acceptance scenario | None / cross-cutting | Cross-cutting / see acceptance scenario | UI/QA | TC-N20 | Pending |
## Counts
| Category | Requirements | Primary test cases drafted | Runtime evidence |
|---|---|---|---|
| Customer | 8 | 8 | 0 |
| Merchant | 7 | 7 | 0 |
| Courier | 5 | 5 | 0 |
| Dispatcher | 5 | 5 | 0 |
| Admin | 7 | 7 | 0 |
| NFR | 20 | 20 | 0 |
| Total | 52 | 52 | 0 |
The catalog additionally contains 16 security/recovery cases, for **68 total drafted cases**. NFR-18/19/20 cover responsive public web, safe errors and both Flutter personas on Android API 26+. Case count is not implementation or pass count. Receipt/dashboard/reports are Must and have TC-C08/TC-M06/TC-A06 plus explicit demo steps. [Coverage denominator](../testing/coverage-summary.md), [results](../testing/test-results.md) and [diagram index](../design/diagrams/README.md) provide separate acceptance evidence.
