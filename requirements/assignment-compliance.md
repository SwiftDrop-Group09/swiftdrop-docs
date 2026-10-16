# Assignment Compliance Map

> Source comparison completed 16 October 2026 · Documentation coverage only; implementation and team sign-off pending

Every row refers to the unchanged [assignment PDF](sources/ead-group-assignment.pdf). “Mapped” means an intended contract or artifact exists, not that its acceptance test ran. The [overview](assignment-overview.md) records provenance, exact assessment labels and the unresolved conversion from the 100-point category labels/+5 bonuses to the stated overall 20 marks.

## Functional and system requirements

| PDF page / requirement | SRS mapping | Canonical design / acceptance evidence to execute |
|---|---|---|
| 1 · Secure signup/login including Google | FR-C01/C02; NFR-05/08 | [Authentication](../security/authentication.md); TC-C01/C02 and TC-SEC-05 |
| 1 · Pickup/drop-off, parcel size/weight booking | FR-C04 | [Quote/confirm contracts](../api/rest-api.md); TC-C04 |
| 1 · Fee estimate before confirmation | FR-C05 | EstimateFee/CreateParcel; TC-C05 and TC-REC-01 |
| 1 · Created, PickedUp, InTransit, OutForDelivery, Delivered/Failed live tracking | FR-C06/R02/R04; NFR-02 | [Canonical transitions](../architecture/parcel-state-machine.md), [SSE](../integration/realtime-tracking.md); TC-C06/R02/R04 |
| 1 · History and receipt download | FR-C07/C08 | ListParcels/DownloadReceipt; TC-C07/C08 |
| 1 · Mobile-friendly public-number tracking | FR-C06; NFR-18 | PublicTrack / PublicTrackingSummary; TC-SEC-01 and TC-N18 |
| 1 · Merchant registration/admin approval | FR-M01/M02/A03 | RegisterMerchant/SetMerchantStatus; TC-M01/M02/A03 |
| 1 · Secured merchant API using keys or OAuth client credentials | FR-M03/M04; NFR-06 | Team selects API keys; [durable merchant order](use-case-specifications.md#uc-02-merchant-order-through-secured-api); TC-M03/M04 |
| 1 · Merchant status webhooks | FR-M05; NFR-07/12/13 | [Signing/retry/ownership](../integration/merchant-webhooks.md); TC-M05, TC-SEC-04/06, TC-REC-07 |
| 1 · Dashboard of orders and states | FR-M06/M07 | MerchantDashboard/ListMerchantOrders/GetMerchantOrder; TC-M06/M07 |
| 2 · Courier authentication | FR-C01/C02 reused for Courier; NFR-05/08 | [Client matrix](../api/api-reference.md); admin-provisioned Courier role, same login handlers; TC-N20/R01 |
| 2 · Courier assigned deliveries for the day | FR-R01 | CourierAssignments date/service-day contract; TC-R01 |
| 2 · Each-stage delivery note or proof | FR-R02/R03 | Required private notes for operational updates; final proof policy is a stronger team choice; TC-R02/R03 |
| 2 · Failed delivery reason | FR-R04 | UpdateDeliveryStatus failureReason; TC-R04 |
| 2 · Unassigned queue and assignment | FR-D01/D02 | ListParcels/AssignCourier; TC-D01/D02 |
| 2 · Active courier workloads | FR-D03 | CourierWorkload and explicit operational couriers ER entity; TC-D03 |
| 2 · Manage users/merchants/zones/pricing | FR-A01/A02/A03/A04/A05 | Admin-scoped [REST operations](../api/rest-api.md); TC-A01–A05 |
| 2 · Deliveries/day and success/failure reports | FR-A06 | DeliveryReport, exact date window/denominator; TC-A06 |
| 2–3 · RBAC, JWT/OAuth, privacy, hashed passwords, input validation and safe errors/logs | NFR-04/05/06/08/09/19; FR-C01 | [Security contracts](../security/authorization.md); TC-N04–N09/N19 and TC-SEC-01–08 |
| 2–3 · Status broker, notification consumer and webhook retry | NFR-11/12/13/15; FR-M05 | [Event catalog](../integration/event-catalog.md): Worker consumes StatusChanged and sends demonstrable mock SMS; TC-N15, TC-REC-03/04/07. At least one actual event-flow test is mandatory |
| 2–3 · Live WebSockets/SSE (page 2 also mentions polling) | FR-C06; NFR-02 | SSE is selected to satisfy page 3's narrower implementation wording; TC-N02/REC-08 |
| 2–3 · Frontend/backend/database/broker containers and Compose | NFR-16 | [Compose reference](../deployment/docker-compose.md); TC-N16 requires real images/migrations and successful startup |

## Design, implementation, tests and submission

| PDF page / deliverable | Documentation coverage | Remaining acceptance evidence |
|---|---|---|
| 2 · Use cases for Customer/Merchant/Courier/Dispatcher | [Actor diagrams](../design/diagrams/use-cases/README.md) and [four narratives](use-case-specifications.md) | Named actor/domain review |
| 2 · ER users/roles/merchants/parcels/history/couriers/zones/pricing | [ER diagrams](../design/diagrams/er/README.md), including explicit couriers and zone membership | Review and migration/schema parity |
| 2 · Justified presentation/business/data architecture | [Technical design](../architecture/technical-design.md), [source/export](../design/diagrams/architecture/architecture.md) | Approved design and source parity |
| 2 · Integration patterns and reasons | [Integration design](../integration/integration-design.md) and [patterns note](../architecture/design-patterns.md) | Domain/integration review |
| 2 · Four sequence/activity flows | [Four-row source/export index](../design/diagrams/README.md#required-assignment-coverage) | Review each flow and all rendered exports |
| 2 · Short patterns/principles note | [SOLID, DRY, Repository, pricing Strategy and event Observer/pub-sub](../architecture/design-patterns.md) | Link actual source examples when implemented |
| 3 · Responsive React/Angular/Vue web frontend | Team selects React; [client scope](../api/api-reference.md) | Working React role screens/public tracking; Flutter is additional scope |
| 3 · Suitable backend and secure versioned REST or GraphQL | [ASP.NET Core proposal](../architecture/technical-design.md), [REST](../api/rest-api.md), [GraphQL](../api/graphql-api.md) | Tested implementation commits; .NET/GraphQL/gRPC are not lecturer-specific mandates |
| 3 · Meaningful exceptions, no duplicated logic, environment config/no secrets | [Patterns note](../architecture/design-patterns.md), [data protection](../security/data-protection.md), [setup](../deployment/local-setup.md) | Actual code review, failure/secret tests |
| 3 · Unit/integration/event and authorization tests; measurable coverage/results | [68 drafted cases](../testing/test-cases.md) and [coverage denominator](../testing/coverage-summary.md) | Actual executed reports; no official numeric minimum is given |
| 3 · Core live demo and architecture/integration/security walkthrough | [Demo script](../submission/demo-plan.md) | Running demo, notification output, reviewed slides/rehearsal; each member explains their contribution |
| 3 · Source repository link and setup README | [Repository index](../README.md#6-github-repository-organization), [local setup](../deployment/local-setup.md) | Real tested source/release links and new-member onboarding |
| 3 · Design documentation PDF | [Architecture and diagram packet](../design/diagrams/README.md#pdf-and-review-evidence) | Final assembled/approved design/report PDF, not diagrams alone |
| 3 · Test reports and coverage summary | [Results ledger](../testing/test-results.md), [coverage](../testing/coverage-summary.md) | Actual CI reports/artifacts |
| 4 · Member responsibility/contribution sheet | [Responsibilities](../project-management/team-responsibilities.md), [contribution log](../project-management/contribution-log.md) | Verified member names/handles, work and sign-off |
| 3 · Optional +5 Kubernetes | [Bonus plan](../deployment/kubernetes.md): full frontend/backend/database/broker; ConfigMaps, Secrets, Services, Ingress; Helm optional | Real cluster/manifests/demo; grading conversion needs lecturer clarification |
| 3 · Optional +5 Generative AI chatbot | [AI scope](../bonus/ai-delivery-assistant.md): backend API tools; MCP encouraged | Real model/chat/API integration and permission/failure tests; grading conversion needs clarification |

## Boundaries clarified by the source

- The PDF names no submission date; 15 November 2026 remains the session-confirmed deadline.
- The PDF does not require Flutter, PostgreSQL, ASP.NET Core, YARP, gRPC, a particular message broker, four databases, an outbox, strict photo/signature completion or numeric quality thresholds. These remain team proposals/targets where adopted.
- Polling appears in the general requirements but not the implementation live-tracking bullet; the SSE baseline satisfies both.
- The lecturer lists design-pattern examples; the note documents applicable choices without pretending each example is separately mandated or already implemented.
- Source verification is complete. Team design approval, runtime tests, named contributions and final submission remain open in [remaining work](../documentation-fix-plan.md).
