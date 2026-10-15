# Authorization & Access Control Architecture

> **Status:** Draft  
> **Version:** 1.0  
> **Last Updated:** October 2026  

---

## 1. Overview

SwiftDrop enforces a hybrid access control model combining **Role-Based Access Control (RBAC)** for broad coarse-grained capabilities and **Attribute-Based Access Control (ABAC)** for fine-grained resource-level ownership validation.

- **Policy Enforcement Points (PEP):**
  1. **YARP Gateway:** Coarse-grained gatekeeper verifying valid token signature, role claims, and IP rate limits.
  2. **Service Layer (ASP.NET Core Controllers & Handlers):** Fine-grained permission checks and ownership verification against domain entity state.
- **Principle of Least Privilege:** Users and services operate with the minimal set of privileges required to perform their functions.

---

## 2. Platform Roles & Personas

| Role | Target Persona | Primary Responsibilities |
|---|---|---|
| **Customer** | End-consumers / General Public | Book personal parcels, view order history, track live shipments, cancel pending bookings. |
| **Courier** | Field delivery personnel | View assigned manifest, accept deliveries, submit status changes (pickup, delivered), upload PoD. |
| **Dispatcher** | Logistics & operations controllers | Monitor active deliveries, assign/reassign couriers, resolve delivery exceptions, manage fleet workload. |
| **Merchant** | E-commerce businesses & vendors | Generate API keys, bulk-import shipments, register webhooks, access merchant shipping analytics. |
| **Admin** | System administrators & compliance | User management, role elevation, merchant approval/suspension, global audit log review. |

---

## 3. Comprehensive Permission Matrix

| Permission Key | Customer | Courier | Dispatcher | Merchant | Admin | Scope & Description |
|---|:---:|:---:|:---:|:---:|:---:|---|
| `auth:profile:read` | ✅ | ✅ | ✅ | ✅ | ✅ | Read authenticated user profile (`/users/me`) |
| `auth:profile:update` | ✅ | ✅ | ✅ | ✅ | ✅ | Update own user profile data |
| `users:list` | ❌ | ❌ | ❌ | ❌ | ✅ | List all platform users |
| `users:roles:manage` | ❌ | ❌ | ❌ | ❌ | ✅ | Elevate or change role assignments |
| `parcels:create` | ✅ | ❌ | ✅ | ✅ | ✅ | Create new individual delivery order |
| `parcels:read:own` | ✅ | ❌ | ❌ | ✅ | ✅ | View parcels created by caller |
| `parcels:read:assigned` | ❌ | ✅ | ❌ | ❌ | ✅ | View parcels currently assigned to caller |
| `parcels:read:all` | ❌ | ❌ | ✅ | ❌ | ✅ | View all platform parcels across zones |
| `parcels:cancel:own` | ✅ | ❌ | ❌ | ✅ | ✅ | Cancel pending order before pickup |
| `deliveries:assign` | ❌ | ❌ | ✅ | ❌ | ✅ | Dispatch or reassign parcel to courier |
| `deliveries:status:update` | ❌ | ✅ | ✅ | ❌ | ✅ | Transition state (InTransit, Delivered, Failed) |
| `deliveries:pod:upload` | ❌ | ✅ | ❌ | ❌ | ✅ | Submit photo & signature Proof of Delivery |
| `couriers:telemetry:write` | ❌ | ✅ | ❌ | ❌ | ❌ | Stream live GPS coordinates via WebSocket |
| `couriers:fleet:monitor` | ❌ | ❌ | ✅ | ❌ | ✅ | Real-time map monitoring of all couriers |
| `merchant:onboard` | ✅ | ❌ | ❌ | ❌ | ✅ | Submit merchant registration request |
| `merchant:approve` | ❌ | ❌ | ❌ | ❌ | ✅ | Approve or reject merchant application |
| `merchant:keys:manage` | ❌ | ❌ | ❌ | ✅ | ✅ | Generate, list, and revoke merchant API keys |
| `merchant:parcels:bulk` | ❌ | ❌ | ❌ | ✅ | ✅ | Ingest bulk consignments via API |
| `merchant:webhooks:manage` | ❌ | ❌ | ❌ | ✅ | ✅ | Register and test webhook delivery endpoints |

---

## 4. Resource Ownership Rules (ABAC)

Even if an actor possesses a permission (e.g., `parcels:read:own`), access is conditionally evaluated against domain entity ownership attributes:

### 4.1. Customer Ownership Invariant
- A user with role `Customer` can **only** view or cancel a parcel if:
  $$\text{Parcel.SenderId} == \text{CurrentUser.Id} \quad \lor \quad \text{Parcel.RecipientPhone} == \text{CurrentUser.Phone}$$
- Any attempt to view a foreign parcel returns `403 Forbidden` (or `404 Not Found` to prevent entity enumeration).

### 4.2. Courier Manifest Invariant
- A user with role `Courier` can **only** advance delivery state or upload Proof of Delivery if:
  $$\text{Delivery.CourierId} == \text{CurrentUser.CourierId} \quad \land \quad \text{Delivery.Status} \in \{\text{Assigned, PickedUp, InTransit}\}$$

### 4.3. Merchant Isolation Invariant
- Requests originating with an API key or `Merchant` bearer token are automatically scoped by `TenantId` / `MerchantId` at the database query layer:
  ```csharp
  // Global Query Filter in DeliveryDbContext & MerchantDbContext
  modelBuilder.Entity<Parcel>()
      .HasQueryFilter(p => _currentUserService.Role == "Admin" 
                        || p.MerchantId == _currentUserService.MerchantId);
  ```

---

## 5. Policy Enforcement Implementation (.NET 8)

Authorization is implemented using ASP.NET Core Policy-based authorization with declarative attributes and custom `AuthorizationHandler<T>` classes.

### 5.1. Policy Registration in `Program.cs`
```csharp
builder.Services.AddAuthorization(options =>
{
    options.AddPolicy("RequireAdmin", policy => 
        policy.RequireRole("Admin"));
        
    options.AddPolicy("RequireDispatcher", policy => 
        policy.RequireRole("Dispatcher", "Admin"));
        
    options.AddPolicy("CanManageDeliveries", policy => 
        policy.RequireRole("Courier", "Dispatcher", "Admin"));

    options.AddPolicy("ParcelOwnerOnly", policy =>
        policy.Requirements.Add(new ParcelOwnershipRequirement()));
});
```

### 5.2. Custom Requirement Handler (Ownership Check)
```csharp
public class ParcelOwnershipHandler : AuthorizationHandler<ParcelOwnershipRequirement, Parcel>
{
    protected override Task HandleRequirementAsync(
        AuthorizationHandlerContext context,
        ParcelOwnershipRequirement requirement,
        Parcel resource)
    {
        var userId = context.User.FindFirst(ClaimTypes.NameIdentifier)?.Value;
        var userRole = context.User.FindFirst(ClaimTypes.Role)?.Value;

        if (userRole == "Admin" || userRole == "Dispatcher")
        {
            context.Succeed(requirement);
            return Task.CompletedTask;
        }

        if (resource.SenderId == userId || resource.MerchantId == userId)
        {
            context.Succeed(requirement);
        }

        return Task.CompletedTask;
    }
}
```
