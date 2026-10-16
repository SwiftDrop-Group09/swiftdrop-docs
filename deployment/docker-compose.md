# Docker Compose Reference

> Status: Proposed reference configuration · Not a verified full-system deployment

[compose.yaml](compose.yaml) is the documentation reference for RabbitMQ, private object storage and the optional application profile. The infrastructure repository contains the runnable dependency stack and app overlay, including backend/frontend build contexts. PostgreSQL is provisioned in Neon, outside local Compose, with four private databases and per-service credentials. This is a deployment choice that differs from the assignment's literal database-container requirement; see the assignment overview and confirm acceptance with the lecturer. Redis and a separate realtime hub are absent.

## Prepare and validate

Run from the documentation repository root. Copy [environment template](.env.example) to ignored `deployment/.env`, replace the Neon connection-string examples when the databases/roles exist, generate distinct local passwords, and select tested/pinned image versions. The latest object-store tags in the template are unresolved placeholders to pin before release, not a tested compatibility claim. Never use REPLACE_LOCAL_ONLY as a password.

```powershell
Copy-Item deployment/.env.example deployment/.env
docker compose --env-file deployment/.env -f deployment/compose.yaml config --quiet
docker compose --env-file deployment/.env -f deployment/compose.yaml up -d
docker compose --env-file deployment/.env -f deployment/compose.yaml ps -a
```

Default profile starts local RabbitMQ and object storage/bootstrap only; Neon databases and owner roles must be created separately. Each future API/Worker owns its EF migrations and receives only its own Neon connection string; do not connect Worker to Merchant/Delivery DB. This local Compose topology does not containerize PostgreSQL.

Rabbit bootstrap creates delivery_bus and worker_bus scoped users, with explicit per-type/receive entity permissions; topology declaration is performed by MassTransit consumers at startup. Broker binding permissions must be verified against the pinned MassTransit version in the runtime smoke test. Object bootstrap creates a private bucket and Delivery-only policy/account; app credentials are not root/admin credentials. Verify selected object images contain the configured health tools.

## Application profile

The infrastructure application overlay builds the three APIs, YARP gateway and Worker using the backend's multi-stage **.NET 10 SDK / ASP.NET Core 10** Dockerfile and builds the web image from the frontend repository. SDK/runtime image patches and dependency image versions are still unpinned; verify and pin them before release.

Use the exact sibling-repository commands in the infra README. The current backend remains a scaffold: no DB/broker/object-store adapters or migrations, application credentials, or feature handlers are implemented. Neon environment values are configuration placeholders and are not consumed by current service code. Health checks are liveness-only; a passing container does not prove dependency or feature readiness.

YARP routes only catalogued public prefixes to the correct API, `/graphql` and SSE to Delivery, and JWKS to Identity. Block `/internal/*`. Non-loopback clients require configured TLS ingress; domain services still validate JWTs. SSE buffering/timeouts must support heartbeats. Merchant's egress network must be constrained with outbound DNS/IP controls; a Compose network alone does not implement SSRF policy.

The application profile is an early implementation baseline, not a verified end-to-end deployment. After SDK-enabled builds and runtime smoke tests pass, validate the four Neon DB migrations/readiness, quote-confirm, Flutter Customer/Courier, outbox outage recovery, notification, Merchant job reconciliation and webhook signing as their implementations become available. Record logs with secrets redacted and source commit.

## Operations

Use `logs --tail 100 <service>` for safe troubleshooting; avoid dumping rendered configuration because it contains local secrets. `down` stops the reference without deleting volumes. Volume destruction requires a separately intentional reset. Backup/restore and clean-empty-machine startup remain pending runtime evidence. [Validation results](../testing/documentation-validation.md) distinguish Compose syntax validation from daemon startup.
