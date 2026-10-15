# Project Risk Management & Risk Register

> **Status:** Active  
> **Version:** 1.0  
> **Last Updated:** October 2026  
> **Course:** Enterprise Application Development (EAD)  

---

## 1. Risk Assessment Methodology

Risks are categorized across **Technical**, **Operational/Team**, and **Security** domains. Each risk is evaluated using a standard 5×5 Probability and Impact matrix:

$$\text{Risk Score} = \text{Probability (1–5)} \times \text{Impact (1–5)}$$

- **Low (Score 1–6):** Managed through standard operational procedures.
- **Medium (Score 8–12):** Requires active mitigation and sprint-level monitoring.
- **High (Score 15–25):** Critical architectural or timeline threat requiring immediate contingency planning.

---

## 2. Comprehensive Risk Register

| Risk ID | Category | Risk Description | Prob (1-5) | Imp (1-5) | Score | Mitigation Strategy | Contingency Plan | Risk Owner | Status |
|---|---|---|:---:|:---:|:---:|---|---|:---:|:---:|
| **RSK-TEC-01** | Technical | **Distributed Dual-Write Inconsistency:** Database commits succeeding while RabbitMQ publish fails. | 4 | 4 | **16 (High)** | Implement the **Transactional Outbox Pattern** saving events in the same database transaction as domain changes. | Background Outbox Worker retries publishing with exponential backoff and DLQ alerting. | Member 6 | Active / Mitigated |
| **RSK-TEC-02** | Technical | **High-Frequency WebSocket Backpressure:** Large influx of courier GPS points saturating backend memory. | 3 | 4 | **12 (Med)** | Throttle client GPS emissions to 5-second intervals; utilize Redis Pub/Sub backplane for horizontal fanout. | Fall back to Server-Sent Events (SSE) or HTTP polling if WebSocket handshake fails. | Member 7 | Active / Mitigated |
| **RSK-TEC-03** | Technical | **PostgreSQL Connection Exhaustion:** Multiple microservices exhausting connection pool during bulk ingestion. | 3 | 3 | **9 (Med)** | Configure connection pooling limits in Npgsql; implement asynchronous I/O and bulk insert batching. | Deploy PgBouncer connection pooler in front of database instances. | Member 3 | Monitored |
| **RSK-SEC-01** | Security | **Merchant API Key Compromise:** Raw API keys leaked in logs or client-side storage. | 2 | 5 | **10 (Med)** | Store only salted SHA-256 hashes of API keys; mask credentials in Serilog; provide instant one-click key revocation in merchant dashboard. | Automated script to immediately revoke compromised key and alert merchant contact email. | Member 2 | Active / Mitigated |
| **RSK-SEC-02** | Security | **Refresh Token Replay / Theft:** Malicious actor intercepting unencrypted refresh token. | 2 | 4 | **8 (Med)** | Enforce Refresh Token Rotation (RTR); revoke entire token family if an invalidated token is re-submitted; store jti in Redis. | Immediate user session lockout requiring fresh Google OIDC sign-in. | Member 2 | Active / Mitigated |
| **RSK-OPS-01** | Operations | **Team Member Workload Imbalance:** Unequal sprint velocity leading to delayed module delivery. | 3 | 4 | **12 (Med)** | Maintain strict RACI matrix and weekly sprint reviews; pair-programming on complex cross-cutting modules (YARP, MassTransit). | Reallocate secondary assignees or descope optional bonus features to protect core MVP. | Member 1 | Active / Monitored |
| **RSK-OPS-02** | Operations | **Testcontainers CI Pipeline Timeouts:** Docker spin-up delays causing GitHub Actions to exceed timeout bounds. | 3 | 3 | **9 (Med)** | Cache base Docker images (`postgres:16-alpine`, `rabbitmq:3-alpine`) in GitHub Actions cache; optimize test database initialization scripts. | Run integration tests against persistent pre-warmed staging database on self-hosted runner. | Member 9 | Active / Mitigated |
| **RSK-EXT-01** | External | **Google OIDC Sandbox Rate Limiting:** Third-party OAuth quota exhausted during automated integration testing. | 2 | 3 | **6 (Low)** | Mock Google OIDC token validation endpoint during automated CI test suite; restrict live Google OAuth to manual QA. | Switch to pre-generated test JWT keys during integration test runs. | Member 10 | Mitigated |

---

## 3. Monitoring & Review Process

The Risk Register is reviewed bi-weekly during sprint planning. Any risk whose score increases into the **High (15–25)** category triggers an immediate architectural review meeting with the Solutions Architect and relevant module leads.
