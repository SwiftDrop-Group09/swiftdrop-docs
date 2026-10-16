# SwiftDrop — Project Documentation

**Enterprise Application Development | Group 09**

Centralized technical documentation, requirements, architecture decisions, integration specifications, and project management resources for the **SwiftDrop Parcel Delivery & Courier Management System**.

[![Documentation](https://img.shields.io/badge/Documentation-In%20Progress-blue)](https://github.com/SwiftDrop-Group09/swiftdrop-docs)
[![Project](https://img.shields.io/badge/Project-SwiftDrop-2E8B57)](https://github.com/SwiftDrop-Group09)
[![GitHub Organization](https://img.shields.io/badge/GitHub-Group%2009-181717?logo=github)](https://github.com/SwiftDrop-Group09)

---

## 1. Project Overview

**SwiftDrop** is an enterprise parcel delivery and courier management platform designed to streamline delivery operations, improve shipment visibility, and support integration with external e-commerce platforms.

The system connects customers, merchants, couriers, dispatchers, and administrators through a unified platform, enabling parcel booking, shipment tracking, delivery management, automated notifications, and third-party integrations.

The project is developed as part of the **Enterprise Application Development** group assignment.

### Key Capabilities

- **Customer Management:** Registration, Google login, parcel booking, fee estimation, real-time tracking, delivery history, and receipts.
- **Merchant Integration:** Merchant onboarding, secured order APIs, webhook notifications, and order management.
- **Courier Operations:** Assigned deliveries, parcel status updates, proof of delivery, and failed delivery reporting.
- **Dispatch Management:** Courier assignment, workload monitoring, and delivery coordination.
- **Administration:** User management, merchant approvals, delivery zones, pricing configurations, and reporting.
- **Enterprise Integration:** REST, GraphQL, gRPC, asynchronous messaging, and real-time communication.
- **Security:** JWT-based authentication, OAuth integration, role-based access control, and secure data handling.

### Project Information

| Property            | Details                            |
| ------------------- | ---------------------------------- |
| Project             | SwiftDrop                          |
| Module              | Enterprise Application Development |
| Group               | Group 09                           |
| Team Size           | 10 Members                         |
| Architecture        | Microservices-based                |
| Development Status  | Planning and Architecture          |
| Submission Deadline | November 15, 2026                  |

---

## 2. Documentation Purpose

This repository serves as the **central source of truth for project-level documentation** across the SwiftDrop development repositories.

Its primary objectives are to:

- Maintain consistent requirements and technical specifications.
- Document architecture decisions and their rationale.
- Define integration protocols and service responsibilities.
- Organize system design diagrams and supporting artifacts.
- Track project milestones, responsibilities, and contributions.
- Maintain testing, deployment, and submission documentation.
- Support collaboration and knowledge sharing among team members.

> **Documentation status:** The reconciled baseline is Proposed and ready for review. Contracts, diagrams, test cases and deployment references describe the intended system; they do not establish implementation completion or team approval. Outstanding verification and approval tasks are recorded in the remaining-work checklist.

---

## 3. Technology Stack

The following technologies represent the current technical direction. Some implementation details and service boundaries remain under review.

| Layer                   | Technologies                            |
| ----------------------- | --------------------------------------- |
| Web Frontend            | React, TypeScript                       |
| Mobile Application      | Flutter Customer and Courier, Dart                           |
| Backend                 | ASP.NET Core, C#                        |
| Database                | PostgreSQL                              |
| API Communication       | REST, GraphQL, gRPC                     |
| Real-Time Communication | Authenticated SSE in Delivery                              |
| Messaging               | RabbitMQ, MassTransit                   |
| Authentication          | JWT, OAuth 2.0 / OpenID Connect         |
| Containerization        | Docker, Docker Compose                  |
| Container Orchestration | Kubernetes (bonus target)               |
| AI Integration          | LLM-based Assistant, MCP (bonus target) |

The authentication implementation, database environments, and final service boundaries will be recorded as architecture decisions once approved.

---

## 4. Documentation Index

Documentation is organized by concern to improve maintainability and navigation.

| Section            | Description                                                        | Entry Point                                            |
| ------------------ | ------------------------------------------------------------------ | ------------------------------------------------------ |
| Requirements       | Assignment scope, SRS, assumptions, and traceability               | [Requirements](requirements/srs.md)                    |
| Architecture       | Technical design, system context, service ownership, and decisions | [Architecture](architecture/technical-design.md)       |
| Integration        | Communication patterns, events, webhooks, and real-time tracking   | [Integration](integration/integration-design.md)       |
| API                | REST, GraphQL, gRPC, and WebSocket documentation                   | [API Reference](api/api-reference.md)                  |
| System Design      | UML, ER, sequence, activity, and architecture diagrams             | [Diagrams](design/diagrams/architecture/README.md)     |
| Security           | Authentication, authorization, and data protection                 | [Security](security/authentication.md)                 |
| Testing            | Test strategy, cases, results, and coverage                        | [Testing](testing/test-strategy.md)                    |
| Deployment         | Local setup, containers, Kubernetes, and CI/CD                     | [Deployment](deployment/local-setup.md)                |
| Project Management | Milestones, team responsibilities, contributions, and risks        | [Project Management](project-management/milestones.md) |
| Submission         | Final report, presentation, demo, and submission checklist         | [Submission](submission/submission-checklist.md)       |
| Bonus Features     | AI Delivery Assistant and related integration                      | [AI Assistant](bonus/ai-delivery-assistant.md)         |

### Architecture Decision Records

Major architectural decisions will be documented using Architecture Decision Records (ADRs).

- [ADR Index](architecture/decisions/README.md)
- [ADR Template](architecture/decisions/adr-template.md)

ADRs should capture the decision context, alternatives considered, selected approach, rationale, and consequences.

---

## 5. System Architecture

SwiftDrop follows a **microservices-based, event-driven architecture**, with independently deployable backend components communicating through synchronous and asynchronous integration patterns.

The proposed architecture separates:

1. **Presentation Layer** — React web application and Flutter mobile application.
2. **API Layer** — External APIs, gateway routing, authentication, and frontend aggregation.
3. **Business Logic Layer** — Domain-oriented backend services handling delivery operations.
4. **Data Layer** — PostgreSQL persistence with service-level data ownership.
5. **Integration Layer** — Internal RPC, message broker, notifications, webhooks, and real-time updates.

### Communication Patterns

| Pattern                | Technology           | Purpose                              |
| ---------------------- | -------------------- | ------------------------------------ |
| Request/Response       | REST / HTTPS         | Public and merchant integrations     |
| Frontend Aggregation   | GraphQL              | Web and mobile queries and mutations |
| Internal RPC           | gRPC                 | Synchronous service communication    |
| Publish/Subscribe      | RabbitMQ             | Asynchronous event distribution      |
| Real-Time Push         | SSE in Delivery           | Live parcel tracking                 |
| Reliable Messaging     | Transactional Outbox | Durable event publication            |
| External Notifications | Webhooks             | Merchant status updates              |

The architecture, integration contracts, and service ownership rules will be finalized and maintained in the relevant documentation sections.

See [Technical Design](architecture/technical-design.md) and [Integration Design](integration/integration-design.md).

---

## 6. GitHub Repository Organization

The SwiftDrop project is distributed across multiple repositories under the [SwiftDrop-Group09 organization](https://github.com/SwiftDrop-Group09).

| Repository                                                                    | Responsibility                                                      |
| ----------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| [swiftdrop-backend](https://github.com/SwiftDrop-Group09/swiftdrop-backend)   | Backend services, gateway, integration contracts, and backend tests |
| [swiftdrop-frontend](https://github.com/SwiftDrop-Group09/swiftdrop-frontend) | React web application                                               |
| [swiftdrop-mobile](https://github.com/SwiftDrop-Group09/swiftdrop-mobile)     | Flutter customer and courier application                            |
| [swiftdrop-infra](https://github.com/SwiftDrop-Group09/swiftdrop-infra)       | Containerization, Kubernetes, and CI/CD configuration               |
| [swiftdrop-docs](https://github.com/SwiftDrop-Group09/swiftdrop-docs)         | Centralized project documentation                                   |

### Documentation Ownership

This repository maintains project-wide requirements, design decisions, architecture documentation, and submission artifacts.

Implementation-specific documentation remains within the corresponding source repository.

**Implementation contracts** belong alongside owning code. This repository now includes validated **design fixtures** for routes, GraphQL, protobuf and events; backend commit parity must be verified before they become an implementation baseline.

---

## 7. Documentation Standards

All contributors should follow consistent documentation practices.

### Formatting

- Use Markdown (`.md`) for textual documentation.
- Maintain clear heading hierarchies.
- Use descriptive, consistent file names in `kebab-case`.
- Prefer relative links for internal documentation references.
- Use tables, diagrams, and examples when they improve clarity.
- Keep terminology consistent across requirements, architecture, and API documentation.

### Documentation Status

Documents should clearly indicate their review status where appropriate.

| Status     | Meaning                                         |
| ---------- | ----------------------------------------------- |
| Draft      | Initial documentation under development         |
| In Review  | Awaiting team feedback or approval              |
| Approved   | Accepted as the current project baseline        |
| Deprecated | Superseded by a newer specification or decision |

Significant changes to approved requirements, service boundaries, or integration contracts should be reviewed and recorded.

### Diagrams

Diagram source files should be preserved in editable formats where practical, such as Mermaid, PlantUML, or diagrams.net.

Exported images or PDFs may be included where necessary for reports and presentations.

### Sensitive Information

Never commit:

- API keys, passwords, tokens, or private credentials.
- Production database connection secrets.
- Sensitive personal data.
- Private configuration files or environment secrets.

Documentation examples should use fictional or sanitized values.

---

## 8. Contributing

All team members are encouraged to maintain documentation alongside their development work.

### Contribution Workflow

1. Clone the documentation repository.

   ```bash
   git clone https://github.com/SwiftDrop-Group09/swiftdrop-docs.git
   cd swiftdrop-docs
   ```

2. Create a descriptive working branch.

   ```bash
   git checkout -b docs/update-architecture
   ```

3. Make the required changes in the appropriate documentation directory.

4. Commit with a meaningful message.

   ```bash
   git add .
   git commit -m "docs: update architecture documentation"
   ```

5. Push the branch.

   ```bash
   git push -u origin docs/update-architecture
   ```

6. Open a Pull Request targeting the agreed baseline branch (`documentation` for this remediation).

7. Request review from the relevant document or component owner before merging.

### Recommended Commit Conventions

| Prefix      | Usage                                                |
| ----------- | ---------------------------------------------------- |
| `docs:`     | Documentation additions and updates                  |
| `fix:`      | Corrections to existing documentation                |
| `refactor:` | Documentation restructuring without changing meaning |
| `chore:`    | Repository maintenance and housekeeping              |

### Pull Request Guidelines

Documentation pull requests should:

- Clearly describe what changed and why.
- Reference related issues or architecture decisions when applicable.
- Update affected links and cross-references.
- Avoid introducing contradictions with approved specifications.
- Receive appropriate review for changes affecting multiple development teams.

---

## 9. Project Coordination

Project milestones, work allocation, risks, and contribution records are maintained in the [Project Management](project-management/milestones.md) section.

Team members are responsible for ensuring that significant implementation changes are reflected in the relevant documentation.

Changes to shared APIs, event contracts, authentication flows, or service ownership should be coordinated with affected contributors before integration.

GitHub Issues and Pull Requests may be used to track documentation tasks, discussions, and reviews.

---

## 10. Testing and Quality Assurance

Testing documentation will cover:

- Backend unit and integration testing.
- Authorization and role-based access tests.
- Event publishing and message consumer tests.
- Merchant webhook integration and retry behavior.
- Frontend and mobile application testing.
- End-to-end delivery workflows.
- Test results and measurable code coverage.

See [Test Strategy](testing/test-strategy.md) and [Coverage Summary](testing/coverage-summary.md).

---

## 11. Deployment Documentation

Deployment documentation will cover development and demonstration environments, including:

- Local environment prerequisites and setup.
- Docker images and Docker Compose orchestration.
- Database and messaging infrastructure configuration.
- Environment variable and secret management.
- Kubernetes deployment for the optional bonus requirement.
- CI/CD and deployment verification.

See [Local Setup](deployment/local-setup.md) and [Kubernetes Deployment](deployment/kubernetes.md).

---

## 12. Assignment Deliverables

The final submission must address the required assessment areas:

| Component                      | Weight |
| ------------------------------ | ------ |
| Design Documentation           | 20%    |
| Implementation                 | 50%    |
| Testing                        | 15%    |
| Presentation and Demonstration | 15%    |

### Bonus Targets

- **Kubernetes Deployment:** Optional bonus; exact additional marks require assignment-PDF verification.
- **AI Delivery Assistant:** Independent optional bonus; exact scoring requires assignment-PDF verification.

### Submission Materials

- Source code repository links and setup instructions.
- Final design documentation in PDF format.
- Architecture, use case, ER, and sequence/activity diagrams.
- Test reports and code coverage summary.
- Individual contribution sheet.
- Functional system demonstration.

**Final Submission Deadline: November 15, 2026**

Track readiness using the [Submission Checklist](submission/submission-checklist.md).

---

## 13. Project Team

**SwiftDrop — Group 09**

Enterprise Application Development Group Assignment

**Team Size:** 10 Members

Individual responsibilities, module ownership, and contribution records will be documented in:

- [Team Responsibilities](project-management/team-responsibilities.md)
- [Contribution Log](project-management/contribution-log.md)

---

**SwiftDrop — Connecting deliveries through modern enterprise technology.**

_Maintained by SwiftDrop Group 09._


## Documentation remediation baseline 2.0

**Status: Proposed; team approval pending.** Outstanding verification, approval and submission tasks are tracked in the [remaining-work checklist](documentation-fix-plan.md). The [decision register](architecture/decisions/README.md) keeps DEC-01–DEC-12 Proposed; no member approval or implementation completion is invented. [Assignment overview](requirements/assignment-overview.md) separates official constraints from team choices; the missing lecturer PDF still requires verification. Assessment is 20 marks overall with 20/50/15/15 category weights.

Canonical design sources are [service catalog](architecture/service-catalog.md), [parcel states](architecture/parcel-state-machine.md), [REST](api/rest-api.md), [events](integration/event-catalog.md), [authentication](security/authentication.md) and [environment matrix](deployment/environments.md). Three APIs + YARP + Worker use four logical DBs on one PostgreSQL instance. GraphQL and SSE live in Delivery; Merchant owns webhook signing/attempts; no cross-service SQL. Redis/GPS/SignalR and bulk ingestion are deferred. React covers all roles/public tracking and Flutter covers Customer **and** Courier. Mandatory receipt, merchant dashboard and Admin reports have explicit interfaces/tests/demo steps.

[Traceability](requirements/requirements-traceability.md) covers **32 FR + 20 NFR = 52** with **68 drafted test cases**, not passing application tests. [Diagram index](design/diagrams/README.md) links sources/exports and four required workflows. [Validation results](testing/documentation-validation.md) record checks actually run; [runtime results](testing/test-results.md) remain unevidenced. [Reference Compose](deployment/docker-compose.md) needs real source images, migrations and secret provisioning before full startup. Named owners/contributions, reviewed PR sign-off and final report submission remain team tasks. External deadline: **15 November 2026**; optional internal freeze: **12 November**.
