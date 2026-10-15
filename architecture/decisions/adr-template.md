# Architecture Decision Record Template

Use this template when documenting a new architecture decision. Copy this file and rename it using the convention `adr-NNN-short-title.md`.

---

## ADR-NNN: [Title of Decision]

**Status:** [Proposed | Accepted | Deprecated | Superseded]  
**Date:** [Date of decision]  
**Deciders:** [Who was involved in the decision]

---

### Context

Describe the situation that requires a decision. Include:

- What problem or requirement drives this decision?
- What constraints exist (technical, organizational, timeline)?
- What is the current state, and why is it insufficient?

### Decision

State the decision clearly in one or two sentences.

> We will use [chosen option] for [purpose].

### Rationale

Explain why this decision was made:

- What are the key reasons for choosing this option?
- How does it align with project goals, constraints, and quality attributes?
- What trade-offs were accepted?

### Alternatives Considered

| Option                | Pros                                          | Cons                                          |
| --------------------- | --------------------------------------------- | --------------------------------------------- |
| [Option A]            | [Advantages]                                  | [Disadvantages]                               |
| [Option B]            | [Advantages]                                  | [Disadvantages]                               |
| **[Chosen Option]**   | **[Advantages]**                              | **[Accepted trade-offs]**                     |

### Consequences

Describe the outcomes of this decision:

- **Positive:** What improvements or benefits does this decision bring?
- **Negative:** What risks, trade-offs, or constraints does it introduce?
- **Neutral:** What changes are required but have no clear positive or negative impact?

### Related Decisions

- [ADR-NNN: Related Decision Title](./adr-NNN-related-title.md)

### References

- [Relevant documentation or external resources]

---

> **Guidance:**  
> - Keep ADRs concise and focused on one decision.  
> - Record the decision as close to the time it was made as practical.  
> - Update the status if a decision is later superseded or deprecated.  
> - Link to related ADRs when decisions are connected.  
> - Add the new ADR to the [ADR Index](README.md).
