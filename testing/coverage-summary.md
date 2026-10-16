# Coverage Targets and Results

> Status: Target definition only · Actual application coverage **not measured**

SRS NFR-17 target: **≥80% unit-test line coverage of hand-written business logic**. Denominator includes executable lines in domain models/rules, pricing, authorization/resource predicates, application handlers, idempotency/outbox orchestration and retry policy code across Identity/Delivery/Merchant/Worker. Exclude generated protobuf/schema clients, generated EF migrations, framework/vendor code and test fixtures; do not exclude hand-written validators/handlers/adapters solely because they are difficult to test. Publish each exclusion and service breakdown.

Report branch coverage separately with its covered/total branches; no branch percentage is silently substituted for line coverage. Aggregate totals from covered/coverable lines, not arithmetic means of service percentages. No undefined “60% integration coverage” target remains: integration completeness is the count of passing required scenarios with artifacts, plus separately labeled optional code coverage if collected.

Planned tooling: xUnit and Coverlet collection into Cobertura with ReportGenerator HTML; actual commands/project paths must come from backend source. Store CI run URL, commit, timestamp, coverage artifact, raw counts and exclusions in [test results](test-results.md). Current measured lines/branches/percentages: **unknown**. Drafted cases: **68**; implemented, executed and passing counts: **not evidenced**. [Traceability](../requirements/requirements-traceability.md) has 52 mapped requirements, which is design mapping, not test execution coverage.
