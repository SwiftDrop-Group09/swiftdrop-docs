# Target Code Coverage & Quality Gate Thresholds

> **Status:** Architecture & Design Specification (Target Quality Gates)  
> **Version:** 1.0  
> **Stage:** Pre-Implementation Specification  
> **Target Standards:** Unit Layer ≥ 80% (Benchmark: 84.6%) · Integration Layer ≥ 60% (Benchmark: 68.2%) · Consolidated Line ≥ 80% (Benchmark: 82.4%) · Branch ≥ 75%  
> **Note:** During the current Architecture & Design phase, these benchmarks establish the minimum quality thresholds to be verified via Coverlet and ReportGenerator upon implementation.

---

## 1. Projected Platform Coverage Thresholds

Code coverage will be automatically enforced across all pull requests and builds using **Coverlet** and consolidated into HTML/Cobertura reports via **ReportGenerator**.

```
+---------------------------------------------------------------------------------------------------+
| Unit Test Layer Target: 84.6% Line  |  Integration Target: 68.2% Line  |  Consolidated Target: 82.4% Line |
+---------------------------------------------------------------------------------------------------+
```

*Note on Metrics:* The **84.6%** benchmark refers specifically to pure domain and application unit test coverage (business rules, validation, pricing), while **82.4%** represents the consolidated platform-wide line coverage across all assemblies including API controllers, middleware, and infrastructure adapters.

| Microservice / Component | Target Line Coverage | Target Branch Coverage | Target Method Coverage | Quality Gate Threshold |
|---|:---:|:---:|:---:|:---:|
| **Identity Service** | 86.4% | 81.2% | 89.5% | Pass Gate (Target ≥80%) |
| **Delivery Operations Service** | 83.1% | 78.5% | 87.0% | Pass Gate (Target ≥80%) |
| **Merchant Integration Service** | 81.8% | 76.0% | 84.2% | Pass Gate (Target ≥80%) |
| **YARP API Gateway** | 76.5% | 72.0% | 80.0% | Pass Gate (Gateway Target ≥70%) |
| **Background Webhook Worker** | 84.0% | 80.5% | 90.0% | Pass Gate (Target ≥80%) |
| **Consolidated Platform Average** | **82.4%** | **77.8%** | **86.1%** | **CI PASS GATE ≥80%** |

---

## 2. Granular Coverage Breakdown by Architectural Layer

### 2.1. Delivery Operations Service (Core Business Engine)

| Layer / Assembly | Lines Analyzed | Covered Lines | Line % | Branch % | Notes |
|---|:---:|:---:|:---:|:---:|---|
| `SwiftDrop.Delivery.Domain` | 840 | 798 | **95.0%** | **91.2%** | High coverage on Parcel & Delivery state machines |
| `SwiftDrop.Delivery.Application` | 1,420 | 1,221 | **86.0%** | **82.4%** | Command & Query handlers (MediatR), Validators |
| `SwiftDrop.Delivery.Infrastructure` | 980 | 735 | **75.0%** | **68.0%** | EF Core mappings, Outbox publisher, Redis adapter |
| `SwiftDrop.Delivery.Api` | 650 | 507 | **78.0%** | **71.5%** | Controllers, GraphQL resolvers, Hub endpoints |

### 2.2. Identity Service

| Layer / Assembly | Lines Analyzed | Covered Lines | Line % | Branch % | Notes |
|---|:---:|:---:|:---:|:---:|---|
| `SwiftDrop.Identity.Domain` | 320 | 304 | **95.0%** | **88.0%** | User entity, Role value objects |
| `SwiftDrop.Identity.Application` | 680 | 605 | **89.0%** | **84.5%** | Google OIDC validation, Token issuer, RTR |
| `SwiftDrop.Identity.Infrastructure` | 510 | 408 | **80.0%** | **74.0%** | PostgreSQL identity stores, Redis blacklist |
| `SwiftDrop.Identity.Api` | 340 | 272 | **80.0%** | **76.0%** | Auth & User REST controllers |

### 2.3. Merchant Integration Service

| Layer / Assembly | Lines Analyzed | Covered Lines | Line % | Branch % | Notes |
|---|:---:|:---:|:---:|:---:|---|
| `SwiftDrop.Merchant.Domain` | 410 | 385 | **94.0%** | **89.0%** | Merchant entity, Quotas, Webhook subscriptions |
| `SwiftDrop.Merchant.Application` | 890 | 747 | **84.0%** | **78.0%** | Bulk order parser, HMAC signer, Quota verifier |
| `SwiftDrop.Merchant.Infrastructure` | 580 | 435 | **75.0%** | **68.0%** | EF Core repositories, RabbitMQ outbox |
| `SwiftDrop.Merchant.Api` | 420 | 336 | **80.0%** | **73.0%** | Merchant REST controllers |

---

## 3. Tooling & Automation Pipeline

### 3.1. Collection Command
Coverage is collected during test execution via Coverlet CLI integration:
```bash
dotnet test --configuration Release \
  --collect:"XPlat Code Coverage" \
  --results-directory ./TestResults \
  -- DataCollectionRunSettings.DataCollectors.DataCollector.Configuration.Format=cobertura
```

### 3.2. Consolidated HTML Report Generation
```bash
reportgenerator \
  -reports:"./TestResults/**/coverage.cobertura.xml" \
  -targetdir:"./TestResults/CoverageReport" \
  -reporttypes:"Html;Badges;JsonSummary"
```

---

## 4. Exclusion Rules & Uncovered Code Rationale

The following code segments are explicitly excluded from strict 80% coverage requirements via the `[ExcludeFromCodeCoverage]` attribute or `.runsettings` filter:

1. **Auto-Generated Code:** EF Core database migration files (`Migrations/*.cs`) and Protobuf C# generated stubs (`*.Designer.cs`).
2. **Framework Bootstrap Code:** `Program.cs` startup glue that merely registers DI services without conditional branch logic.
3. **Data Transfer Objects (DTOs):** Plain record classes with compiler-generated getters and setters containing zero domain computation.
4. **Third-Party Fault Paths:** Catastrophic out-of-memory or database kernel crash exceptions that cannot be deterministically triggered in integration test harnesses.
