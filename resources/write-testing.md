---
description: Draft traceability and pending runtime scenarios for Write operations.
---

# Write testing

> **Status:** DRAFT test design. Artifact checks validate contracts, schemas, links, and examples; they do not establish deployed Write behaviour.

## Verification boundary

The repository validator can check requirement structure, local references, operation identifiers, OpenAPI schemas, and example validity.
It cannot prove current authorisation, commit atomicity, strong preconditions, idempotent replay, protected existence, workflow separation, source behaviour, concurrency, or crash recovery in a deployment.

The cases below are normative verification targets for the selected DRAFT options.
Their runtime status is **pending implementation conformance test** unless a future evidence record identifies the implementation, version, environment, fixtures, requests, responses, source observations, and result.
Schema-valid examples are not recorded as runtime passes.

## Applicability and fixtures

Before executing a runtime case, record:

- the specification and contract version, selected Write options, Registry, Collection, and operation grants;
- the implementation and deployment version, service metadata, source arrangement, and declared component boundary;
- synthetic permitted, denied, unknown, protected, stale, conflicting, and concurrently changed fixtures;
- the trusted actor and purpose contexts, with secrets and personal data excluded from retained evidence;
- the idempotency retention, precondition mechanism, audit scope, request-list bounds, and, where asynchronous execution is offered, Operation retention; and
- which optional facilities are offered, including preview, withdrawal, request listing, asynchronous processing, and separately declared compound guarantees.

An inapplicable optional facility is recorded as not applicable with its contract basis.
It is not counted as a pass and does not weaken another applicable requirement.

## Requirement traceability

| Requirement anchor | Applies when | Exercise | Expected evidence |
|---|---|---|---|
| <a id="write-1"></a>`write-1` | Create selected | Submit valid, invalid, denied, duplicate, and concurrently conflicting Create inputs through every declared synchronous and asynchronous path. | One valid authorised attempt reaches one complete authoritative Record. Each acknowledgement honestly identifies committed or asynchronous status. Rejections and failed work create no Record or partial component. |
| <a id="write-2"></a>`write-2` | Update selected | Update permitted and forbidden fields with matching, omitted, malformed, and stale preconditions, including two concurrent writers and every declared asynchronous path. | Only a currently authorised, valid input with a matching commit-time guard changes the declared fields atomically. Accepted work is not reported as committed, and no intervening change is overwritten. |
| <a id="write-3"></a>`write-3` | Transition selected | Apply every declared transition from valid and invalid source states, then submit an undeclared transition and concurrent attempts through every declared asynchronous path. | Only a permitted transition from its declared current state commits atomically. Accepted work is not reported as committed, and invalid, undeclared, stale, and losing concurrent attempts have no authoritative effect. |
| <a id="write-4"></a>`write-4` | Change Requests selected | Submit valid, invalid, denied, duplicate, and conflicting proposals for each supported proposal kind. | Submission creates one immutable non-authoritative request and no authoritative Record change. Review and application remain separately governed. |
| <a id="write-5"></a>`write-5` | Any Write option selected | Resolve every selected operation from metadata and inspect its typed input, result, Registry, Collection, grant, and mapping into authoritative state or retained provenance. Exercise declaration, correction, evidence, and reason fields where supported. | Declarations are machine-readable, versioned, unambiguous, mutually consistent, and complete for every accepted input. Write input need not equal a Consultation view, and publication does not grant authority. |
| <a id="write-6"></a>`write-6` | Any Write option selected | Inject failures before validation, persistence, commit, acknowledgement, and each separately declared integration boundary. | The operation's own component is all or nothing. Cross-component atomicity passes only where separately declared and exercised. |
| <a id="write-7"></a>`write-7` | Any Write option selected | Replay the same key before, during, and after commit; change content, operation, target, actor, purpose, permissions, and retention state. | One bound request causes at most one committed effect. Mismatched reuse conflicts, current policy is rechecked, and key expiry creates no false retry guarantee. |
| <a id="write-8"></a>`write-8` | Update, Transition, or Change Requests selected | Exercise omitted, malformed, matching, and stale guards; race two writers; change a target after request approval. | The strong target guard is evaluated atomically at commit. At most one competing attempt commits, without requiring published history. |
| <a id="write-9"></a>`write-9` | Any Write option selected | Use read-only, Write-only, combined, and unprivileged actors across operations and targets; where purpose is enforced, vary trusted purpose context. | Read and Write permissions remain independent. Every selected grant and target is checked, and only a declared trusted purpose binding supplies purpose. |
| <a id="write-10"></a>`write-10` | Any Write option selected | Inject actor, reviewer, purpose, approved, applied, and equivalent control fields and flags at every accepted nesting level. | Published schema handling is explicit, and no client field bypasses trusted authentication, authorisation, review, or application controls. |
| <a id="write-11"></a>`write-11` | Any Write option selected | Correlate body-bearing and bodyless success, rejection, replay, asynchronous work, review, and failure before and after commit across protocol responses, state, and audit evidence. | Status, schema, request URI, `Location`, or validator identifies the target, created resource, or Operation as declared and distinguishes committed, non-authoritative, and asynchronous outcomes. Correlation and provenance cover the declared scope without an invented response body, correlation identifier, or timestamp. |
| <a id="write-12"></a>`write-12` | Protected existence applies | Compare unknown and protected Records, Collections, requests, Operations, and operation availability under the same caller context. | Each pair receives the same generic `404` security outcome without resource-specific content or distinguishable workflow, count, or continuation information. |
| <a id="write-13"></a>`write-13` | Preview or validation is offered | Preview valid and invalid changes, alter source state and permissions, then attempt the Write. | Preview is read-only and visibly non-authoritative, allocates no authoritative identity, advances no workflow, and grants no later commit right. |
| <a id="write-14"></a>`write-14` | Change Requests selected | Change proposal content, target, source guard, version, submitter context, and digest before and after a decision; replay the decision elsewhere. | Review and decisions remain bound to the exact immutable request version and content. Altered or cross-request application fails without authoritative effect. |
| <a id="write-15"></a>`write-15` | Change Requests selected | Observe authoritative state while a request is pending, rejected, approved without application, approved with triggered application where offered, processing, applied successfully, blocked, or failed; include withdrawal where offered. | Pending, rejected, and supported withdrawn states have no authoritative effect. Decision and application outcomes remain distinct even in one response, and only successful application changes state. |
| <a id="write-16"></a>`write-16` | Change Requests selected | Exercise submit-only, review-only, apply-only, combined, and denied actors at every workflow stage. | Submission, review, and application each evaluate their own permission and trusted actor context. No stage or approval silently grants another. |
| <a id="write-17"></a>`write-17` | Change Requests selected | After approval, revoke permission, change purpose, protect or remove the target, change source state, invalidate input, and change transition policy. | Application rechecks every current condition atomically with commit. Failure records an explicit unapplied outcome and leaves authoritative state unchanged. |
| <a id="write-18"></a>`write-18` | Any Write option selected | Exercise a synchronous-only deployment without `202` or `getOperation`; synchronous creation and commit; Change Request submission awaiting review; review-only approval; and, where offered, asynchronous acceptance, processing success and failure, and Operation expiry. | Synchronous-only Write needs no Operation resource. `201` identifies a created Record or Change Request. A pending review is not background work. Review-only approval uses the declared Change Request response, such as `200` approved with application not started. `202` identifies retrievable execution work and never substitutes for review state or implies commit, approval, or application. |
| <a id="write-19"></a>`write-19` | Change Request listing offered | Traverse zero, one, and multiple Pages; change bound context and permissions; tamper with and expire cursors; exercise limits, timeout, protected-only matches, and source changes. | Pages are permitted, deterministic, bounded, advancing, reauthorised, and explicit at termination. Invalid continuation never restarts or discloses protected requests. |

## Pending runtime case matrix

| Case | Boundary under test | Required observation | Runtime status |
|---|---|---|---|
| Create commit | Direct Create and source | Acknowledgement, authoritative Record, source write count, and audit correlation agree. | Pending implementation conformance test. |
| Update conflict | Direct Update and source | Two writers using one starting guard produce one commit and one explicit stale-precondition outcome. | Pending implementation conformance test. |
| Transition conflict | Direct Transition and source policy | Invalid source state and a losing concurrent transition produce no authoritative effect. | Pending implementation conformance test. |
| Synchronous-only Write | Selected direct and governed operations | Selected operations declare no `202` outcome, no Operation resource is required, and synchronous success is returned only after the declared commit or request creation completes. | Pending implementation conformance test. |
| Submit request | Change Request intake | `201` identifies one immutable non-authoritative request and the Registry Record remains unchanged. A pending review creates no Operation merely because review will happen later. | Pending implementation conformance test. |
| Approve request | Review decision and optional triggered application | Review-only approval returns the Change Request, such as `200` approved with application not started. Where the review operation also triggers background application, `202` identifies a separate Operation while the Change Request retains the review and application state. | Pending implementation conformance test. |
| Apply request | Application and source | A separate authorised application rechecks current conditions and alone produces the authoritative effect. | Pending implementation conformance test. |
| Rejected or withdrawn request | Workflow and source | Rejection, and withdrawal where offered, cannot mutate authoritative state or be applied later. | Pending implementation conformance test. |
| Permission change after approval | Workflow and current policy | Revoked application permission produces an unapplied outcome without weakening the decision record. | Pending implementation conformance test. |
| Source change after approval | Workflow and source precondition | A stale approved proposal fails at commit and does not overwrite the intervening source change. | Pending implementation conformance test. |
| Idempotent replay after response loss | Client, service, and source | Same actor, key, and content recover one result and one effect. | Pending implementation conformance test. |
| Idempotency mismatch | Client and service | Reuse under changed content, target, actor, operation, or purpose fails explicitly. | Pending implementation conformance test. |
| Crash before commit | Service and source | Recovery exposes no authoritative effect and no false committed acknowledgement. | Pending implementation conformance test. |
| Crash after commit before response | Service and source | Retry recovers the durable committed result without a second effect. | Pending implementation conformance test. |
| Crash during asynchronous work | Operation worker and source, where offered | Operation status reaches one honest terminal outcome and correlates with authoritative state without replacing the Change Request's review or application state. | Pending implementation conformance test. |
| Protected-resource comparison | Access policy and protocol | Unknown and protected fixtures remain indistinguishable at the declared generic `404` boundary. | Pending implementation conformance test. |
| Preview followed by source change | Preview and commit | Preview has no side effect, and commit uses current source and policy rather than previewed assumptions. | Pending implementation conformance test. |
| Request-list source change | Listing and request store | Results follow declared live consistency and bounds without an undeclared exhaustive or snapshot guarantee. | Pending implementation conformance test. |
| Declared compound failure | Write component and declared external components | Every claimed compound guarantee holds at each injected boundary, or the service reports the declared non-atomic outcome. | Pending implementation conformance test. |

## Artifact checks

Artifact validation should confirm that:

- each Write option references `resources/write-api.yml` and its exact primary `operationId`;
- each SERVICE_API requirement resolves its operation in its own declared contract;
- OpenAPI request and response examples validate against their referenced schemas;
- primary and supporting operations use consistent Registry, Collection, identity, error, idempotency, precondition, and acknowledgement definitions;
- operation-specific declaration and correction inputs remain typed, every accepted field maps to authoritative state, retained provenance, or workflow-only context, and no check assumes that Write input equals Consultation `Record.data`;
- local links and all `write-1` through `write-19` anchors resolve; and
- non-normative domain examples do not introduce a domain-schema dependency into the shared contract or requirements.

Passing these checks is artifact evidence only.
Record runtime results separately, including failures and not-applicable cases, and do not convert a schema-valid trace into an implementation pass.
