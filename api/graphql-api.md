# GraphQL API Specification

> **Status:** Draft  
> **Version:** 1.0  
> **Last Updated:** October 2026  

---

## 1. Overview

SwiftDrop provides a GraphQL endpoint alongside the REST API, hosted primarily by the **Delivery Operations Service** (`POST /graphql`). The GraphQL interface acts as a high-performance **Backend-for-Frontend (BFF)** query engine optimized for rich single-page dashboards (e.g., Customer Portal, Dispatcher Live Control Room) where clients require composite data graphs in a single network round-trip without over-fetching or under-fetching.

- **Endpoint:** `https://api.swiftdrop.io/graphql` (Local: `http://localhost:5000/graphql`)
- **Transport:** HTTP POST (JSON body with `query` and `variables`)
- **Authentication:** `Authorization: Bearer <JWT>` header
- **Schema Engine:** HotChocolate on ASP.NET Core 8.0

---

## 2. Schema Definition (GraphQL SDL)

```graphql
"""
ISO-8601 compliant DateTime scalar representation.
"""
scalar DateTime

"""
Arbitrary JSON metadata dictionary scalar.
"""
scalar JSON

# ----------------------------------------------------
# Enums
# ----------------------------------------------------

enum ParcelStatus {
  CREATED
  ASSIGNED
  PICKED_UP
  IN_TRANSIT
  OUT_FOR_DELIVERY
  DELIVERED
  FAILED
  CANCELLED
}

enum DeliveryType {
  STANDARD
  EXPRESS
  SAME_DAY
}

enum CourierDutyStatus {
  ON_DUTY
  OFF_DUTY
  ON_BREAK
}

enum UserRole {
  CUSTOMER
  COURIER
  DISPATCHER
  MERCHANT
  ADMIN
}

# ----------------------------------------------------
# Directives
# ----------------------------------------------------

directive @auth(roles: [UserRole!]!) on FIELD_DEFINITION | OBJECT

# ----------------------------------------------------
# Types
# ----------------------------------------------------

type Address {
  street: String!
  city: String!
  postalCode: String!
  province: String!
  latitude: Float!
  longitude: Float!
}

type Dimensions {
  lengthCm: Float!
  widthCm: Float!
  heightCm: Float!
  volumeCm3: Float!
}

type PackageDetails {
  weightKg: Float!
  dimensions: Dimensions!
  description: String
  isFragile: Boolean!
  specialInstructions: String
}

type PricingSummary {
  baseFare: Float!
  weightSurcharge: Float!
  expressSurcharge: Float!
  totalAmount: Float!
  currency: String!
}

type ProofOfDelivery {
  podId: ID!
  photoUrl: String!
  signatureUrl: String!
  recipientName: String!
  deliveredAt: DateTime!
  deliveryCoordinates: GeoPoint!
}

type GeoPoint {
  latitude: Float!
  longitude: Float!
}

type CourierSummary {
  id: ID!
  fullName: String!
  phoneNumber: String!
  vehicleType: String!
  dutyStatus: CourierDutyStatus!
  activeDeliveriesCount: Int!
  currentLocation: GeoPoint
  rating: Float!
}

type TrackingTimelineEvent {
  id: ID!
  status: ParcelStatus!
  locationDescription: String!
  timestamp: DateTime!
  notes: String
}

type Parcel {
  id: ID!
  trackingNumber: String!
  senderId: ID!
  recipientName: String!
  recipientPhone: String!
  pickupAddress: Address!
  deliveryAddress: Address!
  packageDetails: PackageDetails!
  deliveryType: DeliveryType!
  status: ParcelStatus!
  pricing: PricingSummary!
  assignedCourier: CourierSummary
  proofOfDelivery: ProofOfDelivery
  timeline: [TrackingTimelineEvent!]!
  createdAt: DateTime!
  updatedAt: DateTime!
}

type ParcelConnection {
  items: [Parcel!]!
  totalCount: Int!
  pageInfo: PageInfo!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  currentPage: Int!
  totalPages: Int!
}

type DispatcherOverview {
  activeCouriersCount: Int!
  pendingAssignmentsCount: Int!
  inTransitDeliveriesCount: Int!
  completedTodayCount: Int!
  alertCount: Int!
}

# ----------------------------------------------------
# Queries
# ----------------------------------------------------

type Query {
  """
  Publicly accessible tracking query for recipient or customer.
  """
  trackParcel(trackingNumber: String!): Parcel

  """
  Fetches full parcel details by ID. Restricted to owner, courier, or dispatcher.
  """
  parcelById(id: ID!): Parcel @auth(roles: [CUSTOMER, COURIER, DISPATCHER, ADMIN])

  """
  Paged query of the authenticated customer's or merchant's parcels.
  """
  myParcels(
    status: ParcelStatus
    page: Int = 1
    pageSize: Int = 20
  ): ParcelConnection! @auth(roles: [CUSTOMER, MERCHANT, ADMIN])

  """
  Real-time aggregated metrics for the Dispatcher control center.
  """
  dispatcherDashboard: DispatcherOverview! @auth(roles: [DISPATCHER, ADMIN])

  """
  List couriers for assignment based on geographical bounding box.
  """
  availableCouriers(
    city: String
    maxWorkload: Int = 5
  ): [CourierSummary!]! @auth(roles: [DISPATCHER, ADMIN])
}

# ----------------------------------------------------
# Mutations
# ----------------------------------------------------

input CreateParcelInput {
  recipientName: String!
  recipientPhone: String!
  pickupAddress: AddressInput!
  deliveryAddress: AddressInput!
  weightKg: Float!
  description: String
  isFragile: Boolean = false
  deliveryType: DeliveryType = STANDARD
}

input AddressInput {
  street: String!
  city: String!
  postalCode: String!
  province: String!
  latitude: Float!
  longitude: Float!
}

type CreateParcelPayload {
  parcel: Parcel
  errors: [String!]
}

input AssignCourierInput {
  parcelId: ID!
  courierId: ID!
}

type AssignCourierPayload {
  parcel: Parcel
  success: Boolean!
  message: String
}

type Mutation {
  createParcel(input: CreateParcelInput!): CreateParcelPayload!
    @auth(roles: [CUSTOMER, MERCHANT, ADMIN])

  assignCourier(input: AssignCourierInput!): AssignCourierPayload!
    @auth(roles: [DISPATCHER, ADMIN])
}
```

---

## 3. Query Examples & Usage

### 3.1. Public Tracking Composite Query

Retrieves the current parcel status along with its full timeline, courier identity (if dispatched), and destination city.

**Query:**
```graphql
query GetTrackingDetails($trackingNumber: String!) {
  trackParcel(trackingNumber: $trackingNumber) {
    trackingNumber
    status
    deliveryType
    deliveryAddress {
      city
      province
    }
    assignedCourier {
      fullName
      vehicleType
      rating
    }
    timeline {
      status
      locationDescription
      timestamp
      notes
    }
    proofOfDelivery {
      deliveredAt
      recipientName
      photoUrl
    }
  }
}
```

**Variables:**
```json
{
  "trackingNumber": "TRK-202610-A9B8C7"
}
```

**Response (`200 OK`):**
```json
{
  "data": {
    "trackParcel": {
      "trackingNumber": "TRK-202610-A9B8C7",
      "status": "DELIVERED",
      "deliveryType": "EXPRESS",
      "deliveryAddress": {
        "city": "Kadawatha",
        "province": "Western"
      },
      "assignedCourier": {
        "fullName": "Nuwan Fernando",
        "vehicleType": "Motorcycle",
        "rating": 4.9
      },
      "timeline": [
        {
          "status": "CREATED",
          "locationDescription": "Colombo Central Hub",
          "timestamp": "2026-10-15T10:15:30Z",
          "notes": "Booked by sender"
        },
        {
          "status": "DELIVERED",
          "locationDescription": "28 Kandy Road, Kadawatha",
          "timestamp": "2026-10-15T15:30:22Z",
          "notes": "Signed by recipient"
        }
      ],
      "proofOfDelivery": {
        "deliveredAt": "2026-10-15T15:30:22Z",
        "recipientName": "Kamal Wickramasinghe",
        "photoUrl": "https://storage.swiftdrop.io/pod/20261015/del_10293847_signature.png"
      }
    }
  }
}
```

---

### 3.2. Dispatcher Control Center Query

Aggregates operational counts and active courier workloads in a single operation.

**Query:**
```graphql
query GetDispatcherDashboard {
  dispatcherDashboard {
    activeCouriersCount
    pendingAssignmentsCount
    inTransitDeliveriesCount
    completedTodayCount
    alertCount
  }
  availableCouriers(city: "Colombo", maxWorkload: 3) {
    id
    fullName
    vehicleType
    dutyStatus
    activeDeliveriesCount
    currentLocation {
      latitude
      longitude
    }
  }
}
```

---

## 4. Query Complexity & Security Safeguards

To prevent Denial of Service (DoS) attacks and expensive nested queries against the database, the GraphQL server enforces strict execution rules:

| Security Rule | Configuration Value | Enforcement Mechanism |
|---|---|---|
| **Max Query Depth** | `7 levels` | Rejects recursive queries deeper than 7 layers (e.g., Parcel → Courier → Parcel → Courier). |
| **Max Query Complexity** | `250 points` | Each scalar field costs 1 point; connections cost 10 points × page size. |
| **Execution Timeout** | `5,000 ms` | Long-running queries are aborted and return a cancellation error. |
| **Introspection** | Disabled in Staging/Prod | Introspection enabled only in Development (`ASPNETCORE_ENVIRONMENT=Development`). |
| **Authentication Directive** | `@auth` validated | Field-level authorization checks caller JWT roles via ASP.NET Core Policy middleware. |
