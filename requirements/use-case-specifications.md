# Use-Case Specifications

> Status: Proposed baseline 2.0 · REQ/API/domain/UML sign-off pending

The narratives below govern the four required sequence/activity pairs. They use [REST operation IDs](../api/rest-api.md), the [state matrix](../architecture/parcel-state-machine.md) and [decision register](../architecture/decisions/README.md). Authorization, retries and state changes are identical on React and Flutter where applicable. Inputs/outputs have the validation rules in REST; these narratives do not introduce alternate endpoints.

## UC-01 Customer fee preview and booking

- Actor/client: Customer, React or **Flutter Customer**. Trace: FR-C04, FR-C05, NFR-10/11; TC-C04, TC-C05, TC-REC-01.
- Entry/preconditions: signed-in active Customer, configured zone/pricing; open Book delivery. No parcel exists yet.
- Authorization/input: EstimateFee uses JWT sub and QuoteInput recipient, addresses, positive weight and size; no userId/merchantId or sender-contact field accepted. Validate both zones independently; the user confirmed `deliveryAddress.zoneId` selects the tariff on 23 October 2026. Pickup zone does not affect pricing and no cross-zone surcharge is defined.
- Successful path: validate inputs → calculate versioned price using delivery zone → save full input in a 10-minute owner-bound quote → display total → customer explicitly confirms → CreateParcel(quoteId, acceptTotal, Idempotency-Key) → resolve/reserve unique key → replay identical committed response before quote validation, or validate and consume the owned quote and save Created parcel, price snapshot, history and StatusChanged outbox atomically → return 201 with parcel/tracking/version and Location. Parcel and snapshot retain the delivery tariff zone. Relay publishes later; notification availability does not gate booking.
- Decisions/alternatives: customer declines fee → end with no parcel/outbox; expired quote or changed accepted total → 409, obtain/reconfirm quote; same key/payload within the replay window → original status/body/Location even after quote expiry/consumption; changed fingerprint or expired retained key → 409. Concurrent duplicate requests have one winner via unique constraint, not a check-then-insert race.
- Exceptions: 400 bad input, 401 token failure, 403 wrong role, 404 missing/foreign quote, 422 zone rejection, 503 precommit DB failure; rollback transaction. Lost HTTP response is retried with same key. Broker outage leaves committed outbox pending.
- Output/postcondition: one Created booking and immutable snapshot, or no booking; safe tracking projection differs from owner detail. Receipt is later downloadable only for Delivered.

## UC-02 Merchant order through secured API

- Actor/client: external merchant backend. Trace: FR-M03/04/06/07, NFR-06/10/11; TC-M04, TC-M06, TC-M07, TC-REC-02.
- Entry/preconditions: business Approved, active scoped `X-API-Key`, accepted tariff version, known externalOrderId.
- Authorization/input: Merchant API derives business from key and checks orders:write; MerchantOrderInput cannot override business. Idempotency-Key plus stable business/externalOrderId and fingerprint.
- Successful path: validate → atomic durable inbox job Accepted → 202 with job Location and null parcel IDs → Merchant processor claims job → authenticated CreateBooking RPC → Delivery shared handler saves unique parcel/snapshot/history/outbox → processor records job Created with tracking/parcel → client polls GetMerchantOrder; dashboard lists own jobs/status with lastRefreshedAt.
- Decisions/alternatives: invalid key→401; missing scope→403; suspended business→403; foreign job→404; changed order fingerprint→409. Same order after key rotation still resolves existing job/parcel. Job is not a parcel; Accepted is not a parcel state. Bulk/synchronous creation are deferred.
- Exceptions: gRPC deadline/unavailable→durable Retrying → GetBookingByExternalOrder → existing result finalizes Created; NotFound allows same-key CreateBooking retry. Permanent domain failure marks Failed with safe code; transient failures remain scheduled/alerted. No distributed DB transaction or compensating deletion of a successful booking.
- Output/postcondition: durable queryable job and at most one parcel; no fabricated success on unknown outcome. Reconciliation refreshes parcel status in Merchant for dashboard/polling.

## UC-03 Courier status triggering notifications

- Actor/client: currently assigned Courier in **Flutter Courier**; owner Customer and subscribed Merchant are recipients. Trace: FR-R01/02/03/04, FR-C06, FR-M05, NFR-07/08/11/12/13; TC-R02/03/04, TC-REC-03/04, TC-SEC-01/02/03/04.
- Entry/preconditions: active assigned parcel, legal next state, expectedVersion, Idempotency-Key and a private delivery note for PickedUp/InTransit/OutForDelivery. For delivery completion, state is OutForDelivery and valid proof photo/signature is available.
- Authorization/input: Delivery checks JWT Courier role, current assignment at commit, version and [transition matrix](../architecture/parcel-state-machine.md). Dispatcher/Admin cannot masquerade as Courier.
- Successful path: Flutter sends UpdateDeliveryStatus, or CompleteDeliveryWithProof after object persistence → transaction updates parcel/version, history and one StatusChanged outbox → 200 committed state → relay publishes → Worker deduplicates inbox and creates recipient notification/provider jobs plus merchant dispatch job when applicable → scoped DispatchWebhook causes Merchant to create unique subscription jobs and sign/send → Delivery realtime consumer signals authorized clients with latest snapshot. Each consumer commits durable work before ACK.
- Decisions/alternatives: Failed requires reason; Delivered is only proof endpoint. Same key returns original result; new key same state→409. Public observers receive only safe REST/GraphQL snapshot, not private SSE. Duplicate event creates no duplicate notification or webhook job.
- Exceptions: 400 missing/invalid delivery note or proof input, 401 invalid JWT, 403 wrong role, 404 foreign/unassigned parcel, 409 stale version/invalid transition; all have no committed state/history/outbox effects. Storage failure leaves state unchanged; DB race after successful upload creates only a cleanup-eligible orphan. Broker outage leaves outbox pending. Receiver 429/5xx follows six-attempt policy with fresh timestamp/signature. SSE reconnect subscribes and refetches current state.
- Output/postcondition: committed valid state is independent of provider availability; durable eventual jobs and inspectable failure records remain. No signing secret or foreign DB access is given to Worker.

## UC-04 Google OIDC login

- Actor/client: user in React, Flutter Customer or Flutter Courier. Trace: FR-C02, NFR-05/08; TC-C02, TC-SEC-05.
- Entry/preconditions: configured per-platform Google client/audience and Identity signing keys; user initiates Google SDK sign-in.
- Authorization/input: provider SDK handles its consent/redirect; client submits ID token to GoogleLogin. No backend authorization-code callback is specified. Validate Google signature, issuer, exact audience, expiry, verified email and platform CSRF/nonce requirements.
- Successful path: SDK obtains ID token → GoogleLogin → Identity validates → resolve provider+subject → existing active linked account or atomic new Customer without email collision → issue app JWT ≤900s and rotated refresh session → client opens role-appropriate experience. A newly created Customer cannot become Courier through a client role parameter; admin must assign Courier first.
- Decisions/alternatives: user cancels provider sign-in→no app session; first-time valid identity→Customer only; existing linked identity→same user; matching local email without link→409 account_link_required; LinkGoogle requires own authenticated local session and fresh local-password verification plus valid provider token.
- Exceptions: invalid/expired token→401; disabled user or provider subject already linked elsewhere→reject without mutation; Google/JWKS unavailable→fail closed for unverifiable token. Local login remains a separate documented path, not a silently substituted Google flow.
- Output/postcondition: authenticated application session bound to stable provider subject, or no account/session changes. Tokens are never logged; browser and mobile refresh storage follow [authentication](../security/authentication.md).

## Supporting scenarios

Assignment/reassignment, refresh, merchant onboarding, webhook retry and proof atomicity have supporting diagrams in the [diagram index](../design/diagrams/README.md). Mandatory receipt/dashboard/report acceptance appears in [traceability](requirements-traceability.md) and [demo plan](../submission/demo-plan.md). Every diagram owner and reviewer remains unassigned pending team allocation; written scenarios are reviewable proposals, not approved implementation records.
