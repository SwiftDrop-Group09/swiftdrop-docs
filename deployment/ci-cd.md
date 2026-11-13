# CI/CD and Release Evidence

> Status: Proposed pipeline design · No application workflow execution evidenced here

Documentation validation uses the versioned [validation scripts](../scripts/README.md) to check relative links/anchors, requirement/test/route consistency, JSON Schema, GraphQL/protobuf and diagram renders. Generated output must match editable sources; generated PDF requires visual review. [Recorded documentation results](../testing/documentation-validation.md) are separate from runtime CI evidence.

Backend CI must use the **.NET 10 SDK** and restore/build/test projects targeting `net10.0`; align runtime images with ASP.NET Core 10 and pin the tested 10.x SDK patch/feature band in the owning backend `global.json`. Application repositories should run locked dependency restore, compile/lint, business-logic unit tests with Coverlet/Cobertura, Testcontainers API/PostgreSQL/RabbitMQ/object-store integration and negative authorization tests, web E2E and Flutter tests. Upload dated reports with commit, toolchain and run URL, marking failed/skipped scenarios distinctly. Unit line target is ≥80% of defined business logic; branch coverage is separately reported. No undefined integration percentage is used.

Build/publish application images only after tests pass; keep deployment behind configured environment secrets and deliberate release authorization.

## Implemented Workflows & Branching

- **Branching**: `dev` is the default integration branch (`pull_request` + `push` CI checks); `main` is the production branch; feature work uses `feat/<scope>-<desc>`, `fix/<scope>-<desc>`, `infra/<scope>-<desc>`, and `chore/<scope>-<desc>`.
- **`swiftdrop-backend/.github/workflows/backend-ci.yml`**: Runs `.NET 10` restore, build, test, foundation verification, and PR Docker build validation (`docker-validate`).
- **`swiftdrop-backend/.github/workflows/backend-images.yml`**: On `push` to `main`, builds multi-arch (`linux/amd64,linux/arm64`) images for all 5 services, pushes immutable `sha-<short>` and `latest` tags to GHCR, and runs Trivy (`CRITICAL,HIGH`) vulnerability scans.
- **`swiftdrop-infra/.github/workflows/infra-ci.yml`**: Validates Docker Compose config and renders/schema-checks (`kubeconform`) `k8s/overlays/{dev,staging,prod}`.
- **`swiftdrop-infra/.github/workflows/infra-cd.yml`**: Manual `workflow_dispatch` selecting `staging` or `production` and an immutable `sha-*` image tag, applying Kustomize manifests to K3s, verifying `kubectl rollout status`, and checking Gateway `/health`.
- **`swiftdrop-frontend/.github/workflows/ci.yml`**: Runs Prettier, ESLint, TypeScript, Vitest, and Vite SPA build; Vercel handles PR previews and `main` production deployments.

Preserve logs with credentials/body payloads redacted; see [coverage](../testing/coverage-summary.md) and [submission checklist](../submission/submission-checklist.md).
