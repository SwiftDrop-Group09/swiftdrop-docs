# Cross-service activity auditing

The Admin audit workspace is `/admin/audit`; User management no longer embeds the
log. Reads require a verified Admin JWT at every source. Service databases remain
private: the browser combines authorized source reads rather than querying a
shared database or copying another service's entities.

| Operation | Source endpoint |
| --- | --- |
| ListIdentityActivityAudit | `/api/v1/audit-logs/activity` |
| ListDeliveryActivityAudit | `/api/v1/delivery/audit-logs` |
| ListMerchantActivityAudit | `/api/v1/merchant/audit-logs` |

These operations supplement the legacy ListAudit endpoint. They include current
API request activity and retained security/domain/configuration/background records.
They return ActivityPage: items, totalCount, hasMore and recordingEnabled. Each
ActivityRecord contains id, timestamp, actorId, roles, actorType, service, action,
method, route, resourceId, ipAddress, ipSource, statusCode, outcome, correlationId,
durationMs and kind. Nullable historical fields are not fabricated.

AuditQuery accepts limit (1–100, default 20), before plus beforeId as a paired
descending cursor, from inclusive/to exclusive UTC timestamps, actorId, role,
actorType, ip, action (literal substring), method, outcome, resourceId,
correlationId and kind. UUIDs/IPs/enums and duplicate/unknown filters are validated.
The selected service is a client-side routing filter, not an authorization bypass.

Request audit rows append a start and completion with one operation ID; the query
shows the latest phase. Audited authenticated operations fail before execution if
their initial record cannot be stored. Completion failures leave the start and a
critical diagnostic. An in-progress record has unknown completion, not a synthetic
failure. Existing webhook attempts identify System activity without a client IP.
Readiness, health checks, static files, unknown routes, OPTIONS and local-only UI
interactions are not business activity events. Future workers must participate
when their business operations are implemented.

Record actor identity only from validated server context or a successful Identity
result. Never persist passwords, tokens, cookies, API keys, bodies, query values,
recipient contact data or private notes. An IP address is connection metadata,
not proof of identity. Accept forwarded IP only from configured trusted proxy
peers; the current recorder consumes one trusted appended hop. Review actual
multi-hop topology before asserting a browser public IP. Historical records have
no retroactive IP/role attribution.

Apply Identity migration 004 and the Delivery/Merchant actor-activity migrations
with service-specific migrator credentials before deployment. Runtime privileges
are SELECT/INSERT; activity rows reject changes/deletion. Schema rollback cannot
discard retained events. Define any future legal/operational retention process
explicitly rather than deleting audit history through application screens.

Implementation is on `feat/system-audit-log`. No shared database rollout is claimed.
See the source repository activity-audit documents for configuration and test
boundaries. Existing system-completion findings describe the prior dev baseline;
this branch adds the audit read surface and request IP metadata without completing
unrelated Dispatcher, Merchant order or messaging features.
