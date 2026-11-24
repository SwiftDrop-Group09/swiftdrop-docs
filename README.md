# SwiftDrop Project Documentation

SwiftDrop is a parcel delivery and merchant integration platform developed by Group 09 for the Enterprise Application Development assignment. This repository holds the project-wide requirements, architecture, API design, verification records, and submission material.

The architecture and decision register are marked Proposed. Use the requirements and design fixtures to understand intended behavior, and check test results and source-repository runbooks for implementation and deployment evidence. [Decision register](architecture/decisions/README.md) [Remaining work](documentation-fix-plan.md)

## Documentation index

| Area | Start here |
| --- | --- |
| Requirements | [Assignment overview](requirements/assignment-overview.md), [software requirements](requirements/srs.md), [traceability](requirements/requirements-traceability.md) |
| Architecture | [Technical design](architecture/technical-design.md), [service catalog](architecture/service-catalog.md), [parcel state machine](architecture/parcel-state-machine.md) |
| APIs and integration | [API reference](api/api-reference.md), [REST](api/rest-api.md), [GraphQL](api/graphql-api.md), [gRPC](api/grpc-services.md), [events](integration/event-catalog.md), [real-time tracking](integration/realtime-tracking.md) |
| Diagrams | [Diagram index and source files](design/diagrams/README.md) |
| Security | [Authentication and authorization](security/authentication.md) |
| Testing | [Test strategy](testing/test-strategy.md), [test cases](testing/test-cases.md), [runtime results](testing/test-results.md), [documentation validation](testing/documentation-validation.md) |
| Deployment | [Local setup](deployment/local-setup.md), [environment matrix](deployment/environments.md), [Compose](deployment/docker-compose.md), [Kubernetes](deployment/kubernetes.md) |
| Assessment | [Assignment compliance](requirements/assignment-compliance.md), [demo plan](submission/demo-plan.md), [submission checklist](submission/submission-checklist.md) |
| Team coordination | [Milestones](project-management/milestones.md), [responsibilities](project-management/team-responsibilities.md), [contribution log](project-management/contribution-log.md) |

## Maintain and validate the documentation

Keep design changes aligned across requirements, contracts, diagrams, and traceability. Record changes to architectural decisions in the [decision register](architecture/decisions/README.md). Implementation-specific setup and operational details belong with the owning source repository.

See the [validation and rendering guide](scripts/README.md) for prerequisites and commands to check links and design fixtures, validate GraphQL and Protobuf, and regenerate diagrams. Record application verification separately in the [runtime results](testing/test-results.md). Open documentation pull requests against `dev`.

## SwiftDrop repositories

| Repository | Responsibility |
| --- | --- |
| [Backend](https://github.com/SwiftDrop-Group09/swiftdrop-backend) | Gateway, APIs, background workers, and integration contracts |
| [Web frontend](https://github.com/SwiftDrop-Group09/swiftdrop-frontend) | React web application and role-based workspaces |
| [Mobile app](https://github.com/SwiftDrop-Group09/swiftdrop-mobile) | Flutter application for customers and couriers |
| [Infrastructure](https://github.com/SwiftDrop-Group09/swiftdrop-infra) | Local development, Docker Compose, and Kubernetes deployment |
| [Project documentation](https://github.com/SwiftDrop-Group09/swiftdrop-docs) | Requirements, architecture, integration design, and assessment evidence |
