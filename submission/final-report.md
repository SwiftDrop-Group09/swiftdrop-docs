# Final Report Draft

> Status: Proposed report baseline 2.0 · Implementation, results and member sign-off pending

SwiftDrop (EAD Group 09, 10 members) proposes a parcel-delivery platform with React for all five roles and **Flutter Customer and Courier**. External submission is **15 November 2026**; optional internal freeze/rehearsal is 12 November. The [source/page comparison](../requirements/assignment-compliance.md) is complete. The PDF states 20 marks overall, category labels totaling 100 and +5 per optional bonus; their conversion/scaling still needs lecturer clarification. Do not treat ASP.NET Core/PostgreSQL/microservices/GraphQL/gRPC as official mandates; see [assignment reconciliation](../requirements/assignment-overview.md).

## Requirements and design

[SRS](../requirements/srs.md) has 32 FR and 20 NFR, with mandatory receipt download, merchant own-order/status dashboard, basic Admin reports and mobile-friendly public tracking. [Traceability](../requirements/requirements-traceability.md) maps all 52 to interfaces and drafted tests. [Use-case narratives](../requirements/use-case-specifications.md) and [diagram index](../design/diagrams/README.md) cover the four mandatory flows with editable/rendered artifacts.

The proposed [architecture](../architecture/technical-design.md) targets .NET 10 (`net10.0`) with ASP.NET Core 10 for YARP, the three APIs and the Worker's HTTP health host. It uses four isolated logical databases hosted in Neon, private object storage and RabbitMQ. Delivery owns GraphQL/SSE and local outbox relay; Merchant owns signing and HTTP webhook attempts; Worker calls scoped APIs rather than foreign SQL. [ADRs](../architecture/decisions/README.md) record all alternatives and tradeoffs as Proposed pending named approvals.

## Key guarantees and limits to verify

Quote preview precedes Created booking. A single [state matrix](../architecture/parcel-state-machine.md) guards courier/version updates and proof-required completion. Durable merchant inbox/reconciliation handles unknown create outcomes. StatusChanged is the sole notification trigger, with inbox/job deduplication. Public REST/GraphQL cannot navigate into private data; Google linking uses stable subject plus explicit reauthentication; webhooks use Merchant-only encrypted keys, fresh timestamp/HMAC and SSRF controls. SSE uses one Delivery instance and current-state recovery; no multi-instance broadcast guarantee. JWT logout/role revocation is bounded by 15-minute access expiry; API-key revocation is immediate.

The [patterns/principles note](../architecture/design-patterns.md) covers the required design rationale. A responsive web frontend (React selected), Docker/Compose, an event-consuming email or mock SMS service, and the source-listed design/test/submission artifacts are official requirements; Flutter Customer/Courier and the selected service stack are additional team decisions.

## Implementation, testing and evidence

This repository provides design contracts/reference infrastructure only; actual source parity, full Compose startup, mobile onboarding, application tests and coverage remain unverified. [68 cases](../testing/test-cases.md) are drafted; there is no claim of execution/pass coverage. [Documentation validation](../testing/documentation-validation.md) records only checks actually run here. Populate this section with source commits, real CI/test/coverage artifacts, dated screenshots, limitations and reflections after implementation. No sample metrics or invented individual contributions are results.

## Deployment and submission

[Local setup](../deployment/local-setup.md) includes Flutter both personas, Google SDK/network configuration and secret handling. [Compose](../deployment/docker-compose.md) supplies a reference infrastructure but requires real application images/migrations/keys. [Kubernetes](../deployment/kubernetes.md) and [AI](../bonus/ai-delivery-assistant.md) are independent optional bonuses; bulk and GPS/SignalR are deferred. The mandatory demo must not depend on them.

Before export/submission: complete [checklist](submission-checklist.md), attach tested implementation/release links, final design/report PDF, [demo](demo-plan.md), actual test/coverage evidence and [verified contribution sheet](../project-management/contribution-log.md). The regenerated architecture PDF is a diagram artifact, not the final report or team sign-off.
