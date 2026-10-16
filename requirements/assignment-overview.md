# Assignment Overview

> Source comparison: verified against the supplied four-page PDF on 16 October 2026 · SwiftDrop design approval remains pending

Source: [EAD Group Assignment.pdf](sources/ead-group-assignment.pdf), titled *Assignment Guideline: Parcel Delivery & Courier Management System*. The repository copy is unchanged from the supplied file; SHA-256: `b19457c735e4f3608adf54a5c7d03c06114e021367c66f01366f01c92a0bf5b2`. Page references below use its physical PDF pages 1–4. The [assignment compliance map](assignment-compliance.md) links every requirement/deliverable to design and planned acceptance evidence.

SwiftDrop is Group 09's Parcel Delivery and Courier Management project. The PDF specifies **10 members** and **20 marks overall** on [page 1](sources/ead-group-assignment.pdf#page=1). The session-confirmed external deadline is **15 November 2026**, with **12 November** an optional internal rehearsal/freeze; **the PDF itself contains no submission date**.

## Assessment labels and clarification

| Category | Marks printed in the PDF | Source |
|---|---|---|
| Design documentation | 20 | Page 2 |
| Implementation | 50 | Pages 2–3 |
| Testing | 15 | Page 3 |
| Presentation/demo | 15 | Page 3 |
| Kubernetes deployment bonus | +5 | Page 3 |
| AI delivery assistant bonus | +5 | Page 3 |

The four base category labels total 100, while page 1 states an overall weightage of 20 marks. A proportional 20%/50%/15%/15% rubric is a plausible interpretation, **not an explicit conversion rule in the PDF**. REQ/PM must ask the lecturer how category and bonus marks convert to the overall 20. Do not silently add +10 to 20 or claim a confirmed grading formula. The +5 labels for each bonus are verified; their scaling/capping is the remaining question.

## Official assignment constraints

| Area | Verified requirement | Source |
|---|---|---|
| Customer | Secure signup/login including Google OAuth; delivery request with pickup/drop-off and parcel size/weight; estimate before confirmation; live statuses; history/receipt; mobile-friendly public-number tracking | Page 1 |
| Merchant | Admin-approved registration; secured order API using API keys **or** OAuth client credentials; status webhooks; dashboard of all own orders/states | Page 1 |
| Courier | Authentication; assigned deliveries for the day; stage updates with a note or proof (recipient name/photo are examples); failure reason | Page 2 |
| Dispatcher/Admin | Unassigned queue/assignment, active workloads, user/merchant/zone/pricing management, deliveries/day and success/failure reports | Page 2 |
| Frontend | Responsive **web** UI using React, Angular or Vue | Page 3 |
| Backend/architecture | Suitable backend framework; justified layered, microservice or modular-monolith architecture with presentation/business/data layers | Pages 2–3 |
| APIs/security | Secure REST **or** GraphQL with versioning, validation and centralized errors; JWT, OAuth social/merchant integration, RBAC; hashed passwords and no sensitive logs/errors | Pages 2–3 |
| Status integration | Message broker/status-event integration triggering notifications and merchant webhooks; retry failed webhooks; an email service **or mock SMS consumer** | Pages 2–3 |
| Live tracking | Page 2 permits WebSockets/SSE/polling generally; page 3's implementation requirement names WebSockets/SSE. SwiftDrop selects SSE to meet the stricter wording | Pages 2–3 |
| Containers | Dockerize frontend, backend services, database and broker; **Docker Compose** for local orchestration | Pages 2–3 |
| Design | Use cases; ER covering users/roles/merchants/parcels/history/**couriers**/zones/pricing; architecture justification; integration rationale; four sequence/activity flows; short patterns/principles note | Page 2 |
| Tests | Backend unit/integration tests with at least one event/integration-flow test; authorization negatives; measurable coverage and actual results | Page 3 |
| Demo | Google/customer booking/live tracking; merchant API order+webhook; assignment/courier status; triggered notification; design/security walkthrough; each member explains their contribution | Page 3 |
| Submission | Source link and setup README, design PDF, test reports/coverage, individual responsibility sheet | Pages 3–4 |

## Team-selected design and stronger targets

React is the team's choice among permitted web frameworks. **Flutter Customer and Courier** is additional agreed team scope; the PDF does not require Flutter or allow it to replace the responsive web deliverable. ASP.NET Core 10 on .NET 10 (`net10.0`)/C#, PostgreSQL, three capability APIs, YARP, RabbitMQ/MassTransit, REST **plus** GraphQL and gRPC, four private DBs, outbox and private object storage are team design choices. Docker/Compose and the full containerized system are **official requirements**, even though the precise images/topology are team choices.

The PDF's displayed status path is Created → Picked Up → In Transit → Out for Delivery → Delivered/Failed. Assigned/Cancelled, expected-version/idempotency guards, Google ID-token exchange, 15-minute JWTs, encrypted signing material and strict image/signature proof completion are proposed team refinements. The assignment permits a delivery note or proof, including recipient name; it does not mandate a photo at every stage. The [state machine](../architecture/parcel-state-machine.md) and [REST contracts](../api/rest-api.md) keep the stronger final-proof rule explicit.

The PDF sets no numeric coverage, response-latency, concurrency or Android API target. SRS ≥80% business-logic unit line coverage, 500ms p95, 2s status target, 50 concurrent users, API 26+ and 320px checks are team acceptance targets. “Must” in the team SRS can therefore include an adopted commitment beyond the lecturer minimum.

## Independent optional bonuses

The [Kubernetes bonus](../deployment/kubernetes.md) is **+5** for deploying the full frontend/backend/database/broker system with ConfigMaps, Secrets, Service definitions and Ingress; Helm is a plus, not a stated prerequisite. The [AI bonus](../bonus/ai-delivery-assistant.md) is **+5** for a Generative AI chatbot answering parcel/fee questions through backend API calls; MCP exposure is encouraged, not required. Neither bonus is mandatory for the core release.

The source comparison is complete; source-code execution, named team approvals and submission evidence are still pending in [remaining work](../documentation-fix-plan.md). The SRS retains 32 FR + 20 NFR = 52, mapped to 68 drafted cases. Source verification does not make Proposed ADRs Accepted or draft tests Passing.
