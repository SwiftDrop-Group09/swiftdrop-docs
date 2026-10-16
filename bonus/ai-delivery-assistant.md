# AI Delivery Assistant Bonus

> Status: Optional +5 bonus proposal · Assignment PDF page 3 verified · No implementation or live model/tool integration verified

The [+5 assignment bonus](../requirements/sources/ead-group-assignment.pdf#page=3) requires a Generative AI **chatbot** that answers parcel-location/fee questions by calling backend APIs. A tool catalog alone does not complete the bonus. MCP exposure is encouraged, not mandatory. Work begins only after mandatory APIs and RBAC are settled. The required delivery system must work without AI. Minimal proposed tools are **TrackParcel** and **EstimateFee**; there are no autonomous booking, assignment, status, refund or administration actions. This is independent of the Kubernetes bonus.

| Tool | Backend and authority | Safe output |
|---|---|---|
| TrackParcel | Anonymous PublicTrack returns safe summary; authenticated private tracking requires own Customer/assigned Courier/operations authorization, or merchant-own job through Merchant API | Default public allowlisted summary; no cross-merchant/customer data or proof URL |
| EstimateFee | Customer-scoped EstimateFee handler; merchant pricing requests must use an explicitly reviewed merchant contract before support | Versioned quote total/expiry; user must confirm through normal booking UI |

Never trust model-supplied userId/merchantId/role. Server establishes identity and enforces all resource checks at tool execution. Minimize prompt/tool logs, redact secrets and PII, treat merchant content as data, use exact schema validation, allowlist tools and bound request time/cost. On not-found/unauthorized, dependency failure or invalid input return safe deterministic errors; do not invent tracking events/price or silently perform a write. A quote tool may persist only an owner-bound fee quote, never a booking.

Acceptance scenarios: authorized own tracking, foreign customer/merchant denial, anonymous private-field refusal, expired quote/reprice, invalid parcel data, prompt injection requesting Admin action, hallucinated tool name, timeout and absent model service. Record actual tool-call transcripts with synthetic data, commit, cost/latency and reviewer. Provider/model selection, credentials and grading conversion/scaling remain unconfirmed; do not claim this bonus complete from the written proposal.
