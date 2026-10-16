# Data Architecture

> Status: Proposed baseline 2.0 · 16 October 2026 · DEC-04/06/10/12

One PostgreSQL instance at `postgres:5432` hosts four **logical databases**, each with one owner login and separate EF migrations. The host publishes only loopback 5432; logical databases do not have separate network ports. Applications cannot connect to another owner's DB. Administrators bootstrap database roles; application logins have no cluster administration rights.

| Database | Owner/login | Entities and invariants |
|---|---|---|
| swiftdrop_identity | Identity / identity_app | users (normalized email unique, nullable password_hash, is_active), roles, user_roles, external_identities (provider+subject unique), refresh_sessions (token_hash, family, expiry, revoked), audit_logs |
| swiftdrop_delivery | Delivery / delivery_app | quotes (owner, request fingerprint, pricing version, expires_at, used_by), parcels (customer_id or merchant_id+external_order_id, canonical status, version), couriers (id references Identity user, active/on_duty/capacity), courier_zones, assignments (courier FK, service_date), immutable price_snapshots, booking_history, proof_metadata, idempotency_keys, outbox_messages, realtime consumer inbox, zones, pricing_tiers |
| swiftdrop_merchant | Merchant / merchant_app | businesses, api_keys (key_id, hash, salt, scopes, active), inbox_jobs (merchant_id+external_order_id unique, fingerprint, state, next_retry_at, parcel_id, parcel_status/version, last_status_changed_at, terminal_at), webhook_subscriptions, encrypted_secrets (ciphertext, nonce, key_version), webhook_jobs, webhook_attempts, dispatch inbox |
| swiftdrop_notifications | Worker / notifications_app | inbox_messages (consumer+event_id unique), notification_jobs (event_id+recipient_id+channel unique), provider_attempts, notification_logs, webhook_dispatch_jobs (event_id+merchant_id unique) |

## Transaction and idempotency constraints

Booking uses a unique `(principal_id, operation, idempotency_key)` index and a canonical JSON request fingerprint. Atomic insertion reserves the key in the **same transaction** as parcel, price snapshot, quote consumption, history and outbox. Concurrent duplicates wait for the winner then return its stored status/body; same key with a changed fingerprint returns `409`. After an unresolved lock/deadline return `409 operation_in_progress` with Retry-After; retry using the same key. A committed response remains reproducible for 30 days; expired keys return `409 key_expired` rather than silently creating another parcel. Quotes are single-use; repeated keys are resolved before checking quote expiry/consumption. Merchant external-order uniqueness is retained for the order's lifetime, independent of API key rotation.

Status updates compare `expectedVersion` in an atomic conditional write. Update parcel, assignment if needed, history and outbox together. No notification or webhook occurs inside that transaction. Consumer inbox/job creation commits before broker ACK. Outbox relay marks published only after broker confirmation and may publish a duplicate after crash. See [state rules](parcel-state-machine.md).

## Courier operations and private notes

Delivery owns explicit couriers operational profiles and courier_zones memberships; the local couriers.id equals the referenced Identity user ID, without a cross-database foreign key. assignments.courier_id is a local FK to couriers.id, and courier_zones has a unique (courier_id,zone_id) pair. Seed only verified Courier identities for the demo. Store service_date on each assignment and evaluate daily/overdue queries in configured Operations:TimeZone (proposed Asia/Colombo). Active/on-duty/capacity/zone checks run atomically with assignment.

booking_history.delivery_note stores the required private note for PickedUp/InTransit/OutForDelivery; Failed stores its reason, and proof_metadata.recipient_name belongs to the final proof record. Public summaries and broker events must not serialize these fields.

## Proof and receipt storage

Delivery alone has a private bucket credential. Upload accepts JPEG/PNG by decoded content, at most 5 MiB for each photo/signature (10 MiB combined), with generated object keys; reject executable or malformed data. Stage the upload, confirm object persistence, then authorize and commit proof metadata, `Delivered`, history and outbox with the expected version. A storage failure leaves state unchanged; a transaction failure leaves only an orphan staged object. A daily cleanup removes unreferenced objects older than 24 hours; committed references are protected. Retrying uses the original idempotency key and fingerprint.

Download proof/receipt only via authenticated Delivery endpoints after ownership checks, returning streamed bytes with private/no-store headers. No permanent public URLs or proof identifiers appear in anonymous tracking. Receipts are generated from the immutable snapshot for Delivered parcels. Courier proof upload does not grant receipt access.

## Migrations and retention

The [Compose reference](../deployment/docker-compose.md) creates all databases and owner roles before API startup. Each future image must run a single explicit migration task before readiness; production-style multi-replica automatic migrations are not promised. Verify notification migrations as well as the three APIs. Retain demonstration parcel/history records until an approved deletion policy exists. Purge expired refresh sessions, notification/provider and webhook attempt records after 30 days; never delete unresolved jobs or idempotency tombstones required for deduplication. Logs contain IDs/codes, not credentials or contact/address payloads. Backups, restore verification and retention acceptance remain implementation tasks.

Keep the Delivery eventId→parcel/version provenance index (outbox/history reference) for at least the 30-day consumer replay horizon and for all unresolved notification jobs. NotificationContext must remain able to validate an old but pending event after a broker outage; an outbox cleanup must not make durable jobs unresolvable. Merchant dashboard projections store authoritative Delivery terminal timestamps, never the local polling time.

See [ER source](../design/diagrams/er/README.md) and [security](../security/data-protection.md).
