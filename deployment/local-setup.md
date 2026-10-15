# Local Development Setup Guide

> **Status:** Draft  
> **Version:** 1.0  
> **Last Updated:** October 2026  

---

## 1. Prerequisites & Tooling Requirements

Before setting up SwiftDrop on your workstation, verify that the following runtimes and tools are installed:

| Tool / Runtime | Minimum Version | Verification Command | Purpose |
|---|---|---|---|
| **.NET SDK** | `8.0.x` | `dotnet --version` | Backend microservices, YARP gateway, EF Core |
| **Node.js & npm** | `v20.x LTS` / `npm v10+` | `node -v && npm -v` | Frontend SPAs (Vite/React dashboards) |
| **Docker Desktop / Engine** | `24.0+` with Compose v2 | `docker compose version` | Local infrastructure (Postgres, RabbitMQ, Redis) |
| **Git** | `2.40+` | `git --version` | Version control |
| **curl / httpie / Postman** | Latest | `curl --version` | API testing and endpoint verification |

---

## 2. Step-by-Step Repository Setup

### 2.1. Clone Repository & Submodules
```bash
git clone https://github.com/swiftdrop/swiftdrop-platform.git
cd swiftdrop-platform
```

### 2.2. Environment Configuration
Create a local `.env` file from the provided template:
```bash
cp .env.example .env
```

Review key configuration variables in `.env`:
```ini
# Core Environment
ASPNETCORE_ENVIRONMENT=Development
DOTNET_SYSTEM_GLOBALIZATION_INVARIANT=false

# Ports
GATEWAY_PORT=5000
IDENTITY_PORT=5001
DELIVERY_PORT=5002
MERCHANT_PORT=5003
RABBITMQ_UI_PORT=15672

# Database Passwords (Local Dev Defaults)
POSTGRES_USER=postgres
POSTGRES_PASSWORD=swiftdrop_dev_secret

# JWT Secret & Keys (Dev Only)
JWT_ISSUER=https://identity.swiftdrop.io
JWT_AUDIENCE=https://api.swiftdrop.io
GOOGLE_CLIENT_ID=your-dev-google-client-id.apps.googleusercontent.com
```

---

## 3. Launching Infrastructure via Docker Compose

To run the supporting databases, message broker, and caching layer locally without running full microservice containers:

```bash
# Start all infrastructure backing services
docker compose -f docker-compose.infra.yml up -d

# Verify all containers are healthy
docker compose -f docker-compose.infra.yml ps
```

This spins up:
- **`postgres-identity`** (Port `5432`)
- **`postgres-delivery`** (Port `5433`)
- **`postgres-merchant`** (Port `5434`)
- **`rabbitmq`** (Ports `5672` AMQP, `15672` Web Management)
- **`redis`** (Port `6379`)
- **`minio`** (Port `9000` S3 API, `9001` Web Console)

---

## 4. Applying Database Migrations

Apply Entity Framework Core database migrations for all three bounded contexts:

```bash
# 1. Identity Service Migrations
dotnet ef database update \
  --project src/Services/Identity/SwiftDrop.Identity.Infrastructure \
  --startup-project src/Services/Identity/SwiftDrop.Identity.Api

# 2. Delivery Operations Service Migrations
dotnet ef database update \
  --project src/Services/Delivery/SwiftDrop.Delivery.Infrastructure \
  --startup-project src/Services/Delivery/SwiftDrop.Delivery.Api

# 3. Merchant Integration Service Migrations
dotnet ef database update \
  --project src/Services/Merchant/SwiftDrop.Merchant.Infrastructure \
  --startup-project src/Services/Merchant/SwiftDrop.Merchant.Api
```

---

## 5. Starting Backend Microservices

You can run all services concurrently using the .NET `launchSettings.json` compound configuration or manually in separate terminal windows:

### Terminal 1: Identity Service
```bash
cd src/Services/Identity/SwiftDrop.Identity.Api
dotnet run --launch-profile "Development"
# Listening on http://localhost:5001
```

### Terminal 2: Delivery Operations Service
```bash
cd src/Services/Delivery/SwiftDrop.Delivery.Api
dotnet run --launch-profile "Development"
# Listening on http://localhost:5002
```

### Terminal 3: Merchant Integration Service
```bash
cd src/Services/Merchant/SwiftDrop.Merchant.Api
dotnet run --launch-profile "Development"
# Listening on http://localhost:5003
```

### Terminal 4: Background Webhook Worker
```bash
cd src/Workers/SwiftDrop.WebhookWorker
dotnet run
```

### Terminal 5: YARP API Gateway
```bash
cd src/Gateway/SwiftDrop.Gateway
dotnet run --launch-profile "Development"
# Listening on http://localhost:5000
```

---

## 6. Starting Web Frontend Client

```bash
cd src/Clients/web-portal
npm install
npm run dev
# Vite dev server running at http://localhost:3000
```

---

## 7. Verification & Health Check Smoke Tests

Run the automated local verification smoke check:

```bash
# Verify Gateway Health
curl -s http://localhost:5000/health | jq .

# Expected Output:
# {
#   "status": "Healthy",
#   "results": {
#     "identity": "Healthy",
#     "delivery": "Healthy",
#     "merchant": "Healthy"
#   }
# }
```

- **RabbitMQ Dashboard:** `http://localhost:15672` (User: `guest`, Pass: `guest`)
- **MinIO Storage Console:** `http://localhost:9001` (User: `minioadmin`, Pass: `minioadmin`)
- **Swagger UI (Direct):**
  - Identity: `http://localhost:5001/swagger`
  - Delivery: `http://localhost:5002/swagger`
  - Merchant: `http://localhost:5003/swagger`
- **GraphQL Banana Cake Pop Playground:** `http://localhost:5002/graphql`
