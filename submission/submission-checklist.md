# SwiftDrop Submission Deliverables & Team Task Checklist

> **Course:** Enterprise Application Development (EAD)  
> **Assignment:** Group Project — Parcel Delivery & Courier Management System  
> **Weightage:** 100 Marks (Design 20% · Implementation 50% · Testing 15% · Presentation 15%)  
> **Group Size:** 10 Members  
> **Current Stage:** Architecture & Design Submission Phase  

---

## 1. Project Phase & Evaluation Overview

The assessment is divided into four evaluation components according to the official assignment syllabus:

```
+-----------------------------------------------------------------------------------+
| 1. Design Documentation (20m) | 2. Implementation (50m) | 3. Testing (15m) | 4. Viva / Demo (15m) |
|          [COMPLETED]           |      [IN PLANNING]      |   [IN PLANNING]  |     [SCHEDULED]     |
+-----------------------------------------------------------------------------------+
```

> **Note on Project Status:** At this initial reporting and architecture design stage, the team focused on establishing the architectural foundations, technical proposals, and complete design diagrams. Development assignments, coding, and live test executions will be finalized during the upcoming development sprint.

---

## 2. Deliverables Verification Checklist

### 2.1. Category 1: Design Documentation (20 Marks / 20% Weightage) — [COMPLETED]

The 10-member team divided the design phase work across the **five primary design deliverables** specified in the assignment guideline (assigned in pairs):

| Task # | Design Deliverable Area | Scope & Key Artifacts Included | Assigned Team Members | Status |
|:---:|---|---|:---:|:---:|
| **1** | **Architecture Proposal** | Layered microservices proposal, presentation/business/data tiers, technology justifications (ASP.NET Core 8, YARP, PostgreSQL, RabbitMQ), System Context (C4 Level 1), ADRs, and SOLID/GoF design pattern justifications.<br/>• [`architecture/system-context.md`](../architecture/system-context.md)<br/>• [`architecture/technical-design.md`](../architecture/technical-design.md)<br/>• [`architecture/service-catalog.md`](../architecture/service-catalog.md)<br/>• [`architecture/decisions/README.md`](../architecture/decisions/README.md) | Member 1 & Member 2 | ✅ Complete |
| **2** | **Use Case Diagrams** | Comprehensive use case models covering all 5 system actors (Customer, Merchant, Courier, Dispatcher, Administrator) with detailed actor interactions mapped directly to SRS requirements.<br/>• [`design/diagrams/use-cases/README.md`](../design/diagrams/use-cases/README.md)<br/>• [`requirements/srs.md`](../requirements/srs.md) | Member 3 & Member 4 | ✅ Complete |
| **3** | **ER Diagram & Data Architecture** | Conceptual and physical Entity Relationship diagrams covering users, roles, merchants, parcels, status history, couriers, zones, and pricing tiers. Database-per-service isolation and schema ownership rules.<br/>• [`design/diagrams/er/README.md`](../design/diagrams/er/README.md)<br/>• [`architecture/data-architecture.md`](../architecture/data-architecture.md) | Member 5 & Member 6 | ✅ Complete |
| **4** | **Sequence & Activity Diagrams** | UML Sequence and Activity diagrams for all mandatory assignment workflows:<br/>1. Customer delivery creation & fee estimation<br/>2. Merchant API order submission<br/>3. Courier status update triggering notifications & webhooks<br/>4. Google OAuth 2.0 / OIDC login flow<br/>• [`design/diagrams/sequence/README.md`](../design/diagrams/sequence/README.md)<br/>• [`design/diagrams/activity/README.md`](../design/diagrams/activity/README.md) | Member 7 & Member 8 | ✅ Complete |
| **5** | **Integration Design** | Identification and justification of integration patterns (Request/Reply REST APIs, GraphQL BFF, gRPC inter-service RPC, RabbitMQ Pub/Sub broker, Transactional Outbox pattern, and outbound HMAC-signed merchant webhooks with retry).<br/>• [`integration/integration-design.md`](../integration/integration-design.md)<br/>• [`integration/event-catalog.md`](../integration/event-catalog.md)<br/>• [`integration/merchant-webhooks.md`](../integration/merchant-webhooks.md)<br/>• [`integration/realtime-tracking.md`](../integration/realtime-tracking.md) | Member 9 & Member 10 | ✅ Complete |

---

### 2.2. Category 2: Platform Implementation (50 Marks / 50% Weightage) — [DEVELOPMENT PHASE]

*Implementation roles, code ownership, and repository branch allocations will be decided in the sprint planning meeting following design approval.*

| Workstream ID | Implementation Workstream | Planned Scope & Target Components | Assigned Developers | Status |
|:---:|---|---|:---:|:---:|
| `IMP-01` | **API Gateway & Routing** | YARP reverse proxy, route configurations, rate limiting, and CORS policies | *To be decided (Sprint 1)* | ⏳ In Planning |
| `IMP-02` | **Identity & Access Service** | ASP.NET Core Identity, Google OIDC token exchange, RS256 JWT generation | *To be decided (Sprint 1)* | ⏳ In Planning |
| `IMP-03` | **Delivery Operations Service** | Parcel aggregate, booking CRUD, dynamic pricing calculator, EF Core migrations | *To be decided (Sprint 2)* | ⏳ In Planning |
| `IMP-04` | **Courier & Dispatch Engine** | Courier assignment state machine, workload monitoring, Proof of Delivery (PoD) | *To be decided (Sprint 2)* | ⏳ In Planning |
| `IMP-05` | **Merchant Integration Service** | API key generation & hashing, bulk parcel endpoint, merchant quota checks | *To be decided (Sprint 2)* | ⏳ In Planning |
| `IMP-06` | **Event Broker & Webhook Worker** | RabbitMQ MassTransit integration, Transactional Outbox publisher, Webhook retry | *To be decided (Sprint 3)* | ⏳ In Planning |
| `IMP-07` | **Real-Time Notification & Tracking** | SignalR WebSocket hub / Server-Sent Events (SSE) tracking feed | *To be decided (Sprint 3)* | ⏳ In Planning |
| `IMP-08` | **Frontend Web Application** | Responsive React/Vite SPA for customers, merchants, and dispatch control room | *To be decided (Sprint 4)* | ⏳ In Planning |

---

### 2.3. Category 3: Testing & Quality Assurance (15 Marks / 15% Weightage) — [PLANNED]

| QA ID | Quality Assurance Deliverable | Planned Scope & Specifications Link | Target Benchmark | Status |
|:---:|---|---|:---:|:---:|
| `QA-01` | **Testing Strategy** | Testing pyramid design, tooling selection, CI automation gates<br/>• [`testing/test-strategy.md`](../testing/test-strategy.md) | Pyramid Defined | ✅ Strategy Defined |
| `QA-02` | **Test Cases Specification** | Functional test scenarios mapped to SRS requirements<br/>• [`testing/test-cases.md`](../testing/test-cases.md) | 21 Scenarios Defined | ✅ Test Catalog Ready |
| `QA-03` | **Automated Test Suite** | xUnit unit tests + Testcontainers integration tests for real DB and RabbitMQ | 100% Pass Rate | ⏳ Implementation Phase |
| `QA-04` | **Code Coverage Target** | Automated coverage enforcement via Coverlet in GitHub Actions | ≥ 80% Business Logic | ⏳ Enforced in CI |
| `QA-05` | **Requirements Traceability** | Traceability matrix: SRS Requirement → Service API → Test Scenario<br/>• [`requirements/requirements-traceability.md`](../requirements/requirements-traceability.md) | 32 FRs + 17 NFRs | ✅ Baseline Mapped |

---

### 2.4. Category 4: Presentation, Viva & Final Report (15 Marks / 15% Weightage) — [SCHEDULED]

| Deliverable ID | Final Deliverable | Scope & Structure | Assigned Lead | Status |
|:---:|---|---|:---:|:---:|
| `SUB-01` | **Live Demonstration Plan** | 15-minute viva demonstration script across 5 core user journeys, Q&A defense prep<br/>• [`submission/demo-plan.md`](./demo-plan.md) | Team Lead | 📝 Script Draft Ready |
| `SUB-02` | **Final Academic Report** | Comprehensive academic report synthesising architecture, trade-offs, security, and reflections<br/>• [`submission/final-report.md`](./final-report.md) | All Members | 📝 Draft Structure Ready |
| `SUB-03` | **Deployment Package** | Docker Compose one-command orchestration for live demonstration<br/>• [`deployment/docker-compose.md`](../deployment/docker-compose.md) | DevOps Track | ⏳ Testing Configuration |
| `SUB-04` | **Source Code Repository** | Tagged release on GitHub (`v1.0.0-final`) with clean git commit history | All Members | ⚪ Scheduled at Code Freeze |

---

## 3. Initial Architecture & Design Milestone Sign-Off

- [x] **Architecture Proposal Complete:** Microservices topology with YARP gateway, ASP.NET Core, PostgreSQL, and RabbitMQ fully defined.
- [x] **Use Case Diagrams Complete:** Actors (Customer, Merchant, Courier, Dispatcher, Admin) documented with clear use case models.
- [x] **ER Diagrams Complete:** Entity relationship schemas documented for all bounded database contexts.
- [x] **Sequence & Activity Diagrams Complete:** Booking, merchant API, courier delivery, and OAuth 2.0 flows mapped.
- [x] **Integration Design Complete:** Synchronous REST/gRPC and asynchronous outbox pub/sub patterns specified.
- [x] **Task Distribution Documented:** Workload equitably partitioned among all 10 group members.
- [ ] **Development Sprint Kickoff:** Implementation task assignment to be finalized following design review.
