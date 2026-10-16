# Documentation Remediation Ledger

> Proposed baseline 2.0 · Applied from documentation at 63d0de2 · Branch docs/apply-documentation-fix-plan · 16 October 2026

The user selected the plan’s Proposed baseline. All **68 issue entries** have corresponding documentation changes below. This is completion of the **documentation edits**, not a claim that the plan’s team approvals, source implementation, tests or submission have occurred. Original findings/recommendations are preserved verbatim in the [supplied plan](documentation-fix-plan.md). [Validation evidence](testing/documentation-validation.md) distinguishes executed documentation checks from unexecuted application checks.

| Issue | Priority | Applied correction / primary artifact | Remaining acceptance evidence |
|---|---|---|---|
| REQ-01 | P0 | Official/team/bonus split; overall 20 marks versus 20/50/15/15 weights; PDF unavailable. [Artifact](requirements/assignment-overview.md) | Lecturer PDF comparison pending |
| REQ-02 | P0 | Receipt, merchant dashboard and admin reports now Must; safe mobile public tracking; APIs/tests/demo mapped. [Artifact](requirements/srs.md) | Runtime acceptance pending |
| REQ-03 | P1 | Flutter Customer and Courier across SRS, clients, architecture, setup and demo; MAUI removed. [Artifact](api/api-reference.md) | Both-persona device evidence pending |
| REQ-04 | P1 | Four standardized narratives with inputs, authorization, main/alternate/error flows and postconditions. [Artifact](requirements/use-case-specifications.md) | REQ/domain/UML sign-off pending |
| GOV-01 | P1 | Unsupported completed implementation/design milestones reset to Draft/Proposed/Planned. [Artifact](project-management/milestones.md) | Actual implementation evidence pending |
| GOV-02 | P1 | No student placeholder allocations or contribution percentages; suggested roles separate from evidence. [Artifact](project-management/team-responsibilities.md) | Names and confirmed allocations pending |
| GOV-03 | P1 | Existing ADRs downgraded to Proposed; DEC-01–12 register includes alternatives, consequences and reviewer roles. [Artifact](architecture/decisions/README.md) | Named approver/date/PR pending |
| GOV-04 | P2 | Exact 32 FR + 20 NFR = 52 matrix, including NFR-18–20, with JSON source. [Artifact](requirements/requirements-traceability.md) | Counts checked automatically |
| GOV-05 | P2 | 12 November internal target separated from 15 November 2026 external submission. [Artifact](project-management/milestones.md) | Team schedule confirmation pending |
| GOV-06 | P2 | Drafted/implemented/executed/passing/evidence separated; no unmeasured integration percentage. [Artifact](testing/test-results.md) | Application CI/results pending |
| GOV-07 | P2 | README/final report refreshed from primary contracts and evidence ledger. [Artifact](README.md) | Reviewer sign-off pending |
| GOV-08 | P3 | Kubernetes and AI independently optional; minimal authorized AI tool scope documented. [Artifact](bonus/ai-delivery-assistant.md) | Bonus implementation deferred independently |
| ARC-01 | P1 | Canonical YARP + 3 APIs + Worker, GraphQL/SSE in Delivery, no realtime process. [Artifact](architecture/service-catalog.md) | DEC-03 review pending |
| ARC-02 | P0 | Merchant alone owns secret decryption, send and webhook attempts; Worker uses scoped DispatchWebhook API. [Artifact](architecture/data-architecture.md) | Boundary tests pending |
| ARC-03 | P1 | Delivery GraphQL module routed through YARP; no foreign SQL or unrestricted BFF. [Artifact](api/graphql-api.md) | DEC-11 review pending |
| ARC-04 | P1 | One PostgreSQL instance on 5432, four logical DBs/users, notification migration/readiness contract. [Artifact](deployment/compose.yaml) | Clean-start runtime pending |
| ARC-05 | P2 | No Redis; bounded JWT revocation and single-replica SSE stated consistently. [Artifact](security/authentication.md) | Tradeoff approval pending |
| ARC-06 | P1 | Exact caller/target/method/auth/deadline/recovery matrix; Merchant→Delivery RPCs defined. [Artifact](architecture/service-catalog.md) | Implementation parity pending |
| ARC-07 | P1 | Private proof/receipt streams, upload validation, proof-before-commit and orphan cleanup rules. [Artifact](architecture/data-architecture.md) | Storage/access failure tests pending |
| ARC-08 | P2 | Gateway coarse routing/auth separated from domain role/resource enforcement; no trusted client IDs. [Artifact](security/authorization.md) | Authorization integration tests pending |
| API-01 | P0 | 57 versioned/current canonical operations in JSON and rendered REST catalog; diagrams use operation IDs. [Artifact](api/contracts/routes.json) | Route-reference checks run; backend OpenAPI parity pending |
| API-02 | P1 | Local registration/login/refresh/logout contracts and Identity password_hash model documented. [Artifact](api/rest-api.md) | Authentication implementation pending |
| API-03 | P0 | Google SDK ID-token exchange selected for both clients; no backend code exchange. [Artifact](security/authentication.md) | Web/Android SDK tests and review pending |
| API-04 | P0 | Separate GraphQL PublicTrackingSummary has no private object path. [Artifact](api/contracts/schema.graphql) | SDL/private-field rejection checked; resolver tests pending |
| API-05 | P0 | REST public tracking allowlists safe city/status/timeline projection only. [Artifact](api/rest-api.md) | Anonymous runtime privacy tests pending |
| API-06 | P1 | Owner-bound 10-minute quote, explicit acceptTotal, immutable price snapshot and shared handler. [Artifact](api/rest-api.md) | Quote/expiry/idempotency tests pending |
| API-07 | P1 | Receipt PDF, own Merchant dashboard and Admin daily/success/failure report payload/guards/demo. [Artifact](submission/demo-plan.md) | Mandatory UI/runtime evidence pending |
| API-08 | P0 | Single async durable order endpoint always 202 with job query; bulk/sync explicitly deferred. [Artifact](api/rest-api.md) | Ingestion/reconciliation tests pending |
| API-09 | P0 | Versioned actual .proto defines CreateBooking and GetBookingByExternalOrder. [Artifact](api/contracts/delivery.proto) | Proto compiles; owning-code parity pending |
| API-10 | P1 | GraphQL mutations wrap same REST handlers/fields/roles/idempotency/state guards. [Artifact](api/graphql-api.md) | Protocol-equivalence runtime tests pending |
| API-11 | P1 | X-API-Key swd_test/keyId/random model, one-time 256-bit secret, hash/scope/revoke/approval rules. [Artifact](security/authentication.md) | Key lifecycle tests pending |
| API-12 | P1 | Provider+subject is identity key; email collision requires own local reauthentication/link. [Artifact](security/authentication.md) | Account-link takeover tests pending |
| FLOW-01 | P0 | Eight canonical states with GraphQL mapping, all guards, terminal failure/cancel and Created after fee confirmation. [Artifact](architecture/parcel-state-machine.md) | DEL/REQ state review pending |
| FLOW-02 | P1 | Proof endpoint completes Delivered only after private storage and versioned DB transaction. [Artifact](architecture/data-architecture.md) | Proof/storage race tests pending |
| FLOW-03 | P1 | Atomic unique scoped key reservation/fingerprint and reproducible response, no check-then-insert race. [Artifact](architecture/data-architecture.md) | 20-request concurrency test pending |
| FLOW-04 | P0 | Durable Merchant inbox, stable order identity, unknown-outcome reconciliation and truthful job states. [Artifact](api/grpc-services.md) | Partial-failure recovery test pending |
| FLOW-05 | P1 | Current Courier only operational writes; Dispatcher/Admin assignment/cancel; expectedVersion at commit. [Artifact](security/authorization.md) | Reassignment race and foreign-courier tests pending |
| FLOW-06 | P1 | Every status narrative/diagram commits state/history/outbox before publication and independent notification. [Artifact](design/diagrams/sequence/courier-status-notification.mmd) | Diagram review/runtime outbox tests pending |
| INT-01 | P1 | Explicit MassTransit message-type durable fanout and receive queue bindings; no custom topic. [Artifact](integration/event-catalog.md) | Runtime topology permission smoke pending |
| INT-02 | P1 | Complete producer/message/queue/concrete-consumer/effect matrix; unused specialized events retired. [Artifact](integration/event-catalog.md) | Consumer implementation pending |
| INT-03 | P1 | One StatusChanged trigger with consumer inbox and unique recipient/subscription jobs. [Artifact](integration/event-catalog.md) | Duplicate/reorder tests pending |
| INT-04 | P1 | Broker initial+3 retries separate from HTTP webhook initial+5; exact delays and terminal behavior. [Artifact](integration/merchant-webhooks.md) | Fake-clock retry tests pending |
| INT-05 | P0 | Webhook secrets AEAD encrypted/retrievable only by Merchant; API keys hashed separately. [Artifact](integration/merchant-webhooks.md) | Signing/storage implementation pending |
| INT-06 | P1 | Fresh epoch timestamp/HMAC per attempt, stable event ID/occurredAt, 300s tolerance and dedup. [Artifact](integration/merchant-webhooks.md) | Retry freshness/replay tests pending |
| INT-07 | P0 | HTTPS public-only destination, all DNS results checked/pinned, no redirects, egress/time/size controls. [Artifact](integration/merchant-webhooks.md) | SSRF/rebinding integration tests pending |
| INT-08 | P1 | Browser fetch streaming Bearer auth replaces unsupported native EventSource header options; Flutter streaming. [Artifact](integration/realtime-tracking.md) | Real-browser/device test pending |
| INT-09 | P1 | No durable cursor replay claim; subscribe/register then snapshot with version buffer plus periodic reconciliation. [Artifact](integration/realtime-tracking.md) | Reconnect/race test pending |
| INT-10 | P1 | SSE mandatory status transport in Delivery; GPS/SignalR/map explicitly deferred. [Artifact](api/websocket-protocol.md) | Scope approval pending |
| INT-11 | P1 | One Delivery replica and separate realtime receive queue; shared queue not called broadcast. [Artifact](integration/realtime-tracking.md) | Scale deferred until fanout decision |
| INT-12 | P1 | Minimized versioned event JSON schema rejects address/contact/proof extras. [Artifact](api/contracts/status-changed-v1.schema.json) | Schema/privacy rejection checked; runtime serializer pending |
| UML-01 | P0 | Sequence messages use current REST operation IDs, real RPCs and canonical parcel states. [Artifact](design/diagrams/sequence/README.md) | Rendered; API/domain review pending |
| UML-02 | P0 | Google sequence/activity show SDK ID token, cancellation, invalid token, subject/collision and account branches. [Artifact](design/diagrams/sequence/google-login.mmd) | Rendered; SEC/UI review pending |
| UML-03 | P1 | Flutter Courier lifeline and React Dispatcher with role/assignment/version/proof failure paths. [Artifact](design/diagrams/sequence/assignment-proof.mmd) | Rendered; UI/DEL review pending |
| UML-04 | P1 | Merchant sequence shows scoped key, durable 202 job, defined RPC, timeout and reconciliation branches. [Artifact](design/diagrams/sequence/merchant-order.mmd) | Rendered; MER/API review pending |
| UML-05 | P0 | Webhook sequence calls Merchant API; no Worker→Merchant SQL/hash signing; exact retry policy. [Artifact](design/diagrams/sequence/webhook-delivery.mmd) | Rendered; SEC/MER review pending |
| UML-06 | P1 | Self-contained Courier→commit/outbox→broker→notification/webhook/SSE sequence with dedup. [Artifact](design/diagrams/sequence/courier-status-notification.mmd) | Rendered; MSG/DEL review pending |
| UML-07 | P1 | Formal activities put publication after commit then fork notification/realtime; failure/cancel guards in lifecycle. [Artifact](design/diagrams/activity/courier-status-notification.puml) | Rendered; UML review pending |
| UML-08 | P1 | Four dedicated required activity/sequence pairs linked to standardized narratives. [Artifact](design/diagrams/README.md) | Coverage indexed; approval pending |
| UML-09 | P2 | PlantUML formal activities with swimlanes, initial/final nodes, guards and courier fork/join. [Artifact](design/diagrams/activity/README.md) | Syntax/render checked; academic notation review pending |
| UML-10 | P2 | Versioned diagram index/manifest, editable sources, SVG exports and regenerated architecture PDF. [Artifact](design/diagrams/README.md) | Source/export checks and PDF visual review recorded |
| QA-01 | P1 | Eight explicit security-negative cases plus primary role/privacy/link/proof scenarios. [Artifact](testing/test-cases.md) | Drafted; implementation/execution pending |
| QA-02 | P1 | Eight recovery cases with concurrency/fault injection and exact assertions. [Artifact](testing/test-cases.md) | Drafted; implementation/execution pending |
| QA-03 | P2 | Defined business-logic line denominator/exclusions, branch metrics separate, integration scenario coverage. [Artifact](testing/coverage-summary.md) | Actual CI coverage pending |
| OPS-01 | P1 | Concrete Compose/bootstrap for 4 DBs, Worker-owned DB, scoped broker users/private object policy and health. [Artifact](deployment/compose.yaml) | Config syntax checked; daemon/full-app prerequisites pending |
| OPS-02 | P2 | Single host/container/mobile/nonlocal port and environment-variable matrix; example.invalid placeholders. [Artifact](deployment/environments.md) | Actual environment smoke pending |
| OPS-03 | P2 | Kubernetes explicitly optional/reference, minimal one-node milestone and required manifest/resources/evidence. [Artifact](deployment/kubernetes.md) | Bonus manifests/deployment deferred |
| OPS-04 | P2 | Flutter both-persona bootstrap, API26+, emulator/device/TLS, OAuth clients/SDK links and private dev fixtures. [Artifact](deployment/local-setup.md) | Source-specific commands/onboarding test pending |
| OPS-05 | P2 | Reproducible link/anchor/schema/proto/diagram validation; regenerated PDF visually inspected; truthful evidence ledger. [Artifact](testing/documentation-validation.md) | Documentation checks recorded; final report/runtime/team evidence pending |

## Decision and evidence gates
DEC-01–DEC-12 are recorded with alternatives/consequences and remain **Proposed** until named team members approve them with a dated reviewed PR. Suggested roles are not assigned students. The assignment PDF was not supplied in the repository or located beside the plan; requirement comparison and exact bonus scoring remain explicitly unverified.
The repository has no application source/images/migrations. Reference Compose and contract fixtures are concrete reviewable artifacts, but full-system startup, runtime contract parity, all 68 application tests, coverage, device onboarding and security behavior require the owning repositories. Docker configuration syntax can be checked without a daemon; local Docker daemon is unavailable for container execution. These limitations are tracked in [test results](testing/test-results.md) and [submission checklist](submission/submission-checklist.md), never marked green.
## Review order and sign-off
Review requirements/status → service/data/ADRs → state/API → messaging/security → UML → deployment/tests/submission. Each diagram reviewer must verify actor/client, exact operation/event, ownership/state/version, success/invalid/unauthorized/failure path, outbox ordering, retry/dedup and privacy. Record name/date/PR in the ADR and diagram index; do not infer approval from generated exports. External submission remains **15 November 2026**, with **12 November** an optional internal rehearsal/freeze. Required functionality can be demonstrated independently of Kubernetes/AI; GPS/SignalR and bulk ingestion are deferred explicitly.
