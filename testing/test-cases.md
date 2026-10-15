# Test Cases & Acceptance Criteria Specification

> **Status:** Draft  
> **Version:** 1.0  
> **Last Updated:** October 2026  

---

## 1. Overview

This document catalogs test scenarios, acceptance criteria, test fixtures, and expected results covering all critical functional modules of the SwiftDrop platform. Each test case maps directly to requirements defined in the [Software Requirements Specification (SRS)](../requirements/srs.md).

---

## 2. Module 1: Authentication & Identity Management

| Test Case ID | Test Scenario | Pre-conditions | Test Steps | Expected Result | Level | SRS Trace |
|---|---|---|---|---|---|---|
| **TC-AUTH-001** | Successful Google OIDC token exchange | Valid Google ID token with verified email | 1. POST `/api/v1/auth/google` with `{ idToken }`<br/>2. Inspect HTTP status & response | 200 OK; returns valid RS256 JWT access token and refresh token; provisions user with `Customer` role | Integration | REQ-FR-CUST-01 |
| **TC-AUTH-002** | Rejection of expired Google token | Expired Google ID token | 1. POST `/api/v1/auth/google` with expired token | 401 Unauthorized; ProblemDetails indicates token expiration | Unit | REQ-NFR-SEC-01 |
| **TC-AUTH-003** | Refresh token rotation (RTR) | Active, unrevoked refresh token | 1. POST `/api/v1/auth/refresh`<br/>2. Inspect returned tokens<br/>3. Re-present the old refresh token | Step 1: 200 OK with new access + refresh token.<br/>Step 3: 401 Unauthorized; token family revoked due to replay attempt | Integration | REQ-NFR-SEC-01 |
| **TC-AUTH-004** | User logout & session invalidation | Authenticated session with active JWT | 1. POST `/api/v1/auth/logout`<br/>2. Present JWT to protected endpoint | 200 OK; JWT `jti` added to Redis blacklist; subsequent calls return 401 Unauthorized | Integration | REQ-FR-CUST-01 |
| **TC-AUTH-005** | Unauthorized role access rejection | Authenticated user with `Customer` role | 1. Attempt GET `/api/v1/deliveries/available-couriers` | 403 Forbidden; ProblemDetails indicates role `Dispatcher` or `Admin` required | Integration | REQ-FR-DISP-02 |

---

## 3. Module 2: Parcel Booking & Pricing Engine

| Test Case ID | Test Scenario | Pre-conditions | Test Steps | Expected Result | Level | SRS Trace |
|---|---|---|---|---|---|---|
| **TC-BOOK-001** | Standard parcel booking with valid payload | Authenticated user (`Customer`) | 1. POST `/api/v1/parcels` with valid addresses and 2.5kg weight | 201 Created; returns tracking number matching `TRK-YYYYMM-XXXXXX`; status is `Created`; `ParcelBooked` event written to Outbox table | Integration | REQ-FR-CUST-02 |
| **TC-BOOK-002** | Validation rejection on missing postal code | Authenticated user | 1. POST `/api/v1/parcels` with missing `deliveryAddress.postalCode` | 400 Bad Request; ProblemDetails lists field validation error for `postalCode` | Unit | REQ-FR-CUST-02 |
| **TC-BOOK-003** | Dynamic pricing calculation accuracy | Pure pricing service fixture | 1. Invoke `CalculatePrice(weight: 7.5kg, type: Express, fragile: true)` | Formula matches: Base(450) + Weight(5 * 60) + Express(200) + Fragile(100) = 1,050 LKR | Unit | REQ-FR-CUST-03 |
| **TC-BOOK-004** | Cancellation of pending parcel by owner | Parcel in `Created` status | 1. PUT `/api/v1/parcels/{id}/cancel` by original creator | 200 OK; status transitions to `Cancelled`; outbox event `ParcelCancelled` generated | Integration | REQ-FR-CUST-04 |
| **TC-BOOK-005** | Disallow cancellation of picked-up parcel | Parcel in `InTransit` status | 1. PUT `/api/v1/parcels/{id}/cancel` | 409 Conflict; message states parcel cannot be cancelled once collected | Unit | REQ-FR-CUST-04 |

---

## 4. Module 3: Courier Dispatch & Delivery Execution

| Test Case ID | Test Scenario | Pre-conditions | Test Steps | Expected Result | Level | SRS Trace |
|---|---|---|---|---|---|---|
| **TC-DELV-001** | Manual courier assignment by Dispatcher | Parcel in `Created` state; Courier is `OnDuty` | 1. POST `/api/v1/deliveries/assign` with `{ parcelId, courierId }` | 200 OK; status transitions to `Assigned`; courier assigned count increments | Integration | REQ-FR-DISP-01 |
| **TC-DELV-002** | Over-capacity assignment rejection | Courier currently has 10 active parcels (max limit) | 1. POST `/api/v1/deliveries/assign` for 11th parcel | 422 Unprocessable Entity; error notes courier capacity limit reached | Unit | REQ-FR-DISP-03 |
| **TC-DELV-003** | Valid state progression (Pickup -> InTransit) | Delivery assigned to courier | 1. Courier calls PUT `/api/v1/deliveries/{id}/status` to `PickedUp`<br/>2. Courier calls PUT to `InTransit` | Both return 200 OK; tracking timeline records both events with timestamps | Integration | REQ-FR-COUR-02 |
| **TC-DELV-004** | Illegal state transition rejection | Delivery in `Created` state | 1. Attempt transition directly to `Delivered` | 409 Conflict; state machine rejects invalid transition from `Created` to `Delivered` | Unit | REQ-FR-COUR-02 |
| **TC-DELV-005** | Proof of Delivery upload completion | Delivery in `InTransit` state | 1. POST `/api/v1/deliveries/{id}/pod` with signature PNG & photo JPEG | 200 OK; status becomes `Delivered`; PoD files stored; `DeliveryCompleted` event published | Integration | REQ-FR-COUR-03 |

---

## 5. Module 4: Merchant Integration & Webhook Delivery

| Test Case ID | Test Scenario | Pre-conditions | Test Steps | Expected Result | Level | SRS Trace |
|---|---|---|---|---|---|---|
| **TC-MRCH-001** | Valid merchant API key authentication | Approved merchant with generated API key | 1. GET `/api/v1/merchant/parcels` with `X-API-Key: sk_live_...` | 200 OK; returns list of merchant's parcels | Integration | REQ-FR-MRCH-01 |
| **TC-MRCH-002** | Bulk consignment ingestion (50 orders) | Valid merchant API key | 1. POST `/api/v1/merchant/parcels/bulk` with 50 order items | 202 Accepted; returns 50 tracking numbers and batch UUID; DB records all parcels | Integration | REQ-FR-MRCH-02 |
| **TC-MRCH-003** | Webhook delivery with valid HMAC signature | Registered merchant webhook URL | 1. Trigger `DeliveryCompleted` event<br/>2. Intercept HTTP POST at webhook URL | Payload received with `X-SwiftDrop-Signature` matching `HMAC-SHA256(payload, secret)` | E2E | REQ-FR-MRCH-03 |
| **TC-MRCH-004** | Webhook retry on endpoint failure (500 Server Error) | Merchant receiver returns 500 | 1. Trigger event<br/>2. Worker attempts delivery<br/>3. Inspect retry schedule | Retried up to 5 times with exponential backoff (1m, 5m, 15m, 30m, 1h); moves to DLQ on 5th failure | Integration | REQ-FR-MRCH-03 |

---

## 6. Module 5: Real-Time Tracking & WebSockets

| Test Case ID | Test Scenario | Pre-conditions | Test Steps | Expected Result | Level | SRS Trace |
|---|---|---|---|---|---|---|
| **TC-REAL-001** | Courier GPS streaming broadcast | Courier connected via WebSocket Hub | 1. Invoke `PublishLocation(lat, lng)`<br/>2. Observe connected Dispatcher client | Dispatcher receives `OnCourierLocationUpdated` frame within < 200ms | E2E | REQ-FR-COUR-04 |
| **TC-REAL-002** | Public SSE tracking stream updates | Customer connected to `/api/v1/parcels/track/{trk}/live` | 1. Advance parcel status from `PickedUp` to `InTransit` | SSE client receives JSON event payload automatically without polling | Integration | REQ-FR-CUST-05 |
