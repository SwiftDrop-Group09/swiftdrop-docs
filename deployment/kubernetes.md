# Kubernetes Bonus Reference

> Status: Optional bonus proposal · Not deployed or tested · OPS/QA owner unassigned

Kubernetes is independent of mandatory acceptance; [Compose](docker-compose.md) remains the proposed local baseline. No managed cluster, production guarantees, many replicas or zero-downtime behavior is claimed. There are no Kubernetes manifests in this documentation repository; the first milestone is an implementation PR in the infrastructure repository with version/commit evidence.

## Minimal demonstrable scope

Start with one local kind/minikube cluster and namespace, one replica of each gateway/API/Worker/web process, four private logical databases on one PostgreSQL instance, RabbitMQ and private object storage with persistent volumes. Keep **one Delivery replica** until an approved realtime fanout design exists. Supply actual Deployments, Services, migration Jobs, PVCs, Secrets references and ingress TLS; do not put real secrets in manifests. Pin images to verified digests and set measured resource requests/limits, readiness/liveness, graceful shutdown and retry behavior.

Proposed initial app budgets (to validate on the demo machine): requests 100m CPU/128Mi, limits 500m/512Mi per application; stateful dependencies need separate measured budgets. Secrets for DB, broker, signing and encrypted webhook keys are injected outside Git. NetworkPolicy/egress controls restrict service access and block internal/metadata webhook destinations; app SSRF checks remain necessary.

## Bonus gates

| Milestone | Required evidence | Status |
|---|---|---|
| Manifests reviewed | Versioned files, owner, tested cluster/tool versions | Planned |
| One-node clean deployment | Successful migrations/readiness, PVC persistence and restart | Planned |
| Mandatory flows on cluster | Four workflow tests, web/mobile networking, private data checks | Planned |
| Optional scaling | Approved fanout/backplane, multi-instance clients and failure tests | Deferred |
| Upgrade/availability claims | Measured rolling-update and fault evidence before any guarantee | Deferred |

Use [service catalog](../architecture/service-catalog.md), [environment matrix](environments.md), [security](../security/data-protection.md) and [test plan](../testing/test-strategy.md). Mandatory submission may proceed without this bonus once its own gates pass.
