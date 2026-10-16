# GraphQL API Specification

> Status: Proposed baseline 2.0 · DEC-11 · Delivery owns `/graphql`

YARP routes `/graphql` to Delivery's HTTP listener. [schema.graphql](contracts/schema.graphql) is the validated design SDL fixture. GraphQL is an optional delivery-domain interface alongside complete REST; it is not a separate BFF process and cannot query Identity/Merchant databases. Any future multi-domain resolver must call an authorized API and receive a contract review.

## Public and private results

Only `trackParcel` is anonymous. It returns **PublicTrackingSummary**, a separate scalar/allowlisted timeline tree with no path to Parcel, Address, Recipient, courier, proof or receipt. Public REST uses the identical safe projection with enum name mapping from the [state machine](../architecture/parcel-state-machine.md). Public fields must be tested by anonymous queries, aliases and nested fragments; introspection settings do not substitute for authorization.

```graphql
query PublicTracking {
  trackParcel(trackingNumber: "TRK-example-128-bit-random-code") {
    status originCity destinationCity lastUpdatedAt
    timeline { status timestamp label }
  }
}
```

`parcel` requires owner Customer, currently assigned Courier, Dispatcher or Admin. `myParcels` is Customer-scoped to sub; it cannot accept arbitrary customerId. Merchant clients use Merchant REST/dashboard; a Merchant role alone does not grant Delivery GraphQL access. Enforce roles and ownership **inside shared application handlers**, including each nested private resolver and batch loader; never cache private results across principals.

## Write equivalence

| GraphQL field | Canonical REST operation / handler | Guard |
|---|---|---|
| estimateFee | EstimateFee | Customer; exact QuoteInput/price rules |
| createParcel | CreateParcel | Customer; own valid quote, explicit acceptTotal, same atomic idempotency |
| assignCourier | AssignCourier | Dispatcher/Admin; same expectedVersion/capacity/reassignment |
| updateDeliveryStatus | UpdateDeliveryStatus | Current assigned Courier; same transitions/failureReason/version |

AssignInput.serviceDate uses the same optional YYYY-MM-DD/business-timezone default as REST. StatusInput.notes remains nullable at SDL level for Failed, but the shared handler requires a nonblank note for PickedUp/InTransit/OutForDelivery; missing notes fail before any write. The explicit idempotencyKey argument maps to the same scoped idempotency record used by REST. GraphQL enum values map to canonical domain spelling; StatusInput cannot bypass the prohibition on Delivered (proof endpoint only). File upload/receipt, reporting and merchant management remain REST in this baseline. No parallel GraphQL business rules exist. Decimal scalar parses exact decimal strings and rejects floating-point precision loss.

GraphQL errors use `extensions.code` matching REST codes with `extensions.httpStatus` and correlationId; missing credentials use 401, insufficient role 403, foreign resource 404, invalid state/version/key 409 and field validation 400. Successful transport with field errors must not be mistaken for a committed command. Clients inspect errors before displaying success.

## Limits

Proposed guards: one operation/request, depth ≤8, complexity ≤100, pagination 1–100, alias count ≤10, request body ≤64 KiB, 5s execution deadline, 60 public requests/minute/IP. Reject invalid enum/Decimal/ID before handlers. No subscriptions or public private-data resolver. Public DTO allowlisting and resolver authorization remain mandatory regardless of whether introspection is enabled. Anonymous and owner-negative tests are drafted; runtime execution remains pending.
