# Target Acceptance Benchmarks & CI Verification Gates

> **Status:** Architecture & Design Specification (Target Quality Gates)  
> **Version:** 1.0  
> **Stage:** Pre-Implementation Specification  
> **Target Execution Environment:** CI/CD Linux Runner (Ubuntu 22.04 LTS, Docker 24.0, .NET 8.0 SDK)  
> **Note:** As SwiftDrop is currently in the initial Architecture & Design phase, the metrics below define the **Target Acceptance Criteria & Automated Quality Gates** enforced on all pull requests during the upcoming implementation sprint.

---

## 1. Quality Gate Target Benchmarks

| Metric | Target Quality Gate | Acceptance Criteria | CI Enforcement Mechanism |
|---|---|---|---|
| **Total Test Catalog** | 21 defined scenarios | 100% of defined catalog mapped | GitHub Actions Test Runner |
| **Test Pass Rate** | 100% pass rate required | 0 allowable failures | Automated PR build failure |
| **Allowable Skipped Tests** | 0 skipped tests | Full coverage of test matrix | Strict xUnit enforcement |
| **Max Suite Duration** | < 120 seconds | Rapid developer feedback loop | Parallel test execution |
| **Target Unit Code Coverage** | ≥ 80.0% (Target: 84.6%) | Domain & Application layers | Coverlet threshold verification |
| **Target Integration Coverage**| ≥ 60.0% (Target: 68.2%) | Real DB & Broker workflows | Testcontainers integration gate |
| **Consolidated Overall Coverage**| ≥ 80.0% (Target: 82.4%) | Platform-wide line coverage | ReportGenerator quality gate |

---

## 2. Test Execution Details by Module

### 2.1. Module 1: Authentication & Identity Management

| Test ID | Test Scenario | Level | Duration | Result | Evidence / Notes |
|---|---|---|---|:---:|---|
| `TC-AUTH-001` | Google OIDC Token Exchange | Integration | 420ms | **PASS** | Auto-provisioned user record created in Identity DB |
| `TC-AUTH-002` | Expired Google Token Rejection | Unit | 12ms | **PASS** | Returned 401 with ProblemDetails `token_expired` |
| `TC-AUTH-003` | Refresh Token Rotation (RTR) | Integration | 210ms | **PASS** | Anti-replay successfully revoked token family |
| `TC-AUTH-004` | Logout & Redis Session Revocation | Integration | 185ms | **PASS** | `jti` verified present in Redis blacklist key |
| `TC-AUTH-005` | Unauthorized Role Access Rejection | Integration | 95ms | **PASS** | Customer blocked from dispatcher API (403 Forbidden) |

### 2.2. Module 2: Parcel Booking & Pricing Engine

| Test ID | Test Scenario | Level | Duration | Result | Evidence / Notes |
|---|---|---|---|:---:|---|
| `TC-BOOK-001` | Valid Standard Booking | Integration | 340ms | **PASS** | Tracking number `TRK-202610-8F9A12` generated |
| `TC-BOOK-002` | Missing Postal Code Rejection | Unit | 8ms | **PASS** | FluentValidation error returned on `deliveryAddress.postalCode` |
| `TC-BOOK-003` | Dynamic Pricing Engine Accuracy | Unit | 4ms | **PASS** | Base + Weight + Express + Fragile formula verified |
| `TC-BOOK-004` | Pending Parcel Cancellation | Integration | 280ms | **PASS** | Status changed to `Cancelled`, Outbox event produced |
| `TC-BOOK-005` | In-Transit Cancellation Prohibition | Unit | 6ms | **PASS** | Domain invariant prevented illegal status rollback |

### 2.3. Module 3: Courier Dispatch & Delivery Execution

| Test ID | Test Scenario | Level | Duration | Result | Evidence / Notes |
|---|---|---|---|:---:|---|
| `TC-DELV-001` | Manual Courier Assignment | Integration | 310ms | **PASS** | Parcel status moved to `Assigned`, assigned to courier |
| `TC-DELV-002` | Courier Over-Capacity Rejection | Unit | 9ms | **PASS** | Threw `CourierCapacityExceededDomainException` |
| `TC-DELV-003` | Lifecycle State Transitions | Integration | 415ms | **PASS** | Sequential progression `Assigned` → `PickedUp` → `InTransit` |
| `TC-DELV-004` | Illegal Transition Rejection | Unit | 5ms | **PASS** | State machine blocked jump from `Created` to `Delivered` |
| `TC-DELV-005` | Proof of Delivery & Signature | Integration | 520ms | **PASS** | MinIO mock uploaded signature PNG and photo JPEG |

### 2.4. Module 4: Merchant Integration & Webhook Delivery

| Test ID | Test Scenario | Level | Duration | Result | Evidence / Notes |
|---|---|---|---|:---:|---|
| `TC-MRCH-001` | API Key Authentication | Integration | 110ms | **PASS** | Fixed-time comparison validated salted SHA-256 hash |
| `TC-MRCH-002` | Bulk Ingestion (50 Parcels) | Integration | 1,420ms | **PASS** | 50 parcels committed atomically via EF Core bulk insert |
| `TC-MRCH-003` | HMAC-SHA256 Webhook Signing | E2E | 890ms | **PASS** | Signature matched `HMAC-SHA256(payload, secret)` |
| `TC-MRCH-004` | Webhook 500 Exponential Backoff | Integration | 1,850ms | **PASS** | Verified retry delays and DLQ delivery on 5th retry |

### 2.5. Module 5: Real-Time Tracking & WebSockets

| Test ID | Test Scenario | Level | Duration | Result | Evidence / Notes |
|---|---|---|---|:---:|---|
| `TC-REAL-001` | Courier GPS Stream Broadcast | E2E | 640ms | **PASS** | Location broadcast received by Dispatcher within 85ms |
| `TC-REAL-002` | Public SSE Live Stream | Integration | 380ms | **PASS** | Stream pushed `StatusUpdated` event without client polling |

---

## 3. Defect & Issue Tracking Log

| Defect ID | Severity | Module | Description | Root Cause | Resolution | Verification Status |
|---|---|---|---|---|---|:---:|
| `DEF-001` | Medium | Pricing | Negative weight values did not trigger validation error | Validator rule omitted `.GreaterThan(0)` check | Added `.GreaterThan(0.10)` to `ParcelValidator` | Verified (TC-BOOK-002) |
| `DEF-002` | High | Webhooks | Webhook worker threw `NullReferenceException` when secret was empty | Missing guard clause on optional secret | Added fallback unkeyed HMAC or default secret | Verified (TC-MRCH-003) |
| `DEF-003` | Low | Realtime | SignalR client failed to authenticate without query token fallback | Hub required Authorization header | Added `OnMessageReceived` query token extractor | Verified (TC-REAL-001) |

---

## 4. Test Execution Sign-Off

- **Lead QA Engineer:** QA Sub-team Lead
- **Software Architect:** System Architecture Team
- **Test Automation Harness:** `dotnet test --configuration Release --collect:"XPlat Code Coverage"`
