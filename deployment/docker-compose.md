# Shared Development Deployment

> Neon and secret names confirmed by the user on 23 October 2026 · Full product deployment evidence remains pending

The canonical runnable stack is owned by **swiftdrop-infra**, not this documentation repository: [development README](https://github.com/SwiftDrop-Group09/swiftdrop-infra/blob/main/README.md), [Compose](https://github.com/SwiftDrop-Group09/swiftdrop-infra/blob/main/development/compose.yaml), [runner](https://github.com/SwiftDrop-Group09/swiftdrop-infra/blob/main/development/run.sh), and [environment template](https://github.com/SwiftDrop-Group09/swiftdrop-infra/blob/main/development/.env.example). It builds sibling backend/frontend repositories and runs Gateway, Identity, Delivery, Merchant, Notification Worker, web and RabbitMQ. Neon PostgreSQL is external; no local PostgreSQL or database bootstrap container is part of the shared stack. MinIO is deferred until proof storage is implemented.

The former docs-only `deployment/compose.yaml`, local PostgreSQL initializer, broker bootstrap and object-store bootstrap have been removed because they described an incompatible proposal with extra password names and placeholder application images. Git history retains that superseded reference. The [six-key secret template](.env.example) documents names only; configure actual values privately in ignored `swiftdrop-infra/development/.env`.

## Start and validate

Keep `swiftdrop-infra`, `swiftdrop-backend` and `swiftdrop-frontend` as siblings. Run these commands in the infrastructure repository using its supported shell:

```sh
./development/run.sh up --mode docker --build
./development/run.sh ps
curl --fail http://localhost:5000/health
curl --fail http://localhost:5173/
```

The runner initializes an ignored configuration on first use and generates a local RabbitMQ password without overwriting an existing file. Scaffold process liveness can run without Neon credentials; database-dependent features require provisioned service databases, credentials and migrations. Use [the environment matrix](environments.md) for ports and exact configuration ownership. Do not print rendered Compose configuration containing real secrets.

For host development use `./development/run.sh up --mode host` with the pinned .NET/Node dependencies from the owning repositories. Both modes forward each service's own database connection string. Host mode does not start RabbitMQ. Docker mode remains the required shared acceptance check.

## Migrations and acceptance

Provision Neon databases/roles before migration; the runner does not create them. Identity's opt-in migration uses `IDENTITY_MIGRATION_CONNECTION_STRING`. Delivery has an explicit one-shot `--migrate` task using `DELIVERY_DATABASE_CONNECTION_STRING`; its privileges must be checked before running it. There is no additional Delivery migration secret. Merchant/Notifications migrations and broker publishers/consumers remain future implementation work. Ordinary API startup never performs automatic schema changes.

Run explicit migrations from the infrastructure repository; normal `up` in either mode performs no DDL:

```sh
./development/run.sh migrate --mode host identity-service
./development/run.sh migrate --mode host delivery-service
# Use --mode docker for the equivalent container one-shot tasks.
```

Run each service's implemented migration once and verify database-backed readiness separately from `/health`. Product acceptance still requires quote/confirm, authorization, clients, outbox recovery, notifications, Merchant recovery/webhook signing and private proofs after those features exist. No full-system startup or Neon privilege verification is claimed here. The assignment's literal database-container requirement still needs lecturer/project-lead reconciliation with the user's Neon choice; this does not change that choice or claim lecturer approval.

Use `./development/run.sh logs <service>` for bounded diagnostics and `./development/run.sh down` to stop the stack while retaining broker data. Backups, restore and clean-machine runtime checks remain acceptance evidence, not documentation validation.
