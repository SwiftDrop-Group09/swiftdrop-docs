# Environment and Port Matrix

> Status: Proposed baseline 2.0 · Source of network addresses for all guides

| Component / protocol      | Local host                    | Docker DNS/listener                           | TLS and configuration                                                                       |
| ------------------------- | ----------------------------- | --------------------------------------------- | ------------------------------------------------------------------------------------------- |
| React HTTP                | http://localhost:5173         | web:8080                                      | Loopback-only; reverse-proxies `/api` and `/graphql` to Gateway                             |
| YARP HTTP                 | http://localhost:5000         | gateway:8080                                  | Loopback-only; PUBLIC_API_BASE_URL                                                          |
| Identity HTTP             | Not published                 | identity-service:8080                         | Trusted internal local network; app JWT issuer/JWKS config                                  |
| Delivery HTTP/GraphQL/SSE | Through YARP                  | delivery-service:8080                         | /graphql and /api/v1/parcels/{id}/events routes                                             |
| Delivery gRPC HTTP/2      | Not published                 | delivery-service:8081                         | h2c local only; service JWT mandatory                                                       |
| Merchant HTTP             | Through YARP                  | merchant-service:8080                         | Internal dispatch path not externally routed                                                |
| Worker health HTTP        | Not published                 | notification-worker:8080                      | /health and /ready private                                                                  |
| PostgreSQL                | Neon-managed TLS endpoint     | External Neon endpoint                        | Four logical DBs; restricted application and migration logins per service; no local DB port |
| RabbitMQ AMQP             | Not published                 | rabbitmq:5672                                 | Internal transport; backend adapter not implemented                                         |
| RabbitMQ console HTTP     | http://127.0.0.1:15672        | rabbitmq:15672                                | Local admin only; generated in ignored infra `development/.env`                             |
| Object API/console        | Not started in shared Compose | Deferred until Delivery proof-storage adapter | Planned private proof/receipt storage; not required to run current scaffold                 |

There are no local database host ports, direct API ports 5001–5004, Identity/Merchant gRPC ports or Redis port in the shared developer topology. Neon is external to Compose; Identity consumes its private connection string for Customer registration and its migration. Delivery, Merchant, and Notifications connection strings are reserved for their future service-owned adapters. The developer entry point is `swiftdrop-infra/development/run.sh`; the reference Compose in this docs repository is not the app-start command.

Delivery's proposed `Operations__TimeZone=Asia/Colombo` sets service-day defaults for assignments and Courier manifests; device timezone/clock cannot change resource scope. Date-based delivery reports retain their explicitly documented UTC history windows.

## Secrets

The user confirmed these exact six secret keys on 23 October 2026. Values are supplied privately; no actual Neon credentials were provided in this session. No legacy per-password database/BROKER aliases or extra Delivery migration secret is required.

| Secret key                               | Consumer / purpose                                                                            |
| ---------------------------------------- | --------------------------------------------------------------------------------------------- |
| RABBITMQ_DEFAULT_PASS                    | Local RabbitMQ admin password; application broker integration remains later work              |
| IDENTITY_DATABASE_CONNECTION_STRING      | Identity application; mapped to ConnectionStrings\_\_Database                                 |
| DELIVERY_DATABASE_CONNECTION_STRING      | Delivery application and explicit Delivery migration; mapped to ConnectionStrings\_\_Database |
| MERCHANT_DATABASE_CONNECTION_STRING      | Merchant-owned database; mapped to ConnectionStrings\_\_Database                              |
| NOTIFICATIONS_DATABASE_CONNECTION_STRING | Worker-owned Notifications database; mapped to ConnectionStrings\_\_Database                  |
| IDENTITY_MIGRATION_CONNECTION_STRING     | Identity explicit migration; mapped to ConnectionStrings\_\_MigrationDatabase                 |

Provision the Neon endpoint/database/role and necessary privileges explicitly; do not reuse one service's connection for another or embed credentials in docs, images or logs. This is the current development secret contract, not a claim that future JWT, proof-storage or Merchant encryption adapters are configured. Keep future credential design Proposed until reviewed.

## Clients and non-loopback access

Web uses the configured gateway base, ideally same-origin reverse proxy for `/api` and `/graphql`. Android emulator uses host bridge `10.0.2.2`; that address is **not** localhost inside Android. The safer mobile setup is `adb reverse tcp:5000 tcp:5000` and `adb reverse tcp:5173 tcp:5173`, then use loopback on the device with an explicit debug-only HTTP exception if needed. Physical-device/LAN use must provision a TLS ingress/certificate trusted by the device and set API_BASE_URL accordingly; do not publish plain HTTP development ports broadly. Flutter's build-time API_BASE_URL is client configuration, never a secret.

Proposed nonlocal example: `https://api.example.invalid` and `https://app.example.invalid` (nonresolving placeholders, **not deployed environments**). OPS must provide DNS, ingress/TLS, JWT issuer/audience, CORS/cookie same-site policy, Google client audiences, service TLS and scoped credentials before testing there. No staging, production, mTLS or zero-downtime result is claimed.
