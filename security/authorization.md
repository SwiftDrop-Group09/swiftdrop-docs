# Authorization and Ownership

> Status: Proposed baseline 2.0 · SEC/domain approval pending

YARP routes requests, applies rate limits/TLS ingress and may reject invalid tokens coarsely. **Each domain service** validates credentials, roles/scopes and resource ownership itself. Ignore user/merchant IDs or role headers from external clients; derive identity from validated tokens or Merchant-validated API keys. An internal network is not an authorization boundary. GraphQL resolvers and REST/gRPC wrappers use the same handlers.

| Action | Allowed actor | Mandatory resource guard |
|---|---|---|
| Estimate/confirm Customer booking | Customer JWT | quote.owner_id == sub; immutable input/price snapshot |
| Private parcel/history/SSE | Owner Customer; assigned Courier; Dispatcher/Admin | customer_id == sub or current assignment or operations role; no phone-number ownership shortcut |
| Receipt/proof download | Owner Customer or Admin | own Delivered parcel; private streamed bytes, no public URL |
| Assignment/reassignment | Dispatcher/Admin | valid before-pickup state, courier active/capacity/zone, atomic version |
| PickedUp/InTransit/OutForDelivery/Failed | Current assigned Courier only | assignment.courier_id == sub at **commit**, allowed transition, expectedVersion |
| Complete with proof | Current assigned Courier only | OutForDelivery, stored/valid required proof, version and assignment at commit |
| Cancel | Owner Customer, owning Merchant service, Dispatcher/Admin | Created/Assigned only; merchant service must prove matching parcel merchant_id |
| Merchant onboarding | Authenticated applicant | applicant_id == sub; cannot set Approved |
| Merchant keys/dashboard | Approved merchant human owner | membership business_id from trusted binding; no arbitrary merchantId |
| Merchant order submit/read | Approved merchant API key, exact scope | business_id from active key; external order/job belongs to business |
| Merchant own job reads | Merchant human owner | owned business only |
| Webhooks | Approved owner JWT or webhooks:manage key | subscription belongs to business; URL safety each send |
| Users/roles/approval/zones/pricing/reports/audit | Admin JWT | audited privileged action; no last-Admin removal |
| Public tracking | Anonymous | only PublicTrackingSummary; no private nested fields or SSE |

Dispatcher/Admin cannot advance courier operational status or upload courier proof. A merchant API key never grants Customer/Dispatcher/Admin endpoints or GraphQL private Parcel access. A matching recipient phone, email, supplied merchantId or global query filter alone cannot prove authorization. Use explicit resource predicates and version checks inside the transaction; avoid copying the earlier overbroad universal merchant query filter.

## Internal workload scope

Merchant→Delivery has bookings:create/read and parcels:cancel with aud=delivery-internal. Worker→Delivery has notifications:resolve for verified event/parcel/version IDs only. Worker→Merchant has webhooks:dispatch with aud=merchant-internal; only authenticated events from its durable inbox may be dispatched. Workload credentials are provisioned/rotated privately; public callers cannot mint them. Merchant never shares DB credentials or signing material with Worker.

Return 401 for missing/invalid credential, 403 for missing role/scope, 404 for foreign/missing resource, 409 for authorized stale version/state/key conflict, without private side effects. Reassignment and status writes race under one DB concurrency guard; the losing operation receives 409 or 404 if ownership was lost. Privilege/deactivation JWT changes take effect within the [documented 15-minute bound](authentication.md); API-key revocation is immediate in Merchant. Tests must cover both bounds, bypass attempts via GraphQL and direct service calls, and foreign proof/receipt access.
