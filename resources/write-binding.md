---
description: Interoperable authorised creation, update, transition, and governed change requests for Registry Records.
---

# Write

> **Status:** DRAFT requirements and HTTP binding, for review and implementation trials.

## Purpose and capability model

Write defines how an authorised API consumer proposes or commits a change to a Registry Record without depending on the Registry's internal storage or workflow implementation.
An implementation selects any of the following options independently:

| Option | Primary operation | Outcome |
|---|---|---|
| Create | `createRecord` | Atomically creates one authoritative Record. |
| Update | `updateRecord` | Atomically changes the permitted content of one existing Record. |
| Transition | `applyRecordTransition` | Atomically applies one declared lifecycle or domain transition to an existing Record. |
| Change Requests | `submitChangeRequest` | Creates one non-authoritative immutable proposal for later review and application. |

Selecting one option does not select another.
A Registry can expose direct Create, Update, or Transition without Change Requests, expose Change Requests without public direct mutation endpoints, or expose both under separate grants.
Defining the four options does not require a deployment to implement every operation.

A governed service can manage review within the Registry or use an external workflow service.
The external service submits or applies a proposal through the same Registry boundary and does not bypass current Registry validation, authorisation, preconditions, or transition policy.
This binding does not require a general workflow engine, a particular BReg workflow model, withdrawal, multiple approvers, or atomic changes spanning several Records or systems.

The domain schema, allowed values, transitions, approval policy, and institutional authority remain deployment declarations.
The shared Write contract does not select or require a domain schema vocabulary.
Domain-specific models, input forms, projections, and examples are institution-selected and cannot add an undeclared Write permission, mapping, or workflow guarantee.

<a id="published-write-contract"></a>

## Published Write contract

The canonical [Write OpenAPI contract](write-api.yml) defines the HTTP shapes.
Every selected primary operation publishes:

- a typed input schema and result schema;
- its target Registry and logical Collection;
- the operation grant evaluated for that target;
- a deterministic mapping from accepted input into authoritative Record state and retained provenance;
- authentication and any separately declared trusted purpose binding;
- idempotency, precondition, validation, error, and acknowledgement behaviour; and
- synchronous or asynchronous success outcomes.

The target is the institutionally governed Registry and a logical API Collection, not an internal table or workflow queue.
Publishing an operation, grant name, or metadata entry does not grant authority.
The service evaluates current policy on every attempt.

Write input is an operation contract, not a copy of a Consultation response.
A Create declaration, correction request, Update, Transition, or governed proposal can use its own typed form and can carry evidence, reasons, attestations, or other intake data that is not part of the public or permitted Record view.
The operation declares how every accepted field maps to authoritative domain state, retained provenance, or workflow-only context and rejects accepted input for which that mapping is undefined.
Direct and governed paths that represent the same mutation publish aligned mutation semantics, even when their transport envelopes and workflow metadata differ.
Consultation projections can omit, transform, or combine authoritative fields under their separately declared view without changing the Write input contract.

The contract also defines supporting operations for retrieving writable context, reading and listing Change Requests, recording review decisions, withdrawing a request where supported, and retrieving asynchronous Operation status where offered.
These supporting operations do not become additional options of the `registry-service` variation point.
They support the selected Write option and retain their own access requirements.
Application can be performed by a Registry-managed or external worker under a distinct application permission and can invoke a selected direct operation when the deployment exposes one to that trusted component.
The binding does not require a public Change Request application endpoint.

## Direct Write semantics

Create accepts the complete typed declaration input published for its Collection and returns a durable acknowledgement only after one Record is created or asynchronous work is accepted.
The Registry assigns or accepts Record identity only as declared by the contract.
A preview never allocates authoritative identity.

Update accepts only the fields or components declared by its typed correction or update input.
The contract states whether an omitted field is unchanged, cleared, defaulted, or invalid.
The service does not infer generic patch semantics from the HTTP method or schema shape.

Transition accepts one declared transition name and its typed input.
Each transition declares its valid source conditions, resulting semantics, and operation grant.
Possession of a transition name or Record Identifier is not authority to apply it.

Create, Update, and Transition are independently selectable.
The baseline does not require one operation to emulate another, and it does not require a public direct operation merely because an approved Change Request can ultimately cause the same kind of authoritative change.

## Resource path depth

The API Design Guide §5.4 recommends at most two semantic resource levels after `/v1` as a SHOULD, not a MUST.
A named action after the explicit Collection and Record creates three semantic resource levels.
That additional depth is deliberate: it preserves the selected Collection boundary, the addressed Record, and the fixed action meaning without placing an action name in the Record identifier namespace or turning it into a caller-selected generic command.

The non-normative examples use the same rationale for fixed correction and add-member actions.
Supporting paths such as `/v1/change-requests/{changeRequestId}/approve` have only the Change Request and approval-action levels.
The deeper direct action paths retain the guide warning for review; this draft does not claim an approved exception.

<a id="non-normative-domain-examples"></a>

## Non-normative domain examples

The [example contracts and payloads](../api/examples/README.md) demonstrate how institution-selected domain models can bind to Write without becoming shared requirements.
Their field names, vocabularies, validation rules, permissions, and review policies are examples only.

A civil-registration declaration or correction can use an operational input shape that differs from the permitted Birth read projection.
Reasons, supporting evidence, requester context, fees, review decisions, and application state remain command, provenance, or workflow information rather than Birth facts.
Only successfully applied authoritative content enters the read projection; a pending, rejected, withdrawn, blocked, or failed proposal does not alter it.

A Household can be created using references to existing people.
A profile can also create people and the Household together only when it separately declares and verifies one atomic transaction within the same authoritative source.
Request-local references resolve to authoritative Record identifiers only after that compound commit succeeds.
The same boundary applies when adding a member later: adding an existing person needs no compound creation guarantee, while creating and adding a new person together requires the declared same-source transaction guarantee.

These examples do not require a civil-registration or household model, combine those domains under one authority, define a generic batch language, or promise a distributed transaction.

<a id="atomicity-and-compound-changes"></a>

## Atomicity and compound changes

Each operation declares its own component boundary.
Within that boundary, success is all or nothing: a Create does not leave a partial Record, an Update does not commit only some declared components, a Transition does not advance state without its associated committed data, and a Change Request submission does not create a partially stored proposal.

Atomicity across additional Records, Collections, Registries, messages, credentials, or external systems is a stronger guarantee that a deployment declares and verifies separately.
The baseline permits a workflow to coordinate several independently committed components and report an explicit partial or compensating outcome, provided it does not label that sequence atomic.

<a id="retries-and-idempotency"></a>

## Retries and idempotency

Every selected primary operation accepts the contract's idempotency key and binds it to the authenticated consumer, operation, Registry, Collection, target where present, trusted purpose where required, and canonical request content.
The contract declares key syntax, retention, the replay response, and the conflict returned when the key is reused with different bound content.

A retry with the same key and content cannot create a second committed effect.
The service still applies current authentication and authorisation before executing or disclosing the replayed result.
An idempotency key is neither a credential nor a reservation of future authority.
After the declared retention period, a consumer cannot assume that repeating a mutation is safe and obtains current state before deciding how to recover.

<a id="concurrency-and-commit-guards"></a>

## Concurrency and commit guards

Update and Transition require a strong opaque precondition for the current target representation.
A Change Request that proposes a change to an existing Record captures the same source precondition at submission.
The service rejects an omitted, malformed, or stale required precondition and checks a matching precondition atomically with commit.

The commit guard protects the current target representation.
It does not require a public revision-history operation, retained historical representations, or reconstruction of a revision sequence.
If two writers start from the same target state, at most one can commit under that guard.

<a id="authority-and-purpose"></a>

## Authority and purpose

Read and Write permissions are separate.
A consumer can be allowed to write information it cannot read back, or to read a Record it cannot change.
Create, Update, Transition, Change Request submission, review, and application each have separately evaluated grants and target scopes.

A deployment that enforces purpose declares one trusted binding and controlled values for each affected operation.
Purpose comes from the trusted authentication or authorisation context, not an ordinary query or body field.
Purpose supplements the operation grant and is not consent, institutional authority, approval, or proof of downstream use.

<a id="trusted-context-and-client-input"></a>

## Trusted context and client input

Actor, reviewer, purpose, approval, and application status are derived from trusted security and workflow context.
The service rejects or ignores client-supplied control fields according to the published schema and never treats them as verified authority.
A domain schema can contain fields with similar names as Record data, but those values do not authenticate an actor, select a reviewer, satisfy a purpose rule, approve a request, or apply a change.

<a id="acknowledgement-provenance-and-audit"></a>

## Acknowledgement, provenance, and audit

Every accepted Write uses its declared HTTP status, response schema, target URI, `Location`, or validator to identify the target, created resource, or asynchronous Operation and to distinguish authoritative commit, non-authoritative request creation, and accepted asynchronous work.
A bodyless successful response can identify its existing target through the request URI and validator and does not need an invented response body.
The response does not claim that queued work committed, that a submitted proposal was approved, or that an approved request was applied.
Correlation follows the inherited API guidance and the deployment's published policy rather than requiring a new Write-specific identifier in every response.

The service retains provenance and audit evidence for the trusted actor, selected operation, Registry, Collection, Record or Change Request target, trusted purpose where present, validated input identity, precondition, decision, and committed effect.
The deployment declares retention, integrity, clock, redaction, and access boundaries.
Source or recording time is exposed only when the source provides it with documented source-backed semantics; this binding does not require a new history timestamp.
Audit evidence is protected according to its sensitivity and does not prove legal authority, consent, downstream use, or source facts outside the declared validation scope.

<a id="protected-resources"></a>

## Protected resources

An authenticated caller receives the same generic `404` outcome for an unknown resource and a resource whose existence is protected.
This rule covers protected Records, Collections, Change Requests, Operations, and operation availability where the access policy protects them.
The outcome does not reveal the protected resource through body content, security-relevant headers, workflow state, validation detail, conflict detail, precondition detail, timing classes, counts, or continuation behaviour.
Independently generated trace and correlation values can differ.

Authentication can fail before resource resolution.
After protected resolution begins, the service does not return a more specific conflict or workflow outcome unless the caller is permitted to know that resource and context.

<a id="preview-and-authoritative-state"></a>

## Preview and authoritative state

Validation or preview, when offered, is read-only.
Its response is explicitly non-authoritative and states the policy and source evaluation point used.
It does not allocate an authoritative Record Identifier, advance a Change Request, reserve a transition, or guarantee that a later Write will succeed.

A later Write repeats current authentication, authorisation, input validation, source precondition, trusted-purpose, and transition-policy checks.
Clients distinguish preview data from the authoritative acknowledgement and from Consultation of committed Registry state.

<a id="change-request-lifecycle"></a>

## Change Request lifecycle

Submitting a Change Request creates an immutable non-authoritative resource.
Its stable identifier and version or content digest bind later decisions to the exact proposal content, target, source precondition, submitter context, and provenance reviewed.
Changing any bound proposal content creates another request or version that requires its own decision.
Appending a review note or decision does not change the bound proposal.

Pending and rejected requests have no authoritative Registry side effect.
A withdrawn request also has no authoritative side effect when withdrawal is offered.
Withdrawal is optional, as are multiple reviewers and particular decision rules.

Approval records a decision about the immutable proposal.
Approval alone does not constitute commit and does not guarantee application.
A published review operation can also trigger separately authorised and revalidated application, either synchronously or through an automatic worker, without another public application endpoint.
Its response and request representation distinguish approval with application not started, application processing, applied, blocked, and failed outcomes as supported by the contract.
Only an explicitly acknowledged successful application changes authoritative Registry state.
An approved request can therefore remain unapplied or record an application failure without rewriting the approval decision.

Submission, review, and application use distinct permissions and trusted actor contexts.
One actor can hold several permissions where institutional policy allows it, but each stage is separately authorised and audited.
Distinct permissions do not require distinct HTTP calls.
The workflow can be Registry-managed or external, provided the Registry commit boundary applies the same current checks.

<a id="application-time-revalidation"></a>

## Application-time revalidation

Application rechecks current authentication, application permission, trusted purpose where required, target availability, the retained source precondition, typed input validity, and transition policy.
These checks are atomic with the authoritative commit.
A stale precondition is not weakened, current content is not silently substituted, and changed proposal content is not applied under an earlier decision.

If any check fails, the service records an explicit unapplied outcome and leaves authoritative state unchanged.
The request's approval decision and application outcome remain separately visible to permitted actors.

<a id="http-outcomes"></a>

## HTTP outcomes

Asynchronous execution is optional for each operation and is independent of selecting direct Write, Change Requests, or both.
A synchronous-only deployment omits `202` from its selected operations and, when no Write operation runs asynchronously, need not expose `getOperation`.
The specification defines no separate asynchronous capability flag.

| Situation | Response | Identified resource | Meaning |
|---|---|---|---|
| Authoritative Record created synchronously | `201 Created` | Record | The Record commit completed. |
| Update or Transition committed synchronously | Contract-defined `200` or `204` | Target URI and any declared validator or representation | The authoritative change completed. |
| Change Request submitted for later review | `201 Created` | Change Request | One non-authoritative proposal was created. Waiting for review is not background processing. |
| Review-only approval | `200 OK` | Change Request with approved review and application not started | The decision was recorded; no application work was accepted or completed. |
| Background execution accepted | `202 Accepted` | Operation identified by `Location` | Processing was accepted, but commit, approval, and application remain unproven. |

Every offered `202` path publishes an Operation representation retrievable through `getOperation`, terminal success and failure outcomes, and a retention policy.
An Operation reports execution status only.
It does not replace the Change Request, carry its review authority, or become the source of its review and application state.
The Change Request remains the workflow resource before, during, and after any background application.

A review operation can return `202` only when it also accepts actual background application work.
A review-only decision does not return `202` merely because application might happen later.
An accepted background job can be queued for a worker or scheduled execution and still correctly return `202`.
Update and Transition use their contract-defined synchronous success only after authoritative commit.

<a id="change-request-listing"></a>

## Change Request listing

`listChangeRequests`, when offered, returns only requests permitted for the current caller and context.
It uses deterministic ordering with a unique tie-breaker, bounded Pages, a declared default and maximum size, and opaque integrity-protected continuation.
The cursor is bound to caller context, Registry, Collection, filters, order, and effective page size and expires under the published policy.
Every Page reauthorises.

Malformed, tampered, expired, or context-mismatched cursors fail explicitly and never restart silently.
Empty and short advancing Pages retain the Page shape.
A non-null cursor advances, and `null` marks completion under the declared consistency and result-window policy.
Baseline listing does not promise exhaustive traversal or a fixed source snapshot.

## Conformance boundary

The four Write options are DRAFT and independently selectable under the existing `registry-service` variation point.
Only requirements conditioned on a selected option apply to that option.
Conditional facilities such as preview, withdrawal, asynchronous processing, and request listing apply only when offered.
Stronger compound atomicity, exhaustive listing, snapshot listing, multi-approver policy, and domain-specific state machines are not baseline guarantees.

The OpenAPI contract and examples support artifact review.
They do not establish that a deployed implementation enforces authorisation, atomicity, preconditions, idempotency, workflow separation, protected existence, or crash recovery.
Those claims require the pending runtime scenarios in [Write testing](write-testing.md).
