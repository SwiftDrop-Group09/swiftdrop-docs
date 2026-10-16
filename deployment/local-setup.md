# Local Setup: Web, Backend and Flutter

> Status: Proposed onboarding guide · No application source or tested build supplied here

## Repository and toolchain

This repository contains documentation, design contracts and infrastructure reference files only. The organization lists `swiftdrop-backend`, `swiftdrop-frontend`, `swiftdrop-mobile` and `swiftdrop-infra`; OPS must verify access, actual paths/commands and commit links before onboarding is considered tested. There is no assumed swiftdrop-platform monorepo. Obtain the .NET/Node/Flutter versions from each source repository's lock/config files, then record tested versions. Install Git, Docker Engine/Desktop with Compose, an Android SDK/emulator, Java required by the mobile project and Flutter; run `flutter doctor -v` and `flutter devices`.

## Infrastructure and backend

1. Follow [Compose preparation](docker-compose.md), populate ignored `deployment/.env` with unique local-only secrets, and validate `config --quiet`.
2. Start default infrastructure profile; verify DB bootstrap, broker users, object bucket policy and health. Four DBs share `postgres:5432` with separate app credentials.
3. In the backend source repository, restore/build, apply **each** Identity/Delivery/Merchant/Notifications migration, and seed roles, a local Admin, zones, pricing and fictional fixtures. Exact project paths and commands require code links; no solution file exists here.
4. Provision Identity JWT signing keys, Merchant AEAD key and service JWT credentials through ignored mounted files. Configure trusted issuer/audience/JWKS and workload scopes. Do not reuse sample credentials beyond the local demo.
5. Configure YARP routes and trusted origins from [environment matrix](environments.md); ensure internal routes are unreachable publicly. Build/tag real application images and enable the reference application profile only once the image/migration contract is satisfied.

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
