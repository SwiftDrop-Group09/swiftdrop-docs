# Service Catalog and Ownership

> Status: Proposed baseline 2.0 · 16 October 2026 · DEC-03/04/08/10/11/12 awaiting team approval

The gateway, three capability APIs and Notification/Webhook Worker target **.NET 10** (`net10.0`). All five hosts use ASP.NET Core 10, including the Worker's private HTTP health endpoints. SDK/package patch pins belong in the owning implementation repositories; see the [runtime target](technical-design.md#net-runtime-target).

## Canonical process inventory

| Compose process | Responsibility | Container listener | Host development address | Data owner |
|---|---|---|---|---|
| gateway | YARP routing, TLS at ingress, rate limits, coarse authentication | HTTP 8080 | localhost:5000 (loopback HTTP only) | None |
| identity-service | Local/Google login, profiles, roles, JWKS, refresh sessions | HTTP 8080 | No published port | swiftdrop_identity |
| delivery-service | Quotes, parcels, assignment, status, POD, receipts, reports, GraphQL, SSE, outbox relay | HTTP 8080; gRPC HTTP/2 8081 | No published port | swiftdrop_delivery; private proof bucket |
| merchant-service | Onboarding, keys, durable orders/reconciliation, subscriptions, signing, webhook HTTP attempts | HTTP 8080 | No published port | swiftdrop_merchant |
| notification-worker | Notification consumer, provider jobs, webhook dispatch commands | HTTP health 8080; no client API | No published port | swiftdrop_notifications |
| web | React, all five roles and public tracking | HTTP 8080 | localhost:5173 | None |

Flutter Customer and Courier call YARP; they are clients, not extra backend services. There is no separate realtime process or port 5004. GraphQL is a Delivery module, not a separate BFF process. YARP routes `/graphql` and authenticated `/api/v1/parcels/{id}/events` to Delivery. Domain services independently validate credentials, roles and ownership; no authorization relies on forwarded user headers.

## Infrastructure and network

| Process | Container address | Host binding | Purpose |
|---|---|---|---|
| Neon PostgreSQL | External TLS endpoint | Not published locally | Four logical databases, separate application logins and migrations; managed outside Compose/Kubernetes |
| rabbitmq | rabbitmq:5672; management 15672 | 127.0.0.1:15672 management only | AMQP, per-message-type fanout exchanges |
| object-store | object-store:9000; console 9001 | 127.0.0.1:9001 console only | Private proofs and receipts |

All external non-loopback access requires HTTPS via a configured TLS ingress; no staging/production deployment is asserted. Redis and SignalR are deferred. See [environment matrix](../deployment/environments.md) and [Compose](../deployment/docker-compose.md).

## Operation call matrix

| Initiator → target | Operation | Credential | Deadline / retry / failure |
|---|---|---|---|
| Merchant → Delivery | `swiftdrop.delivery.v1.DeliveryService/CreateBooking` | service JWT aud=delivery-internal, scope=bookings:create | 5s; stable merchant/order identity; unknown outcome reconciled before retry |
| Merchant → Delivery | `swiftdrop.delivery.v1.DeliveryService/GetBookingByExternalOrder` | service JWT, bookings:read | 5s; NotFound permits same-key CreateBooking retry |
| Worker → Merchant | `POST /internal/v1/webhook-dispatches` | service JWT aud=merchant-internal, webhooks:dispatch | 5s; stable event ID and duplicate-safe dispatch creation |
| Worker → Delivery | `POST /internal/v1/notification-context` | service JWT aud=delivery-internal, notifications:resolve | 5s; resolve recipient IDs for exact event/parcel only; no addresses |
| APIs → Identity | `GET /.well-known/jwks.json` | Public key retrieval, trusted configured origin | 5s; cached keys and one unknown-kid refresh; fail closed |
| Delivery → RabbitMQ | Publish StatusChanged via local outbox relay | Dedicated broker user | Retry until publisher confirmation; duplicates possible |
| RabbitMQ → Worker | notification-status queue | Worker broker user | Deduplicated durable notification and webhook-dispatch jobs |
| RabbitMQ → Delivery | delivery-realtime queue | Delivery broker user | SSE wake-up; one Delivery instance; snapshot read heals disconnects |
| Merchant → merchant HTTPS receiver | Send signed webhook attempt | Per-subscription HMAC | 10s; six automatic attempts; URL/egress checks on every attempt |

There is no Delivery→Merchant token-validation call, direct worker→Merchant DB connection or Identity gRPC process. Scope grants are specific to workloads; merchant API keys never authorize internal methods.

## Health and ownership rules

Each process exposes private `/health` and `/ready`; readiness checks its own DB migrations, required credentials and dependencies. Outbox backlog is monitored independently so a broker outage does not invalidate an already committed parcel. Services receive only their own database login. The worker requests Merchant to dispatch; Merchant decrypts signing material, sends HTTPS and owns webhook attempt records. The worker never receives signing secrets. Notification provider attempts belong to Notifications DB and are distinct from Merchant webhook attempts.
