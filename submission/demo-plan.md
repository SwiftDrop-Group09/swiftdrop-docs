# Demonstration Plan

> Status: Draft script · No running-system evidence claimed · Submission 15 November 2026

Proposed rehearsal: 12 November. Use fictional local fixtures, a controlled HTTPS webhook receiver, recorded source commits and known device/API level. If runtime is unavailable show a clearly labeled recording with its execution date; a diagram walkthrough does not count as a working demo.

| Time | Scenario and visible acceptance | SRS / tests |
|---|---|---|
| 0–2 min | React/Flutter Google SDK login, local signup/login; explain provider-subject linking and roles | FR-C01/C02; TC-C01/C02 |
| 2–5 min | Flutter Customer fee preview, decline/requote then confirm; safe mobile-width public tracking and own history | FR-C04/C05/C06/C07; TC-C04/C05/C06/C07 |
| 5–8 min | React Dispatcher queue/workload/assignment; Flutter Courier status→outbox→persisted notification; wrong courier rejected | FR-D01/D02/D03, FR-R01/R02; TC-SEC-02 |
| 8–10 min | Flutter Courier proof completion from OutForDelivery; Customer receipt PDF download; public proof access denied | FR-R03, FR-C08; TC-R03/C08/SEC-07 |
| 10–12 min | Merchant secured async order 202→Created; own dashboard/order status; HMAC webhook and inspectable attempts | FR-M04/M05/M06/M07; TC-M04/M05/M06/M07 |
| 12–13 min | Admin deliveries/day, success/failure rates and empty denominator; compare fixture counts | FR-A06; TC-A06 |
| 13–15 min | Show executed CI/coverage and recovery: unknown gRPC result, broker outage/duplicate event; contribution evidence | NFR-10/11/17; TC-REC-02/03/04 |

Do not promise a GPS map or Redis/SignalR behavior; they are deferred. Kubernetes and AI are separate bonus demonstrations only after mandatory coverage. Rehearsal must record missing/failed scenarios instead of presenting drafted tests as passing evidence. API operations, state names and retry timings must match [contracts](../api/rest-api.md) and [webhook policy](../integration/merchant-webhooks.md).
