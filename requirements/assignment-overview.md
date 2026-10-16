# Assignment Overview

> Status: Draft reconciliation · Baseline 2.0 · 16 October 2026

SwiftDrop is Group 09's Parcel Delivery and Courier Management project for Enterprise Application Development. Submission is **15 November 2026**. The assignment is worth **20 marks overall**; assessment weights are design 20%, implementation 50%, testing 15%, and presentation 15%. These percentages are category weights, not four separate allocations of 20/50/15/15 marks.

## Official assignment constraints

The following records the proposed assignment interpretation. **The lecturer's `EAD Group Assignment.pdf` is not present in this repository and has not been independently compared in this change.** REQ must attach its approved location and verify this table before sign-off; page citations and exact bonus scoring remain unverified. This source check is tracked in [remaining work](../documentation-fix-plan.md).

| Area | Assignment requirement described by the supplied review |
|---|---|
| Application | Suitable backend framework; layered, microservice, or modular-monolith architecture permitted |
| APIs | Secure REST **or** GraphQL APIs; message-broker integration |
| Identity | Secure signup/login and OAuth 2.0 / Google OIDC login with role-based access |
| Customer | Book delivery, preview fee before confirmation, live status/history, download receipt, mobile-friendly public tracking page |
| Merchant | Registration/approval, secured order API, webhooks, own-order status dashboard |
| Courier | Assigned deliveries, status changes, proof of delivery, failed-delivery reporting |
| Operations | Courier assignment/workload, user/role and merchant administration, zones/pricing, basic reports including deliveries/day and success/failure |
| Design | SRS, architecture, ER, use cases, sequence and activity diagrams; four explicit workflows: customer booking, merchant API order, courier status triggering notifications, Google login |
| Submission | Implementation/setup, tests and coverage evidence, design PDF, live demo and individual contribution evidence |

## Team technical choices

ASP.NET Core/C#, PostgreSQL, three capability APIs, YARP, RabbitMQ/MassTransit, REST **plus** GraphQL and gRPC, database isolation, transactional outbox, private object storage and Docker Compose are SwiftDrop design choices. They must not be attributed to the lecturer. React web and Flutter **Customer and Courier** experiences are the agreed client scope described in the review. Individual runtime versions need to be pinned and tested by implementers; none is proven deployed here.

The [decision register](../architecture/decisions/README.md) records a consistent Proposed baseline with alternatives and consequences. Proposed decisions do not imply team approval.

## Bonus targets

Kubernetes and an AI delivery assistant are independent optional bonuses. Exact additional marks must be checked against the PDF; neither is required to demonstrate the mandatory delivery system. See [Kubernetes](../deployment/kubernetes.md) and [AI scope](../bonus/ai-delivery-assistant.md).

## Acceptance and evidence

The [SRS](srs.md) has 32 FRs and 20 NFRs. The [traceability matrix](requirements-traceability.md) maps all 52 to interfaces, clients, suggested owner roles and drafted test cases. Actual individual owners, assignment verification, design approval and runtime evidence remain pending. The optional internal freeze is **12 November 2026**; it does not replace the external deadline.
