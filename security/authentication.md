# Authentication

> Status: Proposed baseline 2.0 · DEC-05/12 · SEC/UI approval pending

## Local and Google login

Identity owns local credentials, external subject links and sessions. Register accepts email/password/fullName and assigns Customer only; normalize/uniquely index email, validate password 12–128 characters, hash with salted Argon2id (parameters measured/configured before release), and return no password/hash. Login uses generic invalid-credentials responses, throttling and escalating account lockout; disabled accounts cannot register a replacement identity or refresh. Password-reset delivery is deferred. Admin-created local fixture accounts use unique generated passwords distributed privately. Never commit real demo passwords.

Both React and Flutter Customer/Courier use their platform Google SDK to obtain a Google **ID token** and POST `{idToken}` to `/api/v1/auth/google`. There is no backend authorization-code exchange or callback endpoint in this baseline. Configure distinct web/Android client IDs and explicit audience allowlist. The SDK owns provider consent/redirect behavior; browser callback/nonce/CSRF checks use the SDK's documented flow. Identity validates signature with cached Google JWKS, `iss` allowlist, exact allowed `aud`, expiry and verified email; enforce azp/nonce checks when the chosen SDK supplies them. Google cancellation creates no session; bad/expired token returns 401 with no account mutation.

Resolve **(provider, subject)**, never email alone:

1. Existing subject → load its linked active user; authenticate only that user.
2. No subject and no normalized-email collision → create Customer and unique external identity atomically.
3. Local account with matching email → `409 account_link_required`; **do not silently merge**, even for verified Google email.
4. Linking requires authenticated local session, fresh password verification and valid Google token in `LinkGoogle`; atomically ensure subject belongs to no other user. Different local/Google email requires a separately verified account-change procedure and is deferred. Disabled users and subject collisions are rejected.

## SwiftDrop tokens and sessions

Use signed RS256 access JWTs with issuer configured per environment, explicit audience, sub, roles, iat/nbf/exp, jti and optional authenticated merchant membership. Lifetime **≤900 seconds**; service clocks allow a small explicit skew (≤30s). Service JWTs have separate audience/scope and ≤5-minute lifetime, issued through controlled workload provisioning, never merchant API keys or caller-supplied role headers. Services validate signature/algorithm/issuer/audience/time independently. Strip untrusted X-User-* headers at gateway; do not replace cryptographic authentication with forwarded claims.

Identity exposes `/.well-known/jwks.json` containing public keys only. It is not presented as a full OIDC authorization server and does not invent discovery/code endpoints. Cache trusted JWKS up to 1h with one bounded unknown-kid refresh; rotate retaining old verification keys through token expiry. Fail closed for unknown keys. Google ID tokens are used only for login/link, not as bearer tokens to Delivery.

Refresh tokens are opaque ≥256 random bits, hashed in Identity DB, expiry 30 days, family-linked and rotated atomically at Refresh. Reuse revokes the entire family. Browser receives refresh token as Secure HttpOnly SameSite=Strict cookie restricted to `/api/v1/auth`; `credentials: include` plus exact allowed Origin and CSRF token are required for refresh/logout. On this client the JSON refresh field is omitted; mobile submits it in the body and stores it in platform secure storage. Never keep browser access tokens in persistent localStorage; use memory. Cross-site frontend/API arrangements require an explicit cookie/CSRF design before deployment.

Logout returns 204 and revokes the **caller's** refresh family. **Existing access JWTs remain valid until expiry (at most 15 minutes)**; role/deactivation changes have the same bound in downstream services. Identity refuses new logins/refresh immediately when disabled. No Redis blacklist/backplane is part of this baseline. If immediate downstream revocation becomes required, add an approved introspection/revocation design and tests before claiming it.

## Merchant credentials

Human merchant owners use app JWTs; their external system uses `X-API-Key` with `swd_test_<keyId>_<random>` for local examples (`swd_live_` reserved for a separately configured deployment). At least 256 random secret bits; show complete key once. Store keyId/prefix, random per-key salt and SHA-256(salt || UTF8(rawKey)), scopes, business, active flag. Locate by public keyId and compare hash in constant time. Merchant API validates business Approved, key active and scope on **each request**; suspension/revocation takes effect immediately. Hashes, keys and request credentials never appear in logs. Owner cannot self-approve or mint Admin roles. Webhook keys are **encrypted retrievable secrets**, distinct from one-way API-key hashes.

See [REST](../api/rest-api.md), [authorization](authorization.md), [data model](../architecture/data-architecture.md) and [negative tests](../testing/test-cases.md).

## Protocol reference

[Google ID-token verification and stable subject identifiers](https://developers.google.com/identity/gsi/web/guides/verify-google-id-token) supports signature/audience/issuer/expiry validation and subject-based identity. The stricter explicit local-account linking policy is SwiftDrop’s proposed security choice.
