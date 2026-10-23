# Kubernetes Bonus Reference

> Status: Optional +5 bonus · Assignment PDF page 3 verified · Kustomize starter exists in `swiftdrop-infra` · Cluster runtime not tested · OPS/QA owner unassigned

Kubernetes is independent of mandatory acceptance; [Compose](docker-compose.md) remains the local baseline. No managed cluster, production guarantees, many replicas or zero-downtime behavior is claimed. The infrastructure repository now has a Kustomize base for local development. Static manifest rendering is not a successful cluster deployment or acceptance evidence.

## Minimal demonstrable scope

The current base defines one replica of each gateway/API/Worker/web process, Neon PostgreSQL as an external managed dependency, RabbitMQ and private object storage with persistent volumes, ConfigMaps, Services, Ingress TLS configuration, and bootstrap resources. Secret values are supplied through ignored per-service environment files. Keep **one Delivery replica** until an approved realtime fanout design exists. Migration Jobs are not provided because backend migrations do not exist yet. Images are not pinned to verified digests; resource budgets are initial estimates, and probes currently check process liveness only. Graceful shutdown, retry behavior, network egress policy and cluster runtime validation remain open.

The assignment's Kubernetes bonus describes the full frontend/backend/**database**/broker system and explicitly requires ConfigMaps, Secrets, Services and Ingress. Using external Neon means PostgreSQL is not deployed in the cluster, so this design does **not yet demonstrate the literal full-database bonus scope**. Confirm with the lecturer whether managed Neon is accepted as the database deployment; if not, add a PostgreSQL workload to the cluster while retaining Neon for shared development.

Initial app budgets in the manifests (to validate on the demo machine): requests 100m CPU/128Mi, limits 500m/512Mi per application; stateful dependencies have separate starting budgets. Neon and broker/object-store secrets are injected outside Git; application signing and encrypted webhook keys are not yet implemented. NetworkPolicy/egress controls still need to restrict service access, permit only required TLS egress to the configured Neon endpoint, and block internal/metadata webhook destinations; app SSRF checks remain necessary.

The [+5 bonus source](../requirements/sources/ead-group-assignment.pdf#page=3) explicitly names ConfigMaps, Secrets, Services and Ingress. Helm charts are encouraged as an extra, not a prerequisite. Scaling/capping of the +5 against overall marks needs lecturer clarification.

## Bonus gates

| Milestone                   | Required evidence                                                   | Status                                                                              |
| --------------------------- | ------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| Manifests reviewed          | Versioned files, owner, tested cluster/tool versions                | Starter rendered with `kubectl kustomize`; review and cluster/tool evidence pending |
| One-node clean deployment   | Successful migrations/readiness, PVC persistence and restart        | Planned; migrations and dependency-aware readiness are not implemented              |
| Mandatory flows on cluster  | Four workflow tests, web/mobile networking, private data checks     | Planned                                                                             |
| Optional scaling            | Approved fanout/backplane, multi-instance clients and failure tests | Deferred                                                                            |
| Upgrade/availability claims | Measured rolling-update and fault evidence before any guarantee     | Deferred                                                                            |

Use [service catalog](../architecture/service-catalog.md), [environment matrix](environments.md), [security](../security/data-protection.md) and [test plan](../testing/test-strategy.md). Mandatory submission may proceed without this bonus once its own gates pass.
