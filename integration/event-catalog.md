# Event Catalog

> Status: Proposed baseline 2.0 · DEC-09 · MSG/DEL/SEC approval pending

**StatusChanged v1 is the sole canonical status side-effect trigger**, including Created, reassignment, failure and cancellation. ParcelBooked/ParcelPickedUp/ParcelDelivered/DeliveryFailed and other specialized events are not published in this baseline. Any future analytics-only event must explicitly prohibit duplicate notification consumers.

## Contract

[JSON Schema](../api/contracts/status-changed-v1.schema.json) and [valid example](../api/contracts/status-changed-v1.example.json) define the complete body: eventId UUID, eventType StatusChanged, schemaVersion 1, occurredAt UTC, parcelId, parcelVersion monotonically increasing integer, nullable merchantId, status, nullable previousStatus (null only on creation), correlationId. No recipient identity/contact, address, exact GPS, courier name, proof URL, token, private notes or signing material belongs in this contract. Do not log whole payloads. The emitter reuses eventId across outbox retransmission; parcelVersion comes from the committed transaction.

## Producer → consumer → effect

| Producer | Message/exchange | Queue and binding | Concrete consumer | Effect / durable uniqueness |
|---|---|---|---|---|
| Delivery local outbox relay | `SwiftDrop.Contracts.V1:StatusChanged` (fanout) | `notification-status` receive exchange → same queue; bind message exchange to receive exchange | Worker StatusNotificationConsumer | Inbox `(consumer,eventId)`; notification `(eventId,recipientId,channel)`; webhook-dispatch job `(eventId,merchantId)` for merchant parcels |
| Delivery local outbox relay | same message exchange | `delivery-realtime` receive exchange → same queue; bind message exchange to receive exchange | Delivery RealtimeStatusConsumer | Deduplicated wake-up; authorized subscribers receive newest safe snapshot/version |

Declare message entity name explicitly with MassTransit `SetEntityName("SwiftDrop.Contracts.V1:StatusChanged")`, receive endpoint names above and message-type bindings. All declared exchanges are durable fanout; queues are durable. There is no custom `swiftdrop.events` topic exchange or implicit routing-key contract. Bootstrap/consumer startup must declare topology before accepting demo writes. Each receive queue has `<queue>_error` for exhausted processing and `<queue>_skipped` for unhandled types; monitor both. Each service uses dedicated least-privilege broker credentials and only its permitted entities; the reference infra provides separate broker users for Delivery and Worker.

The Worker consumes a status only once logically, then resolves the Customer owner recipient **ID**, when present, through Delivery NotificationContext (event/parcel/version verified) and persists notification/provider jobs. Merchant-originated parcels have no Customer owner session in this baseline; their recipient notification path is the merchant webhook, rather than an invented cross-domain owner lookup. In-app records and mock email/SMS provider attempts for Customer bookings are the Worker's responsibility. Merchant event gets a durable webhook-dispatch job; the Worker calls Merchant DispatchWebhook. Merchant deduplicates event and snapshots active subscription jobs in its own DB, then owns sending/retry. It never exposes signing secrets to Worker.

Set `PublishFaults = false` on these receive endpoints: processing errors move to the configured error queue and are monitored there, rather than implicitly publishing undeclared Fault message types outside the scoped broker entity permissions. Verify the exact pinned-runtime topology and binding permissions in integration tests.

## Ordering, retry and replay

Publish only after state/history/outbox commit. Mark an outbox row sent after broker confirmation; crash between confirmation and marking may republish. Consumer transaction commits inbox+jobs before ACK. Older duplicate parcel versions cannot regress SSE or dashboards. Important business actions are not triggered by public timeline text.

Broker processing: **one initial attempt plus three immediate retries** (1s, 5s, 15s), then `<queue>_error`; operator replay is audited and preserves eventId. No delayed broker retry is configured in this baseline. Replaying a broker message cannot bypass durable effect deduplication. This policy is separate from six-attempt **HTTP webhook** scheduling in [webhooks](merchant-webhooks.md). Provider and dispatch jobs are durably scheduled; a transient HTTP call failure must not cause a completed consumer transaction to generate duplicate jobs.

## Version evolution

v1 schemas reject unexpected fields in documentation validation. Implementation consumers tolerate approved additive optional fields within v1; required field removals/type changes require a new message version and explicit dual-consumer migration. Unknown versions route to error/quarantine with alert and no side effects. Contract tests verify IDs, serialization, privacy and duplicate/reordered delivery. Actual broker topology/rendered management evidence is pending backend integration.

## Transport reference

[MassTransit RabbitMQ configuration](https://masstransit.massient.com/configuration/transports/rabbitmq) documents transport topology and publish/receive configuration. The explicit entity names, scopes and retry counts above are proposed SwiftDrop configuration that still requires a pinned-runtime test.
