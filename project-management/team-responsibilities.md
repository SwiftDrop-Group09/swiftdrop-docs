# Team Organization & Responsibilities Matrix

> **Status:** Active  
> **Version:** 1.0  
> **Last Updated:** October 2026  
> **Course:** Enterprise Application Development (EAD)  

---

## 1. Initial Design Phase: Task Division (5 Primary Deliverables)

For the initial architecture and design milestone (20 Marks), the 10-member team divided the work across the **five primary design areas** specified in the assignment guidelines, working in pairs:

| Design Task # | Deliverable Focus | Scope & Primary Artifacts | Assigned Team Members | Status |
|:---:|---|---|---|:---:|
| **1** | **Architecture Proposal** | Layered microservices proposal, technology justifications (ASP.NET Core 8, YARP, PostgreSQL, RabbitMQ), System Context (C4 Level 1), ADRs, and design pattern rationale | **Member 1 & Member 2** | ✅ Completed |
| **2** | **Use Case Diagrams** | Complete use case models covering all 5 actors (Customer, Merchant, Courier, Dispatcher, Admin) mapped directly to SRS requirements | **Member 3 & Member 4** | ✅ Completed |
| **3** | **ER Diagram & Data Architecture** | Conceptual and physical ER schemas for users, roles, merchants, parcels, couriers, zones, and pricing; database-per-service isolation | **Member 5 & Member 6** | ✅ Completed |
| **4** | **Sequence / Activity Diagrams** | Key workflows: parcel booking, merchant API orders, courier status updates & notifications, and OAuth 2.0 / OIDC login flow | **Member 7 & Member 8** | ✅ Completed |
| **5** | **Integration Design** | Integration patterns (REST, GraphQL, gRPC, RabbitMQ pub/sub, transactional outbox, merchant webhooks with retry, real-time tracking) | **Member 9 & Member 10** | ✅ Completed |

---

## 2. Platform Implementation Phase: Preliminary Roles (To Be Finalized)

*Note: Specific microservice coding assignments, backend modules, and frontend components will be formally locked during the development sprint kickoff meeting.*

| Member | Preliminary Track | Proposed Focus Area | Stage Status |
|---|---|---|:---:|
| **Member 1** | Architecture & Gateway | YARP API Gateway, Routing & Cross-Cutting Concerns | ⏳ In Planning |
| **Member 2** | Security & Auth | Identity Service, Google OIDC, JWT Issuance, Token Blacklist | ⏳ In Planning |
| **Member 3** | Delivery Operations Core | Parcel Aggregate, Booking REST API, EF Core Migrations | ⏳ In Planning |
| **Member 4** | Dispatch & Fleet | Courier Assignment State Machine, Capacity Rules, Proof of Delivery | ⏳ In Planning |
| **Member 5** | Merchant Integration | Merchant API, Bulk Order Ingestion, API Key Hashing | ⏳ In Planning |
| **Member 6** | Messaging & Outbox | RabbitMQ MassTransit Event Broker, Transactional Outbox Worker | ⏳ In Planning |
| **Member 7** | Real-Time Telemetry | SignalR WebSocket Tracking Hub, Live Coordinate Streams | ⏳ In Planning |
| **Member 8** | Frontend Lead | React/Vite SPAs (Customer Portal, Dispatcher Dashboard) | ⏳ In Planning |
| **Member 9** | DevOps & Cloud | Docker Compose, Kubernetes Manifests, CI/CD Pipeline | ⏳ In Planning |
| **Member 10** | QA & Automation | Test Strategy, Testcontainers, xUnit, Playwright E2E | ⏳ In Planning |

---

## 2. RACI Responsibility Assignment Matrix

**RACI Key:**
- **R — Responsible:** The individual who completes the deliverable/task.
- **A — Accountable:** The single individual who approves and has final authority.
- **C — Consulted:** Subject-matter experts providing two-way input.
- **I — Informed:** Individuals kept updated on progress or decisions.

| Deliverable / Workstream | M1 (Arch) | M2 (Id) | M3 (Del) | M4 (Disp) | M5 (Merch) | M6 (Msg) | M7 (Real) | M8 (FE) | M9 (Ops) | M10 (QA) |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Software Architecture Document (SAD)** | **A / R** | C | C | C | C | C | C | C | C | C |
| **Software Requirements Specification (SRS)** | **A** | C | R | R | R | C | C | C | I | C |
| **YARP Gateway Configuration** | **A / R** | C | I | I | I | I | C | C | R | I |
| **Identity Service & Google OIDC** | C | **A / R** | I | I | C | I | I | C | I | C |
| **Parcel Booking & Domain Logic** | C | I | **A / R** | C | C | C | I | C | I | C |
| **Courier Dispatch & Assignment Engine** | C | I | C | **A / R** | I | C | C | C | I | C |
| **Merchant Bulk API & Key Management** | C | C | I | I | **A / R** | C | I | I | I | C |
| **RabbitMQ Event Broker & Outbox Worker** | C | I | C | I | C | **A / R** | C | I | C | C |
| **SignalR Real-Time WebSocket Hub** | C | I | C | C | I | C | **A / R** | C | I | C |
| **Customer & Dispatcher Web Portals** | I | C | C | C | C | I | C | **A / R** | I | C |
| **Docker Compose & Local Infrastructure** | C | I | I | I | I | I | I | I | **A / R** | C |
| **Kubernetes Manifests & Production HPA** | C | I | I | I | I | I | I | I | **A / R** | I |
| **GitHub Actions CI/CD Pipeline** | C | I | I | I | I | I | I | I | **A / R** | C |
| **Automated Test Suite (Unit & Integration)**| C | C | C | C | C | C | C | C | C | **A / R** |
| **End-to-End Testing (Playwright)** | I | I | I | I | I | I | I | C | C | **A / R** |
| **Final Academic Report & Submission** | **A** | R | R | R | R | R | R | R | R | R |

---

## 3. Team Communication & Governance Rules

### 3.1. Meeting Cadence
- **Daily Standup (Async / Discord / Slack):** 15-minute daily check-in (Yesterday's progress, Today's goals, Blockers).
- **Weekly Sprint Planning (Sundays 19:00):** Review milestone progress, unblock dependencies, assign sprint backlog items.
- **Sprint Retrospective & Code Review (Wednesdays 20:00):** Architecture alignment and peer code walk-throughs.

### 3.2. Branching & Pull Request Governance
1. Direct commits to `main` and `develop` are permanently blocked via GitHub branch protection.
2. Every feature branch must follow naming convention: `feat/<module>-<description>` (e.g., `feat/delivery-outbox-publisher`).
3. Every Pull Request requires:
   - At least **2 approving peer reviews**.
   - Mandatory sign-off by the module Accountable (A) member.
   - Successful GitHub Actions CI pass (clean build, linting pass, 0 test failures, ≥80% coverage).
