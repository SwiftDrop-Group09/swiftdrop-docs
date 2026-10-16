# WebSocket / SignalR Scope

> Status: Deferred additional scope · DEC-08/12 · Not required by the baseline

Mandatory delivery **status** updates use [SSE in Delivery](../integration/realtime-tracking.md). Customer and Courier Flutter experiences remain mandatory and use REST/SSE without a SignalR dependency. No `/hubs` endpoint, port 5004, separate realtime process, Redis backplane or GPS frame contract is committed by this baseline.

Courier GPS telemetry and a dispatcher live map require a separate approved requirement/ADR before implementation. That design must name host and transport, assignment-scoped publication, dispatcher authorization, explicit location consent, retention (propose ≤24h), minimum sampling, encryption, rate limits and multi-instance broadcast. Exact coordinates must never enter public tracking or general status events. Tests must cover a courier impersonating another courier and unauthorized map viewers. A shared RabbitMQ queue load-balances; it does not broadcast to every server instance.

Kubernetes scaling or SignalR deployment cannot be claimed completed from this document. See [service catalog](../architecture/service-catalog.md) and [decision register](../architecture/decisions/README.md).
