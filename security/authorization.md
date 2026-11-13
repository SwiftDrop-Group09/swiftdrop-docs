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

## Exactly one human role

Every human account has exactly one role from the closed enum Customer, Courier,
Merchant, Dispatcher or Admin. Roles are mutually exclusive; navigation and
permissions do not combine roles. This does not combine human roles with merchant
API-key scopes or workload identities. Registration defaults to Customer; Admins
replace the assigned role through an audited operation. Prevent removing the last
active Admin. Inactive accounts still retain one role.

For v1 compatibility `Profile.roles`, `RolesInput.roles` and JWT `roles` remain
arrays containing exactly one enum name. Reject empty, duplicate, unknown and
multi-role sets. Identity and Delivery reject ambiguous human tokens; Merchant
validates one named role on human JWT authentication. Refresh/re-authentication is
required for previously issued ambiguous tokens.

Identity migration 005 converts stored assignments to PostgreSQL `user_role` enum
columns, adds a unique user assignment and a deferred exactly-one constraint.
Previous assignments are archived in an owner-only table. Existing assignments
are consolidated by Admin > Dispatcher > Merchant > Courier > Customer; accounts
without an assignment become Customer. This is a specific migration policy, not
an ongoing permission hierarchy. No accounts, credentials, parcels or businesses
are deleted. Apply the forward migration before starting the updated services.
