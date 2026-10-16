# Scope and Assumptions

> Status: Proposed baseline 2.0 · 16 October 2026 · Team approval pending

## Required product scope

React web covers Customer, Merchant, Courier, Dispatcher and Admin, including a public tracking page usable at 320px width. Flutter supplies both **Customer and Courier** experiences; it is part of the agreed deliverable, not a courier-only extension.

Customer scope includes local registration/login, Google login, profile, quote before confirmation, booking, safe public/private tracking, history and receipt download. Merchant scope includes approval, scoped API keys, durable single-order ingestion, own-order dashboard and signed status webhooks. Courier scope includes assignment view, guarded status changes, failed delivery and private proof. Operations includes assignment/workload, user/role management, merchant approval, zones/pricing and basic admin reports. Notifications include persisted in-app delivery updates and a demonstrable mock SMS service consuming status events, as required on assignment pages 2–3.

## Team design scope

Three capability APIs plus YARP and one Notification/Webhook Worker; four separately owned logical PostgreSQL databases on one instance; RabbitMQ/MassTransit; private object storage; REST, Delivery-hosted GraphQL and internal gRPC. SSE status streams live in Delivery, with one Delivery replica for the demo. See [service catalog](../architecture/service-catalog.md) and [decisions](../architecture/decisions/README.md). These are Proposed choices, not lecturer mandates or proof of implementation.

## Deferred and excluded scope

Bulk ingestion is explicitly deferred; the baseline has one durable asynchronous order endpoint. GPS telemetry, dispatcher live maps and SignalR are additional unapproved scope. Redis is not required by the proposed demo. Kubernetes and AI are independent bonuses. Payments, route optimization, internationalization, production hosting guarantees and third-party logistics are excluded. Capacity testing for the stated SRS targets remains in scope; meeting a target needs evidence.

## Assumptions to verify

| ID | Assumption and verification |
|---|---|
| A-01 | Team has source repositories and toolchains; OPS must pin tested versions and supply commit links |
| A-02 | Separate web/Android Google clients and consent configuration exist; UI/SEC verify with both personas |
| A-03 | Local infrastructure can run with Compose; clean-start smoke evidence pending |
| A-04 | Single region and one Delivery replica are adequate for the academic demonstration |
| A-05 | Merchants control public HTTPS receivers and can verify timestamped HMAC |
| A-06 | Admin seeds deterministic zones/pricing for demos; no live payment processing |
| A-07 | Flutter and React use the same authorization and application command handlers |
| A-08 | Internal networks still require service credentials; network location alone grants no trust |
| A-09 | Required notification demo uses a mock SMS consumer with durable jobs/attempts; email may be added but a mock-email-only demo does not establish the PDF's email-or-mock-SMS requirement |
| A-10 | All 52 SRS requirements require test coverage; no runtime results are available in this docs repository |

External submission: **15 November 2026**. Proposed internal rehearsal/freeze: **12 November 2026**. The [assignment PDF comparison](assignment-compliance.md) is complete; grading conversion, individual allocations and ADR approvers still need confirmation.
