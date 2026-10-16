# Internal gRPC Contracts

> Status: Proposed baseline 2.0 · DEC-07 · API/MER/DEL approval pending

The authoritative design fixture is [delivery.proto](contracts/delivery.proto), package `swiftdrop.delivery.v1`. Its only service is DeliveryService, hosted by Delivery at `delivery-service:8081` (HTTP/2). It defines **CreateBooking** and **GetBookingByExternalOrder**; no undefined CheckZoneCapacity, ReserveParcelSlot, Identity token-validation RPC or Merchant secret RPC is used. Validation/capacity is performed by the owning command handler. Backend repository parity is pending source access/evidence.

## Method semantics

Merchant's durable inbox processor calls CreateBooking only after accepting a job. Authenticate service JWT (aud=delivery-internal, scope=bookings:create) and restrict merchant_id to the originating job's authenticated business context. Internal merchant_id is trusted only from the authenticated Merchant workload; no public client can set it. Use stable `(merchant_id, external_order_id)` uniqueness independent of API-key ID, with canonical fingerprint and original response. Decimal strings avoid binary floating-point price/weight drift; validate positive weight ≤30 and configured size/zone/pricing version. The shared Delivery handler writes parcel, price/history and StatusChanged outbox atomically. Same identity+payload returns existing result, changed payload returns AlreadyExists; no distributed transaction.

GetBookingByExternalOrder uses aud=delivery-internal and bookings:read. It returns parcel/tracking/status/version/immutable price plus UTC created_at, last_status_changed_at and optional terminal_at, or NotFound. Merchant persists these authoritative timestamps with its status projection so date-range dashboard reports count terminal outcomes by Delivery history time rather than poll time. Merchant uses the RPC after a 5-second deadline/unknown create result and for own-dashboard reconciliation. Retry CreateBooking only with the same stable identity and payload. A recovered created parcel must not be marked Failed because the original response was lost.

## Transport and failures

No gRPC ports are published to the host or through YARP. Loopback/container development may use h2c on the isolated local network; nonlocal environments require configured TLS (mTLS can be added separately) **plus** service JWTs. Do not claim mTLS deployed without evidence. Provision short-lived workload credentials through Identity's administration/bootstrap process; no general public token-mint endpoint. Cache JWKS with bounded expiry and fail closed for unknown keys. Set 5s deadlines, cancellation and correlation IDs; redact address/request bodies from logs.

| gRPC status | Meaning / recovery |
|---|---|
| InvalidArgument | Required address, size or decimal validation failed; permanent job failure |
| Unauthenticated / PermissionDenied | Credential/scope mismatch; stop and alert; never bypass |
| NotFound | Reconciliation found no parcel; retry same-key CreateBooking |
| AlreadyExists | Existing external order with different fingerprint; 409-equivalent permanent conflict |
| FailedPrecondition | Pricing version changed or invalid business state; explicit job error |
| ResourceExhausted | Capacity/limit; retry only if documented transient code |
| DeadlineExceeded / Unavailable | Unknown outcome; durable Retrying and reconcile before repeat |

Compile the fixture using `python -m grpc_tools.protoc -I api/contracts --descriptor_set_out=<temporary-file> api/contracts/delivery.proto`. This checks schema syntax, not a running server. See [merchant use case](../requirements/use-case-specifications.md) and [test cases](../testing/test-cases.md).
