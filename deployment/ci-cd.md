# CI/CD and Release Evidence

> Status: Proposed pipeline design · No application workflow execution evidenced here

Documentation validation uses the versioned [validation scripts](../scripts/README.md) to check relative links/anchors, requirement/test/route consistency, JSON Schema, GraphQL/protobuf and diagram renders. Generated output must match editable sources; generated PDF requires visual review. [Recorded documentation results](../testing/documentation-validation.md) are separate from runtime CI evidence.

Application repositories should run locked dependency restore, compile/lint, business-logic unit tests with Coverlet/Cobertura, Testcontainers API/PostgreSQL/RabbitMQ/object-store integration and negative authorization tests, web E2E and Flutter tests. Upload dated reports with commit, toolchain and run URL, marking failed/skipped scenarios distinctly. Unit line target is ≥80% of defined business logic; branch coverage is separately reported. No undefined integration percentage is used.

Build/publish application images only after tests pass; keep deployment behind configured environment secrets and deliberate release authorization. This change does not publish images or deploy. A release candidate requires four DB migration/readiness checks, mandatory workflow demos and recovered broker/merchant failures. Optional Kubernetes/AI jobs do not block or masquerade as mandatory success. Preserve logs with credentials/body payloads redacted; see [coverage](../testing/coverage-summary.md) and [submission checklist](../submission/submission-checklist.md).
