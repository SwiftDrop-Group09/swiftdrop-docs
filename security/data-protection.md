# Data Protection

> Status: Proposed baseline 2.0 · Design controls; deployment evidence pending

Public tracking uses an allowlisted summary only: tracking number, canonical status, coarse origin/destination city, update time and fixed redacted timeline. It never exposes contact data, complete address, precise location, courier identity, private notes, proof or receipt. Random tracking IDs and rate limits reduce enumeration but do not replace minimization. Private endpoints enforce resource ownership on every request and download.

Secrets and sensitive configuration are injected locally through ignored `.env`/mounted secret files, not versioned plaintext. Use separate DB/broker accounts per workload. API keys/passwords/refresh tokens are one-way hashed; **webhook signing secrets are authenticated-encrypted with key version** so Merchant alone can decrypt for HMAC. Signing/encryption private keys are mounted outside images and repository. Logs use correlation/resource IDs and safe error codes; redact Authorization, cookies, API keys, signatures, query secrets and request bodies.

Non-loopback external traffic requires HTTPS; configured ingress certs and client trust are prerequisites for mobile/remote tests. Loopback HTTP examples are a local-only convenience. Internal HTTP/h2c exists only in isolated local Compose; nonlocal service traffic requires TLS and service JWT. Private object storage accepts only Delivery credentials and private buckets; all proof/receipt delivery is authorized server streaming. Stage/cleanup rules prevent failed uploads falsely completing delivery. See [data architecture](../architecture/data-architecture.md).

Notification events contain IDs and statuses only; Worker resolves minimum recipient IDs through scoped Delivery API. Provider fixtures must use fictional recipients. Webhook sends reject SSRF targets, bind validated DNS addresses, prohibit redirects and apply time/size limits. See [webhook security](../integration/merchant-webhooks.md).

Retain only academic demonstration data until the team approves a retention policy. Proposed 30-day attempt/log retention and 24h orphan cleanup are targets, not claims of configured automation. Backups must be encrypted with a tested restore. QA must record privacy, access-control, dependency-secrets and retention evidence before sign-off; no compliance certification is asserted.
