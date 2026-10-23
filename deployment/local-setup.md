# Local Setup: Web, Backend and Flutter

> Status: Proposed onboarding guide · No application source or tested build supplied here

## Repository and toolchain

This repository contains documentation and design contracts. The sibling repositories `swiftdrop-backend`, `swiftdrop-frontend`, `swiftdrop-mobile` and `swiftdrop-infra` own implementation and pinned toolchains; the [infrastructure runner](docker-compose.md) is the runnable shared-development source. Neon PostgreSQL is the user-selected database host. There is no assumed swiftdrop-platform monorepo. Install the **.NET 10 SDK** for backend work and verify a 10.x SDK with `dotnet --list-sdks`; API/gateway/Worker projects target `net10.0` and ASP.NET Core 10. Pin the tested 10.x patch/feature band in the backend repository's `global.json`. Obtain Node/Flutter versions and backend dependency pins from the owning source repositories' lock/config files, then record tested versions. Install Git, Docker Engine/Desktop with Compose, an Android SDK/emulator, Java required by the mobile project and Flutter; run `flutter doctor -v` and `flutter devices`.

## Infrastructure and backend

1. Keep the infra/backend/frontend repositories as siblings and follow the [canonical runner](docker-compose.md). Configure the six [secret names](environments.md#secrets) privately in ignored `swiftdrop-infra/development/.env`; no secret values belong in Git.
2. Start Docker mode with `./development/run.sh up --mode docker --build` from the infra repository. Verify Gateway/web process health and local RabbitMQ. There is no local PostgreSQL bootstrap or MinIO requirement for this scaffold; databases are provisioned in Neon.
3. For database-backed work, provision the service-owned database/role and apply that service's implemented explicit migration. Identity has a separate migration secret; Delivery reuses its Delivery connection string for its one-shot task. Merchant/Notifications migration implementations are pending. See the owning infra/backend READMEs for current commands. No shared Neon migration/reset is part of these documentation edits.
4. Backend code targets the pinned .NET 10 SDK. `dotnet restore SwiftDrop.sln`, `dotnet build SwiftDrop.sln --configuration Release` and focused service tests run from `swiftdrop-backend`; isolated PostgreSQL integration tests do not use the shared Neon databases. Delivery Phase 1 supplies persistence only, with no booking HTTP handler or outbox relay. No operational tariff is supplied by the documentation examples.
5. Before authenticated product flows are implemented, provision JWT signing/verification, workload scopes and trusted origins according to the security design. Those future credentials/adapters are not provisioned by this six-secret development contract. Private proof storage remains later scope. Follow [environment matrix](environments.md); internal routes must remain private.

## React

Use the frontend repository's package manager/lockfile and documented install/dev command. Set its public API base to `http://localhost:5000` for loopback, not a container DNS address. Set allowed web origin `http://localhost:5173`; refresh-cookie/CSRF policy must match. React supports all five roles and a safe public tracking page at mobile width. Customer receipt, Merchant dashboard and Admin reports are mandatory UI demo entries.

## Flutter Customer and Courier

1. Obtain the actual mobile source and run `flutter pub get`, `flutter doctor -v`, `flutter devices`. Android minimum API level is **26** (SRS NFR-20); configure build SDK/Gradle according to the project's pinned toolchain. Do not guess compatible versions.
2. Configure **both personas** in the same agreed mobile deliverable: Customer quote/confirm/tracking/history/receipt; Courier assigned manifest/status/failure/proof. Camera/photo permission must be limited to proof capture; continuous GPS is deferred.
3. Create configured Google web/server and Android clients. Register the Android application/package ID and debug/release signing fingerprints from the mobile project; add allowed web origins and SDK configuration. Both client flows submit Google SDK ID token to GoogleLogin; there is no SwiftDrop backend code callback. If SDK uses browser redirects/deep links, register the exact SDK-generated scheme/URI in Android manifest and Google config, test cold-start/cancel handling and record values in ignored environment config. No invented redirect URL is required by the ID-token backend contract.
4. Prefer `adb reverse tcp:5000 tcp:5000` and API_BASE_URL `http://localhost:5000` in an isolated debug build; any cleartext exception is debug-only. Emulator `10.0.2.2` refers to host, not Android localhost, and requires a reachable TLS ingress if used outside loopback. Physical device/LAN uses a device-trusted TLS ingress and configured base URL; do not expose unauthenticated plain HTTP listeners broadly.
5. Once source exists, start with `flutter run --dart-define=API_BASE_URL=<configured-base>` if supported by that project's bootstrap. Provide the actual entrypoint/build command in its README. Public compile-time URLs/client IDs are not credentials; store refresh tokens in platform secure storage.
6. Provision fictional Customer and Courier accounts locally; an Admin grants Courier membership. Record account labels only, distribute generated local passwords privately and never commit them. Verify no client can self-assign roles or access another courier's parcel.

## Onboarding acceptance

A new member must demonstrate local signup and Google login; Customer quote/decline/requote/confirm; mobile-safe public tracking; own history/receipt; Dispatcher assignment; Flutter Courier statuses and proof; notifications and merchant webhook; Merchant job/dashboard; Admin delivery report. Attach source commits, commands, device/emulator/API level, logs/screenshots and [test results](../testing/test-results.md). Until that evidence exists, this guide is a proposed checklist rather than a claim that the entire system starts successfully.
