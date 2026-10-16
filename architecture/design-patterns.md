# Design Patterns and Principles

> Proposed design note · Assignment PDF page 2 requirement · Implementation examples/evidence pending

The [assignment](../requirements/sources/ead-group-assignment.pdf#page=2) requires a short patterns/principles note and gives SOLID, DRY, Repository, pricing Strategy and event Observer as examples. The following explains SwiftDrop's proposed use and tradeoffs; it is not a claim that source code exists or that every listed example is independently compulsory.

| Principle/pattern | Intended SwiftDrop application | Reason, constraint and verification |
|---|---|---|
| SOLID: single responsibility | Identity owns credentials; Delivery owns parcels/prices/proof; Merchant owns subscriptions/signing; Worker owns notification jobs | Separate reasons to change. Domain services cannot use another service's DB; verify call/data ownership against the service catalog |
| SOLID: open/closed | Versioned pricing policies selected behind a narrow pricing interface | Additional approved pricing strategies can be added without duplicating booking handlers; the current baseline has one zone/size/weight formula, not an invented set of algorithms |
| SOLID: Liskov substitution/interface segregation | Small quote, proof-store, notification-provider and clock interfaces | Adapters must preserve validation/error semantics; tests can inject a fake clock/store/provider without bypassing ownership or SSRF controls |
| SOLID: dependency inversion | Application handlers depend on domain rules and narrow persistence/provider abstractions | Controllers, EF/storage, broker and HTTP adapters depend inward; secrets/config are injected at the boundary |
| DRY / shared application handlers | REST, GraphQL and internal booking RPC delegate to the same pricing/state/idempotency/authorization policies | One place defines a business transition; protocol-equivalence tests detect drift. Public/private DTOs remain intentionally separate for privacy |
| Repository / unit of work | Domain-oriented persistence operations over the owning EF DbContext; one transaction for parcel/history/outbox | EF already supplies change tracking/unit of work; avoid redundant generic CRUD wrappers. An abstraction never authorizes foreign SQL or distributed DB transactions |
| Strategy for pricing | Pricing policy consumes immutable tariff version, zone, size and weight; quote stores its result | Team baseline formula is baseFee + perKgFee × max(0, weightKg − 1), rounded as defined in REST. Select policies explicitly rather than hard-coding per-controller formulas |
| Observer / publish-subscribe | Committed StatusChanged is published through RabbitMQ to Worker and Delivery realtime consumers | Distributed observers are at-least-once and asynchronous, not synchronous callbacks inside the business transaction. Subscriber failures must not roll back committed parcel status |
| Transactional outbox / inbox | Local state/history/outbox transaction plus durable consumer/job uniqueness | Prevent lost status effects on broker outage and duplicate notifications on redelivery. Test relay crash, duplicates and delayed consumers |
| Reliable request/reply | Merchant durably accepts an order then uses idempotent CreateBooking and GetBookingByExternalOrder | A lost RPC reply is an unknown outcome, so reconciliation precedes retry; no cross-service ACID transaction is assumed |
| State machine / optimistic concurrency | Canonical transition matrix plus expectedVersion and current assignment guard | Reject stale/foreign Courier updates and invalid repeats with no side effects; Delivered requires confirmed proof under the stronger team policy |

## Layers and implementation practice

Presentation (React/Flutter and API adapters) calls application commands/queries; domain pricing/state/ownership rules define valid behavior; infrastructure adapters handle each owner's EF database, private object storage, broker and external calls. YARP routes and applies coarse limits, while services retain domain authorization. This is the chosen microservice style; the PDF also permits other justified architectures.

Use narrow meaningful exception categories translated centrally to safe ProblemDetails/GraphQL/gRPC codes. Persist/retry unknown distributed outcomes rather than pretending errors undo remote commits. Inject environment configuration and mounted secrets, validate startup settings and redact credentials/PII from errors/logs. Do not hard-code live credentials or silently reimplement rules per client.

## Evidence to attach during implementation

Record actual source commit/PR links for a shared quote handler/pricing strategy, ownership/state guard, repository/transaction boundary, outbox relay and mock-SMS consumer. Link executed unit/protocol-equivalence/event/failure tests in [test results](../testing/test-results.md). Until those exist, patterns describe the design only. Related canonical documents: [technical design](technical-design.md), [data architecture](data-architecture.md), [state machine](parcel-state-machine.md) and [integration design](../integration/integration-design.md).
