# Requirements Traceability

> **Status:** Draft  
> **Last Updated:** October 2026

This document maps each functional requirement from the [SRS](srs.md) to the responsible service, implementing API, test case, and verification evidence. It ensures every requirement is accounted for from specification through implementation, testing, and demonstration.

---

## 1. Traceability Matrix — Customer Requirements

| Req ID  | Requirement                        | Service                 | API / Endpoint                     | Test Case     | Evidence       |
| ------- | ---------------------------------- | ----------------------- | ---------------------------------- | ------------- | -------------- |
| FR-C01  | Customer registration              | Identity API            | `POST /api/auth/register`          | TC-C01        | Pending        |
| FR-C02  | Google OIDC login                  | Identity API            | `POST /api/auth/google`            | TC-C02        | Pending        |
| FR-C03  | Profile management                 | Identity API            | `GET/PUT /api/users/me`            | TC-C03        | Pending        |
| FR-C04  | Create parcel booking              | Delivery Operations API | `POST /api/bookings`               | TC-C04        | Pending        |
| FR-C05  | Fee estimation                     | Delivery Operations API | `POST /api/bookings/estimate`      | TC-C05        | Pending        |
| FR-C06  | Real-time parcel tracking          | Delivery Operations API | `GET /api/tracking/{id}` + SSE     | TC-C06        | Pending        |
| FR-C07  | Delivery history                   | Delivery Operations API | `GET /api/bookings/history`        | TC-C07        | Pending        |
| FR-C08  | Download receipt                   | Delivery Operations API | `GET /api/receipts/{id}`           | TC-C08        | Pending        |

## 2. Traceability Matrix — Merchant Requirements

| Req ID  | Requirement                        | Service                    | API / Endpoint                        | Test Case     | Evidence       |
| ------- | ---------------------------------- | -------------------------- | ------------------------------------- | ------------- | -------------- |
| FR-M01  | Merchant registration              | Merchant Integration API   | `POST /api/merchants/register`        | TC-M01        | Pending        |
| FR-M02  | Admin approval workflow            | Merchant Integration API   | `PUT /api/merchants/{id}/approve`     | TC-M02        | Pending        |
| FR-M03  | API key management                 | Merchant Integration API   | `POST /api/merchants/{id}/keys`       | TC-M03        | Pending        |
| FR-M04  | Submit order via API               | Merchant Integration API   | `POST /api/merchant-orders`           | TC-M04        | Pending        |
| FR-M05  | Webhook subscription               | Merchant Integration API   | `POST /api/webhooks/subscribe`        | TC-M05        | Pending        |
| FR-M06  | Merchant dashboard                 | Merchant Integration API   | `GET /api/merchants/{id}/dashboard`   | TC-M06        | Pending        |
| FR-M07  | Order status tracking              | Merchant Integration API   | `GET /api/merchant-orders/{id}`       | TC-M07        | Pending        |

## 3. Traceability Matrix — Courier Requirements

| Req ID  | Requirement                        | Service                 | API / Endpoint                        | Test Case     | Evidence       |
| ------- | ---------------------------------- | ----------------------- | ------------------------------------- | ------------- | -------------- |
| FR-R01  | View assigned deliveries           | Delivery Operations API | `GET /api/couriers/me/assignments`    | TC-R01        | Pending        |
| FR-R02  | Update parcel status               | Delivery Operations API | `PUT /api/parcels/{id}/status`        | TC-R02        | Pending        |
| FR-R03  | Upload proof of delivery           | Delivery Operations API | `POST /api/parcels/{id}/proof`        | TC-R03        | Pending        |
| FR-R04  | Report failed delivery             | Delivery Operations API | `POST /api/parcels/{id}/failure`      | TC-R04        | Pending        |
| FR-R05  | View delivery history              | Delivery Operations API | `GET /api/couriers/me/history`        | TC-R05        | Pending        |

## 4. Traceability Matrix — Dispatcher Requirements

| Req ID  | Requirement                        | Service                 | API / Endpoint                        | Test Case     | Evidence       |
| ------- | ---------------------------------- | ----------------------- | ------------------------------------- | ------------- | -------------- |
| FR-D01  | View unassigned parcels            | Delivery Operations API | `GET /api/dispatch/unassigned`        | TC-D01        | Pending        |
| FR-D02  | Assign courier to parcel           | Delivery Operations API | `POST /api/dispatch/assign`           | TC-D02        | Pending        |
| FR-D03  | Monitor courier workload           | Delivery Operations API | `GET /api/dispatch/workload`          | TC-D03        | Pending        |
| FR-D04  | Reassign delivery                  | Delivery Operations API | `PUT /api/dispatch/reassign`          | TC-D04        | Pending        |
| FR-D05  | View delivery zone summary         | Delivery Operations API | `GET /api/dispatch/zones`             | TC-D05        | Pending        |

## 5. Traceability Matrix — Admin Requirements

| Req ID  | Requirement                        | Service                    | API / Endpoint                        | Test Case     | Evidence       |
| ------- | ---------------------------------- | -------------------------- | ------------------------------------- | ------------- | -------------- |
| FR-A01  | User management (CRUD)             | Identity API               | `GET/POST/PUT/DELETE /api/users`      | TC-A01        | Pending        |
| FR-A02  | Role assignment                    | Identity API               | `PUT /api/users/{id}/roles`           | TC-A02        | Pending        |
| FR-A03  | Merchant approval / rejection      | Merchant Integration API   | `PUT /api/merchants/{id}/approve`     | TC-A03        | Pending        |
| FR-A04  | Configure delivery zones           | Delivery Operations API    | `POST/PUT /api/admin/zones`           | TC-A04        | Pending        |
| FR-A05  | Configure pricing tiers            | Delivery Operations API    | `POST/PUT /api/admin/pricing`         | TC-A05        | Pending        |
| FR-A06  | View system reports                | Delivery Operations API    | `GET /api/admin/reports`              | TC-A06        | Pending        |
| FR-A07  | View audit logs                    | Identity API               | `GET /api/admin/audit`                | TC-A07        | Pending        |

---

## 6. Non-Functional Requirements Traceability

| Req ID  | Requirement                                         | Verification Method                           | Evidence       |
| ------- | --------------------------------------------------- | --------------------------------------------- | -------------- |
| NFR-01  | API response < 500ms (p95)                          | Load test / timing benchmark                  | Pending        |
| NFR-02  | Real-time tracking updates delivered within 2s       | Latency verification on WebSocket/SSE updates | Pending        |
| NFR-03  | 50 concurrent users demonstration scale             | Concurrency benchmark test                    | Pending        |
| NFR-04  | All external API communication uses HTTPS           | Gateway TLS inspection and HSTS audit         | Pending        |
| NFR-05  | JWT token expiry ≤ 15 min (Google OIDC)             | Unit & Integration test on JWT configuration  | Pending        |
| NFR-06  | Merchant API keys stored as salted hashes           | Database inspection & auth integration test   | Pending        |
| NFR-07  | Webhook payloads signed with HMAC-SHA256            | Cryptographic signature verification test     | Pending        |
| NFR-08  | RBAC enforced on every API endpoint                 | Authorization policy integration tests        | Pending        |
| NFR-09  | Merchant secrets and configuration encrypted at rest| Database column and storage volume audit      | Pending        |
| NFR-10  | Idempotent booking operations                       | Integration test with duplicate request keys  | Pending        |
| NFR-11  | Transactional outbox event delivery                 | Integration test with broker assertion        | Pending        |
| NFR-12  | Webhook retry with exponential backoff (5 retries)  | Integration test with mock failure endpoint   | Pending        |
| NFR-13  | Failed webhook attempts logged & inspectable        | Audit log and DLQ inspection                  | Pending        |
| NFR-14  | Database-per-service schema isolation               | Architecture review, schema inspection        | Pending        |
| NFR-15  | Asynchronous RabbitMQ communication                 | MassTransit broker topology review            | Pending        |
| NFR-16  | Containerized deployment via Docker                 | Docker Compose up validation                  | Pending        |
| NFR-17  | ≥ 80% unit test coverage for business logic         | Coverage report from CI pipeline (Coverlet)   | Pending        |

---

## 7. Coverage Summary

| Category                | Total Requirements | Mapped to Service | Test Case Defined | Evidence Collected |
| ----------------------- | ------------------ | ----------------- | ----------------- | ------------------ |
| Customer (FR-C)         | 8                  | 8                 | 0                 | 0                  |
| Merchant (FR-M)         | 7                  | 7                 | 0                 | 0                  |
| Courier (FR-R)          | 5                  | 5                 | 0                 | 0                  |
| Dispatcher (FR-D)       | 5                  | 5                 | 0                 | 0                  |
| Admin (FR-A)            | 7                  | 7                 | 0                 | 0                  |
| Non-Functional (NFR)    | 10                 | 10                | 0                 | 0                  |
| **Total**               | **42**             | **42**            | **0**             | **0**              |

> This matrix will be updated as test cases are written and evidence is collected during the testing phase.

---

## References

- [Software Requirements Specification](srs.md)
- [Test Cases](../testing/test-cases.md)
- [Test Results](../testing/test-results.md)
- [API Reference](../api/api-reference.md)
- [Service Catalog](../architecture/service-catalog.md)
