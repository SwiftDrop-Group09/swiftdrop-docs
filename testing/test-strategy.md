# Test Strategy

> Status: Proposed strategy · No implementation suites executed in this docs repository

The [68-case catalog](test-cases.md) covers all 52 requirements and 16 additional security/recovery scenarios. Distinguish **Drafted → Implemented → Executed → Passing → Evidence attached**; failed, skipped and blocked executions remain explicit. Documentation/schema/render checks are recorded separately in [documentation validation](documentation-validation.md) and cannot establish business test coverage.

## Layers and fixtures

Unit tests: deterministic pricing/rounding/expiry, canonical transitions, ownership predicates, idempotency fingerprints and HMAC bytes/tolerance. Integration tests: actual owning API plus PostgreSQL, RabbitMQ and private storage using Testcontainers; compile actual protobuf and GraphQL against design fixtures. Web E2E: React five-role flows/public tracking at mobile width; Flutter integration: Customer and Courier, API 26+ emulator/device, Google SDK cancel and network reconnect. Use a controllable Google test issuer only in test fixtures; live SDK/device sign-in remains a separately recorded manual check.

## Required failure assertions

Use concurrency barriers for same-key requests and reassign/pickup races. Fault-inject broker outage and relay crash after confirm; assert committed outbox eventually delivers one logical effect. Drop gRPC response after Delivery commit; assert Merchant reconciles existing parcel under the same externalOrderId even after API-key rotation. Deliver duplicate/out-of-order events; assert one notification/channel/subscription job and no status regression. Fail object write and DB commit independently; assert no false Delivered and safe orphan cleanup. Advance fake clock for exact six webhook attempts, 429 Retry-After, fresh HMAC and inspectable terminal failure.

Security gates include anonymous REST/GraphQL field absence, foreign merchant job/attempt access, courier A→B proof/status denial, wrong-role write denial, phone ownership spoofing, Google email collision linking, JWT role/deactivation expiry bound, immediate key revocation, unsafe webhook DNS/IP/redirect rejection and private proof/receipt streaming. Assert both response and **absence of DB/outbox/storage side effects**. Never weaken SSRF validation to test a local receiver: use injected transports or a controlled public test endpoint.

## Reporting

Pin fixture/image/tool versions, seed deterministic tariffs and data, record source commit and UTC execution timestamps. Publish xUnit/TRX/JUnit plus Cobertura coverage and browser/mobile artifacts with sanitized logs. Measure NFR timing targets under declared load/hardware; 50 concurrent users is a test target. [Coverage denominator](coverage-summary.md) excludes no business layer merely to raise results. Runtime evidence remains pending until actual source suites run. QA/SEC/domain roles review negative/recovery results before design approval and submission.


## Assignment notification acceptance

[Assignment pages 2–3](../requirements/sources/ead-group-assignment.pdf#page=2) require an event-consuming email service or mock SMS service. The proposed mandatory demo uses **mock SMS** with an observable provider attempt/output triggered by StatusChanged, plus persisted in-app records. Email may be added; a mock-email-only path or an in-app status screen alone does not establish this requirement. TC-N15/TC-REC-03/04 must execute the actual consumer/event path; all are still drafted, not passing.
