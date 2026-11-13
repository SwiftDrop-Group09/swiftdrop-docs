# System completion and design audit

Audit date: 13 November 2026. This is an implementation and document review,
not a declaration that live acceptance tests passed.

## Verdict

SwiftDrop has substantial implemented Customer, Courier, Identity and Admin
functionality, but it is not yet a complete assignment system. The critical
unfinished chain is merchant order ingestion / dispatcher assignment / courier
status / broker publication / notification / automatic merchant webhook.
Passing component tests and process health checks do not establish that chain.

Prioritize that core chain, security/configuration and submission evidence before
optional Kubernetes or AI work. REST satisfies the assignment; GraphQL, internal
gRPC and Flutter are additional team commitments, not lecturer-mandated frameworks.

## Sources and audit boundary

The original four-page [assignment PDF](requirements/sources/ead-group-assignment.pdf)
was extracted and read again. Its SHA-256 remains
`b19457c735e4f3608adf54a5c7d03c06114e021367c66f01366f01c92a0bf5b2`.
The audit also compared the SRS, REST catalog, authorization matrix, technical/data
design, integration/event/webhook plans, testing records and submission checklist
against the current local source. Checkout revisions inspected:

| Repository | Revision |
| --- | --- |
| Backend | `d4f2bf4` |
| Frontend | `3eea1c4` |
| Infrastructure | `db15d7c` |
| Mobile | `459ac4f` |
| Documentation baseline before this report | `fa5cf9c` |

No production credentials were printed or tested. No database, deployment or
application source was changed. Full application suites, native-device checks
and deployed infrastructure were not rerun during this audit. Existing test
results are historical evidence and must be tied to their actual tested commits.
Remote branches or unmerged work are not counted as delivered functionality.

## Assignment minimum versus team scope

- Mandatory: responsive web, secure Google/local authentication, Customer
  quote/booking/tracking/history/receipt, approved merchant order API/dashboard,
  Dispatcher assignment/workload, Courier updates/failure, real broker-triggered
  notification and retrying webhooks, containers/Compose, tests with measurable
  coverage, design PDF and contribution sheet.
- Additional team scope: Flutter Customer/Courier, four Neon databases,
  database-per-service, outbox/inbox guarantees, strict final proof, specific
  latency/concurrency/coverage targets, GraphQL and gRPC.
- Optional bonuses: full Kubernetes deployment and generative-AI assistant.
- The assignment PDF has no submission date. The documented 15 November deadline
  is an externally supplied team date. The PDF's 20-mark overall weight and
  20/50/15/15 category labels still need the already-recorded grading clarification.

## Functional coverage

"Implemented" below means source and relevant feature tests exist; it does not
mean full deployed acceptance is proved.

| Requirements | Current evidence | Remaining work |
| --- | --- | --- |
| FR-C01–C03 authentication/profile | Identity endpoints and web sign-in, Google linking, sessions, profile and role management | Rehearse real configured Google flow on deployed HTTPS; normal mobile authentication is not connected |
| FR-C04–C05 quote/booking | Real quote, explicit confirmation, immutable price snapshot and idempotent persistence; web and mobile feature clients | Verify fresh deployment, migrations and normal authenticated mobile composition |
| FR-C06–C08 tracking/history/receipt | Public/private reads, SSE, owner history, PDF receipt and web/mobile feature screens | Measure live latency and privacy on deployed clients; mobile normal entry point remains blocked by IAM |
| FR-M01–M03 onboarding/approval/keys | Merchant registration, admin review, scoped key generation/revocation and web screens | Finish actual key authentication for consumers; confirm approved owner navigation/role provisioning |
| FR-M04, M06, M07 order API/dashboard/read | Domain scaffolding and documented contracts | Build durable ingestion, processing/reconciliation, owner reads/statistics, dashboard and orders UI |
| FR-M05 webhooks | Subscription CRUD, encryption/HMAC, sender, attempts/replay, retry worker and UI exist | Connect genuine events and workload authentication; fix resolution and crash-recovery defects below |
| FR-R01–R05 Courier | Assignment reads, service-day filtering, guarded notes/failure/proof, history, web/mobile clients | Provide legitimate operational Courier profiles and assignment creation; run the real cross-role flow |
| FR-D01 unassigned queue | Operations-authorized parcel listing already exists; Created status can form a queue | Build Dispatcher queue UI and required zone filtering; do not describe the entire read API as absent |
| FR-D02–D04 assignment/workload/reassignment | Assignment entities, constraints and retained history exist | Expose guarded assignment/reassignment, workload/capacity reads and their UI |
| FR-D05 zone summary | Backend summary and `/dispatch/zones` web page exist | Connect to acceptance dataset and verify real Dispatcher/Admin access |
| FR-A01–A06 administration | Users/roles, merchant approvals, zones/pricing and delivery reports have APIs and web screens | Verify full-system data, report boundaries, migration/startup and privileged-action acceptance |
| FR-A07 audit | Identity audit UI/API and persisted Delivery configuration audits exist | Define whether the requirement is Identity-only or cross-service; expose/aggregate remaining relevant privileged activity |

### Correction to the earlier frontend audit

The frontend role review said the operations list API was missing. Current
[CustomerTrackingHandler](../swiftdrop-backend/src/Services/Delivery/SwiftDrop.Delivery.Api/Application/DeliveryReads/CustomerTrackingHandler.cs)
and [PostgresDeliveryReadStore](../swiftdrop-backend/src/Services/Delivery/SwiftDrop.Delivery.Api/Infrastructure/DeliveryReads/PostgresDeliveryReadStore.cs)
explicitly support `IsOperations`. The real gaps are the queue UI, zone filter,
assignment/reassignment and workload endpoints. The current route rejects unknown
query parameters, so a client must not invent a zone filter before adding its
backend contract. Correct the earlier review rather than building a duplicate
parcel-list API or exposing Customer-owned reads as an unrestricted shortcut.

## Release blockers and design gaps

### P0 — Complete the mandatory workflow

1. **No broker publication or notification consumer.** Delivery commits outbox
   records, but its host does not register a relay/broker transport. The actual
   [Notification Worker](../swiftdrop-backend/src/Workers/SwiftDrop.Notification.Worker/Program.cs)
   only maps `/health`. Implement acknowledged publication, stable event IDs,
   persisted consumer deduplication, notification jobs and observable mock SMS or
   email output. Provide least-privilege resolution of recipient details rather
   than putting contact data into public events or sharing another service's DB.
   See the existing [outbox handoff](../swiftdrop-backend/docs/delivery-outbox-relay-handoff.md).

2. **Merchant orders have no executable ingestion/read pipeline.** The current
   presentation layer has onboarding, keys and webhooks, not the documented order
   and dashboard operations. Implement scoped API-key authentication, approved
   business binding, durable 202 jobs, merchant/external-order deduplication,
   creation and unknown-outcome reconciliation, owner reads and statistics. Reuse
   the existing Delivery booking policies; do not turn retries into new bookings.

3. **Dispatcher cannot create real assignments through the system.** Implement
   assignment/workload and UI using the existing operations read foundation.
   Enforce current parcel version, before-pickup state, active/on-duty Courier,
   capacity and zone membership atomically with history/outbox/idempotency.
   Test two dispatchers racing and reassignment racing pickup. Courier operational
   profiles are separate from Identity roles: provision them deliberately for
   verified user IDs before the demo. The REST design permits a controlled seed;
   a new general provisioning API is not automatically required.

4. **Automatic webhooks can remain permanently unresolved.** Merchant registers
   [StubWebhookOrderResolver](https://github.com/SwiftDrop-Group09/swiftdrop-backend/blob/d4f2bf44c001f2f8a661a0c8ebd9064b3c5ff0c0/src/Services/Merchant/SwiftDrop.Merchant.Api/Infrastructure/Webhooks/StubWebhookOrderResolver.cs),
   which always returns null. Accepted status events consequently create
   `PendingResolution` jobs. The current dispatch loop claims only `Pending`
   jobs, and no resolution processor is wired. A test webhook is not proof of
   automatic delivery-status notification. Implement owned order/parcel mapping
   and a bounded, durable resolution/retry path before claiming this complete.

5. **Webhook crash recovery has a stranded-job path.**
   [WebhookDeliveryJob.Claim](../swiftdrop-backend/src/Services/Merchant/SwiftDrop.Merchant.Api/Domain/Webhooks/WebhookDeliveryJob.cs)
   moves jobs to `Processing`, while
   [ClaimDueJobsAsync](../swiftdrop-backend/src/Services/Merchant/SwiftDrop.Merchant.Api/Infrastructure/Webhooks/Persistence/PostgresWebhookDispatchStore.cs)
   selects only `Pending`. A process crash after claim leaves expired Processing
   jobs outside the queue. Add expired-lease recovery, token/version fencing and
   atomic attempt/job persistence. Test crash-before-send, crash-after-send,
   concurrent workers and retry exhaustion. At-least-once external delivery must
   retain stable logical event IDs for receiver deduplication.

### P0 — Security and usable deployment

6. **Tracked credential-like configuration.** The tracked Identity
   `appsettings.Development.json` contains a non-placeholder password assignment
   in `ConnectionStrings.Database`. Its validity was not tested; its value is
   intentionally omitted here. Remove it from tracked configuration and use the
   established private secret mechanism. If it is or was valid, rotate it and
   assess repository history/access. Development configuration is not an exemption
   from the assignment's no-hard-coded-secrets requirement.

7. **Human, workload and API-key authentication contracts are not connected.**
   Merchant configures one human JWT audience in
   [IdentityJwksKeyResolver](../swiftdrop-backend/src/Services/Merchant/SwiftDrop.Merchant.Api/Infrastructure/Authentication/IdentityJwksKeyResolver.cs),
   but internal webhook dispatch requires `merchant-internal`. A correctly scoped
   service token will not pass the default human audience configuration. No
   separate workload issuer/client flow or API-key authentication scheme is wired.
   Implement distinct strict schemes/policies and real workload credential
   provisioning. Do not solve this by globally disabling audience validation or
   making service JWTs interchangeable with human Admin tokens. Documented
   webhook API-key access also needs implementation or an explicit contract change.

8. **Production overlay explicitly removes TLS.** The checked-in
   [production overlay](../swiftdrop-infra/k8s/overlays/prod/kustomization.yaml)
   removes ingress TLS and configures an HTTP API/issuer while using a Vercel HTTPS
   origin. As written, this conflicts with external-HTTPS requirements and can
   prevent browser API/cookie use. Verify any real external TLS termination rather
   than assuming it exists. Align public API URL, Google origins, exact issuer,
   cookies, forwarded headers and gateway origin/proxy setup. Test login, refresh,
   logout, SSE and proof download through the actual public ingress.

### P1 — Reconcile adopted design and operational behavior

9. **SSE transport exists; broker-backed realtime does not.**
   [DeliveryReadEndpoints](../swiftdrop-backend/src/Services/Delivery/SwiftDrop.Delivery.Api/Presentation/DeliveryReadEndpoints.cs)
   rechecks the database every two seconds for each stream. This is real SSE and
   should not be called absent. It differs from the proposed realtime consumer
   and may exceed the two-second target after DB/network delay. Measure load,
   connection count and latency; either implement the proposed signal path or
   document and justify the actual polling/SSE design and capacity limits.

10. **Mobile feature screens are not a usable normal authenticated app.**
    [Mobile app composition](../swiftdrop-mobile/lib/app/app.dart) defaults to a
    signed-out session, `UnavailableTransport` and `UnavailableZoneCatalog`.
    Integrate IAM, refresh/session storage, API base/transport, real zone catalog
    and routing for Customer/Courier. Verify Google/native redirect configuration,
    Android API 26+, photo/signature permissions and real device uploads. Harness
    success is feature evidence, not normal-app acceptance. This is team scope;
    it must not displace the lecturer's mandatory responsive web flow.

11. **Liveness is being used where dependency readiness is needed.** Merchant,
    Delivery and Worker health can be green while required schemas, broker,
    storage or downstream features are unavailable. Define separate readiness
    checks and deployment gates. Current shared Compose has Identity/Delivery
    migration tasks, but not a complete four-service schema/bootstrap workflow;
    Delivery migration reuses its runtime connection. Provide explicit migrator
    credentials/tasks, scoped runtime grants, private storage provisioning,
    operational Courier setup and a reproducible clean startup runbook.

12. **Neon and external frontend deployment require an assignment decision.**
    The PDF explicitly names frontend/backend/database/broker containers, and the
    Kubernetes bonus names the full system. Current development Compose uses
    external Neon and no database container; production overlays remove the web
    deployment. Neon remains the user's selected database platform. Obtain written
    lecturer acceptance for this topology or provide a separate compliant local
    container demonstration without replacing the project's Neon environment.
    Kubernetes manifests/CI schema validation alone do not prove the full-system
    bonus or a working cluster. The CD workflow does pin immutable image tags;
    do not misreport the overlay's default `latest` tags as the only deploy path.

13. **Several documented contracts remain declarations.** GraphQL SDL and gRPC
    protobuf assets exist, but Delivery has no mapped GraphQL/gRPC implementation.
    Cancellation is documented but has no mapped operation. Choose which adopted
    contracts must ship, record deferrals/ADR changes and implement the internal
    booking/resolution contract needed by Merchant/Worker. GraphQL itself is not
    needed to satisfy the assignment's REST-or-GraphQL requirement.

14. **Audit and account lifecycle responsibilities need explicit boundaries.**
    Admin currently sees Identity audit, not a combined privileged-action ledger.
    Delivery configuration audit records are persisted without an equivalent read
    surface. Decide the FR-A07 boundary, retention/export and event ownership.
    Merchant approval, Merchant role navigation, Courier role and Courier operational
    profiles are separate concepts; document who reconciles them and how suspended
    businesses and role changes affect active keys, sessions and ongoing work.

15. **Validation, data lifecycle and failure behavior need completion tests.**
    Some admin query parsing defaults/clamps invalid input while other APIs return
    400. Align date/page/unknown-field behavior with the REST contract. Define
    zone deactivation effects on existing work, tariffs versus retained quote
    snapshots, operational timezone versus UTC reports, terminal-failure handling,
    audit/job retention, key rotation and restore/recovery. These are decisions
    to verify, not permission to rewrite the sound immutable booking-price rules.

## Evidence and documentation gaps

- The canonical traceability, test-results and coverage pages still say all
  runtime evidence is pending. Source/tests and recent executed feature runs now
  exist. Reconcile actual cases and commit-bound reports rather than keeping the
  stale all-pending status or marking everything complete from a test count.
- The recent frontend run passed 267 tests and production/browser checks at the
  merged workspace/theme implementation. Earlier backend results apply to their
  tested revisions, not automatically to current `d4f2bf4`. This audit did not
  rerun them or verify hosted CI run URLs.
- Backend CI runs tests with TRX output, but the inspected workflow does not
  collect measured business-logic coverage or publish a release evidence bundle.
  Produce coverage with counts/exclusions and link test artifacts, security
  negatives and at least one real broker integration-flow test.
- Responsive checks recorded for the latest shell use 390/768/1920 pixels and API
  fixtures. The adopted 320px requirement and real deployed multi-role scenario
  still need explicit evidence. Performance p95, 50-user load, realtime latency,
  browser/native-device acceptance, backup restore and clean Compose startup
  cannot be inferred from unit tests.
- Docker/Compose documentation still says database strings are not consumed and
  feature routes/migrations do not exist. Those claims are stale. Update setup,
  secret/migration contracts, architecture diagrams and source links together.
- Responsibilities and contribution records remain unassigned/pending, ADRs are
  Proposed, and final report/submission checklists are unfinished. Populate actual
  member evidence, reviewed design PDF, release links, coverage and demo results;
  do not invent approvals or contributions.

## Recommended completion order and acceptance gates

1. Remove/rotate the tracked credential as appropriate; settle HTTPS, workload
   authentication and the deploy/assignment topology decisions.
2. Complete Dispatcher assignment/workload and a verified Courier fixture/setup.
   Gate: Customer books, Dispatcher assigns, assigned Courier advances/fails or
   completes with private proof; stale/foreign actions fail without side effects.
3. Implement Delivery outbox publication and Notification Worker inbox/provider
   jobs. Gate: broker outage and crash/restart retain events, and an actual status
   change produces one logical observable notification.
4. Implement Merchant ingestion, booking reconciliation, reads and dashboard;
   connect real automatic webhooks and fix resolution/lease recovery.
   Gate: a real scoped merchant key creates one order despite retries/timeouts,
   its parcel is assigned/delivered, dashboard updates, and signed webhooks retry
   and recover after worker crash without losing the logical event.
5. Finish normal mobile IAM if retaining the adopted Flutter scope; reconcile
   audit/cancellation/GraphQL/gRPC decisions. Do not add optional frameworks merely
   to satisfy an inaccurate checklist.
6. Run the complete acceptance matrix on a clean configured deployment, publish
   measured coverage and artifact links, correct docs and diagrams, and finish
   the contribution sheet/final PDF and rehearsal. Only then assess optional bonuses.

Minimum live demo path: real Google login → quote/booking → Dispatcher assignment
→ Courier update/proof → Customer live tracking/receipt, plus real merchant API
order → reconciled parcel → signed webhook and broker-triggered notification.

## Audit validation

The original PDF hash was verified. The existing documentation validator passed
before this report, checking 55 Markdown files, 478 local links/images, 60 REST
operations, 52 requirements, 68 drafted cases, protobuf compilation and 33 rendered
diagram records. That validates document integrity, not runtime implementation,
deployment, diagrams' semantic accuracy or acceptance completion.

After adding this report, the validator passed again with 56 Markdown files and
490 local links/images; the remaining catalog/diagram/protobuf checks also pass.
The report is uncommitted. No implementation fixes or deployment changes were
made as part of the audit.

## Subsequent role-model change

The audit above describes its recorded baseline. The single-role account model
now supersedes its multi-role examples: see [authorization](security/authorization.md).
Removed implementation references are pinned to their historical baseline commit
so they do not imply that the previous stub still exists after later merges.
