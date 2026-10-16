# Local Setup: Web, Backend and Flutter

> Status: Local development workflow documented · Runtime verification pending

## Repository and toolchain

This repository contains project documentation and the reference deployment model. The source repositories are `swiftdrop-backend`, `swiftdrop-frontend`, `swiftdrop-mobile` and `swiftdrop-infra`; they remain separate Git repositories, not a monorepo. The infrastructure repository contains the shared local dependency Compose setup. Its Docker startup and the backend/mobile toolchains still need verification on a developer machine. Install the **.NET 10 SDK** pinned by the backend `global.json` and the Node/npm versions specified by the frontend `.nvmrc` and `package.json`. Install Git, Docker Engine/Desktop with Compose, and the frontend dependencies. Mobile tooling is out of scope for this local web/backend setup.

## Infrastructure and backend

1. In `swiftdrop-infra`, copy `.env.example` to ignored `.env`, replace every empty password with a distinct local-only value, and validate with `docker compose --env-file .env config --quiet`. See its [local infrastructure guide](https://github.com/SwiftDrop-Group09/swiftdrop-infra) for exact commands and port mappings.
2. Start the infrastructure Compose stack and verify RabbitMQ and object-store health/bootstrap. PostgreSQL is managed by Neon and is not a local container. Replace the four per-service TLS connection string examples only after creating the corresponding Neon databases and roles.
3. In `swiftdrop-backend`, run the documented restore/build/test commands, then start the five local hosts from the backend README. The scaffold currently has liveness and Gateway routing only: it has no database/broker/object-store adapters, migrations, seeds, authentication or feature handlers. Do not treat configured Neon values or provisioned dependencies as backend integration.
4. Run the frontend development server as described below. Vite proxies `/api` and `/graphql` to the Gateway at `http://localhost:5000`; unimplemented feature routes currently return `404`.
5. The infrastructure repository now contains backend/frontend image build definitions and an application Compose overlay. Treat it as an early container baseline: image build and runtime smoke tests still need a Docker-enabled host, while migrations, implemented secret-backed authentication and dependency-aware readiness remain future work. Follow the infra README for the exact sibling-repository commands; the docs repository's reference Compose is not the runnable overlay.

## React

Use the frontend repository's documented Node/npm versions and package lockfile:

```sh
npm ci
cp .env.example .env.local
npm run dev
```

The development proxy targets `http://localhost:5000` by default and can be changed with `DEV_GATEWAY_TARGET`; browser calls should use same-origin `/api` or `/graphql`, not container DNS names. The starter has no product screens or API calls yet.

## Flutter Customer and Courier

1. Obtain the actual mobile source and run `flutter pub get`, `flutter doctor -v`, `flutter devices`. Android minimum API level is **26** (SRS NFR-20); configure build SDK/Gradle according to the project's pinned toolchain. Do not guess compatible versions.
2. Configure **both personas** in the same agreed mobile deliverable: Customer quote/confirm/tracking/history/receipt; Courier assigned manifest/status/failure/proof. Camera/photo permission must be limited to proof capture; continuous GPS is deferred.
3. Create configured Google web/server and Android clients. Register the Android application/package ID and debug/release signing fingerprints from the mobile project; add allowed web origins and SDK configuration. Both client flows submit Google SDK ID token to GoogleLogin; there is no SwiftDrop backend code callback. If SDK uses browser redirects/deep links, register the exact SDK-generated scheme/URI in Android manifest and Google config, test cold-start/cancel handling and record values in ignored environment config. No invented redirect URL is required by the ID-token backend contract.
4. Prefer `adb reverse tcp:5000 tcp:5000` and API_BASE_URL `http://localhost:5000` in an isolated debug build; any cleartext exception is debug-only. Emulator `10.0.2.2` refers to host, not Android localhost, and requires a reachable TLS ingress if used outside loopback. Physical device/LAN uses a device-trusted TLS ingress and configured base URL; do not expose unauthenticated plain HTTP listeners broadly.
5. Once source exists, start with `flutter run --dart-define=API_BASE_URL=<configured-base>` if supported by that project's bootstrap. Provide the actual entrypoint/build command in its README. Public compile-time URLs/client IDs are not credentials; store refresh tokens in platform secure storage.
6. Provision fictional Customer and Courier accounts locally; an Admin grants Courier membership. Record account labels only, distribute generated local passwords privately and never commit them. Verify no client can self-assign roles or access another courier's parcel.

## Onboarding acceptance

A new member must demonstrate local signup and Google login; Customer quote/decline/requote/confirm; mobile-safe public tracking; own history/receipt; Dispatcher assignment; Flutter Courier statuses and proof; notifications and merchant webhook; Merchant job/dashboard; Admin delivery report. Attach source commits, commands, device/emulator/API level, logs/screenshots and [test results](../testing/test-results.md). Until that evidence exists, this guide is a proposed checklist rather than a claim that the entire system starts successfully.
