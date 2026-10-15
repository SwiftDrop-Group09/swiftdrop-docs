# Architecture Decision Records

> **Status:** Active  
> **Last Updated:** October 2026

Architecture Decision Records (ADRs) capture the context, reasoning, and consequences of significant technical decisions made during the SwiftDrop project. Each ADR is a lightweight document that records what was decided, why, and what alternatives were considered.

---

## ADR Index

| ID       | Title                                              | Status    | Date         |
| -------- | -------------------------------------------------- | --------- | ------------ |
| ADR-001  | [Adopt YARP as the API Gateway](#adr-001)          | Accepted  | October 2026 |
| ADR-002  | [Database-per-Service with PostgreSQL](#adr-002)   | Accepted  | October 2026 |
| ADR-003  | [Transactional Outbox for Event Publishing](#adr-003) | Accepted | October 2026 |
| ADR-004  | [Google OIDC with Application-Issued JWTs](#adr-004) | Accepted | October 2026 |
| ADR-005  | [MassTransit over RabbitMQ for Messaging](#adr-005)  | Accepted | October 2026 |

---

## ADR-001

### Adopt YARP as the API Gateway

**Status:** Accepted  
**Date:** October 2026

#### Context

SwiftDrop requires a single entry point for all client applications (React SPA, Flutter mobile, merchant systems). The gateway must handle reverse proxy routing, TLS termination, and request forwarding to multiple backend services.

Options considered:
- **YARP (Yet Another Reverse Proxy)** — Microsoft's .NET-native reverse proxy library.
- **Ocelot** — Popular .NET API gateway framework.
- **nginx / Envoy** — Dedicated reverse proxy solutions.

#### Decision

Adopt **YARP** as the API gateway implemented within an ASP.NET Core host.

#### Rationale

- Native .NET integration: YARP runs as middleware in an ASP.NET Core application, enabling full use of the .NET middleware pipeline (authentication, logging, rate limiting).
- Configuration-driven: Routes and clusters are defined in `appsettings.json` with hot-reload support.
- Performance: YARP is built on `HttpClient` and Kestrel with minimal overhead.
- Team familiarity: The team is already working in the .NET ecosystem, reducing the operational burden.
- Ocelot is less actively maintained and lacks some YARP features (e.g., session affinity, load balancing algorithms).
- nginx/Envoy would introduce a separate technology stack and configuration language.

#### Consequences

- The gateway shares the .NET toolchain with backend services.
- Custom middleware can be added for cross-cutting concerns (correlation IDs, rate limiting).
- The team must manage YARP route configuration as part of the codebase.

---

## ADR-002

### Database-per-Service with PostgreSQL

**Status:** Accepted  
**Date:** October 2026

#### Context

SwiftDrop has three capability APIs (Identity, Delivery Operations, Merchant Integration) and a background Worker host (Notification & Webhook consumers), each with distinct domain responsibilities. A decision is needed on whether to share a single database or isolate data per bounded context.

Options considered:
- **Shared database** with open cross-capability queries.
- **Four private databases** on a single PostgreSQL server with complete schema and user isolation, plus dedicated object storage for proof files.

#### Decision

Each bounded context owns a **dedicated private PostgreSQL database** (`swiftdrop_identity`, `swiftdrop_delivery`, `swiftdrop_merchant`, `swiftdrop_notifications`) with exclusive read/write access and separate migrations, accompanied by protected object storage for delivery proofs.

#### Rationale

- Enforces strict data ownership boundaries — no service can execute cross-capability SQL joins.
- Enables independent schema evolution, migrations, and deployment.
- Reduces failure blast radius and eliminates cross-domain locks.
- Aligns directly with enterprise microservices best practices and the official system architecture diagram.
- Cross-domain data access occurs exclusively through well-defined APIs or asynchronous events.

#### Consequences

- Cross-domain queries require API calls (REST / gRPC), adding minor network latency.
- Distributed ACID transactions are avoided in favor of eventual consistency via the Transactional Outbox.
- Four private databases are managed within the PostgreSQL server container.
- Proof binary assets (signatures, photos) are offloaded to dedicated object storage rather than bloated into relational database rows.

---

## ADR-003

### Transactional Outbox for Event Publishing

**Status:** Accepted  
**Date:** October 2026

#### Context

The Delivery Operations API must publish domain events (e.g., `ParcelBooked`, `DeliveryStatusChanged`) to RabbitMQ after business state changes. Direct publish-after-commit risks message loss if the application crashes between the database commit and the broker publish.

Options considered:
- **Direct publish** after database commit.
- **Transactional outbox** — events are stored in the database within the same transaction, then relayed to the broker.
- **Change Data Capture (CDC)** — database log tailing.

#### Decision

Use a **transactional outbox** pattern where domain events are written to an `outbox_messages` table within the same database transaction as the business state change. A background relay process publishes unpublished messages to RabbitMQ.

#### Rationale

- Guarantees at-least-once delivery without distributed transactions.
- Simpler than CDC infrastructure for the academic scope.
- MassTransit provides built-in outbox support with Entity Framework Core.
- Direct publish is unreliable — network failures between commit and publish cause lost events.

#### Consequences

- Consumers must handle duplicate messages idempotently.
- A background relay process must run continuously.
- Slight delay between state change and event publication (acceptable for the use case).
- The outbox table must be monitored for stuck messages.

---

## ADR-004

### Google OIDC with Application-Issued JWTs

**Status:** Accepted  
**Date:** October 2026

#### Context

SwiftDrop needs user authentication that supports social login and issues application-specific tokens for API authorization.

Options considered:
- **Google OIDC only** — use Google ID tokens directly for API auth.
- **Google OIDC + application JWTs** — use Google for identity verification, then issue SwiftDrop-specific JWTs.
- **Self-hosted identity** (e.g., IdentityServer, Keycloak).

#### Decision

Use **Google OIDC for identity verification** and have the **Identity API issue application-specific JWTs** with custom claims (roles, user ID). The Identity API also exposes a JWKS endpoint for token verification by other services.

#### Rationale

- Separates identity verification (Google) from application authorization (SwiftDrop JWTs).
- Application JWTs can carry custom claims (roles, permissions) that Google tokens cannot.
- Other services verify tokens via the JWKS endpoint without calling the Identity API.
- Refresh sessions allow token renewal without re-authenticating with Google.
- Self-hosted identity providers (Keycloak) are too complex for the academic scope.

#### Consequences

- The Identity API is responsible for JWT key management and rotation.
- All services must validate tokens against the JWKS endpoint.
- Refresh token rotation must be implemented to prevent session hijacking.
- Google credentials (client ID, secret) must be securely configured.

---

## ADR-005

### MassTransit over RabbitMQ for Messaging

**Status:** Accepted  
**Date:** October 2026

#### Context

SwiftDrop requires asynchronous messaging for domain event distribution (delivery status changes, webhook triggers). The team needs to decide between using the RabbitMQ client library directly or using a messaging abstraction.

Options considered:
- **RabbitMQ.Client** — low-level AMQP client.
- **MassTransit** — .NET messaging abstraction supporting RabbitMQ, Azure Service Bus, and others.
- **NServiceBus** — commercial messaging framework.

#### Decision

Use **MassTransit** as the messaging abstraction over RabbitMQ.

#### Rationale

- Provides consumer/publisher abstractions, reducing boilerplate.
- Built-in support for the transactional outbox pattern with EF Core.
- Automatic exchange and queue topology management.
- Supports retry, redelivery, and dead-letter handling out of the box.
- Saga support for multi-step workflows if needed.
- Open source with active community support.
- NServiceBus requires a commercial license.

#### Consequences

- MassTransit adds a dependency and learning curve.
- Exchange/queue naming conventions are managed by MassTransit (can be customized).
- All services consuming messages must reference MassTransit packages.
- Raw RabbitMQ management UI shows MassTransit-managed topology.

---

## Template

New ADRs should follow the format defined in [ADR Template](adr-template.md).
