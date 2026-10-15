# REST API Specification

> **Status:** Draft  
> **Version:** 1.0  
> **Last Updated:** October 2026  

---

## 1. Overview

The SwiftDrop REST API provides standard, stateless HTTP endpoints following RESTful resource modeling conventions. All request and response bodies use JSON (`application/json; charset=utf-8`) unless explicitly noted (such as multi-part file uploads for Proof of Delivery).

- **Gateway URL:** `https://api.swiftdrop.io` (Local: `http://localhost:5000`)
- **API Versioning:** URI path versioning (`/api/v1/...`)
- **Response Format:** JSON (camelCase property names)
- **DateTime Representation:** ISO 8601 UTC string (`YYYY-MM-DDTHH:mm:ss.sssZ`)

---

## 2. Identity Service Endpoints

Base Path: `/api/v1`  
Upstream Service: `http://identity-service:8080`

### 2.1. Exchange Google OIDC Token

Exchanges an OpenID Connect `id_token` issued by Google for a SwiftDrop JWT access token and refresh token. If the user does not exist, an account is automatically provisioned with the `Customer` role.

- **Method / Path:** `POST /api/v1/auth/google`
- **Authentication:** None (Public)
- **Rate Limit:** 30 requests / minute / IP

**Request Headers:**
```http
Content-Type: application/json
X-Correlation-ID: 8d6c7b91-44ab-4a47-a8fe-3ef1e92d0012
```

**Request Body:**
```json
{
  "idToken": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjFhMmIzYyJ9..."
}
```

**Success Response (`200 OK`):**
```json
{
  "accessToken": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjU5YTEwY...",
  "tokenType": "Bearer",
  "expiresInSeconds": 900,
  "refreshToken": "rf_7a1e0b9d5c3f4e1290aa81",
  "user": {
    "id": "u_8849b3d0-6218-47f2-9c1a-9f5b61a9bc34",
    "email": "sarah.perera@gmail.com",
    "fullName": "Sarah Perera",
    "profileImageUrl": "https://lh3.googleusercontent.com/a/ACg8ocL...",
    "role": "Customer",
    "phoneNumber": "+94771234567"
  }
}
```

---

### 2.2. Refresh Access Token

Rotates an active refresh token and returns a new access token / refresh token pair. The supplied refresh token is immediately revoked (anti-replay rotation).

- **Method / Path:** `POST /api/v1/auth/refresh`
- **Authentication:** None (Requires valid unrevoked Refresh Token)

**Request Body:**
```json
{
  "refreshToken": "rf_7a1e0b9d5c3f4e1290aa81"
}
```

**Success Response (`200 OK`):**
```json
{
  "accessToken": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjU5YTEwY...",
  "tokenType": "Bearer",
  "expiresInSeconds": 900,
  "refreshToken": "rf_99bb12e4f01c238910bc44"
}
```

---

### 2.3. User Profile Management

#### `GET /api/v1/users/me`
Retrieves the authenticated user's profile details.
- **Headers:** `Authorization: Bearer <JWT>`
- **Response (`200 OK`):**
```json
{
  "id": "u_8849b3d0-6218-47f2-9c1a-9f5b61a9bc34",
  "email": "sarah.perera@gmail.com",
  "fullName": "Sarah Perera",
  "phoneNumber": "+94771234567",
  "role": "Customer",
  "isEmailVerified": true,
  "createdAt": "2026-09-12T08:30:00Z"
}
```

#### `PUT /api/v1/users/me`
Updates user contact details.
- **Headers:** `Authorization: Bearer <JWT>`
- **Request Body:**
```json
{
  "fullName": "Sarah Perera",
  "phoneNumber": "+94779876543"
}
```

---

## 3. Delivery Operations Endpoints

Base Path: `/api/v1`  
Upstream Service: `http://delivery-service:8080`

### 3.1. Book Parcel

Creates a new delivery booking. Upon creation, a domain event `ParcelBooked` is committed via the Transactional Outbox.

- **Method / Path:** `POST /api/v1/parcels`
- **Authentication:** `Bearer <JWT>`
- **Roles Permitted:** `Customer`, `Merchant`, `Admin`

**Request Body:**
```json
{
  "recipient": {
    "name": "Kamal Wickramasinghe",
    "phoneNumber": "+94719876543",
    "email": "kamal.wickrama@outlook.com"
  },
  "pickupAddress": {
    "street": "142 Galle Road",
    "city": "Colombo 03",
    "postalCode": "00300",
    "province": "Western",
    "latitude": 6.90152,
    "longitude": 79.85293
  },
  "deliveryAddress": {
    "street": "28 Kandy Road",
    "city": "Kadawatha",
    "postalCode": "11850",
    "province": "Western",
    "latitude": 7.00192,
    "longitude": 79.95341
  },
  "packageDetails": {
    "weightKg": 2.50,
    "dimensions": {
      "lengthCm": 30.0,
      "widthCm": 20.0,
      "heightCm": 15.0
    },
    "description": "Electronics - Smartphone & Accessories",
    "isFragile": true,
    "specialInstructions": "Call recipient upon arrival at gate"
  },
  "deliveryType": "Express",
  "paymentMethod": "Prepaid"
}
```

**Success Response (`201 Created`):**
```json
{
  "id": "p_550e8400-e29b-41d4-a716-446655440000",
  "trackingNumber": "TRK-202610-A9B8C7",
  "status": "Created",
  "deliveryType": "Express",
  "estimatedDelivery": "2026-10-16T18:00:00Z",
  "pricing": {
    "baseFare": 450.00,
    "weightSurcharge": 150.00,
    "expressSurcharge": 200.00,
    "totalAmount": 800.00,
    "currency": "LKR"
  },
  "createdAt": "2026-10-15T10:15:30Z"
}
```

---

### 3.2. Public Parcel Tracking

Allows public, unauthenticated tracking of any active or delivered parcel by its unique tracking code.

- **Method / Path:** `GET /api/v1/parcels/track/{trackingNumber}`
- **Authentication:** None (Public)
- **Rate Limit:** 60 requests / minute / IP

**Success Response (`200 OK`):**
```json
{
  "trackingNumber": "TRK-202610-A9B8C7",
  "status": "InTransit",
  "deliveryType": "Express",
  "estimatedDeliveryTime": "2026-10-16T17:30:00Z",
  "originCity": "Colombo 03",
  "destinationCity": "Kadawatha",
  "timeline": [
    {
      "status": "Created",
      "timestamp": "2026-10-15T10:15:30Z",
      "location": "Colombo Central Hub",
      "description": "Parcel booked and shipping label generated."
    },
    {
      "status": "Assigned",
      "timestamp": "2026-10-15T11:00:00Z",
      "location": "Colombo Central Hub",
      "description": "Assigned to Courier Nuwan Fernando."
    },
    {
      "status": "PickedUp",
      "timestamp": "2026-10-15T12:20:15Z",
      "location": "142 Galle Road, Colombo 03",
      "description": "Package collected from sender."
    },
    {
      "status": "InTransit",
      "timestamp": "2026-10-15T13:45:00Z",
      "location": "Kadawatha Transit Hub",
      "description": "Parcel is out for delivery."
    }
  ]
}
```

---

### 3.3. Assign Courier to Parcel

Manual or automated dispatch assignment.

- **Method / Path:** `POST /api/v1/deliveries/assign`
- **Authentication:** `Bearer <JWT>`
- **Roles Permitted:** `Dispatcher`, `Admin`

**Request Body:**
```json
{
  "parcelId": "p_550e8400-e29b-41d4-a716-446655440000",
  "courierId": "c_2209a311-b1e8-48b2-b4c9-881239aa8123",
  "assignmentMode": "Manual",
  "priority": "High"
}
```

**Success Response (`200 OK`):**
```json
{
  "deliveryId": "del_10293847-5647-3829-1029-384756102938",
  "parcelId": "p_550e8400-e29b-41d4-a716-446655440000",
  "courierId": "c_2209a311-b1e8-48b2-b4c9-881239aa8123",
  "status": "Assigned",
  "assignedAt": "2026-10-15T11:00:00Z"
}
```

---

### 3.4. Update Delivery Status & Proof of Delivery (PoD)

#### Advance Status: `PUT /api/v1/deliveries/{id}/status`
- **Roles:** `Courier`, `Dispatcher`
- **Request Body:**
```json
{
  "status": "PickedUp",
  "currentLatitude": 6.90155,
  "currentLongitude": 79.85290,
  "notes": "Package scanned and verified."
}
```

#### Upload Proof of Delivery: `POST /api/v1/deliveries/{id}/pod`
- **Content-Type:** `multipart/form-data`
- **Roles:** `Courier`
- **Fields:**
  - `photo`: Image binary file (JPEG/PNG, max 5MB)
  - `signature`: Image binary file (PNG base64 signature curve)
  - `recipientName`: `"Kamal Wickramasinghe"`
  - `deliveredLatitude`: `7.00192`
  - `deliveredLongitude`: `79.95341`

**Success Response (`200 OK`):**
```json
{
  "deliveryId": "del_10293847-5647-3829-1029-384756102938",
  "status": "Delivered",
  "deliveredAt": "2026-10-15T15:30:22Z",
  "podUrl": "https://storage.swiftdrop.io/pod/20261015/del_10293847_signature.png",
  "recipientName": "Kamal Wickramasinghe"
}
```

---

## 4. Merchant Integration Endpoints

Base Path: `/api/v1/merchant`  
Upstream Service: `http://merchant-service:8080`

### 4.1. Bulk Parcel Ingestion

Enables high-volume enterprise merchants to ingest up to 100 delivery requests in a single HTTP POST batch.

- **Method / Path:** `POST /api/v1/merchant/parcels/bulk`
- **Authentication:** `X-API-Key: sk_live_...` or Bearer JWT
- **Roles Permitted:** `Merchant`

**Request Body:**
```json
{
  "batchReference": "BATCH-2026-10-15-001",
  "parcels": [
    {
      "merchantOrderReference": "ORD-991201",
      "recipient": {
        "name": "Nimal Siripala",
        "phoneNumber": "+94770011223"
      },
      "deliveryAddress": {
        "street": "15 Temple Road",
        "city": "Nugegoda",
        "postalCode": "10250",
        "province": "Western"
      },
      "packageDetails": {
        "weightKg": 1.20,
        "description": "Clothing Order #991201"
      },
      "deliveryType": "Standard"
    },
    {
      "merchantOrderReference": "ORD-991202",
      "recipient": {
        "name": "Dilini Perera",
        "phoneNumber": "+94773344556"
      },
      "deliveryAddress": {
        "street": "45 Lake Drive",
        "city": "Rajagiriya",
        "postalCode": "10107",
        "province": "Western"
      },
      "packageDetails": {
        "weightKg": 0.80,
        "description": "Cosmetics Order #991202"
      },
      "deliveryType": "Express"
    }
  ]
}
```

**Success Response (`202 Accepted`):**
```json
{
  "batchReference": "BATCH-2026-10-15-001",
  "totalSubmitted": 2,
  "acceptedCount": 2,
  "rejectedCount": 0,
  "results": [
    {
      "merchantOrderReference": "ORD-991201",
      "status": "Accepted",
      "trackingNumber": "TRK-202610-B1C2D3",
      "parcelId": "p_610e9900-e29b-41d4-a716-112233445566"
    },
    {
      "merchantOrderReference": "ORD-991202",
      "status": "Accepted",
      "trackingNumber": "TRK-202610-E4F5G6",
      "parcelId": "p_720e9900-e29b-41d4-a716-778899001122"
    }
  ]
}
```

---

### 4.2. Webhook Registration & Management

#### Register Webhook: `POST /api/v1/merchant/webhooks`
Registers an HTTPS endpoint to receive asynchronous lifecycle status updates.

- **Authentication:** `X-API-Key: sk_live_...`
- **Request Body:**
```json
{
  "url": "https://store.acme-retail.com/api/webhooks/swiftdrop",
  "events": [
    "delivery.picked_up",
    "delivery.in_transit",
    "delivery.completed",
    "delivery.failed"
  ],
  "secret": "whsec_99a8b7c6d5e4f3a2b1c0"
}
```

**Response (`201 Created`):**
```json
{
  "webhookId": "wh_3309a123-bc45-48b2-b4c9-991238475620",
  "url": "https://store.acme-retail.com/api/webhooks/swiftdrop",
  "events": [
    "delivery.picked_up",
    "delivery.in_transit",
    "delivery.completed",
    "delivery.failed"
  ],
  "status": "Active",
  "createdAt": "2026-10-15T11:45:00Z"
}
```

---

## 5. HTTP Status Code Conventions

| Status Code | Reason Phrase | Typical Trigger Condition in SwiftDrop |
|---|---|---|
| `200 OK` | OK | Successful GET, PUT, or state transition request |
| `201 Created` | Created | Resource successfully created (`POST /api/v1/parcels`, etc.) |
| `202 Accepted` | Accepted | Asynchronous batch job received (`POST /api/v1/merchant/parcels/bulk`) |
| `204 No Content` | No Content | Successful deletion or revocation (`DELETE /api/v1/merchants/api-keys/{id}`) |
| `400 Bad Request` | Bad Request | Schema validation failure, invalid postal code, malformed JSON |
| `401 Unauthorized` | Unauthorized | Missing, expired, or cryptographically invalid Bearer JWT or API key |
| `403 Forbidden` | Forbidden | Authenticated actor lacks required role or resource ownership |
| `404 Not Found` | Not Found | Requested parcel ID or tracking number does not exist |
| `409 Conflict` | Conflict | Business invariant violation (e.g., cancelling a delivered parcel) |
| `422 Unprocessable Entity` | Unprocessable Entity | Domain constraint violation (e.g., assigning courier exceeding capacity) |
| `429 Too Many Requests` | Too Many Requests | Rate limit threshold exceeded on Gateway sliding window |
| `500 Internal Server Error` | Server Error | Unhandled server exception (correlated via `X-Correlation-ID`) |
