# Data Protection & Privacy Architecture

> **Status:** Draft  
> **Version:** 1.0  
> **Last Updated:** October 2026  

---

## 1. Overview

SwiftDrop processes Personally Identifiable Information (PII) including recipient names, phone numbers, delivery addresses, and biometric Proof-of-Delivery signatures. The data protection architecture implements **defense-in-depth**, ensuring end-to-end cryptographic protection across data in transit, data at rest, and data in use, adhering to GDPR, Sri Lankan Data Protection Act, and industry cybersecurity standards.

---

## 2. Data Classification Taxonomy

| Classification Tier | Data Types & Fields | Storage Requirements | Retention Period | Access Restrictions |
|---|---|---|---|---|
| **Restricted (PII)** | Recipient phone numbers, street addresses, recipient signatures, GPS coordinates | Column-level AES-256 encryption at rest; masked in logs | 90 days post-delivery completion | Least-privilege access; logged in audit trail |
| **Confidential** | Merchant API key hashes, webhook secrets, billing amounts, contract rates | Cryptographically hashed (SHA-256) or encrypted with envelope keys | Lifetime of merchant contract | Restricted to automated billing & tenant services |
| **Internal** | Service logs, correlation IDs, event payloads, parcel dimensions, internal notes | Encrypted at storage volume level | 30 days active; 365 days cold archive | Internal engineering & operations staff |
| **Public** | Public tracking status (`InTransit`, `Delivered`), destination city, estimated arrival window | Standard unencrypted database fields | Indefinite / 1 year | Publicly readable via tracking number |

---

## 3. Cryptography & Encryption Standards

### 3.1. Encryption in Transit
- **Public Edge to YARP Gateway:** Enforced **TLS 1.3** (fallback to TLS 1.2 with strict cipher suites: `TLS_AES_256_GCM_SHA384`, `ECDHE-RSA-AES256-GCM-SHA384`). Plain HTTP traffic is permanently redirected (HTTP 301) with HTTP Strict Transport Security (HSTS) enabled:
  ```http
  Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
  ```
- **Internal Service-to-Service:** Inter-service gRPC connections enforce mutual TLS (mTLS) with short-lived certificates issued by HashiCorp Vault.
- **Message Broker & Databases:** AMQP over TLS (port 5671) for RabbitMQ; SSL Mode `Require` for all PostgreSQL connections.

### 3.2. Encryption at Rest
- **Database Storage Volumes:** EBS / Persistent Volumes encrypted using AES-256 block-level encryption managed via KMS.
- **Application Column-Level Encryption:** Sensitive PII columns (recipient phone numbers, exact delivery street addresses) utilize ASP.NET Core Data Protection API with AES-256-GCM authenticated encryption:
  ```csharp
  // EF Core Value Converter for Transparent PII Column Encryption
  public class EncryptedStringConverter : ValueConverter<string, string>
  {
      public EncryptedStringConverter(IDataProtector protector)
          : base(
              plainText => protector.Protect(plainText),
              cipherText => protector.Unprotect(cipherText))
      { }
  }
  ```
- **Object Storage (PoD Signatures & Photos):** S3/MinIO bucket-level server-side encryption (`SSE-S3` or `SSE-KMS`) with private access policies and short-lived pre-signed URLs (15-minute expiration).

---

## 4. Secrets Management & Key Lifecycle

Hardcoded credentials, passwords, and API keys are strictly prohibited across all codebases and configuration files.

- **Development Environment:** Local development uses .NET `User-Secrets` and sanitized `.env` files (excluded via `.gitignore`).
- **Production / Staging:** Centralized key management via Azure Key Vault or HashiCorp Vault injected into container pods at runtime as ephemeral environment variables.
- **Key Rotation Policy:**
  - Token signing RSA key pairs: Rotated every **90 days**.
  - Database master passwords: Rotated every **180 days**.
  - Merchant API keys: Generated on demand with automated instant revocation capabilities.

---

## 5. Privacy, Anonymization & Log Sanitization

### 5.1. Sensitive Log Masking
Logging frameworks (Serilog) are configured with destructive destructurers and masking enrichers to guarantee that PII and tokens are never emitted to stdout or Elasticsearch:

| Field Name | Raw Value | Emitted Log Value |
|---|---|---|
| `Authorization` | `Bearer eyJhbGciOi...` | `[REDACTED_BEARER_TOKEN]` |
| `phoneNumber` | `+94771234567` | `+9477****567` |
| `apiKey` | `sk_live_8f0a39c4...` | `sk_live_****` |
| `signature` | `data:image/png;base64,...` | `[BASE64_IMAGE_DATA]` |

### 5.2. Right to Be Forgotten & Data Retention
Upon delivery completion + 90 days:
1. Automated background maintenance jobs purge recipient street addresses and recipient telephone numbers, replacing them with irreversible hashes.
2. Photographic and signature Proof of Delivery files stored in MinIO/S3 are moved to Glacier cold archival or permanently purged according to regulatory requirements.
3. High-level delivery metrics (weight, zone, city, delivery duration) are retained for aggregated machine learning and operations reporting.

---

## 6. Defensive Coding & Injection Prevention

- **SQL Injection Prevention:** 100% of database interactions occur through **Entity Framework Core 8** using parameterized queries and prepared statements. Dynamic string concatenation in SQL queries is banned and enforced via SonarQube static analysis.
- **Input Sanitization & Validation:** All incoming HTTP requests pass through declarative **FluentValidation** rules validating data types, string length bounds, postal code regex patterns, and stripping malicious HTML/script tags before reaching service logic.
- **Cross-Site Scripting (XSS) & Content Security:** Standard security headers emitted by YARP Gateway:
  ```http
  X-Content-Type-Options: nosniff
  X-Frame-Options: DENY
  Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline';
  Referrer-Policy: strict-origin-when-cross-origin
  ```
