# Submission Checklist

> Status: Draft readiness ledger · External deadline **15 November 2026**

The assignment is worth **20 marks overall** with category weights 20/50/15/15, subject to comparison against the missing lecturer PDF. **12 November** is only the optional internal freeze/rehearsal target. Documentation edits, validation and draft test cases do not prove implementation complete. All approvals/contributions remain evidence-based.

## Design and assignment

- [ ] Attach authoritative assignment PDF and complete requirement/page comparison.
- [ ] Confirm individual owners/reviewers and DEC-01–DEC-12; record actual approver/date/PR.
- [ ] Review SRS: 32 FR + 20 NFR; Must receipt/dashboard/reports and mobile-friendly public tracking.
- [ ] Review Flutter Customer **and** Courier scope.
- [ ] Sign off four use-case narratives and four sequence/activity pairs; ER/service/state/API/event/security parity.
- [ ] Regenerate all diagram exports and visually review final design/report PDF; documentation checks must pass with evidence.

## Implementation and mandatory demo

- [ ] Linked tested backend/web/mobile commits and source package; no placeholder image paths.
- [ ] Local signup/login and Google ID-token login with safe subject linking and RBAC.
- [ ] Quote before confirmation, idempotent booking, own history and safe public/private tracking.
- [ ] Receipt PDF download, merchant own-order/status dashboard, Admin deliveries/day and success/failure reports.
- [ ] Courier assignment/workload and Flutter status/failure/proof completion triggering persisted notifications and Merchant webhook.
- [ ] Durable merchant job plus unknown-outcome reconciliation and duplicate protection.
- [ ] Four private DBs/migrations, broker, private object store and real images pass clean Compose startup.
- [ ] Mandatory flow works without Kubernetes, AI, GPS or SignalR.

## Tests and evidence

- [ ] 68 drafted test cases reconciled with implemented suite; executed/pass/fail/skip statuses attached.
- [ ] Security negatives and distributed failure cases run with assertions and artifacts.
- [ ] Unit business-logic line coverage ≥80% with denominator/exclusions; branch metrics reported separately.
- [ ] CI run URLs, dated coverage, sanitized logs/screenshots and web/mobile device evidence.
- [ ] Source release/tag and setup instructions verified by a new member.
- [ ] Individual contribution sheet supported by actual named-member PR/review evidence.
- [ ] Final report/design PDF and demo rehearsal approved by team before submission.

## Independent optional bonuses

- [ ] Kubernetes minimal local-cluster demo with actual manifests and tested evidence (optional).
- [ ] AI TrackParcel/EstimateFee authorization and failure tests (optional).

Current documented checks are in [documentation validation](../testing/documentation-validation.md). Runtime test results, team approval and contribution proof are pending in [test results](../testing/test-results.md) and [contribution log](../project-management/contribution-log.md); unchecked boxes must not be changed merely because text exists.
