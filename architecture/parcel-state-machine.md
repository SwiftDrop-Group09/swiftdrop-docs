# Parcel State Machine

> Status: Proposed baseline 2.0 · DEC-06 · DEL/REQ/SEC approval pending

A fee quote is not a parcel and emits no delivery event. `Created` exists only after explicit customer confirmation of an unexpired quote (or approved merchant order processing). There is no parcel Pending/Confirmed state. Merchant onboarding and ingestion job states are separate enums.

| Domain / REST / event value | GraphQL enum | Public label |
|---|---|---|
| Created | CREATED | Booked |
| Assigned | ASSIGNED | Assigned |
| PickedUp | PICKED_UP | Collected |
| InTransit | IN_TRANSIT | In transit |
| OutForDelivery | OUT_FOR_DELIVERY | Out for delivery |
| Delivered | DELIVERED | Delivered |
| Failed | FAILED | Delivery unsuccessful |
| Cancelled | CANCELLED | Cancelled |

## Transition matrix

Every accepted transition increments parcel version, appends history and adds one `StatusChanged` outbox record in one transaction. All writes require expectedVersion and current authorization. Unlisted transitions are rejected with `409 invalid_transition` and no effects.

| From → To | Actor / operation | Guard and action |
|---|---|---|
| none → Created | Customer `CreateParcel`; Merchant service `CreateBooking` | Confirmed valid quote/price; atomic idempotency and immutable snapshot |
| Created → Assigned | Dispatcher/Admin `AssignCourier` | Active available courier, zone/capacity verified atomically; create current assignment |
| Assigned → Assigned | Dispatcher/Admin `AssignCourier` | Explicit reassignment before pickup only; expectedVersion; release old capacity and update assignment atomically; emit one event with reassignment reason |
| Assigned → PickedUp | Currently assigned Courier `UpdateDeliveryStatus` | Assignment still matches caller at commit |
| PickedUp → InTransit | Currently assigned Courier `UpdateDeliveryStatus` | Expected version and assignment match |
| InTransit → OutForDelivery | Currently assigned Courier `UpdateDeliveryStatus` | Expected version and assignment match |
| OutForDelivery → Delivered | Currently assigned Courier `CompleteDeliveryWithProof` | Valid required photo or signature stored successfully; status endpoint cannot set Delivered |
| Assigned/PickedUp/InTransit/OutForDelivery → Failed | Currently assigned Courier `UpdateDeliveryStatus` | Required code: RecipientUnavailable, AddressUnreachable, Damaged, Other; notes optional/private |
| Created/Assigned → Cancelled | Customer owner, merchant-owning service, Dispatcher/Admin `CancelParcel` | Before pickup; release any assignment capacity; reason required |

Delivered, Cancelled and Failed are terminal in this baseline. Redelivery/return after custody failure requires a new authorized booking with explicit reference to the failed parcel; no undocumented Failed→Created retry. Physical return resolution is manual and outside the tracked demo lifecycle. Reassignment after pickup is not supported. Dispatcher/Admin may assign/cancel but cannot impersonate a courier to advance operational status or upload proof.

## Concurrency, repeat and failure behavior

A stale expectedVersion returns `409 stale_version`, including current version only to an authorized actor. An unrelated courier gets `404` regardless of state; a role without write permission gets `403`. Retrying the same idempotent operation with an identical payload returns its stored result, without an extra event. A new key repeating a status returns `409`; Assigned→Assigned is allowed only as an explicit valid reassignment. Capacity and assignment concurrency use row locks/conditional updates in the same transaction. Storage and broker failures cannot cause a false Delivered status: storage must succeed before the transaction, and the committed outbox survives broker outage.

Public timelines map statuses to fixed redacted labels and coarse cities; never interpolate private notes, courier names or street locations. See [API contracts](../api/rest-api.md), [events](../integration/event-catalog.md) and [authorization](../security/authorization.md).
