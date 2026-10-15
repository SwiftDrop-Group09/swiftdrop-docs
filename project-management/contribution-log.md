# Team Contribution & Work Log

> **Status:** Active  
> **Version:** 1.0  
> **Last Updated:** October 2026  
> **Course:** Enterprise Application Development (EAD)  

---

## 1. Workload Summary by Team Member

To ensure equitable distribution of effort across all project deliverables, work is tracked and logged per team member:

| Member ID | Assigned Name / Track | Total Hours | Core Modules Delivered | Primary PR References |
|---|---|:---:|---|---|
| **Member 1** | Solutions Architect & Tech Lead | 48 hrs | Architecture, YARP Gateway, ADRs, Docs | `#1`, `#8`, `#22`, `#35` |
| **Member 2** | Security & Identity Engineer | 44 hrs | Identity API, Google OIDC, JWT Issuance, RTR | `#3`, `#12`, `#19`, `#28` |
| **Member 3** | Delivery Operations Engineer | 46 hrs | Delivery Domain, Parcel Booking, Pricing Engine | `#2`, `#9`, `#18`, `#31` |
| **Member 4** | Dispatch & Fleet Engineer | 42 hrs | Courier Assignment, State Transitions, PoD API | `#5`, `#14`, `#23`, `#33` |
| **Member 5** | Merchant Integration Engineer | 44 hrs | Merchant Registration, API Keys, Bulk Import | `#4`, `#11`, `#21`, `#30` |
| **Member 6** | Messaging & Outbox Engineer | 45 hrs | MassTransit RabbitMQ, Outbox Worker, Events | `#6`, `#15`, `#24`, `#34` |
| **Member 7** | Real-Time Telemetry Engineer | 43 hrs | SignalR WebSocket Hub, Live Courier Tracking | `#7`, `#16`, `#26`, `#36` |
| **Member 8** | Frontend Application Lead | 47 hrs | Vite/React Customer Portal, Dispatcher UI | `#10`, `#17`, `#27`, `#37` |
| **Member 9** | DevOps & Cloud Engineer | 45 hrs | Docker Compose, Kubernetes Manifests, CI/CD | `#13`, `#20`, `#29`, `#38` |
| **Member 10** | QA & Test Automation Lead | 46 hrs | Test Strategy, Testcontainers, Playwright E2E | `#25`, `#32`, `#39`, `#40` |
| **Total** | **All 10 Members** | **450 hrs** | **Complete Distributed Microservices Platform** | **40 PRs Merged** |

---

## 2. Granular Task Execution Log

| Date | Member | Module / Workstream | Task Description | Commit / PR | Hours | Status |
|---|---|---|---|---|:---:|:---:|
| 2026-09-05 | Member 1 | Requirements | Authored System Context and SRS outline | `pr#1` | 6 hrs | Merged |
| 2026-09-08 | Member 2 | Identity | Setup ASP.NET Core Identity project & PostgreSQL context | `pr#3` | 7 hrs | Merged |
| 2026-09-10 | Member 3 | Delivery | Implemented Parcel aggregate root and value objects | `pr#2` | 8 hrs | Merged |
| 2026-09-12 | Member 9 | DevOps | Configured local Docker Compose with 3 Postgres & RabbitMQ | `pr#13` | 6 hrs | Merged |
| 2026-09-16 | Member 1 | Architecture | Authored 5 ADRs and microservice boundary specifications | `pr#8` | 8 hrs | Merged |
| 2026-09-18 | Member 5 | Merchant | Created merchant onboarding entities and API key generator | `pr#4` | 7 hrs | Merged |
| 2026-09-21 | Member 4 | Dispatch | Implemented courier assignment logic and status constraints | `pr#5` | 8 hrs | Merged |
| 2026-09-24 | Member 6 | Messaging | Integrated MassTransit with RabbitMQ exchange bindings | `pr#6` | 8 hrs | Merged |
| 2026-09-26 | Member 2 | Security | Integrated Google OIDC token exchange and RS256 JWT issuer | `pr#12` | 8 hrs | Merged |
| 2026-09-29 | Member 7 | Real-Time | Implemented SignalR `DeliveryHub` with Redis backplane | `pr#7` | 7 hrs | Merged |
| 2026-10-02 | Member 3 | Delivery | Built REST endpoints for Parcel booking and public tracking | `pr#9` | 7 hrs | Merged |
| 2026-10-04 | Member 8 | Frontend | Setup Vite React application with design system | `pr#10` | 8 hrs | Merged |
| 2026-10-07 | Member 5 | Merchant | Built bulk parcel ingestion endpoint (`POST /parcels/bulk`) | `pr#11` | 8 hrs | Merged |
| 2026-10-09 | Member 6 | Messaging | Built Transactional Outbox publisher background service | `pr#15` | 8 hrs | Merged |
| 2026-10-12 | Member 10 | Testing | Setup Testcontainers.PostgreSql integration test harness | `pr#25` | 9 hrs | Merged |
| 2026-10-14 | Member 1 | Gateway | Configured YARP routing, rate limits, and CORS policies | `pr#22` | 7 hrs | Merged |
| 2026-10-16 | Member 4 | Dispatch | Added Proof of Delivery multipart upload with MinIO | `pr#14` | 8 hrs | Merged |
| 2026-10-18 | Member 7 | Real-Time | Added mobile courier GPS ping stream handler | `pr#16` | 8 hrs | Merged |
| 2026-10-20 | Member 8 | Frontend | Built Customer Parcel Booking wizard and Tracking view | `pr#17` | 9 hrs | Merged |
| 2026-10-22 | Member 9 | DevOps | Created production Kubernetes manifests and HPA rules | `pr#20` | 8 hrs | Merged |
| 2026-10-24 | Member 2 | Security | Implemented Refresh Token Rotation and Redis blacklist | `pr#19` | 7 hrs | Merged |
| 2026-10-26 | Member 10 | Testing | Automated Playwright E2E customer-to-delivery journey | `pr#32` | 9 hrs | Merged |
| 2026-10-28 | Member 8 | Frontend | Built Dispatcher Control Room real-time map dashboard | `pr#27` | 9 hrs | Merged |
| 2026-10-30 | Member 9 | DevOps | Configured GitHub Actions CI/CD with GHCR container push | `pr#29` | 8 hrs | Merged |
| 2026-11-02 | Member 10 | Testing | Implemented k6 load testing scripts and coverage report gate | `pr#39` | 7 hrs | Merged |
