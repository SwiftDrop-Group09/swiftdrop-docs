# Risk Register

> Status: Proposed mitigation plan · No mitigation verified through implementation

| Risk | Impact | Proposed mitigation / evidence required | Suggested role | Status |
|---|---|---|---|---|
| Grading conversion / design sign-off | Incorrect mark interpretation or unapproved design | [PDF/page comparison complete](../requirements/assignment-compliance.md); clarify overall/rubric/bonus conversion and obtain named approvals | REQ/PM | Source verified; clarification/approval pending |
| Unconfirmed team allocation | Work/attribution gap | Confirm handles and evidence-based allocation | PM | Open |
| Merchant partial failure | Duplicate/lost order | Durable inbox + stable order identity + gRPC reconciliation tests | MER/DEL | Design revised; runtime pending |
| Broker outage/duplicate delivery | Lost or duplicated notifications | Local outbox, consumer inbox and unique jobs; failure tests | MSG/QA | Design revised; runtime pending |
| Public/private tracking leakage | Exposed address/proof/courier | Separate safe DTO, ownership and negative GraphQL/REST tests | SEC/API | Design revised; runtime pending |
| Webhook SSRF/replay/key handling | Internal network access or forged effects | Public HTTPS/DNS pinning, encrypted Merchant-only key, fresh HMAC and dedup | MER/SEC | Design revised; runtime pending |
| Realtime horizontal scaling | Clients miss updates | One Delivery instance; snapshot recovery; approve fanout before scale | ARCH/OPS | Explicit demo limit |
| JWT logout/role-change delay | Old access token retains privileges | Document ≤15-minute expiry bound; revoke refresh immediately; test | SEC | Explicit design tradeoff |
| Missing source images/migrations | Full Compose cannot run | Link actual source/build/health/migration contracts and clean-start smoke | OPS | Open |
| Time pressure / bonuses | Mandatory features missed | Protect receipts/dashboard/reports and Flutter both personas; isolate bonuses | PM | Open |

Suggested roles are not actual assignments. Scores/“Mitigated” claims require team review and evidence; no unsupported Member N ownership remains.
