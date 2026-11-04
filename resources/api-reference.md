---
description: Canonical Registry API for permitted reads, direct writes, change requests, and asynchronous operations.
---

# Registry API reference

Use this API to read permitted Records, commit authorised direct changes, submit
and review Change Requests, and inspect offered asynchronous Operations. A
deployment independently selects its Registry service options and supporting
operations. It does not have to expose both reads and writes. Each operation
publishes its schemas, access rules, and applicable features or workflow contract.

The [canonical OpenAPI](../api/openapi.yaml) is the single normative transport
entry point for this DRAFT specification. For compatibility,
[`api/write.openapi.yaml`](../api/write.openapi.yaml) and
[`resources/write-api.yml`](write-api.yml) resolve to the same contract. The
draft is not ratified and does not establish an approved conformance target.

The contract groups operations as **Read**, **Write**, **Change Requests**, and
**Operations**. Read and Write permissions remain independent. Mutation input
can differ from a permitted read projection, and accepted values map as declared
to authoritative state, retained provenance, or workflow-only context. A commit
receipt establishes the declared commit outcome. It does not guarantee that the
caller may retrieve the resulting Record, or that a permitted projection is
immediately current.

For Update and Transition, the declared companion Retrieve returns its permitted
body and strong ETag from one current authoritative guard evaluation. The guard
invalidates for every field or source condition that can change that mutation's
validation, mapping, or committed effect; unrelated hidden state need not
invalidate it. The opaque tag grants no authority, and a deployment cannot select
the companion view when policy forbids revealing the tag or its change cadence.
Other reads can retain their declared source currency. A matching tag is expected
only when a later companion Retrieve has reached companion currency and observes
that exact committed state, with no intervening mutation-relevant change, under the
same effective authorisation, disclosure, purpose, and field-selection context.
This is not a promise that a future Retrieve eventually returns the mutation
success tag.

The [birth-registration](api-examples/birth-registration.md),
[business](api-examples/business.md), and
[household](api-examples/household.md) contracts show illustrative deployment
bindings. The [Write examples](api-examples/README.md#non-normative-write-examples)
show direct and approval-based changes. These examples do not add requirements
to the canonical contract.
