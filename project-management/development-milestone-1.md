# Development Milestone 1: Shared Runnable Scaffold

## Goal

Every developer can start the common service processes from a clean checkout
using the shared runner and sample local configuration. This is a runtime
scaffold gate, not a claim that product features or database integrations are
complete.

## Feature code present, not a startup prerequisite: Customer registration

Identity has initial code for the existing [Register API contract](../api/rest-api.md):

- `POST /api/v1/auth/register`
- Input: `email` (valid, at most 254 characters), `password` (12–128
  characters), and `fullName` (1–120 characters).
- Success: `201` and a Profile containing `id`, trimmed `email`,
  `fullName`, nullable `phoneNumber`/`address`, `roles`, and `isActive`.
- The service assigns only the `Customer` role. It hashes passwords with
  Argon2id (64 MiB, 3 iterations, single lane; benchmark before release),
  writes user, role assignment, and audit row in one transaction,
  and does not return or log the password/hash.
- Duplicate normalized email returns a generic `409 registration_conflict`.
- Requests are limited to five registrations per minute per source IP.
- Identity owns the schema in `swiftdrop_identity`. A one-shot migration runs
  only when a developer opts into DB-backed Identity work. Migrations use a
  separate `identity_migrator` credential; the running API uses the more
  restricted `identity_app` login. Neither Neon credential is required for
  scaffold startup.

This code is not part of the basic startup acceptance gate. Without configured
Neon credentials and an applied migration, registration explicitly responds
with service unavailable. Login/token issuance, Google sign-in, sessions,
profile editing, and the React registration form are not included.

## Work allocation

No developer names or handles are recorded in the project material, so work is
listed by service/role and remains available for the team to self-assign. Record
the selected owner, reviewer, issue/PR, and date in the team's contribution
log before starting parallel implementation; do not infer a person from a role.

| Work package | Suggested owner | State | Done when |
|---|---|---|---|
| Common Compose/host scaffold startup and health checks | Infrastructure owner | Implemented; verify at runtime | One command starts all processes/containers with sample configuration; Gateway/web and each service's process health pass without Neon |
| Identity registration route, Identity schema/migration, persistence, and focused tests | Identity service owner | Code/tests implemented; separate feature gate | When a developer opts into DB-backed Identity work, the migration applies and registration persists; duplicate and invalid-input cases pass |
| Per-developer Neon/RabbitMQ configuration and Compose acceptance | Infrastructure owner | Optional feature setup documented | Each developer can start without secrets; database credentials are added only for the database-backed service they work on |
| Identity login, access/refresh tokens, Google login/linking, and profile operations | Identity/security owners | Unassigned | Implement only against the existing REST and security contracts, with negative tests |
| Quote and parcel booking, idempotency, history, and outbox in `swiftdrop_delivery` | Delivery owner | Unassigned | Migration, ownership checks, atomic write/idempotency tests, and documented gateway calls pass |
| Merchant registration, approval, keys, and durable order inbox in `swiftdrop_merchant` | Merchant owner | Unassigned | Service-owned migration/data access and approval/duplicate tests pass |
| Notification inbox, job deduplication, and provider-attempt persistence in `swiftdrop_notifications` | Notifications owner | Unassigned | Migration and duplicate-event tests pass; broker consumer acknowledges only after durable commit |
| Customer registration UI and end-to-end checks | Web/QA owners | Unassigned | UI calls the gateway contract and reports validation/conflict responses without exposing credentials |

The table suggests ownership boundaries, not named assignments or completed
work. The contracts in the docs remain the source of truth. A service owner
must update the API contract and obtain the required review before making a
behavioral change.

## Shared developer workflow

1. Clone docs, infra, backend, and frontend as siblings and install the pinned
   .NET and Node/npm toolchains.
2. Create `swiftdrop-infra/development/.env` from `.env.example`; set file
   permissions to `600`; obtain that developer's service-role credentials
   privately. Never copy another developer's populated file.
3. Use `./development/run.sh up --mode host` for iteration or
   `./development/run.sh up --mode docker --build` for the shared container
   path.
4. Before merge, run the focused tests and Docker build/start. Confirm each
   service's `/health`, Gateway `/health`, and the web page. This baseline does
   not require Identity `/ready` or Neon. Record sanitized results; do not print
   Compose's rendered environment.
5. A feature is not complete merely because its process is healthy. Include
   its own migration, data-access tests, service contract tests, and relevant
   end-to-end behavior.
