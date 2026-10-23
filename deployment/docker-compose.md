# Docker Compose Development Environment

> Status: Development Compose defined in `swiftdrop-infra/development` · Runtime acceptance pending

The shared developer environment is in the infrastructure repository's
`development/` folder. It builds and runs separate containers for the
frontend, Gateway, Identity, Delivery, Merchant, Notification Worker, and
RabbitMQ. PostgreSQL remains external in Neon. Do not use this documentation
repository's reference `deployment/compose.yaml` as the developer run command.

Keep `swiftdrop-infra`, `swiftdrop-backend`, and `swiftdrop-frontend` as sibling
repositories, start Docker, then run from `swiftdrop-infra`:

```sh
./development/run.sh up --mode docker --build
```

The script creates ignored local configuration on first use. The web app is
available at `http://localhost:5173`, the Gateway at `http://localhost:5000`,
and RabbitMQ's local management UI at `http://localhost:15672`.

Use the same script to rebuild or operate a selected service:

```sh
./development/run.sh up --mode docker
./development/run.sh up --mode docker --build delivery-service
./development/run.sh logs gateway
./development/run.sh ps
./development/run.sh down
```

Developers may select `./development/run.sh up --mode host` for routine
iteration with local .NET and Node processes. Docker is nevertheless the
required shared acceptance check before merging app/container changes: run the
Docker command with `--build`, verify container startup and Gateway/web health,
and record the result (or obtain equivalent CI/Docker-enabled teammate
evidence). A host-mode run cannot validate container networking or images.

The four Neon connection-string examples are placeholders; current service
code does not consume them. RabbitMQ is included, but there is no broker
adapter yet. MinIO is deferred until proof storage is implemented. `/health`
is process liveness, not dependency readiness; feature routes and DB
migrations are not implemented. A successful Compose parse is not evidence
that images build or the complete application runs.

The choice to use external Neon differs from the assignment's literal
database-container requirement; confirm lecturer acceptance. See the
[assignment overview](../requirements/assignment-overview.md) and
[Kubernetes scope](kubernetes.md).
