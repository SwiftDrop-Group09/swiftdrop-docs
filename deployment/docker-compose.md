# Docker Compose Reference

> Status: Proposed reference configuration · Not a verified full-system deployment

[compose.yaml](compose.yaml) is a concrete configuration with one PostgreSQL instance, four DBs/users, notification persistence, RabbitMQ, private object storage and optional application profile. It aligns with [service ownership](../architecture/service-catalog.md) and the [environment matrix](environments.md). Redis and a separate realtime hub are absent.

## Prepare and validate

Run from the repository root. Copy [environment template](.env.example) to ignored `deployment/.env`, generate distinct local passwords, and select tested/pinned image versions. The latest object-store tags in the template are unresolved placeholders to pin before release, not a tested compatibility claim. Never use REPLACE_LOCAL_ONLY as a password.

```powershell
Copy-Item deployment/.env.example deployment/.env
docker compose --env-file deployment/.env -f deployment/compose.yaml config --quiet
docker compose --env-file deployment/.env -f deployment/compose.yaml up -d
docker compose --env-file deployment/.env -f deployment/compose.yaml ps -a
```

Default profile starts infrastructure/bootstrap only. PostgreSQL init creates the four DBs and owner roles with PUBLIC connection privileges revoked. Existing volumes do not rerun init; missing DBs on an older volume require an explicit reviewed migration/bootstrap, not silent data deletion. Health confirms all four databases exist. Each future API/Worker owns its EF migrations; do not connect Worker to Merchant/Delivery DB.

Rabbit bootstrap creates delivery_bus and worker_bus scoped users, with explicit per-type/receive entity permissions; topology declaration is performed by MassTransit consumers at startup. Broker binding permissions must be verified against the pinned MassTransit version in the runtime smoke test. Object bootstrap creates a private bucket and Delivery-only policy/account; app credentials are not root/admin credentials. Verify selected object images contain the configured health tools.

## Application profile prerequisites

This documentation repository has **no backend/frontend implementation or Dockerfiles**. `design-unbuilt` image names are deliberate placeholders. Before using `--profile application`, provide real images, their build/source commit links, a migration job per DB, supported `/app/healthcheck` executable, actual YARP route config, signing/encryption keys, workload JWT credentials and trusted Google client IDs. Mount secrets as files; do not bake keys into images. The environment names in this reference are the proposed configuration contract and must be mapped by the actual code. Web runtime base-URL injection also needs implementation support.

YARP routes only catalogued public prefixes to the correct API, `/graphql` and SSE to Delivery, and JWKS to Identity. Block `/internal/*`. Non-loopback clients require configured TLS ingress; domain services still validate JWTs. SSE buffering/timeouts must support heartbeats. Merchant's egress network must be constrained with outbound DNS/IP controls; a Compose network alone does not implement SSRF policy.

After providing those prerequisites, run `docker compose --env-file deployment/.env -f deployment/compose.yaml --profile application up -d --build`. Until actual build contexts/images exist, this is an implementation acceptance command, not a working application claim. Smoke test all four DB migrations/readiness, quote-confirm, Flutter Customer/Courier, outbox outage recovery, notification, Merchant job reconciliation and webhook signing. Record logs with secrets redacted and source commit.

## Operations

Use `logs --tail 100 <service>` for safe troubleshooting; avoid dumping rendered configuration because it contains local secrets. `down` stops the reference without deleting volumes. Volume destruction requires a separately intentional reset. Backup/restore and clean-empty-machine startup remain pending runtime evidence. [Validation results](../testing/documentation-validation.md) distinguish Compose syntax validation from daemon startup.
