# Assignment Overview

> **Status:** Approved  
> **Module:** Enterprise Application Development  
> **Group:** 09 — SwiftDrop  
> **Submission Deadline:** November 15, 2026

---

## 1. Assignment Brief

The Enterprise Application Development group assignment requires the design, implementation, testing, and demonstration of a full-stack enterprise application that applies modern software architecture principles, distributed system patterns, and professional engineering practices.

Each group selects a problem domain and delivers a working system supported by comprehensive design documentation, automated testing, and a live demonstration.

**SwiftDrop** addresses the **Parcel Delivery and Courier Management** domain.

---

## 2. Assessment Criteria

| Component                        | Weight | Description                                                                                       |
| -------------------------------- | ------ | ------------------------------------------------------------------------------------------------- |
| **Design Documentation**         | 20%    | Architecture diagrams, SRS, ER diagrams, sequence/activity diagrams, ADRs, integration design     |
| **Implementation**               | 50%    | Working backend services, frontend, API gateway, database, messaging, authentication, integration  |
| **Testing**                      | 15%    | Unit tests, integration tests, end-to-end tests, coverage reports, test evidence                   |
| **Presentation & Demonstration** | 15%    | Live demo of key workflows, architectural walkthrough, Q&A                                         |

### Bonus Targets

| Bonus Feature              | Additional Marks | Description                                                        |
| -------------------------- | ---------------- | ------------------------------------------------------------------ |
| **Kubernetes Deployment**  | Up to 5          | Container orchestration, scaling, health checks, Ingress routing   |
| **AI Delivery Assistant**  | Up to 5          | LLM-based assistant with tool integration for delivery operations  |

---

## 3. Required Deliverables

### 3.1 Design Documentation

- Software Requirements Specification (SRS)
- System architecture diagrams (high-level and component-level)
- Entity Relationship (ER) diagrams for all data stores
- Sequence diagrams for critical workflows
- Activity diagrams for key business processes
- Use case diagrams for all system actors
- Architecture Decision Records (ADRs)
- Integration design documentation
- Security design (authentication, authorization, data protection)

### 3.2 Implementation

- Microservices-based backend with independently deployable services
- API gateway with reverse proxy routing
- RESTful APIs with appropriate HTTP semantics
- GraphQL API for frontend aggregation
- gRPC for internal service-to-service communication
- Asynchronous messaging with a message broker
- Transactional outbox pattern for reliable event publishing
- Real-time communication (WebSockets or SSE)
- External identity provider integration (OAuth 2.0 / OpenID Connect)
- JWT-based authentication with role-based access control
- Database-per-service data isolation
- Webhook integration for external partner notifications
- Containerized deployment with Docker Compose

### 3.3 Testing

- Unit tests for business logic and domain rules
- Integration tests for API endpoints and data access
- Security tests for authentication and authorization
- End-to-end tests for critical user workflows
- Measurable code coverage reports
- Documented test results and evidence

### 3.4 Presentation and Demonstration

- Architectural overview presentation
- Live demonstration of end-to-end workflows
- Demonstration of enterprise integration patterns
- Individual contribution evidence
- Q&A readiness

---

## 4. Technical Constraints

| Constraint                     | Requirement                                                    |
| ------------------------------ | -------------------------------------------------------------- |
| Backend framework              | ASP.NET Core with C#                                           |
| Database                       | PostgreSQL                                                     |
| Frontend                       | React (web) and/or Flutter (mobile)                            |
| API protocols                  | REST, GraphQL, gRPC required                                   |
| Messaging                      | RabbitMQ or equivalent message broker                          |
| Authentication                 | OAuth 2.0 / OpenID Connect with an external provider           |
| Containerization               | Docker and Docker Compose required                             |
| Version control                | Git with GitHub organization                                   |
| Documentation format           | Markdown with diagrams (Mermaid, PlantUML, or diagrams.net)    |

---

## 5. Team Composition

| Property      | Details                            |
| ------------- | ---------------------------------- |
| Group         | Group 09                           |
| Team Size     | 10 Members                         |
| Project Name  | SwiftDrop                          |
| Organization  | [SwiftDrop-Group09](https://github.com/SwiftDrop-Group09) |

Individual responsibilities and module ownership are documented in [Team Responsibilities](../project-management/team-responsibilities.md).

---

## 6. Key Dates

| Milestone                       | Target Date         |
| ------------------------------- | ------------------- |
| Project kickoff and scaffolding | Week 1              |
| Requirements and architecture   | Week 2–3            |
| Core implementation sprint      | Week 4–7            |
| Integration and testing sprint  | Week 8–9            |
| Documentation finalization      | Week 10             |
| Presentation rehearsal          | Week 11             |
| **Final Submission**            | **November 15, 2026** |

See [Milestones](../project-management/milestones.md) for detailed phase planning.

---

## References

- [Software Requirements Specification](srs.md)
- [Scope and Assumptions](scope-and-assumptions.md)
- [Technical Design](../architecture/technical-design.md)
- [Submission Checklist](../submission/submission-checklist.md)
