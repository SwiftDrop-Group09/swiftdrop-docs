# Kubernetes Bonus Reference

> Status: Optional +5 bonus proposal · Assignment PDF page 3 verified · Not deployed or tested · OPS/QA owner unassigned

Kubernetes is independent of mandatory acceptance; [Compose](docker-compose.md) remains the proposed local baseline. No managed cluster, production guarantees, many replicas or zero-downtime behavior is claimed. The infrastructure repository owns an optional, unverified Kubernetes baseline; no cluster/runtime evidence is claimed by this documentation repository. Reconcile its manifests with the Neon/six-secret development contract before use.

## Minimal demonstrable scope

Start with one local kind/minikube cluster and namespace, one replica of each gateway/API/Worker/web process, four private logical Neon PostgreSQL databases, RabbitMQ and private object storage (broker/object persistent volumes managed by the cluster). Keep **one Delivery replica** until an approved realtime fanout design exists. Supply actual Deployments, **ConfigMaps**, **Secrets**, **Service definitions** and **Ingress** for the full frontend/backend/database/broker system, plus migration Jobs, PVCs and ingress TLS; do not put real secrets in manifests. Pin images to verified digests and set measured resource requests/limits, readiness/liveness, graceful shutdown and retry behavior.

Proposed initial app budgets (to validate on the demo machine): requests 100m CPU/128Mi, limits 500m/512Mi per application; stateful dependencies need separate measured budgets. Secrets for DB, broker, signing and encrypted webhook keys are injected outside Git. NetworkPolicy/egress controls restrict service access and block internal/metadata webhook destinations; app SSRF checks remain necessary.

The [+5 bonus source](../requirements/sources/ead-group-assignment.pdf#page=3) explicitly names ConfigMaps, Secrets, Services and Ingress. Helm charts are encouraged as an extra, not a prerequisite. Scaling/capping of the +5 against overall marks needs lecturer clarification.

## Bonus gates

| Milestone | Required evidence | Status |
|---|---|---|
| Manifests reviewed | Versioned files, owner, tested cluster/tool versions | Planned |
| One-node clean deployment | Successful migrations/readiness, PVC persistence and restart | Planned |
| Mandatory flows on cluster | Four workflow tests, web/mobile networking, private data checks | Planned |
| Optional scaling | Approved fanout/backplane, multi-instance clients and failure tests | Deferred |
| Upgrade/availability claims | Measured rolling-update and fault evidence before any guarantee | Deferred |

Use [service catalog](../architecture/service-catalog.md), [environment matrix](environments.md), [security](../security/data-protection.md) and [test plan](../testing/test-strategy.md). Mandatory submission may proceed without this bonus once its own gates pass.
