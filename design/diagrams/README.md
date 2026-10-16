# Diagram Index and Sign-Off Register

> Proposed baseline 2.0 · 16 October 2026 · All named owners/review dates pending

Editable sources and rendered SVGs below follow the same [use-case narratives](../../requirements/use-case-specifications.md), [REST operations](../../api/rest-api.md), [gRPC](../../api/grpc-services.md), [state matrix](../../architecture/parcel-state-machine.md), [events](../../integration/event-catalog.md) and [ADR register](../../architecture/decisions/README.md). Machine-readable IDs, requirement/operation mapping, version and review fields live in [manifest.json](manifest.json). All exports are generated, **not approved**. IDs for embedded diagrams identify the source Markdown and mermaid-block number.

## Required assignment coverage

| Workflow | Narrative | Sequence | Formal activity |
|---|---|---|---|
| Customer booking / fee confirmation | UC-01 | [SEQ-customer-booking](sequence/customer-booking.mmd) | [ACT-customer-booking](activity/customer-booking.puml) |
| Merchant secured API order | UC-02 | [SEQ-merchant-order](sequence/merchant-order.mmd) | [ACT-merchant-order](activity/merchant-order.puml) |
| Courier status triggers notifications | UC-03 | [SEQ-courier-status-notification](sequence/courier-status-notification.mmd) | [ACT-courier-status-notification](activity/courier-status-notification.puml) |
| Google OAuth/OIDC login | UC-04 | [SEQ-google-login](sequence/google-login.mmd) | [ACT-google-login](activity/google-login.puml) |

## Source/export inventory

| Diagram ID | Scenario / SRS IDs | Editable source | Rendered artifact | Version | Owner | Review date / approval |
|---|---|---|---|---|---|---|
| DIA-01 | Cross-cutting; NFR-14, NFR-15, NFR-16 | [design/diagrams/architecture/architecture.mmd](architecture/architecture.mmd) | [SVG](architecture/architecture.svg) | 2.0 | Unassigned | Pending |
| SEQ-assignment-proof | UC-03; FR-D02, FR-D03, FR-D04, FR-R03 | [design/diagrams/sequence/assignment-proof.mmd](sequence/assignment-proof.mmd) | [SVG](sequence/assignment-proof.svg) | 2.0 | Unassigned | Pending |
| SEQ-courier-status-notification | UC-03; FR-R02, FR-R03, FR-R04, FR-C06, FR-M05, NFR-11 | [design/diagrams/sequence/courier-status-notification.mmd](sequence/courier-status-notification.mmd) | [SVG](sequence/courier-status-notification.svg) | 2.0 | Unassigned | Pending |
| SEQ-customer-booking | UC-01; FR-C04, FR-C05, NFR-10, NFR-11 | [design/diagrams/sequence/customer-booking.mmd](sequence/customer-booking.mmd) | [SVG](sequence/customer-booking.svg) | 2.0 | Unassigned | Pending |
| SEQ-google-login | UC-04; FR-C02, NFR-05, NFR-08 | [design/diagrams/sequence/google-login.mmd](sequence/google-login.mmd) | [SVG](sequence/google-login.svg) | 2.0 | Unassigned | Pending |
| SEQ-merchant-order | UC-02; FR-M03, FR-M04, FR-M06, FR-M07, NFR-10 | [design/diagrams/sequence/merchant-order.mmd](sequence/merchant-order.mmd) | [SVG](sequence/merchant-order.svg) | 2.0 | Unassigned | Pending |
| SEQ-refresh-session | UC-04; FR-C01, NFR-05 | [design/diagrams/sequence/refresh-session.mmd](sequence/refresh-session.mmd) | [SVG](sequence/refresh-session.svg) | 2.0 | Unassigned | Pending |
| SEQ-webhook-delivery | UC-03; FR-M05, NFR-07, NFR-12, NFR-13 | [design/diagrams/sequence/webhook-delivery.mmd](sequence/webhook-delivery.mmd) | [SVG](sequence/webhook-delivery.svg) | 2.0 | Unassigned | Pending |
| DIA-09 | Cross-cutting; NFR-14, NFR-15, NFR-16 | [architecture/system-context.md#mermaid-1](../../architecture/system-context.md) | [SVG](generated/architecture-system-context-1.svg) | 2.0 | Unassigned | Pending |
| DIA-10 | Cross-cutting; NFR-14, NFR-15, NFR-16 | [design/diagrams/architecture/architecture.md#mermaid-1](architecture/architecture.md) | [SVG](generated/design-diagrams-architecture-architecture-1.svg) | 2.0 | Unassigned | Pending |
| DIA-11 | Cross-cutting; NFR-14, FR-C01, FR-C04, FR-M05, NFR-11 | [design/diagrams/er/README.md#mermaid-1](er/README.md) | [SVG](generated/design-diagrams-er-README-1.svg) | 2.0 | Unassigned | Pending |
| DIA-12 | Cross-cutting; NFR-14, FR-C01, FR-C04, FR-M05, NFR-11 | [design/diagrams/er/README.md#mermaid-2](er/README.md) | [SVG](generated/design-diagrams-er-README-2.svg) | 2.0 | Unassigned | Pending |
| DIA-13 | Cross-cutting; NFR-14, FR-C01, FR-C04, FR-M05, NFR-11 | [design/diagrams/er/README.md#mermaid-3](er/README.md) | [SVG](generated/design-diagrams-er-README-3.svg) | 2.0 | Unassigned | Pending |
| DIA-14 | Cross-cutting; NFR-14, FR-C01, FR-C04, FR-M05, NFR-11 | [design/diagrams/er/README.md#mermaid-4](er/README.md) | [SVG](generated/design-diagrams-er-README-4.svg) | 2.0 | Unassigned | Pending |
| DIA-15 | Cross-cutting; NFR-14, FR-C01, FR-C04, FR-M05, NFR-11 | [design/diagrams/er/README.md#mermaid-5](er/README.md) | [SVG](generated/design-diagrams-er-README-5.svg) | 2.0 | Unassigned | Pending |
| DIA-16 | Cross-cutting; NFR-14, FR-C01, FR-C04, FR-M05, NFR-11 | [design/diagrams/er/README.md#mermaid-6](er/README.md) | [SVG](generated/design-diagrams-er-README-6.svg) | 2.0 | Unassigned | Pending |
| DIA-17 | Cross-cutting; NFR-14, FR-C01, FR-C04, FR-M05, NFR-11 | [design/diagrams/er/README.md#mermaid-7](er/README.md) | [SVG](generated/design-diagrams-er-README-7.svg) | 2.0 | Unassigned | Pending |
| DIA-18 | Cross-cutting; FR-C04, FR-M04, FR-R02, FR-C02 | [design/diagrams/use-cases/README.md#mermaid-1](use-cases/README.md) | [SVG](generated/design-diagrams-use-cases-README-1.svg) | 2.0 | Unassigned | Pending |
| DIA-19 | Cross-cutting; FR-C04, FR-M04, FR-R02, FR-C02 | [design/diagrams/use-cases/README.md#mermaid-2](use-cases/README.md) | [SVG](generated/design-diagrams-use-cases-README-2.svg) | 2.0 | Unassigned | Pending |
| DIA-20 | Cross-cutting; FR-C04, FR-M04, FR-R02, FR-C02 | [design/diagrams/use-cases/README.md#mermaid-3](use-cases/README.md) | [SVG](generated/design-diagrams-use-cases-README-3.svg) | 2.0 | Unassigned | Pending |
| DIA-21 | Cross-cutting; FR-C04, FR-M04, FR-R02, FR-C02 | [design/diagrams/use-cases/README.md#mermaid-4](use-cases/README.md) | [SVG](generated/design-diagrams-use-cases-README-4.svg) | 2.0 | Unassigned | Pending |
| DIA-22 | Cross-cutting; FR-C04, FR-M04, FR-R02, FR-C02 | [design/diagrams/use-cases/README.md#mermaid-5](use-cases/README.md) | [SVG](generated/design-diagrams-use-cases-README-5.svg) | 2.0 | Unassigned | Pending |
| DIA-23 | Cross-cutting; FR-C04, FR-M04, FR-R02, FR-C02 | [design/diagrams/use-cases/README.md#mermaid-6](use-cases/README.md) | [SVG](generated/design-diagrams-use-cases-README-6.svg) | 2.0 | Unassigned | Pending |
| DIA-24 | Cross-cutting; NFR-14, NFR-15, NFR-16 | [integration/integration-design.md#mermaid-1](../../integration/integration-design.md) | [SVG](generated/integration-integration-design-1.svg) | 2.0 | Unassigned | Pending |
| DIA-25 | Cross-cutting; NFR-14, NFR-15, NFR-16 | [integration/merchant-webhooks.md#mermaid-1](../../integration/merchant-webhooks.md) | [SVG](generated/integration-merchant-webhooks-1.svg) | 2.0 | Unassigned | Pending |
| DIA-26 | Cross-cutting; FR-C04, FR-M04, FR-R02, FR-C02 | [requirements/srs.md#mermaid-1](../../requirements/srs.md) | [SVG](generated/requirements-srs-1.svg) | 2.0 | Unassigned | Pending |
| DIA-27 | Cross-cutting; FR-C04, FR-M04, FR-R02, FR-C02 | [requirements/srs.md#mermaid-2](../../requirements/srs.md) | [SVG](generated/requirements-srs-2.svg) | 2.0 | Unassigned | Pending |
| ACT-assignment-workload | Supporting; FR-D01, FR-D02, FR-D03, FR-D04, FR-D05 | [design/diagrams/activity/assignment-workload.puml](activity/assignment-workload.puml) | [SVG](activity/assignment-workload.svg) | 2.0 | Unassigned | Pending |
| ACT-courier-status-notification | UC-03; FR-R02, FR-R03, FR-R04, FR-C06, FR-M05, NFR-11 | [design/diagrams/activity/courier-status-notification.puml](activity/courier-status-notification.puml) | [SVG](activity/courier-status-notification.svg) | 2.0 | Unassigned | Pending |
| ACT-customer-booking | UC-01; FR-C04, FR-C05, NFR-10, NFR-11 | [design/diagrams/activity/customer-booking.puml](activity/customer-booking.puml) | [SVG](activity/customer-booking.svg) | 2.0 | Unassigned | Pending |
| ACT-google-login | UC-04; FR-C02, NFR-05, NFR-08 | [design/diagrams/activity/google-login.puml](activity/google-login.puml) | [SVG](activity/google-login.svg) | 2.0 | Unassigned | Pending |
| ACT-merchant-onboarding | Supporting; FR-M01, FR-M02, FR-A03 | [design/diagrams/activity/merchant-onboarding.puml](activity/merchant-onboarding.puml) | [SVG](activity/merchant-onboarding.svg) | 2.0 | Unassigned | Pending |
| ACT-merchant-order | UC-02; FR-M03, FR-M04, FR-M06, FR-M07, NFR-10 | [design/diagrams/activity/merchant-order.puml](activity/merchant-order.puml) | [SVG](activity/merchant-order.svg) | 2.0 | Unassigned | Pending |

## PDF and review evidence

[Architecture PDF](architecture/swiftdrop-architecture.pdf) is regenerated from architecture.mmd. [Design diagram packet](swiftdrop-design-baseline.pdf) includes the proposed overview and all rendered diagrams; it is a review export, not a final report with implementation/test evidence. Render checks and visual-review limitations are in [documentation validation](../../testing/documentation-validation.md). Source history preserves the prior baseline at 63d0de2.

For each review record the named reviewer/date/PR and check actor/client, exact endpoint/RPC/event, role/resource guard, version/state/persistence owner, success/invalid/unauthorized/failure branches, outbox timing, retries/dedup and public/private data segregation. API plus owning domain approve; SEC/MSG/UI participate when affected. No sign-off is inferred from a renderer passing. Rebuild using [validation scripts](../../scripts/README.md) after contract/source changes.
