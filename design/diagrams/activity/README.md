# Activity Diagrams

> **Status:** Draft  
> **Last Updated:** October 2026

This document contains activity diagrams for key business processes in the SwiftDrop system. Activity diagrams model the flow of activities, decision points, and parallel paths within a process.

---

## 1. Parcel Delivery Lifecycle

This diagram models the complete lifecycle of a parcel from booking creation through to delivery completion or failure handling.

```mermaid
flowchart TD
    start([Customer initiates booking]) --> estimate[Calculate fee estimate]
    estimate --> showFee{Customer accepts fee?}

    showFee -->|No| cancel([Booking cancelled])
    showFee -->|Yes| createBooking[Create parcel booking]

    createBooking --> checkIdem{Idempotency key exists?}
    checkIdem -->|Yes| returnExisting[Return existing booking]
    checkIdem -->|No| persist[Persist parcel + price snapshot + outbox event]

    persist --> statusPending[Status: Pending]
    returnExisting --> statusPending

    statusPending --> confirmed[Status: Confirmed]
    confirmed --> waitAssign[Await dispatcher assignment]

    waitAssign --> assignCourier[Dispatcher assigns courier]
    assignCourier --> statusAssigned[Status: Assigned]

    statusAssigned --> courierPickup{Courier picks up parcel?}
    courierPickup -->|Yes| statusPickedUp[Status: Picked Up]
    courierPickup -->|No timeout| reassign{Reassign to another courier?}

    reassign -->|Yes| assignCourier
    reassign -->|No| escalate[Escalate to dispatcher]
    escalate --> assignCourier

    statusPickedUp --> statusInTransit[Status: In Transit]
    statusInTransit --> deliveryAttempt{Delivery successful?}

    deliveryAttempt -->|Yes| uploadProof[Courier uploads proof of delivery]
    uploadProof --> statusDelivered[Status: Delivered]
    statusDelivered --> generateReceipt[Generate delivery receipt]
    generateReceipt --> notifyCustomer[Notify customer]
    notifyCustomer --> publishEvent[Publish ParcelDelivered event]
    publishEvent --> webhookCheck{Merchant order?}
    webhookCheck -->|Yes| sendWebhook[Send webhook to merchant]
    webhookCheck -->|No| complete([Delivery complete])
    sendWebhook --> complete

    deliveryAttempt -->|No| reportFailure[Courier reports failure + reason]
    reportFailure --> statusFailed[Status: Failed]
    statusFailed --> failureReview{Retry delivery?}
    failureReview -->|Yes| assignCourier
    failureReview -->|No| returnToSender([Return to sender])
```

---

## 2. Merchant Onboarding and Approval

This diagram models the merchant registration, admin review, and integration setup process.

```mermaid
flowchart TD
    start([Merchant submits registration]) --> validate[Validate business details]
    validate --> validCheck{Details valid?}

    validCheck -->|No| reject1[Return validation errors]
    reject1 --> start

    validCheck -->|Yes| createAccount[Create merchant account]
    createAccount --> statusPending[Status: Pending Approval]

    statusPending --> notifyAdmin[Notify admin of new application]
    notifyAdmin --> adminReview[Admin reviews application]

    adminReview --> decision{Admin decision}

    decision -->|Approve| approve[Set status: Approved]
    approve --> notifyMerchant[Notify merchant of approval]
    notifyMerchant --> setupPhase[Merchant setup phase]

    setupPhase --> generateKeys[Generate API keys]
    generateKeys --> configWebhooks[Configure webhook URLs]
    configWebhooks --> testIntegration[Test integration with sandbox]
    testIntegration --> integrationReady{Tests pass?}

    integrationReady -->|Yes| goLive([Merchant goes live])
    integrationReady -->|No| troubleshoot[Review and fix configuration]
    troubleshoot --> testIntegration

    decision -->|Reject| rejectApp[Set status: Rejected]
    rejectApp --> notifyRejection[Notify merchant with reason]
    notifyRejection --> endReject([Application closed])

    decision -->|Request Info| requestInfo[Request additional information]
    requestInfo --> merchantResponds[Merchant submits additional info]
    merchantResponds --> adminReview
```

---

## 3. Courier Assignment and Workload Management

This diagram models how dispatchers manage courier assignments based on workload and zone considerations.

```mermaid
flowchart TD
    start([New parcel confirmed]) --> enterQueue[Parcel enters assignment queue]
    enterQueue --> dispatchView[Dispatcher views unassigned parcels]

    dispatchView --> selectParcel[Select parcel for assignment]
    selectParcel --> identifyZone[Identify delivery zone]
    identifyZone --> listCouriers[List available couriers in zone]

    listCouriers --> checkAvail{Couriers available?}
    checkAvail -->|No| expandZone{Expand to adjacent zones?}
    expandZone -->|Yes| listCouriers
    expandZone -->|No| waitQueue[Keep in queue, alert dispatcher]
    waitQueue --> dispatchView

    checkAvail -->|Yes| viewWorkload[View courier current workload]
    viewWorkload --> selectCourier[Select courier with capacity]

    selectCourier --> assign[Assign courier to parcel]
    assign --> notifyCourier[Notify courier of new assignment]
    notifyCourier --> courierResponse{Courier acknowledges?}

    courierResponse -->|Yes| inProgress([Assignment active])
    courierResponse -->|No timeout| autoReassign{Auto-reassign?}
    autoReassign -->|Yes| selectCourier
    autoReassign -->|No| manualReview[Flag for dispatcher review]
    manualReview --> dispatchView
```

---

## 4. User Authentication Decision Flow

This diagram models the authentication decision process including new user registration vs. existing user login.

```mermaid
flowchart TD
    start([User opens application]) --> authCheck{Already authenticated?}

    authCheck -->|Yes, valid token| dashboard([Show dashboard])
    authCheck -->|Yes, expired token| refreshFlow[Attempt token refresh]

    refreshFlow --> refreshValid{Refresh token valid?}
    refreshValid -->|Yes| issueNewTokens[Issue new access + refresh tokens]
    issueNewTokens --> dashboard
    refreshValid -->|No| loginRequired[Redirect to login]

    authCheck -->|No| loginRequired

    loginRequired --> loginMethod{Login method}

    loginMethod -->|Google OIDC| googleRedirect[Redirect to Google consent]
    googleRedirect --> googleAuth[User authenticates with Google]
    googleAuth --> receiveCode[Receive authorization code]
    receiveCode --> exchangeCode[Exchange code for Google tokens]
    exchangeCode --> validateIdToken[Validate Google ID token]

    validateIdToken --> userExists{User exists in system?}
    userExists -->|Yes| linkCheck{External identity linked?}
    linkCheck -->|Yes| issueAppTokens[Issue application JWT + refresh token]
    linkCheck -->|No| linkIdentity[Link external identity to user]
    linkIdentity --> issueAppTokens

    userExists -->|No| createUser[Create new user account]
    createUser --> assignRole[Assign default Customer role]
    assignRole --> linkNewIdentity[Link external identity]
    linkNewIdentity --> issueAppTokens

    loginMethod -->|Email + Password| emailLogin[Submit credentials]
    emailLogin --> validateCreds{Credentials valid?}
    validateCreds -->|Yes| issueAppTokens
    validateCreds -->|No| showError[Show authentication error]
    showError --> loginRequired

    issueAppTokens --> auditLog[Write audit log entry]
    auditLog --> dashboard
```

---

## References

- [Sequence Diagrams](../sequence/README.md)
- [Use Case Diagrams](../use-cases/README.md)
- [SRS](../../../requirements/srs.md)
- [Architecture Diagram](../architecture/architecture.md)
