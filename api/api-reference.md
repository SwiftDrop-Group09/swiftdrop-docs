# API Reference and Client Matrix

> Status: Proposed baseline 2.0 · 16 October 2026

The [REST route inventory](rest-api.md) is the canonical operation catalog, with a [JSON design fixture](contracts/routes.json). YARP is the external entry point. Identity owns auth/users/JWKS; Delivery owns quotes, parcels, operations, reports, GraphQL and SSE; Merchant owns businesses, keys, order jobs and webhooks. The Worker has no public client API. Ports and environments are defined once in the [environment matrix](../deployment/environments.md).

| Client | Required capabilities | Credential / transport |
|---|---|---|
| React Customer | Signup/local and Google login, quote/confirm, own tracking/history, receipt | Human JWT; REST or equivalent GraphQL; fetch SSE |
| Flutter Customer | Same Customer booking/tracking/history/receipt scope | Human JWT; REST; authenticated streaming HTTP |
| Flutter Courier | Login, assigned manifest, status/failure, proof upload | Human JWT; REST; ownership at commit |
| React Courier | Equivalent authorized operational views | Human JWT; REST |
| React Merchant | Onboarding, key/webhook management, own-order/status dashboard | Human JWT; Merchant REST |
| Merchant external system | Submit/poll own durable orders, scoped webhook management | X-API-Key; REST |
| React Dispatcher | Unassigned queue, assignment, workload, zone summary | Human JWT; REST/GraphQL and authorized SSE |
| React Admin | Users/roles, merchant approval, zones/pricing, basic reports/audit | Human JWT; REST |
| Public mobile-friendly web | Safe tracking snapshot only | Anonymous; REST or safe GraphQL query; no private SSE |

## Protocol ownership

- [REST](rest-api.md): complete mandatory capabilities and resource authorization.
- [GraphQL](graphql-api.md): Delivery module at `/graphql`, YARP routes directly; wrappers reuse application handlers. No unrestricted cross-domain BFF.
- [gRPC](grpc-services.md): only Merchant→Delivery CreateBooking and GetBookingByExternalOrder; internal HTTP/2 with scoped service JWT. [Proto source](contracts/delivery.proto).
- [SSE](../integration/realtime-tracking.md): Delivery hosts `/api/v1/parcels/{id}/events`; authenticated current-state snapshots and refetch on reconnect, one Delivery replica.
- [WebSocket](websocket-protocol.md): GPS/SignalR deferred; no public hub, separate realtime service or Redis dependency in the baseline.

Correlation uses X-Correlation-ID (generated if absent), never a credential. Lists use page/pageSize (max 100) and stable ordering. Services validate JWT issuer/audience/expiry and ownership regardless of gateway filters. Public responses are allowlisted projections. Secrets occur once at creation, never in lists, events or logs. JSON/GraphQL/protobuf files here are validated **design fixtures**; source-repository code compatibility and generated OpenAPI remain unverified until commit links are attached.
