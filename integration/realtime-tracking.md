# Real-Time Status Tracking

> Status: Proposed baseline 2.0 · DEC-08 · One Delivery instance for demo

Delivery hosts authenticated `GET /api/v1/parcels/{id}/events` through YARP; allow owner Customer, assigned Courier, Dispatcher/Admin. Public tracking uses only the safe snapshot endpoint/GraphQL and has no private SSE subscription. Flutter **Customer and Courier** share backend authorization; React provides all roles. There is no standalone realtime process or SignalR requirement.

## Browser and mobile authentication

Native browser EventSource cannot set an arbitrary Authorization header. React uses `fetch` streaming with Bearer access token and AbortController. Do not place long-lived tokens into query strings. Browser refresh tokens use a Secure HttpOnly same-site cookie; access token stays in memory. Flutter uses a streaming HTTP client with Bearer header and platform secure storage for refresh token. Gateway enforces a known-origin CORS policy; preflight and HTTPS must be configured for the actual client origin.

```javascript
// openEvents and parseSse are application adapters, not native EventSource options.
async function trackParcel(baseUrl, parcelId, token, signal, apply) {
  const headers = { Authorization: `Bearer ${token}` };
  const response = await fetch(`${baseUrl}/api/v1/parcels/${encodeURIComponent(parcelId)}/events`, {
    headers, signal, cache: "no-store"
  });
  if (!response.ok || !response.body) throw new Error(`SSE ${response.status}`);
  // Start consuming immediately, buffering snapshots until current state is fetched.
  const buffered = [];
  let ready = false;
  let version = 0;
  const accept = value => {
    if (!ready) buffered.push(value);
    else if (value.version > version) { version = value.version; apply(value); }
  };
  const consume = parseSse(response.body, accept, signal);
  const snapshotResponse = await fetch(`${baseUrl}/api/v1/parcels/${encodeURIComponent(parcelId)}`, { headers, signal, cache: "no-store" });
  if (!snapshotResponse.ok) { await response.body.cancel().catch(() => {}); throw new Error(`Snapshot ${snapshotResponse.status}`); }
  const current = await snapshotResponse.json();
  version = current.version;
  apply(current);
  ready = true;
  buffered.sort((a, b) => a.version - b.version).forEach(accept);
  await consume; // parseSse must handle chunked UTF-8, multiline data and comments.
}
```

This is a control-flow example; `parseSse` requires a tested incremental SSE parser, bounded buffer and caller cancellation/retry handling. On snapshot failure abort the whole connection through the caller's controller; do not leave an unobserved consume promise. On 401 refresh once and reconnect; on 403/404 stop; on network loss retry with jittered 1s→30s backoff. Do not deploy the sketch as a complete client library.

## Snapshot and reconnect contract

Connection registration occurs before its initial DB snapshot. Send `event: snapshot`, `id: <parcelId>:<version>` and `data: {id,status,version,lastUpdatedAt}` only; an authorized client fetches private details separately. Subsequent broker wake-ups read the latest DB status, not an older event payload. Keep a per-connection maximum version; apply only newer versions. Send heartbeat comments every 15s and a DB snapshot reconciliation every 30s so a lost wake-up cannot permanently hide a committed status. Terminate at token expiry and recheck assignment/ownership at each snapshot/wake-up; reassignment closes old courier access.

On every reconnect subscribe/register first and fetch an authorized current snapshot while buffering updates, then apply only versions newer than the snapshot. This closes the refetch→subscribe gap. `Last-Event-ID` is informational; **no durable missed-event replay is promised**. Clients obtain timeline history by authenticated GetParcel if needed. Server sends no-cache/no-transform, disables proxy buffering, flushes heartbeats and bounds slow-client queues (close/refetch on overflow). Status target ≤2s is a test goal, not a measured result.

## Broker and scaling boundary

Delivery's `delivery-realtime` queue receives a copy of StatusChanged independently of Worker `notification-status`. One queue with multiple consumers load-balances messages; it does **not** send each event to every Delivery replica. The demo therefore uses one Delivery instance. Horizontal scaling requires unique per-instance fanout subscriptions or an approved pub/sub backplane, plus auth/reconnection tests across replicas. Redis/GPS/SignalR are deferred additional scope. [Event topology](event-catalog.md) and [service inventory](../architecture/service-catalog.md) define the same ownership.

## Protocol reference

[WHATWG EventSource interface](https://html.spec.whatwg.org/multipage/server-sent-events.html#the-eventsource-interface) defines URL/withCredentials construction, without arbitrary request headers. Authenticated fetch streaming and the snapshot recovery policy are SwiftDrop’s proposed client design.
