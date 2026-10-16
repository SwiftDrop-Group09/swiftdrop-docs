# SwiftDrop Documentation Alignment & Remediation Plan

> **Document status:** Proposed remediation plan — for team review  
> **Source baseline:** [`SwiftDrop-Group09/swiftdrop-docs`, `documentation` branch](https://github.com/SwiftDrop-Group09/swiftdrop-docs/tree/documentation)  
> **Reviewed snapshot:** `63d0de2230309dea4be7e9005ae6dbe62a79cd56` (16 October 2026)  
> **Authoritative assignment:** `EAD Group Assignment.pdf` supplied by the team  
> **Target submission:** **15 November 2026**  
> **Suggested repository location for this file:** `swiftdrop-docs/documentation-fix-plan.md`  
> **Status convention:** Findings describe **documented inconsistencies**, not defects verified in implemented source code.

## 1. Purpose and scope

This plan fixes the inconsistencies, incomplete contracts, privacy/security problems, unsupported progress claims, and diagram mismatches discovered during the documentation review. The goal is to establish one internally consistent, reviewable baseline **before implementing dependent features or signing off the sequence/activity diagrams**.

**Do not silently replace the team's design with the recommendations here.** Where several implementations are valid, the designated owners must choose one, record the decision in an Architecture Decision Record (ADR), and update all dependent documents together.

### Priority definitions

| Priority | Meaning | Gate |
|---|---|---|
| **P0 — Blocker** | Security issue, fundamental architecture/contract contradiction, or incorrect assignment requirement | Resolve before approving design contracts or implementing affected functionality |
| **P1 — High** | Affects diagrams, team integration, essential workflow behavior or required assignment functionality | Resolve before finalizing sequence/activity diagrams or merging the documentation baseline |
| **P2 — Medium** | Traceability, testing, deployability or documentation accuracy | Resolve before full integration and submission |
| **P3 — Later** | Optional enhancement or bonus documentation | Plan after mandatory features are covered |

### Suggested ownership roles (not actual assignments)

**REQ** — requirements coordinator; **ARCH** — architecture/service boundary coordinator; **API** — API/contracts coordinator; **SEC** — security/identity coordinator; **DEL** — delivery/dispatch coordinator; **MER** — merchant integration coordinator; **MSG** — messaging/notifications coordinator; **UI** — web/mobile coordinator; **UML** — sequence/activity owners; **OPS** — deployment coordinator; **QA** — testing coordinator; **PM** — team/project coordinator.

The team has not confirmed individual implementation ownership. These are **suggested responsibilities**, not records of real contributions.

---

## 2. Decisions to approve first (architecture decision register)

| Decision | Proposed direction **for review** | Alternatives / confirmation needed | Owner | Downstream documents |
|---|---|---|---|---|
| **DEC-01: Official vs team requirements** | Keep official assignment requirements separate from optional/team-selected technology decisions | Confirm every Must feature and bonus classification | REQ | Assignment overview, SRS, scope, traceability, README |
| **DEC-02: Client scope** | React web; Flutter **Customer and Courier** experiences | Confirm which functions also appear on web | REQ + UI | SRS, architecture, API inventory, diagrams, roadmap |
| **DEC-03: Capability services** | Identity API, Delivery Operations API, Merchant Integration API, YARP Gateway, and Notification/Webhook Worker | Decide whether SignalR hub lives in Delivery API or a justified separate component | ARCH | Technical design, service catalog, API, diagrams, deployment |
| **DEC-04: Database runtime** | Four separately owned logical databases, including notifications; **decide** one PostgreSQL instance with four DBs vs four containers | Determine local/staging configuration and physical port map | ARCH + OPS | Data architecture, Docker, local setup, ER diagrams |
| **DEC-05: Login protocol** | Prefer consistent `POST /api/v1/auth/google` with client-supplied Google ID token **if** approved for both clients | Or authorization-code + PKCE flow and matching backend endpoint; document both client flows separately if necessary | SEC + UI | Auth spec, REST, sequence/activity diagrams |
| **DEC-06: Canonical parcel state machine** | Define a single status enum and transition matrix; a created booking exists **after** customer confirms fee | Explicit handling of `Pending`/`Confirmed`, `OutForDelivery`, `Failed`, cancellation, retry, reassign | DEL + REQ | SRS, ER, GraphQL, REST, events, UML |
| **DEC-07: Merchant order ingestion** | Document single-order synchronous and/or bulk asynchronous flows explicitly, including durable recovery and idempotency | Do not mix `201 Created`, `202 Accepted`, and undefined gRPC calls for one operation | MER + DEL + API | Merchant REST, gRPC, integration, UML |
| **DEC-08: Realtime responsibilities** | Consider SSE for parcel status; SignalR/WebSockets only for an **approved** courier telemetry/live map requirement | Could use SSE only for mandatory live status, since bonus GPS telemetry adds workload | ARCH + UI | API, integration, realtime, WebSocket, deployment |
| **DEC-09: Event contract and routing** | Use declared MassTransit publish/consume topology with **one authoritative event schema catalog** | Define whether `StatusChanged` is the canonical notification trigger; suppress duplicate notifications from specialized events | MSG + DEL | Event catalog, integration, webhook, UML |
| **DEC-10: Webhook ownership** | Merchant API owns subscriptions/secrets/attempt records; worker calls approved Merchant API or receives scoped signing material securely | Do not allow worker to directly query/write Merchant DB in violation of boundaries | MER + MSG + SEC | Service catalog, data architecture, webhook, UML |
| **DEC-11: GraphQL placement** | Host GraphQL at an explicitly named service, accessed through YARP; document whether it is a BFF or Delivery API module | Clarify the owner of multi-domain resolvers | ARCH + API | Technical design, GraphQL, service catalog, deployment |
| **DEC-12: Scope of Redis and object storage** | Treat each as explicitly adopted infrastructure or remove unsupported dependencies | Resolve JWT revocation, SignalR backplane, SSE topology, private POD storage | SEC + OPS + ARCH | Data architecture, auth, WebSocket, Docker/K8s |

**ADR approval rule:** An ADR may say `Accepted` only after the responsible team member(s) approve it. Otherwise mark it `Proposed`. Capture the approver/date and link the corresponding code or design issue.

---

## 3. Complete issue → fix register

Each entry contains the observed issue, affected source files, the concrete correction, and an acceptance check. Relative links assume this file is placed at the repository root.

### A. Assignment, requirements, governance and project status

#### REQ-01 · P0 · Team-selected technologies misrepresented as lecturer mandates
- **Issue:** [`requirements/assignment-overview.md`](requirements/assignment-overview.md) presents ASP.NET Core, PostgreSQL, microservices, GraphQL, and gRPC as mandatory. The original assignment allows a suitable backend framework and layered/microservice/modular-monolith architecture, and requires secure **REST or GraphQL** APIs. It requires message-broker integration, not RabbitMQ specifically.
- **Fix:** Split requirements into **Official assignment constraints**, **Team technical choices**, and **Bonus targets**. Keep the approved .NET stack, PostgreSQL, YARP, RabbitMQ and any additional protocols under team decisions. Clarify the assignment is worth **20 marks overall**, while its four assessment categories are weighted 20/50/15/15.
- **Done when:** Each lecturer requirement can be traced verbatim in meaning to the assignment PDF; chosen technologies are not falsely attributed to it. **Owner:** REQ.

#### REQ-02 · P0 · Mandatory features categorized as `Should`
- **Issue:** [`requirements/srs.md`](requirements/srs.md) marks **download receipt (FR-C08)**, **merchant dashboard (FR-M06)**, and **basic admin reports (FR-A06)** as `Should`, although the assignment explicitly requires all three. The assignment also requires a mobile-friendly **public tracking page**.
- **Fix:** Change these to `Must`; state minimum acceptance criteria (receipt download, merchant order/status dashboard, deliveries-per-day and success/failure reports, safe public tracking). Update scope, traceability, tests, demos and work allocation.
- **Done when:** Every official functional requirement is marked `Must` and linked to API/UI/test owners. **Owner:** REQ.

#### REQ-03 · P1 · Flutter scope contradicts confirmed agreement
- **Issue:** [`architecture/technical-design.md`](architecture/technical-design.md) calls Flutter a dedicated Courier app, and [`api/api-reference.md`](api/api-reference.md) alternates between Flutter/MAUI and courier-only. The agreed deliverable is **Flutter for Customer and Courier**.
- **Fix:** Update SRS interfaces, technical design, API client matrix, diagrams, test strategy, deployment/setup and roadmap to explicitly cover both mobile personas. Remove unexplained MAUI references.
- **Done when:** Customer booking/tracking and courier assignment/status are documented for Flutter, with API authentication and access control. **Owner:** REQ + UI.

#### REQ-04 · P1 · Use cases lack fully standardized narrative flows
- **Issue:** [`design/diagrams/use-cases/README.md`](design/diagrams/use-cases/README.md) contains useful actor/use-case mapping, but the core flows lack uniformly specified preconditions, successful path, alternatives, exceptions and postconditions.
- **Fix:** Add `requirements/use-case-specifications.md` (or one file per use case). Describe at least booking/fee estimate, merchant order creation, courier status+notifications, and Google login. Include actor, entry point, authorization, inputs, decisions, failure cases, outputs, state changes and traceability ID.
- **Done when:** Sequence and activity diagrams can be reproduced from approved use-case narratives without inventing behavior. **Owner:** REQ + UML.

#### GOV-01 · P1 · Documentation claims completed implementation despite planning status
- **Issue:** [`project-management/milestones.md`](project-management/milestones.md) marks Identity, Delivery, Merchant, and other implementation milestones as completed; [`submission/submission-checklist.md`](submission/submission-checklist.md) marks diagram/design work complete. The most recent team clarification described work as **planning only**; implementation completion was not independently verified.
- **Fix:** Verify completion against linked PRs, tested builds, running demo, commits, and reviewed diagrams. If unsupported, change to `Planned`, `Draft` or `In Review`; record the evidence link for each genuinely completed item.
- **Done when:** Status labels reflect demonstrable reality instead of a speculative schedule. **Owner:** PM + QA.

#### GOV-02 · P1 · Member assignments presented as factual before allocation
- **Issue:** [`project-management/team-responsibilities.md`](project-management/team-responsibilities.md) assigns `Member 1`…`Member 10`, records paired design tasks as completed, and gives a RACI matrix although team allocation was previously undecided.
- **Fix:** Mark allocations `Proposed` unless confirmed by a team meeting; replace placeholders with actual approved GitHub handles/names when available. Maintain a distinct contribution-evidence log, with PR links and review sign-off.
- **Done when:** No member is attributed work they did not perform; every confirmed allocation has an owner and evidence. **Owner:** PM.

#### GOV-03 · P1 · ADR `Accepted` conflicts with draft/unapproved baseline
- **Issue:** [`architecture/technical-design.md`](architecture/technical-design.md) and [`architecture/decisions/README.md`](architecture/decisions/README.md) label decisions `Accepted`, while conflicting parts of the design remain `Draft`.
- **Fix:** Confirm actual approval; downgrade unapproved ADRs to `Proposed`; include decision date, approver, alternatives, consequences, and linked affected documents. Create ADRs for DEC-03 through DEC-12 where appropriate.
- **Done when:** Accepted ADRs and all dependent technical documents agree. **Owner:** ARCH + PM.

#### GOV-04 · P2 · Requirement traceability counts are incorrect
- **Issue:** [`requirements/srs.md`](requirements/srs.md) lists **32 functional requirements** (8 customer, 7 merchant, 5 courier, 5 dispatcher, 7 admin) and **20 NFRs**. [`requirements/requirements-traceability.md`](requirements/requirements-traceability.md) summarizes only 10 NFRs and a total of 42, although the current SRS yields **52** requirements.
- **Fix:** Recalculate the matrix from all FR and NFR IDs; map NFR-18 through NFR-20 as well. Reconcile counts with the actual test-case catalog. Make the summary derive from table entries or verify with a review checklist.
- **Done when:** Per-category and total counts add up to 32 FR + 20 NFR = 52, unless the SRS is formally revised. **Owner:** REQ + QA.

#### GOV-05 · P2 · Internal schedule versus confirmed submission date is unclear
- **Issue:** [`project-management/milestones.md`](project-management/milestones.md) lists an internal November 12 final milestone and September–October tasks as already done, while **15 November 2026** is the confirmed submission deadline.
- **Fix:** Clearly label November 12 as optional internal code freeze/rehearsal; keep November 15 as external submission. Refresh task dates based on actual progress and assignment approvals, not generated historical milestones.
- **Done when:** Schedule, submission checklist, demo plan and README consistently distinguish freeze from submission. **Owner:** PM.

#### GOV-06 · P2 · Documentation/test completion claims exceed evidence
- **Issue:** [`submission/submission-checklist.md`](submission/submission-checklist.md) and [`testing/`](testing/) may refer to ready catalogs, success gates or coverage targets as if tests have been executed. Coverage targets alone are not test results.
- **Fix:** Distinguish `Test cases drafted`, `Tests implemented`, `Tests executed`, `Passing`, and `Evidence attached`. Use actual CI artifact URLs and dated coverage output. Review SRS acceptance text claiming **≥60% integration coverage**, which is not separately defined or measured elsewhere.
- **Done when:** Every green/check-marked verification has reproducible evidence. **Owner:** QA + PM.

#### GOV-07 · P2 · README and final-report summaries can drift
- **Issue:** Root [`README.md`](README.md), [`submission/final-report.md`](submission/final-report.md), and other summaries may preserve prior service inventory, technology mandates or unverified completion statements after fixes.
- **Fix:** Update overview tables **last**, after the approved architecture/contract corrections. Keep high-level docs linked to the primary source instead of copying large mutable contract tables.
- **Done when:** Summary statements match current ADRs, service catalog, SRS and actual progress. **Owner:** PM + ARCH.

#### GOV-08 · P3 · Bonus features not consistently separated from required delivery
- **Issue:** Kubernetes is sometimes described as standard production deployment; [`bonus/ai-delivery-assistant.md`](bonus/ai-delivery-assistant.md) is still a placeholder despite both bonuses being targeted.
- **Fix:** Keep Kubernetes and AI explicitly **bonus** unless separately required by the team. Define a minimal AI scope only after APIs and RBAC are settled: `TrackParcel` and `EstimateFee` tool calls with strict user/merchant authorization, no unsupported autonomous actions. Track each bonus independently from mandatory release acceptance.
- **Done when:** The required system can be demonstrated without depending on either bonus. **Owner:** ARCH + OPS + PM.

### B. Architecture, data ownership and infrastructure

#### ARC-01 · P1 · Canonical service inventory and real-time hub hosting disagree
- **Issue:** [`architecture/technical-design.md`](architecture/technical-design.md) describes three capability APIs plus gateway/worker. [`api/api-reference.md`](api/api-reference.md) adds a `:5004` real-time hub, and various diagrams show differing components.
- **Fix:** Publish one canonical service inventory with process/container name, responsibility, host, port and data owner. Decide whether realtime lives inside Delivery API or is an explicitly justified separate service; update service diagrams and Compose accordingly.
- **Done when:** Every architecture and deployment document shows the same processes and routes. **Owner:** ARCH + API + OPS.

#### ARC-02 · P0 · Background worker accesses Merchant DB across service boundary
- **Issue:** [`architecture/service-catalog.md`](architecture/service-catalog.md) says private databases, but the worker reads Merchant signing secrets and writes Merchant delivery attempts directly; [`integration/merchant-webhooks.md`](integration/merchant-webhooks.md) diagrams do the same.
- **Fix:** Define a Merchant API operation or tightly controlled event/command interface for subscription lookup, signing authorization and attempt logging. If worker must own delivery attempts, move that table to the worker database and expose it through an API instead; do not keep conflicting ownership models.
- **Done when:** The service interaction matrix, ER diagram and all webhook sequences show **no unauthorized cross-service DB access**. **Owner:** ARCH + MER + MSG.

#### ARC-03 · P1 · GraphQL BFF responsibility is ambiguous
- **Issue:** [`api/graphql-api.md`](api/graphql-api.md) says the GraphQL endpoint is mainly hosted by Delivery Operations, while technical design calls it a frontend aggregation/BFF layer and the API inventory depicts inconsistent routing.
- **Fix:** Choose a deployment location and resolver ownership. Clarify that YARP routes `/graphql` to that host; cross-domain data is fetched through service APIs, not other services' databases. Keep mutations calling shared application handlers rather than implementing separate business rules from REST.
- **Done when:** GraphQL's host, gateway route and service dependencies appear identically in service catalog/API/Compose. **Owner:** ARCH + API.

#### ARC-04 · P1 · Physical database topology and fourth database disagree
- **Issue:** [`architecture/data-architecture.md`](architecture/data-architecture.md) claims four private DBs on one PostgreSQL server; [`architecture/service-catalog.md`](architecture/service-catalog.md) presents four DB ports; [`deployment/docker-compose.md`](deployment/docker-compose.md) describes only three PostgreSQL containers while the worker owns `swiftdrop_notifications`.
- **Fix:** Approve either (a) one PostgreSQL instance hosting four logical databases with separate users, or (b) four PostgreSQL containers with consistent internal/host port mappings. Add the notification DB and its migration/volume/healthcheck everywhere. A DB's internal `5432` port is not automatically the host port.
- **Done when:** A clean Compose environment creates all intended databases and no service uses another service's credentials. **Owner:** ARCH + OPS.

#### ARC-05 · P2 · Redis appears without a consistently agreed role
- **Issue:** [`security/authentication.md`](security/authentication.md) uses Redis for token revocation; [`api/websocket-protocol.md`](api/websocket-protocol.md) specifies a Redis SignalR backplane; deployment includes Redis, but some architecture diagrams do not.
- **Fix:** Record whether Redis is necessary for the demo. If adopted, document which service depends on it, failure behavior and Compose/K8s configuration. If not, remove Redis-backed commitments and state the simpler session/revocation model.
- **Done when:** Every infrastructure dependency has a documented reason and matching deployment config. **Owner:** ARCH + SEC + OPS.

#### ARC-06 · P1 · Service-to-service direction and operation ownership mismatch
- **Issue:** Service catalog emphasizes Delivery → Merchant validation, while the merchant order sequence calls Merchant → Delivery to create parcels. [`api/grpc-services.md`](api/grpc-services.md) includes other internal calls not represented consistently.
- **Fix:** Define a call matrix per business operation: initiator, target, method, authentication, timeout, idempotency and failure semantics. Show both directions only where needed. Avoid a direct call merely to validate tokens if local JWT/JWKS verification is the approved mechanism.
- **Done when:** Every drawn synchronous arrow maps to an actual published contract. **Owner:** ARCH + MER + DEL + API.

#### ARC-07 · P1 · Proof/receipt storage and access rules incomplete
- **Issue:** [`architecture/data-architecture.md`](architecture/data-architecture.md) correctly proposes private object storage, but API examples expose direct storage URLs and do not fully specify who authorizes downloads or how upload errors interact with final delivery status.
- **Fix:** Specify private storage, authorized download endpoints or short-lived signed URLs, content/size validation, lifecycle/cleanup of orphan uploads, and what happens when proof save succeeds but DB status transaction fails.
- **Done when:** Unrelated customers and public tracking users cannot access POD images/signatures or private receipts. **Owner:** SEC + DEL.

#### ARC-08 · P2 · Gateway versus domain authorization is not completely distinguished
- **Issue:** Some docs suggest JWT and API key validation at YARP, while others validate merchant keys only in Merchant API and verify ownership at Delivery API.
- **Fix:** Specify gateway responsibilities (routing, optional coarse authentication, rate limiting) versus service responsibilities (token/key validation as appropriate, role and **resource ownership**). Do not trust client-submitted merchant/user IDs. Clarify key revocation/role changes and internal service JWT rules.
- **Done when:** Authorization policies are consistent in service catalog, REST, GraphQL, security spec and tests. **Owner:** SEC + ARCH.

### C. API contracts and account security

#### API-01 · P0 · Path/version contract drift
- **Issue:** [`api/rest-api.md`](api/rest-api.md) primarily uses `/api/v1/parcels`, `/api/v1/deliveries`, etc., while [`requirements/requirements-traceability.md`](requirements/requirements-traceability.md), [`design/diagrams/sequence/README.md`](design/diagrams/sequence/README.md), and some webhook docs use `/api/bookings`, `/api/dispatch`, `/api/merchant-orders`, or `/api/webhooks/subscribe`.
- **Fix:** Adopt a canonical versioned REST route catalog with method, operation ID, ownership, auth and request/response. Update all references. If backward-compatible aliases are intended, explicitly document them rather than silently allowing alternatives.
- **Done when:** No diagram/traceability entry calls a nonexistent or differently named operation. **Owner:** API.

#### API-02 · P1 · Local signup/login endpoints missing from REST baseline
- **Issue:** The assignment and SRS require secure signup/login and the authentication document specifies email/password with Argon2id, but the REST reference mainly documents Google and refresh.
- **Fix:** Define registration, password login, validation/rate limiting, password reset only if in scope, and account linking policy. Add corresponding error cases/tests. Add `password_hash`/local credentials to the Identity data model if local login remains supported.
- **Done when:** Every SRS authentication Must maps to an endpoint and concrete database fields. **Owner:** SEC + API.

#### API-03 · P0 · Google OAuth/OIDC flow conflicts between documents
- **Issue:** [`design/diagrams/sequence/README.md`](design/diagrams/sequence/README.md) models Google returning an **authorization code** and Identity API exchanging it. [`security/authentication.md`](security/authentication.md), [`api/rest-api.md`](api/rest-api.md) and [`api/api-reference.md`](api/api-reference.md) specify frontend ID-token exchange.
- **Fix:** Approve a **single flow per client**. For ID-token exchange, show Google SDK sign-in, frontend obtains ID token, backend validates issuer/audience/signature/expiry and issues app tokens; for authorization-code+PKCE, define redirect URI, code exchange and browser/mobile handling. Update the endpoint request body and both diagrams to match.
- **Done when:** The sequence can be implemented directly from the REST/auth specifications without a protocol substitution. **Owner:** SEC + UI + UML.

#### API-04 · P0 · Unsafe public GraphQL tracking result
- **Issue:** [`api/graphql-api.md`](api/graphql-api.md) exposes public `trackParcel(trackingNumber): Parcel`, where `Parcel` includes recipient phone, complete addresses, assigned courier and proof-of-delivery URL fields. The public tracking query example requests some of these private details.
- **Fix:** Introduce `PublicTrackingSummary` with safe status, coarse origin/destination, last update and redacted timeline. Use a separate authenticated/authorized `Parcel` query for sensitive details. Disable field-level leakage through nested objects or introspection-based assumptions; test anonymous access.
- **Done when:** Anonymous tracking cannot retrieve addresses, contact numbers, POD files or private courier details. **Owner:** API + SEC.

#### API-05 · P0 · Public REST tracking returns overly detailed location/identity
- **Issue:** [`api/rest-api.md`](api/rest-api.md) public tracking example contains a street address in its timeline and identifies the courier.
- **Fix:** Use the same privacy-limited tracking projection as GraphQL; redact precise addresses, recipient/driver contacts and POD. Keep authenticated owner/admin detail endpoints separate.
- **Done when:** Public REST and GraphQL disclose only the same approved safe tracking fields. **Owner:** API + SEC.

#### API-06 · P1 · Fee estimation/confirmation contract incomplete
- **Issue:** The assignment requires fee preview **before** confirmation, and [`design/diagrams/sequence/README.md`](design/diagrams/sequence/README.md) calls `/api/bookings/estimate`, but [`api/rest-api.md`](api/rest-api.md) does not fully define a matching fee-quote operation. GraphQL mutation creates a parcel directly.
- **Fix:** Define quote request/response, validation, pricing rules, quote expiry or snapshot policy, and booking-confirmation input (with or without quote ID). Ensure REST and GraphQL invoke equivalent pricing/booking logic.
- **Done when:** Price shown before confirm is reproducible and the booking stores a consistent price snapshot. **Owner:** DEL + API.

#### API-07 · P1 · Mandatory receipt, dashboard and report interfaces missing/incomplete
- **Issue:** Required receipt download, merchant dashboard, and admin operational reports are not fully specified in API/traceability.
- **Fix:** Define minimal authenticated endpoints or GraphQL queries with authorization and payloads, including receipt file access, merchant's orders and statuses, deliveries/day, and delivery success/failure rates. Map FR-C08, FR-M06 and FR-A06 to tests.
- **Done when:** Each feature has a UI entry, API operation, test case and demo step. **Owner:** API + DEL + MER + REQ.

#### API-08 · P0 · Merchant single-order versus bulk contract conflict
- **Issue:** [`design/diagrams/sequence/README.md`](design/diagrams/sequence/README.md) shows `POST /api/merchant-orders` returning `201`, while [`api/rest-api.md`](api/rest-api.md) emphasizes `POST /api/v1/merchant/parcels/bulk` returning `202`.
- **Fix:** Document **two separate endpoints** if both are needed, with explicit sync/async outcomes, job status retrieval and idempotency. Otherwise retire one flow and update all diagrams. State whether the merchant dashboard reads order jobs or confirmed Delivery parcels.
- **Done when:** A merchant client can determine if an order was created, merely accepted, rejected or awaiting retry. **Owner:** MER + API + DEL.

#### API-09 · P0 · Merchant sequence calls undefined gRPC method
- **Issue:** The merchant sequence uses `CreateBooking(order, service_jwt)`, but [`api/grpc-services.md`](api/grpc-services.md) defines `CheckZoneCapacity`, `ReserveParcelSlot`, and `GetDeliveryStatus` for Delivery; there is no matching `CreateBooking` RPC.
- **Fix:** Either define and version `CreateBooking`/`CreateParcels` in the `.proto` contract with response/error/idempotency semantics, or redesign ingestion to use the existing reservation+event workflow. Ensure code contract files, REST endpoints and diagrams agree.
- **Done when:** Every gRPC method shown in diagrams exists verbatim in the authoritative `.proto` specification. **Owner:** API + MER + DEL.

#### API-10 · P1 · GraphQL and REST can diverge on writes
- **Issue:** `createParcel` and `assignCourier` GraphQL mutations overlap REST operations, with differences in request fields, roles and statuses.
- **Fix:** Map both protocols to the same application command handlers and business policies. Normalize status enums, auth requirements, error mapping and important fields; document the canonical write operation and expose wrappers as necessary.
- **Done when:** Identical business actions through either protocol produce equivalent validation and state changes. **Owner:** API + DEL.

#### API-11 · P1 · Merchant API credentials are inconsistently specified
- **Issue:** Examples alternate among `sk_live_...`, `swd_live_...`, `X-API-Key` and JWT. API key hashing, scopes and registration permissions need one policy across specs.
- **Fix:** Standardize format, header, storage with high-entropy one-time-visible secret, key revocation, scopes, approval prerequisite, and whether a merchant human uses app JWT while their external system uses an API key. Never put secrets in sample logs.
- **Done when:** All merchant endpoint auth tables, examples and tests share one credential model. **Owner:** SEC + MER + API.

#### API-12 · P1 · Google account linking by email risks unintended linking
- **Issue:** [`security/authentication.md`](security/authentication.md) permits finding/creating records by Google subject **or email** and linking identities without an explicit account ownership verification step.
- **Fix:** Make provider subject the stable identity key; if a matching local email exists, require an approved verified-account linking procedure rather than silently merging identities. Cover first-time, returning, email collision and disabled-account cases.
- **Done when:** A Google response cannot automatically take over or link another account just because emails match. **Owner:** SEC.

### D. Delivery workflows, states and distributed consistency

#### FLOW-01 · P0 · Parcel status vocabulary and transitions differ
- **Issue:** [`design/diagrams/er/README.md`](design/diagrams/er/README.md) uses `Pending → Confirmed → Assigned → PickedUp → InTransit → Delivered/Failed`; [`api/graphql-api.md`](api/graphql-api.md) uses `CREATED, ASSIGNED, PICKED_UP, IN_TRANSIT, OUT_FOR_DELIVERY, DELIVERED, FAILED, CANCELLED`; REST examples use `Created`; activity diagrams add other implicit transitions.
- **Fix:** Publish `architecture/parcel-state-machine.md` with a canonical enum, transition table (from/to, role, guard, action, event), public labels and internal enum mapping. Cover `OutForDelivery`, cancellation, failure after pickup, reassignment, terminal states and invalid repeats. Define when a quote becomes a booking.
- **Done when:** SRS, ER state diagram, REST, GraphQL, events, tests, all sequence/activity diagrams share one transition policy. **Owner:** DEL + REQ.

#### FLOW-02 · P1 · Proof of delivery and final state have unclear atomicity
- **Issue:** [`api/rest-api.md`](api/rest-api.md) suggests POSTing POD marks delivery `Delivered`, while the sequence shows status and proof operations with unclear ordering and rollback behavior.
- **Fix:** Define whether POD upload completes delivery or is a prerequisite for a separate status mutation. Specify storage confirmation, DB transaction, authorization, required fields, failure retry and idempotency. Mark `Delivered` only after approved proof conditions are met.
- **Done when:** Courier cannot mark someone else's parcel delivered or complete a required-POD delivery without acceptable proof. **Owner:** DEL + SEC.

#### FLOW-03 · P1 · Booking idempotency checks are race-prone in diagram form
- **Issue:** [`design/diagrams/sequence/README.md`](design/diagrams/sequence/README.md) shows check-then-insert idempotency; under concurrent requests, both checks may report no record.
- **Fix:** Define a unique database constraint and atomic reservation/insert/transaction behavior; bind keys to customer/merchant and request fingerprint; store reproducible response; specify `409` for same key with different payload. Add concurrent duplicate-request tests.
- **Done when:** Concurrent retries cannot create duplicate parcels or charge/quote twice. **Owner:** DEL + API + QA.

#### FLOW-04 · P0 · Merchant and Delivery writes lack durable partial-failure recovery
- **Issue:** Merchant DB inbox job and Delivery DB parcel are not one atomic transaction. The current sequence lacks timeout, duplication and unknown-outcome recovery paths.
- **Fix:** Adopt an explicit reliable workflow: durable merchant inbox job, stable external order ID/idempotency key, Delivery create/reservation operation, retry with reconciliation, final job state and status query. Define compensating action if needed, and avoid distributed DB transactions for the academic baseline.
- **Done when:** Merchant can distinguish `Accepted`, `Created`, `Failed`, `Retrying`; a retry never creates two parcels. **Owner:** MER + DEL + MSG.

#### FLOW-05 · P1 · Courier assignment and status authorization need a single policy
- **Issue:** Different API/authorization diagrams allow Dispatcher/Admin status writes in some places, while Courier is assignment-scoped; validation and reassignment race cases are under-specified.
- **Fix:** Approve actor-to-transition permission matrix, ownership checks, expected concurrency token/version, valid reassignment/cancellation actions, and complete error outcomes. Apply it to API and UML alternatives.
- **Done when:** A courier cannot update an unassigned parcel, and reassignment/status racing requests behave predictably. **Owner:** DEL + SEC.

#### FLOW-06 · P1 · Event publication and business status are ordered inconsistently
- **Issue:** [`design/diagrams/activity/README.md`](design/diagrams/activity/README.md) shows notify customer and then publish the delivered event, while the technical architecture requires committing state+outbox **before** asynchronous publication and consumer notification.
- **Fix:** In every diagram: validate → atomically persist state/history/outbox → return or acknowledge → outbox relay publishes → independent consumers notify/update realtime/send webhooks. Show async interactions separately from the user request timeline.
- **Done when:** No diagram implies successful notification/webhook is a prerequisite for a committed delivery status change. **Owner:** UML + MSG + DEL.

### E. Messaging, webhooks and real-time delivery

#### INT-01 · P1 · RabbitMQ exchange topology contradicts itself
- **Issue:** [`architecture/service-catalog.md`](architecture/service-catalog.md) advertises `swiftdrop.events` **topic** exchange; [`integration/event-catalog.md`](integration/event-catalog.md) and [`integration/integration-design.md`](integration/integration-design.md) use MassTransit fanout exchanges per message type.
- **Fix:** Select one actual MassTransit topology; publish exact message type, exchange, queue, binding, consumer and retry/error queue. Avoid documenting a custom single topic exchange unless explicitly configured.
- **Done when:** Event catalog's topology corresponds to the infrastructure the team will actually start. **Owner:** MSG.

#### INT-02 · P1 · Event producers/consumers and queues are not consistent
- **Issue:** The catalog lists events with no consumers, consumer names not found in the service inventory, and both `StatusChanged` and specialized events with overlapping listeners.
- **Fix:** Define a complete producer → message → consumer → effect matrix. Remove unused event contracts or label them planned; ensure notifications, webhook dispatcher, and realtime are explicitly assigned to concrete worker/API components.
- **Done when:** Every required status-change side effect has exactly one documented consumer path and corresponding test. **Owner:** MSG + ARCH.

#### INT-03 · P1 · Duplicate status events could cause duplicate notifications
- **Issue:** `StatusChanged`, `ParcelPickedUp`, `ParcelDelivered` and `DeliveryFailed` can describe the same transition, potentially triggering the same webhook or notification more than once.
- **Fix:** Designate canonical trigger(s) and subscriber filter rules. Add stable event IDs, inbox deduplication per consumer, idempotent webhook job creation per event/subscription, and clear event type mapping for external webhooks.
- **Done when:** One business transition produces one intended notification/webhook per recipient, despite broker retries. **Owner:** MSG + MER.

#### INT-04 · P1 · Consumer retries and external webhook retries are conflated
- **Issue:** [`integration/integration-design.md`](integration/integration-design.md) documents 3 immediate + 3 delayed messaging retries; [`integration/merchant-webhooks.md`](integration/merchant-webhooks.md) has five webhook delivery attempts; the webhook sequence lists a different five-retry delay series.
- **Fix:** Separate **broker message redelivery** from **HTTP webhook delivery**. Specify total attempts vs retries (e.g., first try plus four retries), exact schedule, 429/4xx/5xx handling, DLQ/manual replay, and attempt-level persistence.
- **Done when:** The event, integration, webhook and sequence docs all reference the same policy with no off-by-one attempt count. **Owner:** MSG + MER.

#### INT-05 · P0 · HMAC signing cannot use a stored one-way secret hash
- **Issue:** [`design/diagrams/sequence/README.md`](design/diagrams/sequence/README.md) passes `secret_hash` to the worker for HMAC, while Merchant API data model separately stores encrypted secrets.
- **Fix:** Store a retrievable **encrypted webhook signing secret**, with authorization-controlled decryption only in the owning component; do not sign using a password-style hash. Revise payload signing and rotation approach. Keep merchant API keys hashed separately.
- **Done when:** A registered merchant can independently verify delivered signatures, and private signing material is not exposed through public APIs or logs. **Owner:** SEC + MER + MSG.

#### INT-06 · P1 · Webhook retry timestamps and replay windows must be compatible
- **Issue:** Webhook docs recommend rejecting signed payloads older than five minutes but retry the same event for over an hour. Reusing the original signature timestamp could make valid retries unverifiable.
- **Fix:** Recompute `X-SwiftDrop-Timestamp` and signature **on every attempt** while retaining the stable `X-SwiftDrop-Event-Id`; document signing bytes, timestamp tolerance, clock skew and deduplication.
- **Done when:** Retried webhooks remain valid without permitting arbitrary replay. **Owner:** MER + SEC.

#### INT-07 · P0 · Webhook destination SSRF/control validation missing
- **Issue:** Merchant webhook URLs are user-configurable; the current description does not establish sufficient restrictions against local network/internal metadata destinations or redirect abuse.
- **Fix:** Validate `https` URLs, reject localhost/private/link-local/metadata addresses and unsafe DNS results, re-check redirects and resolution at send time, limit response size/time, and restrict worker egress if feasible. Record failures safely.
- **Done when:** Integration tests reject attempted internal-resource webhook targets. **Owner:** SEC + MER.

#### INT-08 · P1 · Browser `EventSource` example uses unsupported Authorization headers
- **Issue:** [`integration/realtime-tracking.md`](integration/realtime-tracking.md) uses `new EventSource(url, { headers: { Authorization: ... } })`; native browser EventSource does not support arbitrary headers.
- **Fix:** Use an approved cookie/session-based SSE mechanism (with CSRF considerations) or an authenticated fetch-streaming client that can set headers. Do not put long-lived JWTs into general query strings. Update React/Flutter examples and auth spec.
- **Done when:** Real browser and Flutter clients can subscribe with correctly enforced parcel ownership. **Owner:** UI + SEC + API.

#### INT-09 · P1 · SSE `Last-Event-ID` replay is promised but not implemented in the design
- **Issue:** [`integration/realtime-tracking.md`](integration/realtime-tracking.md) claims missed events replay after reconnection while showing only an in-memory connection manager.
- **Fix:** Either design durable replay from `booking_history`/event log with cursor rules and retention **or** explicitly state that reconnect refetches the current parcel state before resubscribing (appropriate for status dashboards). Align event IDs and ordering semantics.
- **Done when:** A disconnect/reconnect test produces correct current tracking state without missing permanent updates. **Owner:** MSG + API.

#### INT-10 · P1 · SSE vs SignalR/WebSocket usage and hub ownership inconsistent
- **Issue:** SRS states SSE; [`api/websocket-protocol.md`](api/websocket-protocol.md) defines SignalR courier GPS, Redis backplane and a separate hub; other docs describe SSE/WebSocket as interchangeable.
- **Fix:** Explicitly classify **status notifications**, **GPS telemetry**, and **dispatcher live map**; assign one protocol and owning host per use case. Treat GPS telemetry as additional planned scope unless approved by requirements; add privacy/authorization/retention limits for location telemetry.
- **Done when:** Client capability matrix, infra architecture, endpoint inventory and mobile specs use the same transport and host. **Owner:** ARCH + UI + MSG.

#### INT-11 · P1 · RabbitMQ consumer load-balancing is mistaken for realtime broadcast
- **Issue:** SSE documentation says RabbitMQ distributes tracking events to all API instances; a shared queue normally load-balances messages, not duplicates them to every instance.
- **Fix:** For horizontal scale, declare unique per-instance fanout subscriptions, a dedicated pub/sub backplane, or a shared realtime relay; alternatively keep a single instance for demo and label its limits. If using SignalR multi-instance, document Redis backplane and auth/connection routing.
- **Done when:** An event reaches all connected authorized clients regardless of which instance they use. **Owner:** MSG + OPS + ARCH.

#### INT-12 · P1 · Event payloads include unnecessary personal data
- **Issue:** [`integration/event-catalog.md`](integration/event-catalog.md) includes complete pickup/drop-off addresses in `ParcelBooked`, increasing data exposure across queues and logs.
- **Fix:** Minimize events to IDs, statuses, timestamps and information consumers strictly require; fetch sensitive details via an authorized service API when needed. Specify event versions, field schema and logging redaction.
- **Done when:** Subscribing workers cannot receive unneeded private addresses or phone numbers. **Owner:** SEC + MSG.

### F. Sequence/activity diagrams and design artifacts

#### UML-01 · P0 · Sequence messages use wrong endpoint names and status vocabulary
- **Issue:** [`design/diagrams/sequence/README.md`](design/diagrams/sequence/README.md) uses `/api/bookings`, `/api/dispatch/assign`, `/api/parcels/{id}/proof` and `Pending/Confirmed` while API/state documents use different routes/states.
- **Fix:** Update all sequence messages only **after** API-01 and FLOW-01 are approved. Cite the API operation ID and state-machine transition in each diagram's accompanying text.
- **Done when:** Every message and guard can be traced to an agreed API/event contract. **Owner:** UML + API.

#### UML-02 · P0 · Google login sequence does not match authentication spec
- **Issue:** Current Google sequence assumes frontend receives a code and backend exchanges it; authentication spec currently expects ID token.
- **Fix:** Redraw with the selected DEC-05 login protocol; include failed/cancelled Google login, invalid token and new/existing user branches. Cover Flutter if its flow materially differs from web.
- **Done when:** Authentication owners approve the same flow in the sequence, activity, security and REST docs. **Owner:** UML + SEC.

#### UML-03 · P1 · Courier sequence incorrectly uses React as the only client
- **Issue:** Courier assignment/status sequence shows Courier using the React SPA despite approved Flutter Courier scope.
- **Fix:** Add Flutter Courier App lifeline for courier-specific actions; retain React Dispatcher UI where appropriate. Include role/resource validation, invalid status and proof-upload failure paths.
- **Done when:** Sequence participants match the approved client-service architecture. **Owner:** UML + UI + DEL.

#### UML-04 · P1 · Merchant order sequence uses undefined method and hides recovery
- **Issue:** Merchant order sequence calls nonexistent `CreateBooking` RPC and shows only success.
- **Fix:** Reflect DEC-07 and API-08/API-09, including API-key validation, idempotent inbox job, Delivery creation/reservation, accepted/pending result, timeout/retry, unknown-outcome reconciliation and final status.
- **Done when:** Both main and failure path map to approved merchant/Delivery contracts and persistence. **Owner:** UML + MER + API.

#### UML-05 · P0 · Webhook sequence leaks architecture boundary and uses hashed secret
- **Issue:** Worker reads/writes Merchant DB and gets `secret_hash` for HMAC.
- **Fix:** Replace direct DB arrows with the approved Merchant API/service contract, retrieve/use encrypted signing material only through allowed boundaries, use persisted attempts and defined retry behavior.
- **Done when:** Webhook sequence passes ARC-02, INT-04, INT-05 and INT-06 checks. **Owner:** UML + MER + MSG + SEC.

#### UML-06 · P1 · Courier status → notification sequence not shown end-to-end
- **Issue:** Assignment/courier lifecycle and webhook delivery are separate, but the assignment explicitly asks for a courier status change **triggering notifications**.
- **Fix:** Add a self-contained sequence: Flutter Courier → YARP → Delivery Ops (authorization + transition) → DB/history/outbox transaction → relay → RabbitMQ → Notification Worker **and** merchant webhook (for merchant order) **and** authorized realtime feed. Show failure/duplicate protection.
- **Done when:** The required status-to-notification scenario is visible in one diagram and test case. **Owner:** UML + MSG + DEL.

#### UML-07 · P1 · Activity diagrams put asynchronous effects in the wrong order
- **Issue:** Lifecycle activity diagram shows receipt/notification before publishing its triggering event.
- **Fix:** Follow FLOW-06; distinguish business transaction from asynchronous consumer activities using swimlanes or separate activities. Add guards for fee refusal, no courier, failed delivery, cancellation and valid retry.
- **Done when:** Activity ordering agrees with outbox design and approved state machine. **Owner:** UML + DEL.

#### UML-08 · P1 · Mandatory activity coverage is not clearly complete
- **Issue:** [`design/diagrams/activity/README.md`](design/diagrams/activity/README.md) contains lifecycle, merchant onboarding, assignment/workload and auth activities; the **merchant API order** and **courier status-to-notification** paths are not individually represented as complete activities.
- **Fix:** Cover the four assignment flows, either with dedicated diagrams or clearly identifiable complete subflows and cross-references. Explicitly include merchant key validation, queued/created/rejected states, and async notification steps.
- **Done when:** A four-row assignment-to-diagram matrix has no missing process. **Owner:** UML + REQ.

#### UML-09 · P2 · Mermaid business flowcharts are not necessarily formal UML activities
- **Issue:** Current Mermaid `flowchart` diagrams are readable but not automatically full UML Activity notation (swimlanes, activity forks/joins, guards, initial/final nodes).
- **Fix:** For the final academic submission, prefer PlantUML activity syntax or diagrams.net UML activity symbols where swimlanes/forks are needed. Keep editable source plus consistent SVG/PNG/PDF exports. Do not overcomplicate simple workflows.
- **Done when:** Each submitted diagram is readable, technically accurate and reproducible from versioned source. **Owner:** UML.

#### UML-10 · P2 · Design diagram and final PDF traceability incomplete
- **Issue:** Architecture/ER/use-case/sequence/activity documents live in README files; exported assets and their design baselines are not uniformly indexed.
- **Fix:** Maintain a diagram index with ID, business scenario, SRS IDs, source file, rendered artifact, version, owner, review date, and related API/ADR links. Regenerate graphics after contracts change.
- **Done when:** Assessors can locate every mandatory diagram and reproduce its output. **Owner:** UML + PM.

### G. Testing, operations and final submission

#### QA-01 · P1 · Missing negative/security acceptance tests
- **Issue:** Testing and traceability docs do not consistently specify cases for public tracking leakage, cross-merchant access, courier accessing another courier's parcel, webhook replay/SSRF, auth linking and unauthorized POD access.
- **Fix:** Add tests for `401/403/404`, sensitive-field absence, assignment ownership, webhook HMAC verification/freshness, unsafe URL rejection, role changes and signed object downloads. Link each to SRS/SEC issues.
- **Done when:** Negative tests are specified and executed as part of integration gates. **Owner:** QA + SEC.

#### QA-02 · P1 · Distributed failure and idempotency tests incomplete
- **Issue:** Merchant partial failures, duplicate API requests, outbox replay, consumer duplicates, webhook retry and concurrent status transitions are important but not fully evidenced in the test plan.
- **Fix:** Add repeatable Testcontainers/integration scenarios: broker unavailable then reconnect, unknown gRPC outcome, duplicate merchant order, concurrent same idempotency key, duplicate `StatusChanged`, stale client transition, failed POD store and webhook endpoint 429/5xx.
- **Done when:** Each important recovery branch has at least one automated assertion. **Owner:** QA + DEL + MER + MSG.

#### QA-03 · P2 · Coverage counts and targets need a defined denominator
- **Issue:** SRS mentions ≥80% unit business-logic coverage and an unexplained ≥60% integration coverage requirement in acceptance text. Traceability/test dashboards are inconsistent on test case counts.
- **Fix:** Define what is included/excluded in unit coverage, how integration coverage would be calculated if retained, and the CI tools/reporting format. Report actual branch/line metrics separately; do not call planned percentages achieved.
- **Done when:** Coverage values come from dated CI reports and test totals match catalog entries. **Owner:** QA.

#### OPS-01 · P1 · Compose/architecture mismatch for DBs and worker dependencies
- **Issue:** [`deployment/docker-compose.md`](deployment/docker-compose.md) states three databases while documentation declares four. Worker access and notification persistence are unclear.
- **Fix:** Bring Compose in line with DEC-04 and ARC-02: four logical DBs, credentials, EF migrations, worker connection, data volumes, healthchecks, broker initialization and protected object storage. Check gateway/frontend/mobile access routing.
- **Done when:** `docker compose up --build` starts the required services and smoke tests pass on an empty development machine. **Owner:** OPS + ARCH.

#### OPS-02 · P2 · Port and environment addresses are not consistently labeled
- **Issue:** Local guides mix `localhost:5001/5002/5003`, container DNS names, several PostgreSQL ports, production-looking URLs and gRPC ports without clearly separating host and container networks.
- **Fix:** Maintain a single environment/port matrix: local host, Docker network, optional staging, protocol, purpose, TLS, source of environment variable. Use example domains as placeholders, not active environments.
- **Done when:** All setup instructions and integration examples resolve to an explicitly declared environment. **Owner:** OPS.

#### OPS-03 · P2 · Kubernetes write-up overclaims current deployment maturity
- **Issue:** [`deployment/kubernetes.md`](deployment/kubernetes.md) describes managed clusters, many replicas, zero-downtime and production guarantees, even though Kubernetes is a **bonus goal** and actual deployment was not verified.
- **Fix:** Label target/reference topology, keep a minimal reproducible local Kubernetes demo as first bonus milestone, and document actual manifests, resource constraints, health, secrets, DB and broker deployment. Claims such as zero-downtime must be backed by tests.
- **Done when:** The document differentiates proposed infrastructure from demonstrated deployment. **Owner:** OPS + QA.

#### OPS-04 · P2 · Local setup omits full mobile onboarding and sensitive config guidance
- **Issue:** [`deployment/local-setup.md`](deployment/local-setup.md) focuses on backend and web; the agreed Flutter Customer+Courier setup requires device/emulator, mobile OAuth configuration, base URLs and clear handling of dev secrets.
- **Fix:** Add Flutter environment/bootstrap, Android minimum version, emulator/physical-device networking, test accounts and OIDC redirect/deep-link configuration. Keep any demo passwords unmistakably local-only; never commit real secrets.
- **Done when:** A new team member can run the whole mandatory flow including Flutter without undocumented steps. **Owner:** OPS + UI.

#### OPS-05 · P2 · Submission evidence and documentation validation not yet fully checked
- **Issue:** Previous review did **not** complete automated broken-link checking or visually validate the committed architecture PDF. These are **verification gaps, not confirmed broken links or invalid graphics**.
- **Fix:** Run Markdown link checks (relative paths, anchors), Mermaid/PlantUML render checks, JSON/GraphQL/protobuf contract validation, and visually review diagrams and architecture PDF. Attach final screenshots/test/coverage/CI evidence and accurate member contribution sheet.
- **Done when:** No invalid internal links, diagrams render, files match the agreed baseline and the final PDF includes all mandatory deliverables. **Owner:** QA + PM + UML.

---

## 4. Required documentation updates by file

The following is a practical **file-level change checklist**; the issue register above provides details.

| File / group | Must update because of issues |
|---|---|
| `requirements/assignment-overview.md` | REQ-01, GOV-08 |
| `requirements/srs.md` | REQ-02, REQ-03, FLOW-01, API-02, API-06, GOV-04 |
| `requirements/scope-and-assumptions.md` | REQ-02, REQ-03, ARC-04, INT-10 |
| **NEW:** `requirements/use-case-specifications.md` | REQ-04, UML-06, UML-08 |
| `requirements/requirements-traceability.md` | GOV-04, API-01, API-02, API-07, QA-01, QA-03 |
| `architecture/service-catalog.md` | ARC-01, ARC-02, ARC-03, ARC-04, ARC-06, ARC-08 |
| `architecture/technical-design.md` | REQ-01, REQ-03, ARC-01, ARC-03, ARC-04, INT-10 |
| `architecture/data-architecture.md` | ARC-02, ARC-04, ARC-07, FLOW-02 |
| **NEW:** `architecture/parcel-state-machine.md` | FLOW-01, FLOW-02, FLOW-05 |
| `architecture/decisions/README.md` | GOV-03, DEC-01 through DEC-12 |
| `api/api-reference.md` | API-01, API-03, API-08, ARC-01, ARC-03, INT-10 |
| `api/rest-api.md` | API-01 through API-09, API-11 |
| `api/graphql-api.md` | API-04, API-06, API-10, ARC-03 |
| `api/grpc-services.md` | API-09, ARC-06, FLOW-04 |
| `api/websocket-protocol.md` | ARC-01, ARC-05, INT-10, INT-11 |
| `integration/integration-design.md` | INT-01, INT-02, INT-03, INT-04, FLOW-04 |
| `integration/event-catalog.md` | INT-01, INT-02, INT-03, INT-12 |
| `integration/merchant-webhooks.md` | ARC-02, INT-04, INT-05, INT-06, INT-07 |
| `integration/realtime-tracking.md` | INT-08, INT-09, INT-10, INT-11 |
| `security/authentication.md` | API-02, API-03, API-11, API-12, ARC-05 |
| `security/authorization.md` | ARC-08, FLOW-05, API-04, API-05, API-07 |
| `design/diagrams/sequence/README.md` | UML-01 through UML-06 |
| `design/diagrams/activity/README.md` | UML-07 through UML-09 |
| `design/diagrams/er/README.md` | ARC-02, ARC-04, FLOW-01, API-02 |
| `design/diagrams/architecture/architecture.md` + PDF | ARC-01 through ARC-06, REQ-03, INT-10, OPS-05 |
| `design/diagrams/use-cases/README.md` | REQ-02, REQ-04, API-07 |
| `testing/*` | GOV-06, QA-01, QA-02, QA-03 |
| `deployment/docker-compose.md` | ARC-04, ARC-05, OPS-01, OPS-02 |
| `deployment/local-setup.md` | OPS-01, OPS-02, OPS-04 |
| `deployment/kubernetes.md` | GOV-08, OPS-03 |
| `project-management/milestones.md` | GOV-01, GOV-05 |
| `project-management/team-responsibilities.md` | GOV-02 |
| `project-management/contribution-log.md` | GOV-02, GOV-06 |
| `submission/submission-checklist.md` | GOV-01, GOV-05, GOV-06, OPS-05 |
| `submission/final-report.md` + root `README.md` | GOV-07, REQ-01, GOV-08 |
| `bonus/ai-delivery-assistant.md` | GOV-08 (bonus, later) |

---

## 5. Implementation order and dependency gates

### Phase 0 — Confirm factual baseline (P0/P1)
**Participants:** PM, REQ, ARCH, diagram owners.

- [ ] Reconcile the lecturer assignment against SRS, including compulsory receipt, merchant dashboard, admin reporting and public tracking.
- [ ] Confirm the agreed Flutter **Customer + Courier** scope.
- [ ] Correct speculative completion statements, assignments, deadlines and accepted ADR labels.
- [ ] Identify one approver per shared contract and open issue/PR tracking for this register.

**Exit gate:** Mandatory functionality, status of each document and decision authority are unambiguous.

### Phase 1 — Freeze domain and service contracts (P0)
**Participants:** ARCH, DEL, MER, SEC, API, MSG.

- [ ] Approve service list, BFF/GraphQL hosting and four-DB topology.
- [ ] Fix worker-vs-Merchant data ownership and webhook signing secret model.
- [ ] Approve parcel state-transition table (including `OutForDelivery`, failure and cancellation).
- [ ] Approve Google flow, local login support and secure provider account linking.
- [ ] Choose merchant ingestion model and partial-failure recovery; define missing gRPC operations.
- [ ] Publish canonical REST route and event contract catalogs.

**Exit gate:** DEC-01–DEC-12 either approved or explicitly deferred with a safe scope decision; no P0 security or ownership contradiction remains.

### Phase 2 — Align external and internal interfaces (P0/P1)
**Participants:** API, DEL, MER, SEC, MSG, UI.

- [ ] Update REST, GraphQL, protobuf/gRPC and websocket/SSE specifications.
- [ ] Split public safe tracking from authenticated private tracking.
- [ ] Add quote, local signup/login, receipt, merchant dashboard and reporting contracts.
- [ ] Standardize event routing, idempotency, retry attempts and webhook timestamp/signature rules.
- [ ] Correct browser SSE authentication and reconnection/realtime topology.
- [ ] Build requirement → endpoint → event → test mapping for all 52 current SRS requirements (until SRS count changes).

**Exit gate:** All shared contracts are internally consistent, privacy-reviewed and ready for service implementation.

### Phase 3 — Correct UML artifacts (P1)
**Participants:** UML, REQ, API, DEL, MER, SEC, MSG, UI.

- [ ] Write four approved textual use-case specifications.
- [ ] Redraw customer fee estimate → confirm → booking sequence/activity.
- [ ] Redraw merchant secured API order → durable processing → parcel outcome sequence/activity.
- [ ] Redraw Flutter courier status change → outbox → RabbitMQ → notifications/webhook/SSE sequence/activity.
- [ ] Redraw Google OIDC authentication sequence/activity with one agreed token/code flow.
- [ ] Reconcile assignment/POD/webhook supporting diagrams and canonical status machine.
- [ ] Update diagram index and export editable + rendered copies.

**Exit gate:** Diagram owners and relevant backend/frontend owners approve every lifeline, operation, status and alternative path; all mandatory four flows are covered.

### Phase 4 — Validate deployment, tests and governance (P1/P2)
**Participants:** OPS, QA, PM, implementers.

- [ ] Make Docker Compose/local setup reflect actual services, four logical databases, secrets and storage.
- [ ] Define security, negative, recovery, idempotency, event and webhook integration tests.
- [ ] Verify real automated test results and coverage; remove unsupported completion claims.
- [ ] Check document links, rendered Mermaid/PlantUML, API schemas, actual code contracts and generated PDF.
- [ ] Refresh README, final report and submission checklist from approved primary documentation.

**Exit gate:** Design can be built, tested and demonstrated end-to-end, or unimplemented components are correctly marked planned.

### Phase 5 — Optional bonus preparation (P3)
**Participants:** OPS, AI feature owner, SEC, QA.

- [ ] Implement/document Kubernetes bonus on a demonstrable minimal environment, then expand only if time permits.
- [ ] Define the AI assistant's explicit permitted tool actions, authorization boundaries, test queries and error handling.
- [ ] Keep bonus work isolated from the ability to complete compulsory workflows and submission materials.

---

## 6. Diagram sign-off checklist (for assigned sequence/activity owners)

For **each** sequence/activity diagram, record:

- [ ] Diagram ID and title; SRS requirement ID(s); use-case reference.
- [ ] Actor/client correctly shown (React or **Flutter Customer/Courier**).
- [ ] Exact approved endpoint, RPC/event name and responsible service.
- [ ] Correct permissions and resource ownership guard.
- [ ] Valid state transition and persistence owner.
- [ ] Success branch, invalid input, unauthorized request and failure path.
- [ ] Correct outbox timing and asynchronous consumer behavior.
- [ ] Idempotency or retry branch where relevant.
- [ ] Public/private data segregation and no secret leakage.
- [ ] Review sign-off from API + owning domain (and SEC/MSG if relevant).

| Required assignment flow | Suggested sequence diagram | Suggested activity diagram | Prerequisite decisions |
|---|---|---|---|
| Customer creates delivery | `customer-booking-sequence` | `customer-booking-activity` | DEC-02, DEC-06, API-01/06 |
| Merchant creates order through API | `merchant-order-sequence` | `merchant-order-activity` | DEC-07, ARC-02, API-08/09 |
| Courier status triggers notifications | `courier-status-notification-sequence` | `courier-status-notification-activity` | DEC-06, DEC-09/10, INT-01/03/04 |
| OAuth 2.0 / Google OIDC login | `google-login-sequence` | `google-login-activity` | DEC-05, API-02/03/12 |

**Recommended drawing rule:** A sequence diagram explains **which participant calls whom and when**; an activity diagram explains **process decisions, actions and parallel branches**. Do not copy a sequence into a flowchart without modeling decisions and alternative paths.

---

## 7. Validation and acceptance test matrix

| Check ID | Verification | Expected evidence |
|---|---|---|
| VAL-01 | Compare required features against `EAD Group Assignment.pdf` | Every official requirement mapped to SRS `Must`, diagram/test/demo when applicable |
| VAL-02 | Compare REST paths in API catalog, traceability and sequence docs | Zero unexplained mismatched routes or methods |
| VAL-03 | Compare canonical states across SRS, ER, REST, GraphQL, events and UML | One enum + approved transition matrix |
| VAL-04 | Compare actual `.proto` definitions with every documented gRPC call | Every call/method exists and version matches |
| VAL-05 | Anonymous REST/GraphQL public tracking test | No address, phone, POD, private courier or user data exposure |
| VAL-06 | Courier A attempts to modify courier B's delivery | Rejected with no side effects |
| VAL-07 | Duplicate and concurrent booking/order requests | One logical booking per idempotent operation |
| VAL-08 | Delivery created but merchant call times out | Durable reconciliation; no duplicate parcel on retry |
| VAL-09 | Broker unavailable during parcel status update | Committed outbox eventually publishes on recovery |
| VAL-10 | Same RabbitMQ event delivered twice | Exactly one intended notification/webhook job per recipient |
| VAL-11 | Webhook fails 5xx/429 then succeeds | Correct retry count, schedule, fresh signature timestamp and attempt logs |
| VAL-12 | Webhook configured with localhost/private IP URL | URL rejected or outbound request blocked |
| VAL-13 | React browser SSE auth + reconnect | Correct permission checks and state recovery |
| VAL-14 | Flutter customer and courier use cases | Both personas authenticate and call approved APIs |
| VAL-15 | Docker clean start | Gateway, 3 APIs, worker, broker, object store and 4 logical DBs (if retained) healthy |
| VAL-16 | Requirements and test traceability | Counts and IDs valid; actual evidence not confused with planned work |
| VAL-17 | Markdown/diagram integrity | No broken relative links; Mermaid/PlantUML renders; diagrams legible in PDF |
| VAL-18 | Actual progress/ownership | No false completed milestones or attribution of work |

---

## 8. Definition of done for the documentation branch

The `documentation` branch is ready to become the **approved design baseline** only when:

1. [ ] All **P0** issues are closed with changes and reviewer sign-off.
2. [ ] All **P1** issues affecting the four mandatory UML flows are closed.
3. [ ] The official assignment and team-selected technical decisions are clearly separated.
4. [ ] One approved service inventory, data ownership map, API route catalog, event catalog, authentication flow, and parcel state machine exist.
5. [ ] The mandatory receipt, merchant dashboard, admin reporting, public tracking and notification consumer are included in requirements, APIs and tests.
6. [ ] Public tracking, webhook signing, cross-service data access and account linking pass design/security review.
7. [ ] All four mandatory sequence/activity workflows have accurate, reviewed diagrams and editable source.
8. [ ] Traceability counts are correct and progress/test claims are evidence-based.
9. [ ] Any remaining **P2/P3** items have named owners, realistic deadlines and explicit limitations.
10. [ ] The team approves the revised baseline through a reviewed pull request; no bulk unreviewed rewrite replaces the existing work.

### Suggested pull request breakdown

Avoid one enormous PR. Use small, reviewable commits/PRs in dependency order:

1. `docs: correct official requirements and project status` — REQ/GOV corrections.
2. `docs: finalize service ownership and architecture decisions` — ARC and ADRs.
3. `docs: standardize parcel lifecycle and external API contracts` — FLOW/API.
4. `docs: reconcile messaging webhooks and realtime security` — INT/SEC.
5. `docs: revise sequence and activity diagrams` — UML.
6. `docs: align tests deployment and submission evidence` — QA/OPS/PM.

### Source precedence when reconciling conflicts

1. **Official lecturer assignment** — authoritative for mandatory deliverables and grading.
2. **Explicit team-approved decisions / ADRs** — authoritative for SwiftDrop's chosen implementation approach, unless they violate the assignment.
3. **Approved SRS and use-case flows** — authoritative for business behavior.
4. **Approved service catalog, API/proto/event contracts** — authoritative for component interactions.
5. **Diagram narratives and summaries** — must be updated to match the above, not treated as independent truth.

---

## 9. Review limitations and notes

- Findings are grounded in the reviewed **`documentation` branch snapshot** and the supplied assignment PDF, plus the team clarifications already given. If the branch has changed since the snapshot, re-check each entry before opening an issue.
- This is a **documentation reconciliation plan**, not proof that existing code is defective or that any planned component has been deployed.
- The previous review **did not** finish a full automatic Markdown link audit or visual verification of the architecture PDF. These are listed as pending QA activities, not confirmed defects.
- The example routes and architectural directions in this plan are **proposals** until approved by the team. Do not invent new implementation commitments merely to make the documents look complete.
- Preserve existing source diagrams and documents through branch history; adjust them incrementally and cite the approving ADR or contract PR.

**End of plan.**
