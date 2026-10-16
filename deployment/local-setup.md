# Local Setup: Web and Backend

> Status: Shared Docker Compose scaffold is runnable without Neon · Feature acceptance remains separate

## Repositories and prerequisites

The docs, infra, backend, frontend, and mobile repositories remain separate.
For the shared web/backend environment, keep `swiftdrop-infra`,
`swiftdrop-backend`, and `swiftdrop-frontend` as sibling directories. Install
Docker Engine/Desktop with Compose and start the daemon. Developers working on
backend code should also install the .NET 10 SDK pinned by the backend
`global.json`; frontend contributors should use the Node/npm versions pinned
by its `.nvmrc` and `package.json`. Mobile is outside this setup.

## Choose a development mode

For quick iteration, developers may run the hosts directly. Docker Compose is
the shared container/network verification path. Both are selected through the
infra runner.

## Per-developer configuration

The default shared scaffold can start with sample configuration and does not
require any Neon credentials. Each developer can run the runner once to create
the ignored local environment file automatically, or copy it explicitly:

```sh
cp development/.env.example development/.env
chmod 600 development/.env
```

Neon credentials are needed only to work on database-backed features, not to
start the shared stack. For Identity feature development, configure
`IDENTITY_DATABASE_CONNECTION_STRING` using the provisioned runtime
`identity_app` role and `IDENTITY_MIGRATION_CONNECTION_STRING` using a separate
`identity_migrator` login; keep TLS required and do not give DDL rights to the
runtime role. If the migration role does not exist yet, a Neon database owner
can create it while connected to `swiftdrop_identity`:

```sql
CREATE ROLE identity_migrator LOGIN;
GRANT CONNECT ON DATABASE swiftdrop_identity TO identity_migrator;
GRANT USAGE, CREATE ON SCHEMA public TO identity_migrator;
GRANT USAGE ON SCHEMA public TO identity_app;
```

Set the role password through Neon’s role controls and store it only in the
local environment file; never put it in SQL history, commit it, or share it.
The Identity migration grants the required DML permissions to `identity_app`.
Do not copy another developer's populated `.env`, commit it, paste connection
strings into tickets/chat, or print rendered Compose configuration. The runner
creates a local RabbitMQ password on first use. Other DB entries are reserved
for their service adapters.

### Host mode

Install the pinned .NET SDK, Node/npm, run `npm ci` once in
`swiftdrop-frontend`, populate the local environment file, then from
`swiftdrop-infra`:

```sh
./development/run.sh up --mode host
```

The runner starts five backend processes and Vite on their documented
loopback addresses; press Ctrl-C to stop them. It does not start RabbitMQ
because application services do not yet use the broker. When a valid Identity
migration connection is configured, the runner applies that migration before
starting; otherwise it skips migrations and still starts the scaffold.

### Docker mode

Start Docker Engine/Desktop and run from `swiftdrop-infra`:

```sh
./development/run.sh up --mode docker --build
```

This builds and starts Gateway, Identity, Delivery, Merchant, Notification
Worker, web, and local RabbitMQ as separate containers without requiring Neon.
Identity `/health` confirms process liveness; its database `/ready` endpoint is
separate and requires a configured connection and applied migration. Open
`http://localhost:5173`; Gateway is at `http://localhost:5000`.

Confirm the baseline without displaying any environment values:

```sh
./development/run.sh ps
curl --fail http://localhost:5000/health
curl --fail http://localhost:5173/
```

Use the runner for rebuilds, logs, status, and shutdown:

```sh
./development/run.sh up --mode docker
./development/run.sh up --mode docker --build delivery-service
./development/run.sh logs gateway
./development/run.sh ps
./development/run.sh down
```

Developers can use host mode for normal coding, but Docker build/start is
required before a change affecting an app or container setup can be considered
verified for merge. Run the full Docker command above and confirm Gateway/web
health, or get the same result from CI/a Docker-enabled teammate. Record the
result. Host mode alone does not check image builds, Compose networking, or
container listeners.

Neon PostgreSQL remains external and optional for this scaffold-startup
milestone. Identity's registration and migration code are present but are not
required by the default run command; use real runtime and migration credentials
before exercising DB-backed registration. Delivery, Merchant, and
Notifications have no DB adapters yet. RabbitMQ is included, but application
services do not yet connect to it. MinIO is deferred until Delivery's
proof-storage adapter is implemented.

## Current limitations

The immediate outcome is a common runnable process baseline, not a completed
product feature. Login/token issuance, authenticated profile routes,
Delivery/Merchant product features, and broker/object-store flows remain future
work. `/health` is process liveness; Identity `/ready` is its separate
database-backed readiness check. Do not infer feature readiness from the
scaffold health checks.

## Flutter Customer and Courier

Mobile development is tracked separately and is not required to start this
web/backend Compose environment. When mobile source is ready:

1. Install Flutter and verify with `flutter doctor -v`, `flutter devices`.
   Android minimum API level is **26** (SRS NFR-20).
2. Configure both Customer and Courier flows, Google clients, and the
   configured API base URL. Prefer `adb reverse tcp:5000 tcp:5000` for local
   emulator access; physical devices require a trusted TLS ingress.
3. Keep build-time API URLs/client IDs as public configuration, store refresh
   tokens in platform secure storage, and never commit local credentials.

## Onboarding acceptance

A clean-checkout startup is only the first gate. The team still needs evidence
for customer booking/tracking, courier assignment/status/proof, merchant
orders/webhooks, notifications, authorization negatives, and its branch/PR
review workflow. Attach commands, source commits, sanitized logs, and
[test results](../testing/test-results.md); do not claim a feature passes before
it is implemented and exercised.

See the [Milestone 1 feature and role-based work packages](../project-management/development-milestone-1.md)
to self-assign the remaining service work.
