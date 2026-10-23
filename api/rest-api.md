# REST API Specification

> Status: Proposed contract baseline 2.0 · 16 October 2026 · API/SEC/domain approval pending

All external requests use YARP and `/api/v1`; no legacy aliases are proposed. JSON is camelCase, times are UTC ISO 8601, IDs are opaque strings, prices are decimal LKR rounded half-up to two decimals. All `{id}` delivery routes use the **parcel ID**, not a second delivery identifier. Static routes (`track`, `me`, `summary`) take precedence over parameter routes. Internal routes are not exposed by YARP. [Machine-readable route inventory](contracts/routes.json) is the design source for the table below; implementation OpenAPI must be reconciled in the owning source repository.

## Route catalog

`Human JWT` means a SwiftDrop access token, with service-side resource authorization. API keys are accepted only where stated; they are never interchangeable with an Admin or Customer JWT.

| Operation ID | Method | Path | Owner | Authentication / resource guard | Input | Output | Success |
|---|---|---|---|---|---|---|---|
| Register | POST | /api/v1/auth/register | Identity | Public; throttled | RegisterInput | Profile | 201 |
| Login | POST | /api/v1/auth/login | Identity | Public; throttled | LoginInput | TokenPair | 200 |
| GoogleLogin | POST | /api/v1/auth/google | Identity | Public; throttled | GoogleInput | TokenPair | 200 |
| LinkGoogle | POST | /api/v1/auth/google/link | Identity | Human JWT; fresh local reauthentication | LinkInput | Profile | 200 |
| Refresh | POST | /api/v1/auth/refresh | Identity | Valid refresh token | RefreshInput | TokenPair | 200 |
| Logout | POST | /api/v1/auth/logout | Identity | Human JWT; own refresh family | RefreshInput | Empty | 204 |
| GetProfile | GET | /api/v1/users/me | Identity | Human JWT; self | None | Profile | 200 |
| UpdateProfile | PUT | /api/v1/users/me | Identity | Human JWT; self | ProfileInput | Profile | 200 |
| ListUsers | GET | /api/v1/users | Identity | Human JWT; Admin | PageQuery | ProfilePage | 200 |
| CreateUser | POST | /api/v1/users | Identity | Human JWT; Admin | AdminUserInput | Profile | 201 |
| UpdateUser | PUT | /api/v1/users/{id} | Identity | Human JWT; Admin | AdminUserInput | Profile | 200 |
| DeactivateUser | DELETE | /api/v1/users/{id} | Identity | Human JWT; Admin; soft delete | None | Empty | 204 |
| SetRoles | PUT | /api/v1/users/{id}/roles | Identity | Human JWT; Admin | RolesInput | Profile | 200 |
| ListAudit | GET | /api/v1/audit-logs | Identity | Human JWT; Admin | PageQuery | AuditPage | 200 |
| GetJwks | GET | /.well-known/jwks.json | Identity | Public; trusted issuer origin | None | Jwks | 200 |
| EstimateFee | POST | /api/v1/quotes | Delivery | Human JWT; Customer | QuoteInput | Quote | 200 |
| CreateParcel | POST | /api/v1/parcels | Delivery | Human JWT; Customer; own quote | ConfirmInput | Parcel | 201 |
| ListParcels | GET | /api/v1/parcels | Delivery | Human JWT; own Customer or Dispatcher/Admin | ParcelQuery | ParcelPage | 200 |
| GetParcel | GET | /api/v1/parcels/{id} | Delivery | Human JWT; owner, assigned Courier, Dispatcher/Admin | None | Parcel | 200 |
| PublicTrack | GET | /api/v1/parcels/track/{trackingNumber} | Delivery | Public; rate limited | None | PublicTrackingSummary | 200 |
| ParcelEvents | GET | /api/v1/parcels/{id}/events | Delivery | Human JWT; owner, assigned Courier, Dispatcher/Admin | None | SseSnapshot | 200 |
| CancelParcel | PUT | /api/v1/parcels/{id}/cancel | Delivery | Human JWT; own Customer or Dispatcher/Admin | CancelInput | Parcel | 200 |
| DownloadReceipt | GET | /api/v1/parcels/{id}/receipt | Delivery | Human JWT; own Customer, Admin; Delivered only | None | PdfBytes | 200 |
| DownloadProof | GET | /api/v1/parcels/{id}/pod | Delivery | Human JWT; own Customer, Admin; Delivered only | None | ImageBytes | 200 |
| AssignCourier | POST | /api/v1/deliveries/assign | Delivery | Human JWT; Dispatcher/Admin | AssignInput | Parcel | 200 |
| UpdateDeliveryStatus | PUT | /api/v1/deliveries/{id}/status | Delivery | Human JWT; currently assigned Courier | StatusInput | Parcel | 200 |
| CompleteDeliveryWithProof | POST | /api/v1/deliveries/{id}/pod | Delivery | Human JWT; currently assigned Courier | ProofInput | Parcel | 200 |
| CourierAssignments | GET | /api/v1/couriers/me/assignments | Delivery | Human JWT; Courier self | AssignmentQuery | ParcelPage | 200 |
| CourierHistory | GET | /api/v1/couriers/me/history | Delivery | Human JWT; Courier self | PageQuery | ParcelPage | 200 |
| CourierWorkload | GET | /api/v1/couriers/workload | Delivery | Human JWT; Dispatcher/Admin | PageQuery | WorkloadPage | 200 |
| ZoneSummary | GET | /api/v1/zones/summary | Delivery | Human JWT; Dispatcher/Admin | DateQuery | ZoneSummary | 200 |
| ListZones | GET | /api/v1/zones | Delivery | Human JWT; Admin | PageQuery | ZonePage | 200 |
| CreateZone | POST | /api/v1/zones | Delivery | Human JWT; Admin | ZoneInput | Zone | 201 |
| UpdateZone | PUT | /api/v1/zones/{id} | Delivery | Human JWT; Admin | ZoneInput | Zone | 200 |
| ListPricing | GET | /api/v1/pricing-tiers | Delivery | Human JWT; Admin | PageQuery | PricingPage | 200 |
| CreatePricing | POST | /api/v1/pricing-tiers | Delivery | Human JWT; Admin | PricingInput | Pricing | 201 |
| UpdatePricing | PUT | /api/v1/pricing-tiers/{id} | Delivery | Human JWT; Admin | PricingInput | Pricing | 200 |
| DeliveryReport | GET | /api/v1/reports/deliveries | Delivery | Human JWT; Admin | DateQuery | DeliveryReport | 200 |
| RegisterMerchant | POST | /api/v1/merchants/register | Merchant | Human JWT; self applicant | MerchantInput | Business | 201 |
| GetMerchant | GET | /api/v1/merchants/me | Merchant | Human JWT; own applicant/business | None | Business | 200 |
| ListMerchants | GET | /api/v1/merchants | Merchant | Human JWT; Admin | PageQuery | BusinessPage | 200 |
| SetMerchantStatus | PUT | /api/v1/merchants/{id}/status | Merchant | Human JWT; Admin | ApprovalInput | Business | 200 |
| CreateApiKey | POST | /api/v1/merchants/api-keys | Merchant | Human JWT; approved Merchant owner | ScopesInput | OneTimeKey | 201 |
| ListApiKeys | GET | /api/v1/merchants/api-keys | Merchant | Human JWT; approved Merchant owner | PageQuery | KeyMetadataPage | 200 |
| RevokeApiKey | DELETE | /api/v1/merchants/api-keys/{keyId} | Merchant | Human JWT; own approved Merchant | None | Empty | 204 |
| SubmitMerchantOrder | POST | /api/v1/merchant/orders | Merchant | X-API-Key; approved Merchant; orders:write | MerchantOrderInput | OrderJob | 202 |
| ListMerchantOrders | GET | /api/v1/merchant/orders | Merchant | Human JWT Merchant owner OR X-API-Key orders:read | PageQuery | OrderJobPage | 200 |
| GetMerchantOrder | GET | /api/v1/merchant/orders/{id} | Merchant | Human JWT Merchant owner OR X-API-Key orders:read | None | OrderJob | 200 |
| MerchantDashboard | GET | /api/v1/merchants/me/dashboard | Merchant | Human JWT; approved Merchant owner | DateQuery | MerchantDashboard | 200 |
| CreateWebhook | POST | /api/v1/merchant/webhooks | Merchant | Human JWT owner OR X-API-Key webhooks:manage; approved | WebhookInput | OneTimeWebhook | 201 |
| ListWebhooks | GET | /api/v1/merchant/webhooks | Merchant | Human JWT owner OR X-API-Key webhooks:manage; approved | PageQuery | WebhookPage | 200 |
| DeleteWebhook | DELETE | /api/v1/merchant/webhooks/{id} | Merchant | Human JWT owner OR X-API-Key webhooks:manage; approved | None | Empty | 204 |
| ListWebhookAttempts | GET | /api/v1/merchant/webhooks/{id}/attempts | Merchant | Human JWT; approved Merchant owner | PageQuery | WebhookAttemptPage | 200 |
| ReplayWebhook | POST | /api/v1/merchant/webhooks/{id}/replays | Merchant | Human JWT; approved Merchant owner; audit | ReplayInput | WebhookJob | 202 |
| DispatchWebhook | POST | /internal/v1/webhook-dispatches | Merchant | Service JWT; worker; webhooks:dispatch | StatusChanged | DispatchResult | 202 |
| NotificationContext | POST | /internal/v1/notification-context | Delivery | Service JWT; worker; notifications:resolve | EventReference | NotificationContext | 200 |
| CancelMerchantParcel | PUT | /internal/v1/parcels/{id}/cancel | Delivery | Service JWT; Merchant; parcels:cancel; owning merchant | MerchantCancelInput | Parcel | 200 |

## Shared request and response contracts

All body fields below are required unless marked optional. Reject unknown authorization fields such as userId/merchantId/role in external booking inputs. Never derive owner identity from caller-supplied IDs. Idempotency-Key (UUID/opaque ≤128 chars) is required for CreateParcel, SubmitMerchantOrder, AssignCourier, UpdateDeliveryStatus and CompleteDeliveryWithProof. A key scopes to authenticated principal+operation; persist canonical-body fingerprint and exact response atomically. Merchant ingestion additionally deduplicates merchant+externalOrderId across key rotation. See [data constraints](../architecture/data-architecture.md).

| Input | Fields / validation |
|---|---|
| RegisterInput | email ≤254, password 12–128 chars, fullName 1–120; server assigns Customer only; duplicate returns generic 409 registration_conflict; do not log password |
| LoginInput | email, password; generic 401 invalid_credentials for unknown, disabled or wrong password |
| GoogleInput | idToken from configured web/Android Google SDK; signature/iss/aud/exp/email_verified checked; SDK nonce/CSRF checks per client |
| LinkInput | idToken and currentPassword; valid app JWT plus successful fresh local-password check; collision never automatically links by email |
| RefreshInput | refreshToken; token hash stored; rotate atomically; reuse revokes family; browser refresh token in secure HttpOnly cookie instead of JSON; see authentication |
| ProfileInput | fullName, phoneNumber, address (optional); no roles or ownership fields |
| AdminUserInput | email, fullName, isActive; CreateUser also requires a generated local password distributed privately; admin cannot read password hashes; self-service password reset is deferred |
| RolesInput | roles array from Customer/Courier/Merchant/Dispatcher/Admin; audit changes, prevent removing last active Admin |
| QuoteInput | pickupAddress, deliveryAddress (street, city, postalCode, zoneId), packageDetails (weightKg >0 ≤30, size Small/Medium/Large); recipient (name, phoneNumber) is included in quote fingerprint |
| ConfirmInput | quoteId, acceptTotal decimal; owner and full quote fingerprint checked; server reads delivery details from quote |
| AssignInput | parcelId, courierId, expectedVersion integer ≥1, reassign boolean (default false), reason required if reassign; optional serviceDate YYYY-MM-DD defaults to today in configured business timezone |
| StatusInput | status PickedUp/InTransit/OutForDelivery/Failed, expectedVersion; nonblank private notes 1–500 required for PickedUp/InTransit/OutForDelivery; failureReason required for Failed, where additional notes are optional |
| ProofInput | multipart photo or signature (at least one, JPEG/PNG ≤5 MiB each), recipientName ≤120, expectedVersion; only OutForDelivery may complete; Idempotency-Key fingerprint includes content hashes |
| CancelInput | expectedVersion, reason ≤500; permitted only before pickup |
| MerchantCancelInput | merchantId, expectedVersion, reason; trusted service credential plus parcel merchant ownership match required |
| MerchantInput | businessName ≤200, contactEmail, pickupAddress; applicant user from token; initial status Pending |
| ApprovalInput | status Approved/Rejected/Suspended, reason; Pending→Approved/Rejected; Approved→Suspended; suspension disables keys/dispatch; role grant via scoped Identity administration is audited and manual for baseline |
| ScopesInput | scopes subset orders:write, orders:read, webhooks:manage; cannot grant beyond business privileges |
| MerchantOrderInput | externalOrderId ≤128, QuoteInput fields, acceptedPriceVersion; server calculates and snapshots tariff matching accepted version; mismatch returns 409 pricing_changed before acceptance |
| WebhookInput | url HTTPS public destination, events subset delivery.created/assigned/picked_up/in_transit/out_for_delivery/delivered/failed/cancelled; server creates signing secret; no user-provided secret |
| ReplayInput | eventId, reason; creates audited new replay job only for own failed event/subscription, original event ID preserved |
| ZoneInput | name, coarse city, servicePostalCodes array, active, expectedVersion on update; no overlapping postal-code ownership |
| PricingInput | zoneId, size, baseFee ≥0, perKgFee ≥0, currency LKR, expectedVersion on update; version immutable once used |
| PageQuery | page ≥1 default 1, pageSize 1–100 default 20; stable createdAt+id ordering |
| AssignmentQuery | PageQuery plus optional date YYYY-MM-DD (default today in Operations:TimeZone, proposed Asia/Colombo), includeOverdue boolean default true; server always scopes current assignments to Courier sub |
| ParcelQuery | PageQuery + optional status, from/to UTC dates; Created filter covers dispatcher unassigned; owner filter is forced server-side |
| DateQuery | from inclusive/to exclusive UTC timestamps, maximum 366 days; required for reports, default current UTC day for dashboard |
| EventReference | eventId, parcelId, parcelVersion; verifies persisted event belongs to that parcel/version before resolving |

Quote pricing: `total = baseFee(zone,size,pricingVersion) + perKgFee * max(0, weightKg - 1)`. The user confirmed on 23 October 2026 that `zone` is `deliveryAddress.zoneId`; the selected tier, parcel zone and price snapshot all use that delivery zone. Independently validate `pickupAddress.zoneId` as an eligible active service zone and preserve it with the pickup address; it does not affect the tariff. No cross-zone surcharge is defined. Return quoteId, total, currency, pricingVersion, expiresAt (10 minutes) and fingerprint; bind quote to owner. Example seed: base 450, perKg 60, weight 2.5 → LKR 540.00. Repricing never silently changes a confirmed quote. Expired quote returns 409 quote_expired; client obtains and confirms a new quote. Successful CreateParcel consumes quote once, returns 201 and Location to GetParcel; duplicate same key returns original 201/body even after expiry.

| Output | Minimal fields and behavior |
|---|---|
| Profile | id, email, fullName, phoneNumber, address, roles, isActive; self or Admin only |
| TokenPair | accessToken, tokenType Bearer, expiresInSeconds 900, user Profile; mobile gets refreshToken, browser gets HttpOnly cookie; never return local/provider credentials |
| Quote | quoteId, total, currency, pricingVersion, expiresAt, fingerprint |
| Parcel | id, trackingNumber, status, version, priceSnapshot, createdAt; authenticated projection additionally contains authorized recipient/address, assignment and private history; never raw storage URL |
| OrderJob | id, externalOrderId, state Accepted/Retrying/Created/Failed, attempts, nextRetryAt nullable, parcelId/trackingNumber nullable until Created, parcelStatus/parcelVersion/lastStatusChangedAt/terminalAt nullable, errorCode nullable; no false parcel result before creation |
| OneTimeKey | keyId, apiKey `swd_test_<keyId>_<random>` (local examples), scopes; raw secret only on creation; metadata lists omit secret/hash |
| OneTimeWebhook | id, url, events, active, secret one time, keyVersion; lists omit secret/ciphertext |
| DispatchResult | eventId, accepted true; Merchant durably deduplicates before 202; response exposes no subscription secret |
| NotificationContext | customerUserId nullable for the verified event; Customer-originated parcels notify that owner, Merchant-originated parcels use merchant webhooks; no street, phone, coordinates or proof |
| WorkloadPage | items (courierId, onDuty, activeCount, capacity, zoneIds), totalCount/page/pageSize |
| ZoneSummary | zones (zoneId, statusCounts, total) scoped date range |
| Business | id, applicantUserId, businessName, status, reason, approvedAt nullable; own applicant or Admin |
| Zone / Pricing | id, version plus validated configuration fields |
| AuditPage | items (id, actorId, action, resourceId, timestamp, resultCode); redact secrets and request bodies |
| WebhookJob / WebhookAttemptPage | jobId, eventId, subscriptionId, state, attemptNumber, attempt timestamp, response code, safe errorCode, nextRetryAt; no bodies/keys |
| Jwks | keys array with public kty/use/alg/kid/n/e; no private key components |
| *Page | items, totalCount, page, pageSize; stable sorting and forced resource scope |
| PdfBytes / ImageBytes | application/pdf or image/jpeg/png; Content-Disposition; private,no-store; streaming after authorization |
| Empty | no body |
| SseSnapshot | text/event-stream: event snapshot, id parcelId:version, JSON id/status/version/lastUpdatedAt; authorization/reconnect rules in realtime specification |

## Public tracking projection

REST and GraphQL return exactly the same allowlisted fields (enum spelling maps as defined in the state machine). Tracking codes have ≥128 random bits, are nonsequential, and are rate limited to 60/minute/IP. No nested Parcel object, address, phone, precise coordinate, courier identity, private notes, proof or receipt is reachable. Unknown codes return 404; public timeline labels are server constants.

```json
{
  "trackingNumber": "TRK-example-128-bit-random-code",
  "status": "InTransit",
  "originCity": "Colombo",
  "destinationCity": "Kandy",
  "lastUpdatedAt": "2026-10-16T10:00:00Z",
  "timeline": [
    {"status": "Created", "timestamp": "2026-10-16T08:00:00Z", "label": "Booked"},
    {"status": "InTransit", "timestamp": "2026-10-16T10:00:00Z", "label": "In transit"}
  ]
}
```

## Mandatory dashboards, receipts and reports

React Customer and Flutter Customer expose Receipt from Delivered history; DownloadReceipt verifies customer_id==sub or Admin. A merchant human's dashboard displays only owned orders/jobs, pendingCount (Accepted/Retrying), statusCounts, terminalDeliveredCount, terminalFailedCount and success/failure rates. Merchant has no unrestricted Delivery query: its reconciliation loop reads Delivery `GetBookingByExternalOrder`, updates owned parcelStatus/parcelVersion, and surfaces `lastRefreshedAt`; stale data is labeled and refreshed on polling, not presented as guaranteed realtime. Orders:read keys see only own OrderJob data.

Admin DeliveryReport returns from/to, `days[{date,delivered,failed}]`, delivered, failed, terminalCount, successRate and failureRate. Count terminal transitions by UTC history timestamp in [from,to); terminalCount=delivered+failed; successRate=delivered/terminalCount and failureRate=failed/terminalCount, or both 0 when no terminal outcomes. Cancelled is a separate count, excluded from those denominators. Merchant dashboard uses the same formula for its scope and additionally shows Created/Assigned/active counts. No revenue/payment-collection claim is made; any fee totals are snapshot totals only.

## Merchant ingestion and partial failures

SubmitMerchantOrder is **always durable asynchronous 202**, not a synchronous 201 parcel creation. Validate scope, approved business, tariff version and required fields, atomically store inbox job plus unique merchant/external order key, then return Location to GetMerchantOrder. Response has null parcel/tracking fields until processing succeeds. An embedded Merchant inbox processor claims jobs, calls the defined `CreateBooking` RPC and marks Created. Timeout means unknown outcome: set Retrying, call GetBookingByExternalOrder, then retry with the same stable key only if NotFound. Permanent validation failure sets Failed with safe reason. Retry delays 5s, 30s, 2m, 10m, then hourly with alert after 10 failures; no job is silently lost. Reconciliation of an existing successful parcel always wins over a timeout. Bulk `/parcels/bulk` and synchronous order creation are deferred and are not supported routes. Admin approval is not a parcel state.

## Courier day and stage-note rules

CourierAssignments returns the current Courier's active assignments with assignment.serviceDate equal to the selected date, plus still-active earlier service dates when includeOverdue=true. A future day's work is absent from today's result. Each authenticated item includes serviceDate and isOverdue; CourierHistory remains the separate terminal-history view. The server uses its configured business timezone rather than the device clock. AssignCourier records serviceDate atomically with the assignment; reassignment may explicitly reschedule it before pickup.

Delivery owns couriers operational profiles (id references the Identity user ID, active, onDuty, capacity and zone memberships) and the assignment foreign key points to this local profile. A Courier role alone cannot manufacture an operational profile or assignment. The local demo seeds profiles for verified Courier identities; an unprovisioned/inactive/out-of-zone/full courier is rejected by assignment validation. No service queries Identity SQL. A separate general provisioning API is not assumed by this fixture.

PickedUp/InTransit/OutForDelivery require a nonblank delivery note; missing notes return 400 before history/state/outbox changes. Failed stores its required reason; final completion stores recipientName and valid photo/signature. Notes/proof remain private and absent from StatusChanged and public timelines. The assignment permits note or proof, while the final-image/signature requirement is a proposed stronger team policy.

## Status, proof and error behavior

All state changes obey the [single transition matrix](../architecture/parcel-state-machine.md). Assign/status/proof commands require expectedVersion and Idempotency-Key. Proof upload **completes** delivery; no separate Delivered status write is accepted. A storage failure returns 503 without changing state; a stale concurrent state after upload returns 409 and staged object is cleaned up later. Authorized downloads stream through Delivery; raw storage locations stay private.

Errors use ProblemDetails: type (stable code URI under example.invalid/problems), title, status, code, correlationId, and optional field errors. Do not return credentials, stack traces or private resource fields. 400 = malformed/field validation; 401 = missing/invalid credential; 403 = valid credential but missing role/scope; 404 = missing or foreign resource to prevent enumeration; 409 = idempotency mismatch, operation in progress, stale version, quote/pricing conflict or invalid state; 422 = capacity/zone domain rejection; 429 = throttled with Retry-After; 503 = dependency/storage unavailable before commit. A committed parcel remains committed during broker outage. Auth endpoints: registration 5/minute/IP, login/Google 10/minute/IP plus account lockout escalation; all limits are proposed and require implementation evidence.

Client IDs, hosts and TLS policy: [environment matrix](../deployment/environments.md). Session/cookie behavior: [authentication](../security/authentication.md). Planned acceptance tests: [catalog](../testing/test-cases.md).
