# Local Setup: Web and Backend

> Status: Docker Compose development workflow defined · Runtime verification pending

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

### Host mode

Install the pinned .NET SDK, Node/npm, run `npm ci` once in
`swiftdrop-frontend`, then from `swiftdrop-infra`:

```sh
./development/run.sh up --mode host
```

This runs five backend processes and the Vite frontend on the documented
loopback addresses; press Ctrl-C to stop them. It does not start RabbitMQ
because the current scaffold has no broker adapter.

### Docker mode

Start Docker Engine/Desktop and run from `swiftdrop-infra`:

```sh
./development/run.sh up --mode docker --build
```

This builds and starts Gateway, Identity, Delivery, Merchant, Notification
Worker, web, and local RabbitMQ as separate containers. The script creates an
ignored `development/.env` with a generated local RabbitMQ password on first
use. Open `http://localhost:5173`; Gateway is at `http://localhost:5000`.

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

Neon PostgreSQL remains external. Its per-service strings in
`development/.env.example` are placeholders and are not consumed by the
current backend scaffold. RabbitMQ is included as the selected broker, but
backend services do not yet connect to it. MinIO is deferred until Delivery's
proof-storage adapter is implemented. Do not treat these configuration entries
or dependency containers as completed service integrations.

## Current limitations

The containers currently demonstrate process startup and Gateway routing only.
Product handlers, authentication, database/broker/object-store adapters,
migrations, dependency-aware readiness, and notification/webhook flows still
need implementation and testing. Feature API routes currently return `404`;
`/health` confirms process liveness only. Docker image build and clean-checkout
runtime acceptance remain pending on a Docker-enabled machine.

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
