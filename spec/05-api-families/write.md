---
description: Authorised creation and revision of Registry Records.
---

# Write

> **Status:** Informative. See [Conformance](../04-conformance.md#44-capability-claims).

## Purpose and applicability

Write creates a Record or accepts a new authoritative revision. It applies when the Registry exposes mutation to authorised external actors rather than receiving all changes through internal administration or offline processes.

## Capability patterns

| Pattern | Outcome |
|---|---|
| Direct write | An actor authorised for the relevant transition commits a final change without a Registry-managed approval workflow. |
| Governed write | A proposed change becomes authoritative only after the required review or approval process. |
| Correction | A subject or authorised actor requests correction through the governed path defined for that Registry. |

Deployment rules cover accepted transitions, validation, transition-specific authorisation, idempotency, concurrency, provenance, correction, retirement, and any legally defined deletion behaviour.

## Capability boundary

The Registry Authority remains responsible for accepted transitions and the resulting authoritative state. A Registration, Workflow, or sector-specific service can own intake and approval and then submit an approved result. Write does not require the Registry to implement a general workflow engine.

## Implementation options

Illustrative, non-normative options include synchronous HTTP described by OpenAPI for immediate changes and an asynchronous status pattern for governed or long-running changes.

## Example

After completing its approval process, a land-transfer service submits the approved ownership change. The land Registry validates the transition and records a new authoritative revision.
