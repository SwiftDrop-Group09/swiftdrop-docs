# Documentation Validation Evidence

> Baseline 2.0 · Review date 16 October 2026 · Documentation/design fixtures only

The following commands were executed locally against the revised files. These are **documentation/design checks**, separate from [application tests](test-results.md); none establishes deployment, business-test coverage or team approval.

| Check | Command / tool | Observed result |
|---|---|---|
| Markdown integrity | `python scripts/validate-docs.py` | PASS: link validation rerun after assignment alignment; all relative paths/anchors/images resolve across 54 Markdown files; zero reported errors |
| Assignment source comparison | Original/copy byte comparison, four-page text extraction and visual review | PASS: unchanged [assignment PDF](../requirements/sources/ead-group-assignment.pdf), page-cited [compliance map](../requirements/assignment-compliance.md); exact +5 bonus labels verified; grading conversion remains open |
| Route/requirement/test consistency | Same validator | PASS: 57 unique canonical operations; 32 FR + 20 NFR = 52 mapped; 68 unique drafted cases; three required priorities Must |
| JSON/event schema | Draft 2020-12 validator plus format checks | PASS: JSON parses; event example validates; injected private address field rejected; canonical state mapping matches |
| GraphQL design | `node scripts/validate-graphql.mjs` | PASS: SDL and safe public query valid; attempted private fields rejected by schema; runtime resolvers not tested |
| Protobuf design | `grpc_tools.protoc` via validator | PASS: actual delivery.proto compiles to descriptor; source-server implementation parity unverified |
| Compose syntax | `docker compose --env-file deployment/.env.example -f deployment/compose.yaml --profile application config --quiet` | PASS: full reference configuration parses using placeholder values; no containers started |
| Diagram renders | `node scripts/render-diagrams.mjs` | PASS: 33 diagrams, including seven standalone sequences and six formal PlantUML activities; embedded ER/context/use-case/state diagrams render |
| Source/export parity | SHA-256 of normalized diagram sources | PASS: manifest hashes match each source block/file and all indexed SVGs exist |
| PDF integrity | `python scripts/review-pdfs.py` | PASS: one-page architecture PDF and 33-page design diagram packet; each formal activity title appears on its corresponding page |
| Patch whitespace | `git diff --check` | PASS: no whitespace errors |

## Visual review

Raster previews of the regenerated architecture PDF, courier status→notification sequence, courier activity and merchant-order activity were inspected locally. The export initially revealed an activity overflowing onto the next page; SVG size overrides were corrected and the corresponding-page title checks now pass. The revised overview, swimlanes, guards and async branches are visible without clipped diagram content in the inspected pages. PDFs use a large-format 594 × 420 mm vector layout; dense sequence labels should be read with PDF zoom or the individual SVG. This is a technical preview review, **not** academic/UML or security sign-off of every diagram. The team must still approve all indexed diagrams and the eventual final report PDF.

## Reproduction environment

Windows PowerShell; Python 3.14.3; Node 24.9.0; Java 21.0.8; PlantUML 1.2026.8; Mermaid CLI 12.0.0 (Mermaid 12.2.0); GraphQL 17.0.2. Python validator packages are pinned in [requirements.txt](../scripts/requirements.txt); Node packages are locked in [package-lock.json](../scripts/package-lock.json). The local run used isolated dependencies under ignored `.validation-tools`; the [reproduction guide](../scripts/README.md) also supports an isolated virtual environment and scripts-local install. Generated previews and downloaded tools are excluded from Git.

## Assignment alignment verification

The supplied four-page assignment was extracted and all four pages visually inspected on 16 October 2026. Its repository copy matches the original byte-for-byte (SHA-256 is recorded in the assignment overview). The source comparison closes the missing-PDF task and adds the required [patterns note](../architecture/design-patterns.md), explicit Courier/zone ER entities, service-day manifests, private delivery notes, required mock-SMS consumer evidence and exact bonus scope. These edits retain 52 SRS requirements and 68 drafted cases; no new runtime pass result is claimed.

After regenerating all 33 diagrams/PDFs, the Delivery ER page was checked for couriers, courier_zones, service_date, delivery_note and recipient_name and visually reviewed for clipping/readability. Schema, protobuf, Compose parsing, relative links and source/export hashes pass. The assignment names React/Angular/Vue alternatives, Docker/Compose and email-or-mock-SMS; Flutter, the selected stack and numeric quality targets remain team decisions. Its category/overall grading mismatch is recorded explicitly rather than resolved by assumption.

## Unexecuted gates

- Lecturer grading conversion/scaling: source comparison is now complete in the [assignment compliance map](../requirements/assignment-compliance.md); how the 100-point category labels/+5 bonuses map to the overall 20 remains unclarified.
- Backend OpenAPI/protobuf/GraphQL implementation parity and all application unit/integration/security/recovery tests: source/build evidence absent; 68 cases are Drafted only.
- Docker empty-machine startup, applied migrations, private-storage/broker permissions, health and end-to-end smoke: Docker daemon unavailable (`dockerDesktopLinuxEngine` named pipe missing) and real app images/migrations absent. Configuration parsing is not startup evidence.
- Flutter Customer/Courier device onboarding, browser SSE reconnect, actual latency/load/coverage reports and final report/demo evidence: pending owning implementations.
- Named team allocation, individual contribution verification and ADR/diagram/PR approval: pending team records; all design decisions remain Proposed.

Outstanding verification, approvals and submission tasks are consolidated in the [remaining-work checklist](../documentation-fix-plan.md); no unexecuted check above is recorded as passing.
