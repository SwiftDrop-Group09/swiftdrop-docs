# Technical Design

> Status: Proposed baseline 2.0 · 16 October 2026 · No implementation or approval evidence attached

SwiftDrop targets **.NET 10** (`net10.0`) for the Identity, Delivery Operations and Merchant Integration APIs, YARP gateway and Notification/Webhook Worker. The API/gateway hosts and Worker HTTP health host use **ASP.NET Core 10**. These component/framework choices are team decisions; the [verified assignment](../requirements/assignment-overview.md) permits other suitable architectures and secure REST or GraphQL. Responsive web and full-system Docker/Compose are official requirements; React is the chosen permitted web framework.

React supports all five roles plus public tracking. Flutter supports **Customer and Courier** as required by the agreed client scope. Both use versioned REST; optional GraphQL wrappers call the same Delivery application handlers. GraphQL is hosted in Delivery and routed through YARP at `/graphql`; it is a delivery-domain query module, not an unrestricted cross-domain BFF. Future multi-domain resolvers must use service APIs and receive a separate ADR.

The assignment-required [patterns and principles note](design-patterns.md) explains SOLID/DRY, Repository/unit of work, pricing Strategy, event Observer/pub-sub and reliability tradeoffs. These are proposed designs until implementation evidence is linked.

## .NET runtime target

Use the **.NET 10 SDK** to build backend projects targeting `<TargetFramework>net10.0</TargetFramework>`. Use the matching ASP.NET Core 10 runtime for the three APIs, YARP and Worker with its HTTP health listener. Pin the tested 10.x SDK patch/feature band in the backend repository's `global.json` and compatible EF Core/Npgsql/YARP/MassTransit packages in its project/lock files; no exact patch or dependency compatibility is claimed by this documentation-only change.

The runtime/SDK and TFM naming follow [Microsoft's .NET 10 overview](https://learn.microsoft.com/en-us/dotnet/core/whats-new/dotnet-10/overview) and [target-framework reference](https://learn.microsoft.com/en-us/dotnet/standard/frameworks).

## Structure and reliability

Each API uses presentation → application handlers → domain rules → infrastructure adapters. REST, GraphQL and internal gRPC share domain policies, price calculation, ownership and concurrency guards. Four private logical databases are hosted by Neon PostgreSQL; four credentials isolate owners. Database transactions never span services. Merchant ingestion commits an inbox job first, then calls idempotent Delivery `CreateBooking` with durable reconciliation after timeout.

Delivery atomically commits parcel/history/version/outbox before acknowledging. Its relay publishes `StatusChanged` through MassTransit per-message-type fanout topology. The Worker creates durable notification/provider and webhook-dispatch jobs; Merchant owns webhook subscriptions, encrypted secrets and HTTP attempts. Delivery consumes its own realtime queue to signal authenticated SSE clients. Duplicate effects are prevented with durable uniqueness constraints.

## Client and infrastructure policy

| Concern | Proposed baseline |
|---|---|
| Authentication | Local Argon2id credentials and Google SDK ID-token exchange; app JWT ≤15 minutes; refresh rotation |
| Status transport | Authenticated fetch-stream SSE in Delivery; public tracking uses safe snapshot REST/GraphQL |
| Reconnect | Subscribe then fetch snapshot; apply only newer parcel versions; no durable SSE cursor replay promise |
| Realtime scale | One Delivery replica for demo; a shared competing queue is not broadcast across replicas |
| Storage | Private object storage; Delivery authorizes proof/receipt download and stages proof before final state |
| Revocation | Revoke refresh family in Identity DB; access/role changes bounded by 15-minute expiry; no Redis blacklist |
| Deployment | Compose reference infrastructure; actual source images/migrations and clean-start evidence pending |
| Additional scope | GPS/SignalR and bulk orders deferred; Kubernetes and AI independent bonuses |

Exact hosts, protocols and ports are maintained only in the [service catalog](service-catalog.md) and [environment matrix](../deployment/environments.md). The [state machine](parcel-state-machine.md), [REST](../api/rest-api.md), [event catalog](../integration/event-catalog.md) and [decision register](decisions/README.md) govern dependent diagrams. All selected options remain Proposed pending named approver/date and a reviewed PR.
