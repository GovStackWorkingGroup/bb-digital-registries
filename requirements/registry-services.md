---
title: Provide Registry Services
description: |
  An API consumer uses the Registry service operations declared in the Registry's published contract.
realises: [registry-services]
conformance: CORE
requirements:
  - id:
    key: registry-service
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    statement: The Digital Registry provides at least one Registry service through a defined option (consultation-retrieve, consultation-lookup, consultation-list, consultation-search, consultation-revision-list, consultation-revision-retrieve, write-create, write-update, write-transition, or write-change-requests).
    documentation: |
      Purpose: Every conformant Digital Registry provides a useful Registry service while allowing an implementation to expose only the operations its source and policy support.
      Scope: This is the Registry-wide service choice, not a permanent requirement for the Consultation family. This draft defines six Consultation options and four Write options. The remaining six families remain informative and cannot count toward this choice. A future version can define options from those families when their requirements, contracts, and tests are approved.
      Constraint: Only PUBLISHED options count toward the minimum. Publishing another option follows the framework's major-version rule. Selectable read features declared in an operation's `features` array and caller capability discovery are not options; they add requirements to a claim but do not by themselves satisfy this choice.
      Verification: Count the selected options that pass their requirements; at least one passes.
    select:
      min: 1
  - id:
    key: consultation-retrieve
    option_of: registry-service
    status: DRAFT
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: SERVICE_API
    contract: resources/api.yml
    api_operation_id: retrieveRecord
    statement: The Digital Registry retrieves a Record in the selected Collection by a valid Record Identifier, returning by default the latest permitted representation available under the declared currency contract and, only when the operation declares a temporal feature and the request supplies its selector, the source-backed representation selected by that temporal context with the applied context echoed.
    documentation: |
      Purpose: An API consumer obtains the latest representation of one known Record, or an explicitly selected source-backed temporal state, without changing the source Record.
      Prerequisite: The Collection declares its Registry context and view.
      Constraint: Temporal override is always explicit; omission selects the latest representation. An unknown identifier, a Record outside the Collection, or unavailable protected history receives the binding's unavailable-Record outcome, subject to protected-existence handling.
      Verification: Retrieve a known source fixture without a temporal selector and check its latest identity, schema, currency documentation, and declared metadata. Where temporal features are selected, repeat with explicit supported selectors and compare the echoed context and representation with source history. Confirm that the source Record is unchanged; exercise an unknown identifier and, where applicable, an identifier belonging to another Collection.
    test: resources/testing.md#consultation-1
  - id:
    key: consultation-lookup
    option_of: registry-service
    status: DRAFT
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: SERVICE_API
    contract: resources/api.yml
    api_operation_id: lookupRecord
    statement: The Digital Registry resolves a Record through a published exact selector within the selector's declared uniqueness scope.
    documentation: |
      Purpose: An API consumer resolves a Record from a declared exact domain key without depending on the Registry's Record Identifier.
      Prerequisite: Every selector declares its required key components, comparison and normalisation rules, uniqueness scope, and any components derived from verified consumer context.
      Constraint: A selector can be composite and resolves at most one Record. A permitted unique match in the selected collection returns that Record; zero matches produce the unresolved outcome. A source uniqueness violation produces a failure governed by disclosure policy. Invalid, incomplete, incorrectly typed, and unsupported inputs are rejected. A fully context-derived selector accepts an empty caller-supplied `values` object.
      Verification: Exercise known, unknown, incomplete, incorrectly typed, and unsupported inputs, plus a source uniqueness violation. Verify comparison rules, composite keys where supported, context-derived components where declared, and protected-existence handling.
    test: resources/testing.md#consultation-4
  - id:
    key: consultation-list
    option_of: registry-service
    status: DRAFT
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: SERVICE_API
    contract: resources/api.yml
    api_operation_id: listRecords
    statement: The Digital Registry returns a bounded Page of permitted Records from a declared collection using its supported equality filters and deterministic ordering.
    documentation: |
      Purpose: An API consumer traverses a declared collection through a bounded and predictable operation.
      Prerequisite: The collection declares its order, unique tie-breaker, filters, and sorting.
      Constraint: Filters address declared non-personal fields only. Zero and single-result collections retain the Page shape. Unsupported filters or sorting produce a validation error.
      Verification: Use fixtures with zero, one, and multiple results, including tied sort values where applicable. Check membership, schemas, order, size bounds, and rejection of unsupported inputs.
    test: resources/testing.md#consultation-5
  - id:
    key: consultation-search
    option_of: registry-service
    status: DRAFT
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: SERVICE_API
    contract: resources/api.yml
    api_operation_id: searchRecords
    statement: The Digital Registry returns a bounded Page of permitted Records in the selected Collection that match a published search name and its typed criteria under the independently selected reusable comparison semantics and any domain-specific rules declared by that search.
    documentation: |
      Purpose: An API consumer performs a declared search without exposing personal criteria in request URLs or logs.
      Prerequisite: Every search declares its criteria schema, applicable reusable semantics, combination rules, and any domain-specific matching rules.
      Constraint: Zero and single-result searches retain the Page shape. A successful query with zero permitted matches returns `200` with an empty `items` array, including when source matches exist but disclosure policy filters all of them. A search contract can support equality, range, set-membership, prefix, or another named typed semantic without implementing the others. Unsupported searches, operators, criteria, and invalid inputs produce a validation error.
      Verification: Execute declared searches with valid and invalid inputs. Check matching results, a true zero-result Page, and a `200` empty Page whose source matches are all protected or withheld. For temporal Search, distinguish a successful empty Page from `409 temporal-state-not-available` when the source cannot evaluate the requested historical query. Check applicable disclosure contexts and use of the binding's protected request locations for personal criteria.
    test: resources/testing.md#consultation-6
  - id:
    key: consultation-revision-list
    option_of: registry-service
    status: DRAFT
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: SERVICE_API
    contract: resources/api.yml
    api_operation_id: listRecordRevisions
    statement: The Digital Registry returns a bounded RevisionPage of source-backed retained revisions for one Record in the selected Collection, each a RecordRevision with a stable recordId equal to the parent path identifier, the declared history view, and a required revision.revisionId.
    documentation: |
      Purpose: An API consumer reads the retained history of one known Record without fabricated history or a false completeness claim.
      Prerequisite: The source retains distinguishable revisions, and the operation declares a history view and pagination contract.
      Constraint: `revision.recordedAt` is included only when supported by the source. The contract declares revision order, tie-breaker, retention, known and unknown gap semantics, schema-version interpretation, and unavailable-history outcomes. A history view can normalise older source schemas into its declared schema while preserving source values and meanings. When a retained revision cannot be mapped faithfully, the operation returns its declared explicit failure instead of returning an arbitrary raw schema or fabricating values. A result never presents omitted or unavailable history as complete.
      Verification: List retained revisions for fixtures with several revisions, a single revision, a documented gap, and history outside the retention boundary. Check stable Record identity, source-backed revision identity and time, declared order, schema interpretation, current authorisation on every Page, and protected unavailable outcomes.
    test: resources/testing.md#consultation-12
  - id:
    key: consultation-revision-retrieve
    option_of: registry-service
    status: DRAFT
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: SERVICE_API
    contract: resources/api.yml
    api_operation_id: retrieveRecordRevision
    statement: The Digital Registry resolves a declared Revision Identifier for one Record in the selected Collection and returns that source-backed RecordRevision with recordId equal to the parent path identifier.
    documentation: |
      Purpose: An API consumer reads one identified retained revision of a Record without substitution of another state.
      Prerequisite: The source can address retained revisions by stable identifiers.
      Constraint: Record and Revision Identifiers are opaque and are not reconstructed from timestamps. An unknown, expired, removed, outside-retention, protected, or otherwise unavailable revision produces the declared unavailable outcome. The service does not substitute the latest Record, a nearby revision, or a fabricated representation.
      Verification: Retrieve known retained revisions represented under applicable schema versions. Exercise unknown, removed, outside-retention, protected, and Record-mismatched revision identifiers and verify the declared unavailable outcome without fallback or existence disclosure.
    test: resources/testing.md#consultation-13
  - id:
    key: write-create
    option_of: registry-service
    status: DRAFT
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: SERVICE_API
    contract: resources/write-api.yml
    api_operation_id: createRecord
    statement: The Digital Registry accepts an authorised typed Create input for a declared target Registry and Collection and either atomically creates one authoritative Record with a durable acknowledgement or accepts separately identifiable asynchronous work whose terminal success represents that commit.
    documentation: |
      Purpose: An authorised API consumer creates one authoritative Record without depending on the Registry's internal storage or administration interface.
      Prerequisite: The operation publishes its input schema, target Registry and Collection, applicable operation grant, and successful acknowledgement schema.
      Constraint: Selecting Create does not select Update, Transition, or Change Requests. The service validates the complete submitted input and does not present accepted asynchronous work or a partially committed Record as successful.
      Verification: Submit valid, invalid, unauthorised, duplicate, and concurrently conflicting inputs through every declared synchronous and asynchronous path. Confirm that exactly one valid authorised attempt reaches a terminal committed Record, each acknowledgement identifies its honest stage, and failed attempts leave no authoritative Record or partial component.
    test: resources/write-testing.md#write-1
  - id:
    key: write-update
    option_of: registry-service
    status: DRAFT
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: SERVICE_API
    contract: resources/write-api.yml
    api_operation_id: updateRecord
    statement: The Digital Registry accepts an authorised typed Update input for one existing Record in a declared target Registry and Collection and either atomically commits the permitted change against the required current target state or accepts separately identifiable asynchronous work that rechecks that state at commit.
    documentation: |
      Purpose: An authorised API consumer changes the declared content of one authoritative Record without losing concurrent changes.
      Prerequisite: The operation publishes its input schema, target Registry and Collection, operation grant, update semantics, and strong precondition mechanism.
      Constraint: Selecting Update does not select Create, Transition, or Change Requests. The operation changes only the fields and components allowed by its contract and does not require the Registry to expose retained revision history.
      Verification: Exercise every declared synchronous and asynchronous path with valid and invalid inputs, omitted and stale preconditions, concurrent writers, unauthorised changes, and fields outside the permitted update shape. Confirm one atomic committed result or an explicit unsuccessful outcome without partial mutation.
    test: resources/write-testing.md#write-2
  - id:
    key: write-transition
    option_of: registry-service
    status: DRAFT
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: SERVICE_API
    contract: resources/write-api.yml
    api_operation_id: applyRecordTransition
    statement: The Digital Registry accepts an authorised typed Transition input naming a declared transition for one existing Record and either atomically commits it when valid for the required current target state or accepts separately identifiable asynchronous work that rechecks that state at commit.
    documentation: |
      Purpose: An authorised API consumer applies a Registry-defined lifecycle or domain transition without obtaining a generic mutation capability.
      Prerequisite: The operation publishes each supported transition's input schema, target Registry and Collection, operation grant, permitted source states, resulting semantics, and strong precondition mechanism.
      Constraint: Selecting Transition does not select Create, Update, or Change Requests. The transition name grants no authority by itself, and the specification does not prescribe a domain state machine.
      Verification: Exercise every declared synchronous and asynchronous path for each declared transition from valid and invalid source states, with valid, invalid, omitted, and stale preconditions and concurrent attempts. Confirm the declared atomic result and rejection of undeclared transitions.
    test: resources/write-testing.md#write-3
  - id:
    key: write-change-requests
    option_of: registry-service
    status: DRAFT
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: SERVICE_API
    contract: resources/write-api.yml
    api_operation_id: submitChangeRequest
    statement: The Digital Registry accepts an authorised typed change request for a declared target Registry and Collection as a non-authoritative immutable proposal whose later review and application are governed independently from submission.
    documentation: |
      Purpose: A Registry-managed or external workflow can submit proposed creation, update, or transition content without making that content authoritative at submission time.
      Prerequisite: The operation publishes the allowed proposal kinds and input schemas, target Registry and Collection, submission grant, request representation, and lifecycle semantics.
      Constraint: Selecting Change Requests does not select any direct Write option and does not require public Create, Update, or Transition endpoints. It does not require withdrawal, multiple approvers, or a particular workflow implementation.
      Verification: Submit valid, invalid, unauthorised, duplicate, and conflicting proposals. Confirm that a successful submission creates one immutable request and no authoritative Record change, and that review and application follow their separately authorised lifecycle.
    test: resources/write-testing.md#write-4
  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: FILE
    contract: requirements/registry-services.md#write-published-write-contract
    applies_when: [write-create, write-update, write-transition, write-change-requests]
    statement: Every selected Write operation publishes typed input and result schemas, its required operation grant, an unambiguous target Registry and Collection, and a deterministic mapping from every accepted input field into authoritative domain state, retained provenance, or workflow-only context in its machine-readable contract.
    documentation: |
      Purpose: Consumers can determine what they can submit, which authority is required, and where an accepted change applies without relying on storage names or undocumented conventions.
      Prerequisite: The Registry publishes metadata for the target Registry and a versioned Write contract.
      Constraint: A Collection is a logical API grouping. Publication of an operation or grant name does not grant authority. Shared schemas can be reused, but each operation declares its own target and access requirement. An operation-specific declaration or correction input can differ from the Consultation view and can carry evidence or reason data that is not Record output. Its contract still types that input and declares how accepted values, evidence, and reasons map to authoritative state or retained provenance.
      Verification: Resolve each selected operation from Registry metadata and inspect its input, result, Registry, Collection, operation-grant, and mapping declarations. Exercise every declared input variant, including evidence and reason fields where supported, and reject missing, contradictory, ambiguous, or unresolvable declarations and unmapped accepted input.
    test: resources/write-testing.md#write-5
  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: PROTOCOL
    contract: requirements/registry-services.md#write-atomicity-and-compound-changes
    applies_when: [write-create, write-update, write-transition, write-change-requests]
    statement: A Write operation commits or records its own declared component atomically, and it claims atomicity across additional Records, Collections, Registries, or external systems only when that compound boundary and its failure guarantees are separately declared.
    documentation: |
      Purpose: A successful outcome never hides a partial mutation inside the operation's own component, while deployments remain free to offer stronger compound guarantees explicitly.
      Prerequisite: The operation contract defines its component boundary and success outcome.
      Constraint: The baseline does not require multi-Record, cross-Collection, cross-Registry, or distributed transaction atomicity. A workflow can coordinate several independently committed components when it does not claim compound atomicity.
      Verification: Inject validation, persistence, acknowledgement, and declared integration failures around the commit boundary. Confirm all-or-nothing behaviour inside the component and verify every separately declared compound guarantee at each failure point.
    test: resources/write-testing.md#write-6
  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: PROTOCOL
    contract: requirements/registry-services.md#write-retries-and-idempotency
    applies_when: [write-create, write-update, write-transition, write-change-requests]
    statement: Every selected Write operation defines retry and idempotency behaviour, binds an idempotency key to the authenticated consumer, operation, target, and canonical request content, and applies current authentication and authorisation on every attempt without treating the key as authority.
    documentation: |
      Purpose: A consumer can recover from a lost response without accidentally repeating a change or replaying another consumer's request.
      Prerequisite: The contract declares the idempotency-key syntax, retention, replay result, and conflict outcome.
      Constraint: Reuse with different bound content fails explicitly. Reuse after permission loss does not execute or disclose a result that current policy withholds. Expiry does not imply that a repeated mutation is safe.
      Verification: Retry before, during, and after commit with the same key and content; change the content, operation, target, consumer, purpose, and permissions; then retry after retention expiry. Confirm one committed effect and the declared current-authorisation outcomes.
    test: resources/write-testing.md#write-7
  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: PROTOCOL
    contract: requirements/registry-services.md#write-concurrency-and-commit-guards
    applies_when: [write-update, write-transition, write-change-requests]
    statement: An operation that proposes or commits a change to an existing Record uses a strong precondition bound to the current target representation and re-evaluates that guard at commit, rejecting an omitted, invalid, or stale precondition without overwriting intervening change.
    documentation: |
      Purpose: Concurrent writers do not silently lose one another's committed changes.
      Prerequisite: The service exposes a strong opaque validator or another contract-defined compare-and-commit token for the target representation.
      Constraint: The guard is checked atomically with commit. It protects the current target and does not require the Registry to publish or retain revision history. A submitted change request retains its source precondition for later re-evaluation.
      Verification: Submit omitted, malformed, matching, and stale guards; race two matching attempts; and change the target between request approval and application. Confirm that only a guard matching the commit-time target can commit.
    test: resources/write-testing.md#write-8
  - id:
    status: DRAFT
    level: REQUIRED
    observability: AUDITABLE
    mutability: EXTENSIBLE
    interaction: INTERNAL
    contract: requirements/registry-services.md#write-authority-and-purpose
    applies_when: [write-create, write-update, write-transition, write-change-requests]
    statement: The Digital Registry authorises Write independently from read disclosure, evaluates the selected operation's grant for the current actor and target, and, when purpose is enforced, obtains it only through a separately declared trusted purpose binding.
    documentation: |
      Purpose: Permission to observe a Record neither grants permission to change it nor follows automatically from permission to submit, review, or apply a proposal.
      Prerequisite: The deployment documents the authentication boundary, operation grants, target scope, and any trusted purpose binding and controlled values.
      Constraint: Write permission does not imply read permission, and read permission does not imply Write permission. Purpose is not accepted from an ordinary body or query field and is not treated as consent, legal authority, approval, or proof of downstream use.
      Evidence: Access-policy configuration and audit evidence for permitted and denied actors, separate read and Write entitlements, target scope, and any trusted purpose evaluation.
      Verification: Exercise actors with read-only, Write-only, both, and neither permission across targets and operations. Where purpose is enforced, exercise missing, untrusted, malformed, allowed, and disallowed trusted contexts.
    test: resources/write-testing.md#write-9
  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: PROTOCOL
    contract: requirements/registry-services.md#write-trusted-context-and-client-input
    applies_when: [write-create, write-update, write-transition, write-change-requests]
    statement: The service never treats client-supplied actor, reviewer, purpose, or approval fields or flags as verified authority and rejects or ignores them according to the published schema without silently bypassing authentication, authorisation, review, or application controls.
    documentation: |
      Purpose: A caller cannot impersonate another actor or turn a proposal into an approved or applied change by setting request fields.
      Prerequisite: The contract distinguishes client input from values derived through trusted authentication, authorisation, and workflow context.
      Constraint: Domain data can contain similarly named fields when the schema defines them as Record content, but those values do not control access or workflow decisions.
      Verification: Inject actor, reviewer, purpose, approved, applied, status, and equivalent fields at every accepted nesting level. Confirm schema handling and verify that all security and workflow decisions use trusted context.
    test: resources/write-testing.md#write-10
  - id:
    status: DRAFT
    level: REQUIRED
    observability: AUDITABLE
    mutability: EXTENSIBLE
    interaction: INTERNAL
    contract: requirements/registry-services.md#write-acknowledgement-provenance-and-audit
    applies_when: [write-create, write-update, write-transition, write-change-requests]
    statement: Every accepted Write uses its HTTP status, response schema, target URI, `Location`, or validator as declared to identify the target, created resource, or asynchronous Operation and distinguish a committed change from accepted work or a non-authoritative request, while the service retains provenance and audit evidence for the actor, operation, target, trusted context, validation, decision, and committed effect within its declared audit scope.
    documentation: |
      Purpose: A consumer can distinguish a committed Record change, a submitted request, and accepted asynchronous work, and an assessor can reconstruct the decision without inferring facts outside the declared audit scope.
      Prerequisite: The service publishes each response contract and documents correlation under the inherited API guidance plus audit retention, access, integrity, clock, and redaction boundaries.
      Constraint: A successful bodyless response can identify its existing target through the request URI and validator and need not invent a response body. Source or recording time is included only when the source supplies it with documented source-backed semantics. Audit evidence does not by itself prove legal authority, consent, downstream use, or source facts that the operation did not validate. Sensitive request content is protected in retained evidence.
      Evidence: Protocol responses and integrity-protected audit records correlated according to the declared policy across success, rejection, replay, review, asynchronous processing, and commit failure.
      Verification: Correlate protocol responses with authoritative state, request state, and audit evidence. Exercise body-bearing and bodyless success where declared, rejection, idempotent replay, and failure before and after commit, checking target or resource identification and honest status without requiring an invented timestamp or body.
    test: resources/write-testing.md#write-11
  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: PROTOCOL
    contract: requirements/registry-services.md#write-protected-resources
    applies_when: [write-create, write-update, write-transition, write-change-requests]
    statement: When target Record, Collection, Change Request, or operation existence is protected, the Write service gives an unknown and a protected resource the same generic `404` outcome without resource-specific content or a distinguishable workflow, timing, or continuation signal.
    documentation: |
      Purpose: A caller cannot use a Write endpoint to discover protected Registry resources or request activity.
      Prerequisite: The access policy declares protected existence and supplies unknown and protected fixtures under the same caller context.
      Constraint: Authentication can fail before resource resolution. Once an authenticated caller reaches protected resolution, validation, conflict, precondition, or workflow details do not reveal the protected resource.
      Verification: Compare unknown and protected Records, Collections, requests, and operations under the same context across body, headers, security-relevant metadata, workflow state, pagination, and independently generated trace values.
    test: resources/write-testing.md#write-12
  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: PROTOCOL
    contract: requirements/registry-services.md#write-preview-and-authoritative-state
    applies_when: [write-create, write-update, write-transition, write-change-requests]
    statement: A validation or preview operation is read-only and labels its result as non-authoritative, never allocates an authoritative Record identity, advances a Change Request, reserves a transition, or presents predicted content as committed state.
    documentation: |
      Purpose: A caller can inspect a possible outcome without confusing prediction with Registry authority.
      Condition: The selected Write binding offers validation or preview.
      Prerequisite: The preview contract declares the data and policy evaluation point and its non-authoritative response schema.
      Constraint: Preview can become stale immediately and grants no right to a later commit. A later Write performs current validation, authorisation, precondition, and policy checks.
      Verification: Preview valid and invalid inputs, change source state and permissions, then attempt commit. Confirm no side effect from preview and distinguish every preview representation and identifier from authoritative acknowledgement.
    test: resources/write-testing.md#write-13
  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: SERVICE_API
    contract: resources/write-api.yml
    api_operation_id: submitChangeRequest
    applies_when: [write-change-requests]
    statement: "A submitted Change Request is immutable: review, approval, rejection, withdrawal when offered, and application remain bound to its exact request version, canonical proposal content, target, source precondition, submitter context, and recorded provenance."
    documentation: |
      Purpose: A decision cannot be reused for changed proposal content or a different target.
      Prerequisite: The Change Request representation carries a stable request identifier and immutable version or content digest.
      Constraint: Correcting proposal content creates another request or version that requires its own review under the published lifecycle. A note or decision can be appended without changing the bound proposal.
      Verification: Alter every bound element before and after a decision, replay a decision against another request or version, and verify explicit rejection without authoritative side effect.
    test: resources/write-testing.md#write-14
  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: PROTOCOL
    contract: requirements/registry-services.md#write-change-request-lifecycle
    applies_when: [write-change-requests]
    statement: Pending and rejected Change Requests, and withdrawn Change Requests when withdrawal is offered, have no authoritative Registry side effect; approval records a decision but does not by itself represent or guarantee application.
    documentation: |
      Purpose: Workflow state cannot be mistaken for committed Registry state.
      Prerequisite: The service documents its request states, allowed decisions, terminal states, and application outcome.
      Constraint: Withdrawal is optional. Multiple reviewers and approval rules are deployment choices. An approved request can remain unapplied or fail application. A review operation can trigger separately authorised and revalidated application without another public endpoint, but its response distinguishes approval, processing, applied, blocked, and failed outcomes as applicable. Only an explicitly acknowledged successful commit changes authoritative state.
      Verification: Exercise pending, rejection, approval without application, approval that triggers application where offered, application success and failure, plus withdrawal where offered. Read authoritative state after every step and confirm that only successful application changes it and that one response never conflates the decision with the commit outcome.
    test: resources/write-testing.md#write-15
  - id:
    status: DRAFT
    level: REQUIRED
    observability: AUDITABLE
    mutability: EXTENSIBLE
    interaction: INTERNAL
    contract: requirements/registry-services.md#write-change-request-lifecycle
    applies_when: [write-change-requests]
    statement: Submission, review, and application use distinct permissions and trusted actor contexts, and no permission or successful decision in one stage grants another stage or makes an approved request equivalent to an applied change.
    documentation: |
      Purpose: A deployment preserves separation of duties without imposing one approval topology.
      Prerequisite: The workflow declares which component performs each stage and the grants it evaluates, whether Registry-managed or external.
      Constraint: The same actor can hold several permissions when institutional policy allows it, but each stage is still separately authorised and audited. Distinct permissions do not require distinct HTTP calls: one published review operation can approve and trigger application only after evaluating both stages. The specification does not require multiple approvers, a separate application endpoint, or a Registry-managed workflow engine.
      Evidence: Access-policy configuration and correlated audit records for submission, review decisions, application attempts, and denials at each stage.
      Verification: Exercise submit-only, review-only, apply-only, combined, and unauthorised actors. Confirm that each stage evaluates only its own grant and that approval alone leaves authoritative state unchanged.
    test: resources/write-testing.md#write-16
  - id:
    status: DRAFT
    level: REQUIRED
    observability: AUDITABLE
    mutability: EXTENSIBLE
    interaction: INTERNAL
    contract: requirements/registry-services.md#write-application-time-revalidation
    applies_when: [write-change-requests]
    statement: Application of an approved Change Request re-evaluates current authentication, application permission, trusted purpose where required, target availability, source precondition, input validity, and transition policy atomically with commit, and records an explicit unapplied outcome when any check fails.
    documentation: |
      Purpose: Approval does not freeze permissions or silently overwrite changes made after submission.
      Prerequisite: The approved request retains the exact proposal and source guard needed for commit-time evaluation.
      Constraint: The service does not weaken a stale guard, substitute current content, or silently resubmit a changed proposal. A failed application leaves the approval decision distinguishable from the unapplied authoritative outcome.
      Evidence: Correlated request, decision, application-attempt, policy-evaluation, precondition, and commit records.
      Verification: After approval, revoke each permission, change purpose, protect or remove the target, change the Record, invalidate the input, and change transition policy. Confirm explicit failure and no authoritative side effect for every case.
    test: resources/write-testing.md#write-17
  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: PROTOCOL
    contract: requirements/registry-services.md#write-http-outcomes
    applies_when: [write-create, write-update, write-transition, write-change-requests]
    statement: A selected Write operation returns `201 Created` only when it creates the identified resource, including a newly submitted Change Request, and, when that operation offers asynchronous execution, returns `202 Accepted` only for separately identifiable background work whose Operation status can be retrieved without implying a committed Record change, review decision, or applied request.
    documentation: |
      Purpose: A consumer can distinguish a created resource from queued work and from an authoritative commit.
      Condition: Asynchronous execution is optional for each selected operation independently of whether the deployment selects direct Write, Change Requests, or both.
      Prerequisite: Every offered asynchronous path publishes an Operation representation, status retrieval, terminal outcomes, and retention policy.
      Constraint: A synchronous-only operation omits `202`. A deployment with no asynchronous Write path need not expose `getOperation`. A `202` acknowledgement is not success of the requested mutation. Completed Change Request creation uses `201` and waiting for manual review is not background processing. Review-only approval returns the declared Change Request success response, such as `200` with approved and application not started, rather than `202`; an Operation cannot replace the Change Request's review or application state. A review operation uses `202` only when it also accepts actual background application work.
      Verification: Exercise a synchronous-only deployment with no `202` response or Operation endpoint, synchronous Record creation and commit, Change Request submission awaiting review, review-only approval, and, where offered, asynchronous acceptance, processing success, processing failure, and status expiry. Correlate each response with its Record, Change Request, or Operation and authoritative state.
    test: resources/write-testing.md#write-18
  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: PROTOCOL
    contract: requirements/registry-services.md#write-change-request-listing
    applies_when: [write-change-requests]
    statement: A Change Request listing operation, when offered, returns only permitted requests in deterministic bounded Pages, uses an opaque integrity-protected cursor bound to the caller context, Registry, Collection, filters, ordering, and effective page size, and reauthorises every Page without claiming exhaustive or snapshot traversal unless separately declared.
    documentation: |
      Purpose: Reviewers can traverse authorised work queues without unbounded responses, cursor substitution, or protected-request disclosure.
      Condition: The service offers Change Request listing.
      Prerequisite: The contract declares filters, deterministic order and unique tie-breaker, default and maximum page sizes, cursor expiry, source-consistency behaviour, timeout outcome, and any result-window bound.
      Constraint: Malformed, expired, tampered, or context-mismatched cursors fail explicitly and never restart silently. Empty and short Pages retain the Page shape and a non-null cursor advances; `null` marks completion under the declared baseline semantics.
      Verification: Traverse zero, one, and multi-page permitted fixtures; change each bound context value and permissions between Pages; exercise malformed, expired, and tampered cursors, declared limits, timeout, protected-only matches, and source changes.
    test: resources/write-testing.md#write-19
  - id:
    status: DRAFT
    level: REQUIRED
    observability: AUDITABLE
    mutability: EXTENSIBLE
    interaction: INTERNAL
    statement: The Digital Registry keeps each Record Identifier unchanged throughout the Record's lifecycle and revisions and never reassigns it to another Record.
    documentation: |
      Purpose: A Record reference remains unambiguous after changes, retirement, archival, or deletion.
      Prerequisite: The implementation has a documented Record Identifier lifecycle policy, which can be the source system's policy adopted by an adaptor.
      Constraint: An adaptor over an existing source can inherit the source's identifier policy when that policy keeps identifiers stable and prevents reassignment.
      Evidence: The identifier lifecycle policy and evidence covering successive revisions, distinct Records, retirement, archival, and deletion.
      Verification: Review the policy and evidence showing that successive revisions retain the same identifier, distinct Records do not share an identifier, and retired identifiers are not returned to the allocation pool.
    test: resources/testing.md#core-3
  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: FILE
    contract: requirements/registry-services.md#core-domain-semantics-and-extensions
    statement: The Digital Registry publishes the representation format, unambiguously identified resolvable machine-readable schemas, and documented field meanings for its Registry service operations.
    documentation: |
      Purpose: API consumers can decode, validate, and interpret a representation without knowledge of internal storage.
      Prerequisite: The implementation has published the applicable representation format, schemas, and domain documentation.
      Constraint: Documentation covers adopted model versions, mappings, extensions, field meanings, units, code lists, absence semantics, components, Record references, embedded representations, collection bounds, completeness semantics, any applicable target Registry context and read binding, and a formal semantic-model reference where the selected capability or profile requires one.
      Verification: Use only the published contract and response context to identify each format and schema. Check the documented semantics and resolve a formal semantic-model reference where the selected contract requires one.
    test: resources/testing.md#core-4

  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: SERVICE_API
    contract: resources/api.yml
    api_operation_id: getCallerCapabilities
    statement: The caller capability discovery operation, when offered, returns one bounded CallerCapabilities document filtered for the authenticated caller and current trusted request context that identifies each visible Collection by its collectionId and registry and each visible operation by its operationId, capability annotation, view, and version-specific HTTPS contract, without granting authority or replacing authorisation at invocation time.
    documentation: |
      Purpose: A caller learns which declared Consultation operations are currently disclosed as available to it, while every invocation remains separately authorised.
      Condition: The Digital Registry offers caller capability discovery. Offering it does not by itself satisfy the minimum Registry service choice.
      Prerequisite: The service publishes the bounded response schema and authentication requirements.
      Constraint: The filtering context includes a verified purpose when one is present. The document can omit operations whose required purpose is absent from that context; discovery itself does not select `purpose-bound` or create a new purpose input. The document contains at most 64 Collections, each with at most 16 operations. `collectionId` is unique within the document, and each `(contract, operationId)` pair is unique. An operation entry can additionally publish bounded `readableFields`, selector and named Search identifiers, feature annotations, and purpose requirements. `readableFields` describes fields the caller can receive under current policy. It is distinct from `field-selection`, does not advertise a `fields` input, and need not be present even when readable fields exist.
      Constraint: Known discovery annotations agree with the linked operation's Collection, capability, view, selected features, and purpose declaration. Capability and feature annotations in `CallerCapabilities` are extensible for forward-compatible advisory discovery: a client skips an operation entry whose capability annotation it does not understand and ignores unknown feature annotations on an otherwise understood entry. The normative `x-govstack-digital-registries` extension in the linked versioned operation remains closed to the capability and feature values defined by that contract version. Unknown discovery metadata never grants authority, adds an operation, or widens fields. The identifiers point into the contract; the response does not reproduce their complete schemas. Contradictory duplicates or known metadata produce the declared explicit validation failure; the service does not silently merge them. The response uses `Cache-Control: no-store`. If the caller-available description exceeds a declared array or document bound, the service returns its declared explicit error instead of truncating entries, silently omitting authorised capabilities, or substituting an empty array. `collections: []` is reserved for the valid case where no operation is visible to that caller.
      Constraint: The document is advisory. It does not grant authority, replace authorisation at invocation time, promise access to any particular Record, require disclosure of every readable field, or define a reusable profile model. An omitted operation or field establishes only that it is not disclosed as available in that response.
      Verification: Request discovery under callers and trusted contexts with different permissions. Validate bounds, unique Collection identifiers and `(contract, operationId)` pairs, contract agreement, `readableFields`, selectors, searches, known features, purpose requirements, and `no-store`; confirm that `readableFields` does not imply `field-selection`. Submit an unknown capability annotation and verify that the entry is skipped; submit an unknown advisory feature and verify that it is ignored without granting authority. Confirm that the linked operation extension still rejects unknown capability and feature values. Submit contradictory duplicates and contradictory known metadata and exceed every declared bound, verifying explicit failures without merge, truncation, or silent omission. Then verify that every discovered operation still performs current authorisation and that no record-level permission can be inferred.
    test: resources/testing.md#consultation-17

  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: SERVICE_API
    contract: resources/api.yml
    api_operation_id: retrieveRecord
    applies_when: [consultation-retrieve]
    statement: The Retrieve operation returns every Record representation with a Record Identifier that, together with the unambiguous Registry context defined by the binding, uniquely identifies that Record.
    documentation: |
      Purpose: Consumers distinguish Records from different Registries and refer to one Record without depending on mutable domain attributes.
      Prerequisite: A Record has been accepted into the Registry.
      Constraint: The binding defines how the consumer determines the Registry Identifier from the request, published contract and service metadata, or the representation itself.
      Verification: Obtain two distinct Record fixtures through Retrieve and verify their different Record Identifiers and Registry context. Where several Registries are exposed, verify that identical local identifiers remain distinguishable.
    test: resources/testing.md#core-2
  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: SERVICE_API
    contract: resources/api.yml
    api_operation_id: retrieveRecord
    applies_when: [consultation-retrieve]
    statement: The Retrieve operation returns Record representations in the published format that validate against the operation's unambiguously identified schema and use its documented field meanings.
    documentation: |
      Purpose: Consumers decode, validate, and interpret Retrieve representations without knowledge of internal storage.
      Prerequisite: The applicable representation format, schema, and domain documentation are published.
      Verification: Obtain a Retrieve representation, identify its format and schema using only the published contract and response context, validate it, and check the published field and nested-value semantics against the fixture.
    test: resources/testing.md#core-4
  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: SERVICE_API
    contract: resources/api.yml
    api_operation_id: retrieveRecord
    applies_when: [consultation-retrieve]
    statement: The Retrieve operation returns exposed revision and lifecycle metadata with the source semantics declared in the representation schema.
    documentation: |
      Purpose: Consumers interpret available revision and lifecycle information without inferring guarantees that the source does not provide.
      Condition: The Retrieve response exposes revision or lifecycle metadata; otherwise the metadata scenarios are not applicable.
      Constraint: A selected capability or profile supplies any additional guarantees. Baseline Record reads do not require revision or lifecycle fields, and a representation validator is not presented as a source revision unless the source contract establishes that equivalence.
      Verification: Compare provided metadata with source fixtures and the declared schema, including the meaning of revisions and exposed lifecycle states.
    test: resources/testing.md#core-5
  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: SERVICE_API
    contract: resources/api.yml
    api_operation_id: retrieveRecord
    applies_when: [consultation-retrieve]
    statement: The Retrieve operation returns a Registry context that resolves through published metadata to the responsible Registry Authority and returns any additional exposed Record provenance with its documented, source-supported meaning.
    documentation: |
      Purpose: A consumer identifies the institutional source and interprets available provenance without fabricated source facts.
      Condition: Additional provenance checks apply only to fields exposed by the Retrieve contract.
      Constraint: A recording time is required only where the selected capability or profile requires it; retrieval time is not substituted for recording time, and unavailable provenance that the capability or profile does not require is omitted rather than inferred.
      Verification: Resolve the Record's Registry context to its published authority and compare every additional exposed provenance value and meaning with source evidence.
    test: resources/testing.md#core-6
  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: FILE
    contract: api/extensions/x-govstack-digital-registries.schema.json
    applies_when: [consultation-retrieve]
    statement: The Digital Registry publishes an OpenAPI contract that declares the Retrieve operation's Registry Identifier, Collection, capability, view, and any selected selectable read features through a valid x-govstack-digital-registries extension, with the Collection equal to the operation path's collectionId or its fixed concrete value, the Registry Identifier resolving to published Registry metadata, the same Record schema used by every operation declaring the same Collection and view, the features array listing only the read features the operation implements, and a valid purpose declaration with its trusted binding when the operation selects purpose-bound.
    documentation: |
      Purpose: A consumer or validator determines from the contract which Registry, logical Collection, and authority the Retrieve operation belongs to, which representation it returns, and which selectable guarantees it supports.
      Prerequisite: Registry metadata and the OpenAPI contract are published.
      Constraint: Each listed feature respects its capability applicability and dependencies. An absent or empty `features` array establishes no selectable feature claim. Caller capability discovery follows its separate cross-Collection schema and is verified under its own requirement.
      Verification: Validate the Retrieve extension against its schema, resolve its Registry Identifier through the metadata, compare its Collection with the path, and compare response schemas for operations sharing the Collection and view. Check each selected feature against the operation's inputs, responses, and declared guarantees, and validate any required purpose object and trusted binding.
    test: resources/testing.md#core-8
  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: SERVICE_API
    contract: resources/api.yml
    api_operation_id: retrieveRecord
    applies_when: [consultation-retrieve]
    statement: The Retrieve operation returns a representation valid against the declared view schema and exposes only information permitted for the consumer and request context, including through fields, metadata, references, embedded data, errors, and other result information.
    documentation: |
      Purpose: A consumer receives the permitted representation without disclosure through adjacent response content.
      Prerequisite: The access policy for the declared view is documented.
      Constraint: Withholding and consumer field selection operate within the declared view schema; neither substitutes another schema nor grants additional disclosure rights. Disclosure also governs counts and continuation information where present.
      Verification: Exercise Retrieve with fixtures for each applicable access policy, including different entitlements where offered, and check representation validity and every permitted information channel.
    test: resources/testing.md#consultation-2
  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: SERVICE_API
    contract: resources/api.yml
    api_operation_id: retrieveRecord
    applies_when: [consultation-retrieve]
    statement: The Retrieve operation gives unknown and protected Records the same unresolved outcome, including equivalent protocol status, security-relevant metadata, error type, response structure, and non-Record-specific values, without Record-specific data and with independently generated trace and correlation values.
    documentation: |
      Purpose: A caller cannot determine protected Record existence from the unresolved outcome.
      Condition: The access policy protects Record existence.
      Prerequisite: The access policy declares which Records have protected existence. Protected and unknown fixtures are available under the same consumer context.
      Verification: Compare protected and unknown Retrieve fixtures under the same consumer context and check every listed aspect of the outcome and its trace values.
    test: resources/testing.md#consultation-3
  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: SERVICE_API
    contract: resources/api.yml
    api_operation_id: retrieveRecord
    applies_when: [consultation-retrieve]
    statement: The Retrieve operation declaring conditional-read returns a representation ETag on successful responses, accepts If-None-Match, and evaluates current authorisation before returning a bodyless 304 with the matching ETag.
    documentation: |
      Purpose: A consumer revalidates a permitted representation without receiving an unchanged body again.
      Condition: The Retrieve operation declares `conditional-read` in its `features` array. An operation without this feature need not support conditional GET.
      Prerequisite: The operation declares `If-None-Match`, `200` and `304` responses, and their ETag headers.
      Constraint: The validator identifies the permitted representation, including effective field selection where supported; it is not a source revision identifier.
      Verification: Retrieve a permitted representation, repeat with its validator, and check the bodyless `304`. Change the represented data or selected fields and check validator behaviour. Revoke access before a conditional request and verify that authorisation is applied before any `304` response.
    test: resources/testing.md#consultation-8
  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: SERVICE_API
    contract: resources/api.yml
    api_operation_id: retrieveRecord
    applies_when: [consultation-retrieve]
    statement: The Retrieve operation declaring field-selection accepts a non-empty, duplicate-free list of declared top-level data field names and returns only the selected fields that disclosure policy permits, together with any mandatory data fields documented by the view.
    documentation: |
      Purpose: A consumer requests a declared subset of the view's selectable `data` fields without a different view schema or additional disclosure rights.
      Condition: The Retrieve operation declares `field-selection` in its `features` array.
      Prerequisite: The operation publishes its allowed field names, default field set, mandatory fields if any, selection bounds, and omission semantics.
      Constraint: `recordId` and the `data` object remain present even when no selected field can be disclosed. Selectable fields are not required in the view schema so default and selected responses validate against the same schema. Omission of the input uses the declared default field set. Unknown selections and invalid inputs are rejected.
      Verification: Select one and several supported fields, check schema validity and retained identity, and compare default and selected responses under applicable disclosure policies. Reject empty, duplicate, unknown, and incorrectly typed selections.
    test: resources/testing.md#consultation-9
  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: SERVICE_API
    contract: resources/api.yml
    api_operation_id: retrieveRecord
    applies_when: [consultation-retrieve]
    statement: The Retrieve operation declaring recorded-time accepts recordedAsOf, a date-time cutoff for information accepted by the source, returns a representation based only on source knowledge accepted no later than that cutoff, and echoes the applied recordedAsOf context in a TemporalRecord.
    documentation: |
      Purpose: A consumer reads what the source knew at a declared acceptance cutoff.
      Condition: The Retrieve operation declares `recorded-time` in its `features` array.
      Prerequisite: The operation documents the source event that establishes acceptance, timestamp precision, timezone treatment, inclusivity, retention, and unavailable-history outcome.
      Constraint: The selection is subject to the source's declared recording semantics, corrections, retention, and gaps. Omitting this coordinate selects the latest available source knowledge while still applying any supplied `effectiveAt`; it makes no historical-knowledge claim. Revision operations instead identify history directly by Record and Revision Identifiers and do not accept this selector.
      Verification: Select cutoffs before, at, and after accepted source revisions, including a correction and any declared gap. Compare the result and echoed context with source evidence. Distinguish a proven absent item (`404 record-not-available`) from a source unable to evaluate the requested historical selection (`409 temporal-state-not-available`). Verify that request time, adapter ingestion time, event occurrence time, and registration date are not substituted unless the source contract explicitly defines one as its acceptance time.
    test: resources/testing.md#consultation-14
  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: SERVICE_API
    contract: resources/api.yml
    api_operation_id: retrieveRecord
    applies_when: [consultation-retrieve]
    statement: The Retrieve operation declaring effective-time accepts effectiveAt, a date or date-time at which the source declares information applicable, returns the source-backed representation selected by that applicability, and echoes the applied effectiveAt context in a TemporalRecord.
    documentation: |
      Purpose: A consumer reads the information the source declares applicable at a date or instant.
      Condition: The Retrieve operation declares `effective-time` in its `features` array.
      Prerequisite: The source has a declared applicability model supporting the accepted selector precision.
      Constraint: The contract defines whether it accepts dates, instants, or both, plus boundary, timezone, overlap, correction, and no-applicable-state semantics. Omitting this coordinate uses the operation's declared default applicability without overriding any supplied `recordedAsOf`; it makes no explicit effective-time claim. Revision operations instead identify history directly by Record and Revision Identifiers and do not accept this selector.
      Constraint: Event occurrence and registration dates are domain facts, not automatically effective-time coordinates. A source can define either as effective time for a particular field or history model, but the service does not infer that equivalence.
      Verification: Exercise date and instant boundaries supported by the contract, overlapping or corrected applicability where possible, and a point with no applicable state. Distinguish a proven absent item (`404 record-not-available`) from a source unable to evaluate the requested historical selection (`409 temporal-state-not-available`). Compare the result and echoed context with source evidence and confirm that occurrence or registration dates are not silently substituted.
    test: resources/testing.md#consultation-15
  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: SERVICE_API
    contract: resources/api.yml
    api_operation_id: retrieveRecord
    applies_when: [consultation-retrieve]
    statement: The Retrieve operation declaring purpose-bound declares a purpose object with required set to true, a non-empty unique allowedPurposes list of controlled bounded non-whitespace codes or absolute URIs, and one trusted binding, obtains the purpose only from that binding, and rejects a missing, untrusted, malformed, or unallowed purpose before Record information is disclosed.
    documentation: |
      Purpose: A deployment enforces a trusted, controlled purpose for the operation without treating it as consent, authority, or proof of use.
      Condition: The Retrieve operation declares `purpose-bound` in its `features` array.
      Prerequisite: The deployment has a trusted purpose binding, and its controlled allowed values and audit treatment are documented.
      Constraint: `access-token-claim` also requires the `claim` name. `trusted-authorization-context` obtains the value from the deployment's authentication and authorisation boundary. Purpose is not accepted from a query parameter or request body.
      Constraint: The effective purpose is bound to cursors, conditional validators, current and historical reads, temporal selection, and the service's audit evidence. A continuation or validator cannot be replayed under another purpose. The contract documents how multiple values and purpose changes are handled.
      Constraint: Declared purpose is distinct from consent, legal or institutional authority, and actual downstream use. One does not prove the others. This feature supplements the inherited authentication and authorisation contract; operations that do not select it retain their inherited security requirements and do not acquire a universal purpose parameter.
      Verification: Exercise missing, malformed, untrusted, allowed, and disallowed purpose contexts; reuse a cursor and conditional validator under another purpose; and compare current, historical, and temporal behaviour. Check rejection before disclosure and verify the recorded effective purpose without treating it as evidence of consent, authority, or downstream use.
    test: resources/testing.md#consultation-18

  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: SERVICE_API
    contract: resources/api.yml
    api_operation_id: lookupRecord
    applies_when: [consultation-lookup]
    statement: The Lookup operation returns every Record representation with a Record Identifier that, together with the unambiguous Registry context defined by the binding, uniquely identifies that Record.
    documentation: |
      Purpose: Consumers distinguish Records from different Registries and refer to one Record without depending on mutable domain attributes.
      Prerequisite: A Record has been accepted into the Registry.
      Constraint: The binding defines how the consumer determines the Registry Identifier from the request, published contract and service metadata, or the representation itself.
      Verification: Obtain two distinct Record fixtures through Lookup and verify their different Record Identifiers and Registry context. Where several Registries are exposed, verify that identical local identifiers remain distinguishable.
    test: resources/testing.md#core-2
  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: SERVICE_API
    contract: resources/api.yml
    api_operation_id: lookupRecord
    applies_when: [consultation-lookup]
    statement: The Lookup operation returns Record representations in the published format that validate against the operation's unambiguously identified schema and use its documented field meanings.
    documentation: |
      Purpose: Consumers decode, validate, and interpret Lookup representations without knowledge of internal storage.
      Prerequisite: The applicable representation format, schema, and domain documentation are published.
      Verification: Obtain a Lookup representation, identify its format and schema using only the published contract and response context, validate it, and check the published field and nested-value semantics against the fixture.
    test: resources/testing.md#core-4
  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: SERVICE_API
    contract: resources/api.yml
    api_operation_id: lookupRecord
    applies_when: [consultation-lookup]
    statement: The Lookup operation returns exposed revision and lifecycle metadata with the source semantics declared in the representation schema.
    documentation: |
      Purpose: Consumers interpret available revision and lifecycle information without inferring guarantees that the source does not provide.
      Condition: The Lookup response exposes revision or lifecycle metadata; otherwise the metadata scenarios are not applicable.
      Constraint: A selected capability or profile supplies any additional guarantees. Baseline Record reads do not require revision or lifecycle fields, and a representation validator is not presented as a source revision unless the source contract establishes that equivalence.
      Verification: Compare provided metadata with source fixtures and the declared schema, including the meaning of revisions and exposed lifecycle states.
    test: resources/testing.md#core-5
  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: SERVICE_API
    contract: resources/api.yml
    api_operation_id: lookupRecord
    applies_when: [consultation-lookup]
    statement: The Lookup operation returns a Registry context that resolves through published metadata to the responsible Registry Authority and returns any additional exposed Record provenance with its documented, source-supported meaning.
    documentation: |
      Purpose: A consumer identifies the institutional source and interprets available provenance without fabricated source facts.
      Condition: Additional provenance checks apply only to fields exposed by the Lookup contract.
      Constraint: A recording time is required only where the selected capability or profile requires it; retrieval time is not substituted for recording time, and unavailable provenance that the capability or profile does not require is omitted rather than inferred.
      Verification: Resolve the Record's Registry context to its published authority and compare every additional exposed provenance value and meaning with source evidence.
    test: resources/testing.md#core-6
  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: FILE
    contract: api/extensions/x-govstack-digital-registries.schema.json
    applies_when: [consultation-lookup]
    statement: The Digital Registry publishes an OpenAPI contract that declares the Lookup operation's Registry Identifier, Collection, capability, view, and any selected selectable read features through a valid x-govstack-digital-registries extension, with the Collection equal to the operation path's collectionId or its fixed concrete value, the Registry Identifier resolving to published Registry metadata, the same Record schema used by every operation declaring the same Collection and view, the features array listing only the read features the operation implements, and a valid purpose declaration with its trusted binding when the operation selects purpose-bound.
    documentation: |
      Purpose: A consumer or validator determines from the contract which Registry, logical Collection, and authority the Lookup operation belongs to, which representation it returns, and which selectable guarantees it supports.
      Prerequisite: Registry metadata and the OpenAPI contract are published.
      Constraint: Each listed feature respects its capability applicability and dependencies. An absent or empty `features` array establishes no selectable feature claim. Caller capability discovery follows its separate cross-Collection schema and is verified under its own requirement.
      Verification: Validate the Lookup extension against its schema, resolve its Registry Identifier through the metadata, compare its Collection with the path, and compare response schemas for operations sharing the Collection and view. Check each selected feature against the operation's inputs, responses, and declared guarantees, and validate any required purpose object and trusted binding.
    test: resources/testing.md#core-8
  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: SERVICE_API
    contract: resources/api.yml
    api_operation_id: lookupRecord
    applies_when: [consultation-lookup]
    statement: The Lookup operation returns a representation valid against the declared view schema and exposes only information permitted for the consumer and request context, including through fields, metadata, references, embedded data, errors, and other result information.
    documentation: |
      Purpose: A consumer receives the permitted representation without disclosure through adjacent response content.
      Prerequisite: The access policy for the declared view is documented.
      Constraint: Withholding and consumer field selection operate within the declared view schema; neither substitutes another schema nor grants additional disclosure rights. Disclosure also governs counts and continuation information where present.
      Verification: Exercise Lookup with fixtures for each applicable access policy, including different entitlements where offered, and check representation validity and every permitted information channel.
    test: resources/testing.md#consultation-2
  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: SERVICE_API
    contract: resources/api.yml
    api_operation_id: lookupRecord
    applies_when: [consultation-lookup]
    statement: The Lookup operation gives unknown and protected Records and protected-key source uniqueness violations the same unresolved outcome, including equivalent protocol status, security-relevant metadata, error type, response structure, and non-Record-specific values, without Record-specific data and with independently generated trace and correlation values.
    documentation: |
      Purpose: A caller cannot determine protected Record or key existence from the unresolved outcome.
      Condition: The access policy protects Record or key existence.
      Prerequisite: The access policy declares which Records and selector keys have protected existence. Protected, unknown, and source-uniqueness-violation fixtures are available under the same consumer context.
      Verification: Compare protected, unknown, and protected-key uniqueness-violation Lookup fixtures under the same consumer context and check every listed aspect of the outcome and its trace values.
    test: resources/testing.md#consultation-3
  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: SERVICE_API
    contract: resources/api.yml
    api_operation_id: lookupRecord
    applies_when: [consultation-lookup]
    statement: The Lookup operation declaring field-selection accepts a non-empty, duplicate-free list of declared top-level data field names and returns only the selected fields that disclosure policy permits, together with any mandatory data fields documented by the view.
    documentation: |
      Purpose: A consumer requests a declared subset of the view's selectable `data` fields without a different view schema or additional disclosure rights.
      Condition: The Lookup operation declares `field-selection` in its `features` array.
      Prerequisite: The operation publishes its allowed field names, default field set, mandatory fields if any, selection bounds, and omission semantics.
      Constraint: `recordId` and the `data` object remain present even when no selected field can be disclosed. Selectable fields are not required in the view schema so default and selected responses validate against the same schema. Omission of the input uses the declared default field set. Unknown selections and invalid inputs are rejected.
      Verification: Select one and several supported fields, check schema validity and retained identity, and compare default and selected responses under applicable disclosure policies. Reject empty, duplicate, unknown, and incorrectly typed selections.
    test: resources/testing.md#consultation-9
  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: SERVICE_API
    contract: resources/api.yml
    api_operation_id: lookupRecord
    applies_when: [consultation-lookup]
    statement: The Lookup operation declaring recorded-time accepts recordedAsOf, a date-time cutoff for information accepted by the source, returns a representation based only on source knowledge accepted no later than that cutoff, and echoes the applied recordedAsOf context in a TemporalRecord.
    documentation: |
      Purpose: A consumer reads what the source knew at a declared acceptance cutoff.
      Condition: The Lookup operation declares `recorded-time` in its `features` array.
      Prerequisite: The operation documents the source event that establishes acceptance, timestamp precision, timezone treatment, inclusivity, retention, and unavailable-history outcome.
      Constraint: The selection is subject to the source's declared recording semantics, corrections, retention, and gaps. Omitting this coordinate selects the latest available source knowledge while still applying any supplied `effectiveAt`; it makes no historical-knowledge claim. Revision operations instead identify history directly by Record and Revision Identifiers and do not accept this selector.
      Verification: Select cutoffs before, at, and after accepted source revisions, including a correction and any declared gap. Compare the result and echoed context with source evidence. Distinguish a proven absent item (`404 record-not-available`) from a source unable to evaluate the requested historical selection (`409 temporal-state-not-available`). Verify that request time, adapter ingestion time, event occurrence time, and registration date are not substituted unless the source contract explicitly defines one as its acceptance time.
    test: resources/testing.md#consultation-14
  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: SERVICE_API
    contract: resources/api.yml
    api_operation_id: lookupRecord
    applies_when: [consultation-lookup]
    statement: The Lookup operation declaring effective-time accepts effectiveAt, a date or date-time at which the source declares information applicable, returns the source-backed representation selected by that applicability, and echoes the applied effectiveAt context in a TemporalRecord.
    documentation: |
      Purpose: A consumer reads the information the source declares applicable at a date or instant.
      Condition: The Lookup operation declares `effective-time` in its `features` array.
      Prerequisite: The source has a declared applicability model supporting the accepted selector precision.
      Constraint: The contract defines whether it accepts dates, instants, or both, plus boundary, timezone, overlap, correction, and no-applicable-state semantics. Omitting this coordinate uses the operation's declared default applicability without overriding any supplied `recordedAsOf`; it makes no explicit effective-time claim. Revision operations instead identify history directly by Record and Revision Identifiers and do not accept this selector.
      Constraint: Event occurrence and registration dates are domain facts, not automatically effective-time coordinates. A source can define either as effective time for a particular field or history model, but the service does not infer that equivalence.
      Verification: Exercise date and instant boundaries supported by the contract, overlapping or corrected applicability where possible, and a point with no applicable state. Distinguish a proven absent item (`404 record-not-available`) from a source unable to evaluate the requested historical selection (`409 temporal-state-not-available`). Compare the result and echoed context with source evidence and confirm that occurrence or registration dates are not silently substituted.
    test: resources/testing.md#consultation-15
  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: SERVICE_API
    contract: resources/api.yml
    api_operation_id: lookupRecord
    applies_when: [consultation-lookup]
    statement: The Lookup operation declaring purpose-bound declares a purpose object with required set to true, a non-empty unique allowedPurposes list of controlled bounded non-whitespace codes or absolute URIs, and one trusted binding, obtains the purpose only from that binding, and rejects a missing, untrusted, malformed, or unallowed purpose before Record information is disclosed.
    documentation: |
      Purpose: A deployment enforces a trusted, controlled purpose for the operation without treating it as consent, authority, or proof of use.
      Condition: The Lookup operation declares `purpose-bound` in its `features` array.
      Prerequisite: The deployment has a trusted purpose binding, and its controlled allowed values and audit treatment are documented.
      Constraint: `access-token-claim` also requires the `claim` name. `trusted-authorization-context` obtains the value from the deployment's authentication and authorisation boundary. Purpose is not accepted from a query parameter or request body.
      Constraint: The effective purpose is bound to cursors, conditional validators, current and historical reads, temporal selection, and the service's audit evidence. A continuation or validator cannot be replayed under another purpose. The contract documents how multiple values and purpose changes are handled.
      Constraint: Declared purpose is distinct from consent, legal or institutional authority, and actual downstream use. One does not prove the others. This feature supplements the inherited authentication and authorisation contract; operations that do not select it retain their inherited security requirements and do not acquire a universal purpose parameter.
      Verification: Exercise missing, malformed, untrusted, allowed, and disallowed purpose contexts; reuse a cursor and conditional validator under another purpose; and compare current, historical, and temporal behaviour. Check rejection before disclosure and verify the recorded effective purpose without treating it as evidence of consent, authority, or downstream use.
    test: resources/testing.md#consultation-18

  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: SERVICE_API
    contract: resources/api.yml
    api_operation_id: listRecords
    applies_when: [consultation-list]
    statement: The List operation returns every Record representation with a Record Identifier that, together with the unambiguous Registry context defined by the binding, uniquely identifies that Record.
    documentation: |
      Purpose: Consumers distinguish Records from different Registries and refer to one Record without depending on mutable domain attributes.
      Prerequisite: A Record has been accepted into the Registry.
      Constraint: The binding defines how the consumer determines the Registry Identifier from the request, published contract and service metadata, or the representation itself.
      Verification: Obtain two distinct Record fixtures through List and verify their different Record Identifiers and Registry context. Where several Registries are exposed, verify that identical local identifiers remain distinguishable.
    test: resources/testing.md#core-2
  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: SERVICE_API
    contract: resources/api.yml
    api_operation_id: listRecords
    applies_when: [consultation-list]
    statement: The List operation returns Record representations in the published format that validate against the operation's unambiguously identified schema and use its documented field meanings.
    documentation: |
      Purpose: Consumers decode, validate, and interpret List representations without knowledge of internal storage.
      Prerequisite: The applicable representation format, schema, and domain documentation are published.
      Verification: Obtain a List representation, identify its format and schema using only the published contract and response context, validate it, and check the published field and nested-value semantics against the fixture.
    test: resources/testing.md#core-4
  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: SERVICE_API
    contract: resources/api.yml
    api_operation_id: listRecords
    applies_when: [consultation-list]
    statement: The List operation returns exposed revision and lifecycle metadata with the source semantics declared in the representation schema.
    documentation: |
      Purpose: Consumers interpret available revision and lifecycle information without inferring guarantees that the source does not provide.
      Condition: A List Record exposes revision or lifecycle metadata; otherwise the metadata scenarios are not applicable.
      Constraint: A selected capability or profile supplies any additional guarantees. Baseline Record reads do not require revision or lifecycle fields, and a representation validator is not presented as a source revision unless the source contract establishes that equivalence.
      Verification: Compare provided metadata with source fixtures and the declared schema, including the meaning of revisions and exposed lifecycle states.
    test: resources/testing.md#core-5
  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: SERVICE_API
    contract: resources/api.yml
    api_operation_id: listRecords
    applies_when: [consultation-list]
    statement: The List operation returns a Registry context that resolves through published metadata to the responsible Registry Authority and returns any additional exposed Record provenance with its documented, source-supported meaning.
    documentation: |
      Purpose: A consumer identifies the institutional source and interprets available provenance without fabricated source facts.
      Condition: Additional provenance checks apply only to fields exposed by the List contract.
      Constraint: A recording time is required only where the selected capability or profile requires it; retrieval time is not substituted for recording time, and unavailable provenance that the capability or profile does not require is omitted rather than inferred.
      Verification: Resolve each Record's Registry context to its published authority and compare every additional exposed provenance value and meaning with source evidence.
    test: resources/testing.md#core-6
  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: FILE
    contract: api/extensions/x-govstack-digital-registries.schema.json
    applies_when: [consultation-list]
    statement: The Digital Registry publishes an OpenAPI contract that declares the List operation's Registry Identifier, Collection, capability, view, and any selected selectable read features through a valid x-govstack-digital-registries extension, with the Collection equal to the operation path's collectionId or its fixed concrete value, the Registry Identifier resolving to published Registry metadata, the same Record schema used by every operation declaring the same Collection and view, the features array listing only the read features the operation implements, and a valid purpose declaration with its trusted binding when the operation selects purpose-bound.
    documentation: |
      Purpose: A consumer or validator determines from the contract which Registry, logical Collection, and authority the List operation belongs to, which representation it returns, and which selectable guarantees it supports.
      Prerequisite: Registry metadata and the OpenAPI contract are published.
      Constraint: Each listed feature respects its capability applicability and dependencies. An absent or empty `features` array establishes no selectable feature claim. Caller capability discovery follows its separate cross-Collection schema and is verified under its own requirement.
      Verification: Validate the List extension against its schema, resolve its Registry Identifier through the metadata, compare its Collection with the path, and compare response schemas for operations sharing the Collection and view. Check each selected feature against the operation's inputs, responses, and declared guarantees, and validate any required purpose object and trusted binding.
    test: resources/testing.md#core-8
  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: SERVICE_API
    contract: resources/api.yml
    api_operation_id: listRecords
    applies_when: [consultation-list]
    statement: The List operation returns a representation valid against the declared view schema and exposes only information permitted for the consumer and request context, including through Records, fields, metadata, references, embedded data, counts, errors, continuation information, and other result information.
    documentation: |
      Purpose: A consumer receives the permitted representation without disclosure through adjacent response content.
      Prerequisite: The access policy for the declared view is documented.
      Constraint: Withholding and consumer field selection operate within the declared view schema; neither substitutes another schema nor grants additional disclosure rights.
      Verification: Exercise List with fixtures for each applicable access policy, including different entitlements where offered, and check representation validity and every permitted information channel.
    test: resources/testing.md#consultation-2
  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: SERVICE_API
    contract: resources/api.yml
    api_operation_id: listRecords
    applies_when: [consultation-list]
    statement: The List operation uses a declared deterministic default order with a unique tie-breaker, returns a bounded Page under current authorisation on each request, and advances continuation that preserves the Collection, operation, query, view, and effective field selection where supported to an explicit completion signal, rejecting invalid continuation with 400 invalid-cursor.
    documentation: |
      Purpose: A consumer browses bounded result Pages to an explicit completion signal without silent restarts under the declared source consistency and limit policy.
      Prerequisite: The contract declares cursor expiry, page-size bounds, resource limits, deterministic order, unique tie-breaker, and traversal consistency.
      Constraint: The contract declares resource limits, timeout behaviour, and any limits on the traversable result set. Baseline pagination supports browsing under the declared source consistency and limit policy. It does not establish a complete export or a snapshot; the `complete-traversal` and `snapshot-traversal` features add those guarantees.
      Constraint: Live pagination can observe source changes that move, add, or remove Records and cause omissions or repeats. Disclosure policy governs counts, page sizes, and continuation patterns, including short or empty advancing Pages. Response bounds and timeout controls do not require a particular database pagination technique or a page-size-proportional bound on source work.
      Consumer guidance (informative): Consumers treat cursors as opaque, return them unchanged with the original query inputs, and follow the completion signal, including when an intermediate Page is empty.
      Verification: Traverse multi-page fixtures and check identity, declared order, size bounds, progress, termination, and the published consistency and limit policy. Exercise malformed, expired, and mismatched cursors, source changes, applicable access changes, and the declared timeout outcome. Check permitted page patterns and any total against the full permitted query. Exhaustive membership and snapshot checks apply only to the corresponding selected features.
    test: resources/testing.md#consultation-7
  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: SERVICE_API
    contract: resources/api.yml
    api_operation_id: listRecords
    applies_when: [consultation-list]
    statement: The List operation declaring field-selection accepts a non-empty, duplicate-free list of declared top-level data field names and returns only the selected fields that disclosure policy permits, together with any mandatory data fields documented by the view.
    documentation: |
      Purpose: A consumer requests a declared subset of the view's selectable `data` fields without a different view schema or additional disclosure rights.
      Condition: The List operation declares `field-selection` in its `features` array.
      Prerequisite: The operation publishes its allowed field names, default field set, mandatory fields if any, selection bounds, and omission semantics.
      Constraint: `recordId` and the `data` object remain present even when no selected field can be disclosed. Selectable fields are not required in the view schema so default and selected responses validate against the same schema. Omission of the input uses the declared default field set. Unknown selections and invalid inputs are rejected. Pagination preserves the effective field set.
      Verification: Select one and several supported fields, check schema validity and retained identity, and compare default and selected responses under applicable disclosure policies. Reject empty, duplicate, unknown, and incorrectly typed selections. Check field-selection mismatch on continuation.
    test: resources/testing.md#consultation-9
  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: SERVICE_API
    contract: resources/api.yml
    api_operation_id: listRecords
    applies_when: [consultation-list]
    statement: The List operation declaring complete-traversal returns each permitted matching Record once when the declared traversal is followed to completion over unchanged source data and access conditions, without silently omitting results because of an internal result window or limit.
    documentation: |
      Purpose: A consumer that follows a traversal to completion obtains every permitted match once under unchanged source data and access conditions.
      Condition: The List operation declares `complete-traversal` in its `features` array.
      Prerequisite: The operation publishes its traversal availability and failure conditions.
      Constraint: A limit that prevents complete traversal produces a declared failure rather than a completion signal. This feature does not imply a source snapshot or a bound on database work.
      Verification: Traverse unchanged multi-page fixtures, including tied sort values and filtered-out source candidates, and compare the complete set with the permitted query. Check for missing or repeated Records and exercise limits that prevent completion.
    test: resources/testing.md#consultation-10
  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: SERVICE_API
    contract: resources/api.yml
    api_operation_id: listRecords
    applies_when: [consultation-list]
    statement: The List operation declaring snapshot-traversal also declares complete-traversal, fixes source membership, ordering, and represented data at one declared snapshot evaluation point on the first request, and uses that snapshot for every continuation while applying current authorisation and disclosure policy.
    documentation: |
      Purpose: A consumer traverses a result whose source membership, order, and data do not change between Pages.
      Condition: The List operation declares `snapshot-traversal` in its `features` array.
      Prerequisite: The operation declares both traversal features and the snapshot semantics and availability policy.
      Constraint: The contract defines how the snapshot evaluation point is identified, its availability and expiry, and its failure outcome. An unavailable or expired snapshot produces `400 invalid-cursor`; the service never silently switches to live data or another snapshot. Snapshot traversal fixes one collection traversal; it does not by itself make historical Record states addressable.
      Verification: Establish a snapshot, then insert, change, and remove source fixtures between Pages. Check unchanged snapshot membership, ordering, and source values under unchanged access conditions. Exercise expiry and lost snapshot state, and revoke access between Pages to verify current authorisation.
    test: resources/testing.md#consultation-11
  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: SERVICE_API
    contract: resources/api.yml
    api_operation_id: listRecords
    applies_when: [consultation-list]
    statement: The List operation declaring recorded-time accepts recordedAsOf, a date-time cutoff for information accepted by the source, returns a representation based only on source knowledge accepted no later than that cutoff, and echoes the applied recordedAsOf context in a TemporalRecordPage, including an empty Page.
    documentation: |
      Purpose: A consumer reads what the source knew at a declared acceptance cutoff.
      Condition: The List operation declares `recorded-time` in its `features` array.
      Prerequisite: The operation documents the source event that establishes acceptance, timestamp precision, timezone treatment, inclusivity, retention, and unavailable-history outcome.
      Constraint: The selection is subject to the source's declared recording semantics, corrections, retention, and gaps. Omitting this coordinate selects the latest available source knowledge while still applying any supplied `effectiveAt`; it makes no historical-knowledge claim. Revision operations instead identify history directly by Record and Revision Identifiers and do not accept this selector.
      Verification: Select cutoffs before, at, and after accepted source revisions, including a correction and any declared gap. Compare the result and echoed context with source evidence. Distinguish a successful List with zero permitted matches (`200` with empty `items` and echoed temporal context) from a source unable to evaluate the requested historical selection (`409 temporal-state-not-available`). Verify that request time, adapter ingestion time, event occurrence time, and registration date are not substituted unless the source contract explicitly defines one as its acceptance time.
    test: resources/testing.md#consultation-14
  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: SERVICE_API
    contract: resources/api.yml
    api_operation_id: listRecords
    applies_when: [consultation-list]
    statement: The List operation declaring effective-time accepts effectiveAt, a date or date-time at which the source declares information applicable, returns the source-backed representation selected by that applicability, and echoes the applied effectiveAt context in a TemporalRecordPage, including an empty Page.
    documentation: |
      Purpose: A consumer reads the information the source declares applicable at a date or instant.
      Condition: The List operation declares `effective-time` in its `features` array.
      Prerequisite: The source has a declared applicability model supporting the accepted selector precision.
      Constraint: The contract defines whether it accepts dates, instants, or both, plus boundary, timezone, overlap, correction, and no-applicable-state semantics. Omitting this coordinate uses the operation's declared default applicability without overriding any supplied `recordedAsOf`; it makes no explicit effective-time claim. Revision operations instead identify history directly by Record and Revision Identifiers and do not accept this selector.
      Constraint: Event occurrence and registration dates are domain facts, not automatically effective-time coordinates. A source can define either as effective time for a particular field or history model, but the service does not infer that equivalence.
      Verification: Exercise date and instant boundaries supported by the contract, overlapping or corrected applicability where possible, and a point with no applicable state. Distinguish a successful List with zero permitted matches (`200` with empty `items` and echoed temporal context) from a source unable to evaluate the requested historical selection (`409 temporal-state-not-available`). Compare the result and echoed context with source evidence and confirm that occurrence or registration dates are not silently substituted.
    test: resources/testing.md#consultation-15
  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: SERVICE_API
    contract: resources/api.yml
    api_operation_id: listRecords
    applies_when: [consultation-list]
    statement: The List operation declaring purpose-bound declares a purpose object with required set to true, a non-empty unique allowedPurposes list of controlled bounded non-whitespace codes or absolute URIs, and one trusted binding, obtains the purpose only from that binding, and rejects a missing, untrusted, malformed, or unallowed purpose before Record information is disclosed.
    documentation: |
      Purpose: A deployment enforces a trusted, controlled purpose for the operation without treating it as consent, authority, or proof of use.
      Condition: The List operation declares `purpose-bound` in its `features` array.
      Prerequisite: The deployment has a trusted purpose binding, and its controlled allowed values and audit treatment are documented.
      Constraint: `access-token-claim` also requires the `claim` name. `trusted-authorization-context` obtains the value from the deployment's authentication and authorisation boundary. Purpose is not accepted from a query parameter or request body.
      Constraint: The effective purpose is bound to cursors, conditional validators, current and historical reads, temporal selection, and the service's audit evidence. A continuation or validator cannot be replayed under another purpose. The contract documents how multiple values and purpose changes are handled.
      Constraint: Declared purpose is distinct from consent, legal or institutional authority, and actual downstream use. One does not prove the others. This feature supplements the inherited authentication and authorisation contract; operations that do not select it retain their inherited security requirements and do not acquire a universal purpose parameter.
      Verification: Exercise missing, malformed, untrusted, allowed, and disallowed purpose contexts; reuse a cursor and conditional validator under another purpose; and compare current, historical, and temporal behaviour. Check rejection before disclosure and verify the recorded effective purpose without treating it as evidence of consent, authority, or downstream use.
    test: resources/testing.md#consultation-18

  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: SERVICE_API
    contract: resources/api.yml
    api_operation_id: searchRecords
    applies_when: [consultation-search]
    statement: The Search operation returns every Record representation with a Record Identifier that, together with the unambiguous Registry context defined by the binding, uniquely identifies that Record.
    documentation: |
      Purpose: Consumers distinguish Records from different Registries and refer to one Record without depending on mutable domain attributes.
      Prerequisite: A Record has been accepted into the Registry.
      Constraint: The binding defines how the consumer determines the Registry Identifier from the request, published contract and service metadata, or the representation itself.
      Verification: Obtain two distinct Record fixtures through Search and verify their different Record Identifiers and Registry context. Where several Registries are exposed, verify that identical local identifiers remain distinguishable.
    test: resources/testing.md#core-2
  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: SERVICE_API
    contract: resources/api.yml
    api_operation_id: searchRecords
    applies_when: [consultation-search]
    statement: The Search operation returns Record representations in the published format that validate against the operation's unambiguously identified schema and use its documented field meanings.
    documentation: |
      Purpose: Consumers decode, validate, and interpret Search representations without knowledge of internal storage.
      Prerequisite: The applicable representation format, schema, and domain documentation are published.
      Verification: Obtain a Search representation, identify its format and schema using only the published contract and response context, validate it, and check the published field and nested-value semantics against the fixture.
    test: resources/testing.md#core-4
  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: SERVICE_API
    contract: resources/api.yml
    api_operation_id: searchRecords
    applies_when: [consultation-search]
    statement: The Search operation returns exposed revision and lifecycle metadata with the source semantics declared in the representation schema.
    documentation: |
      Purpose: Consumers interpret available revision and lifecycle information without inferring guarantees that the source does not provide.
      Condition: A Search Record exposes revision or lifecycle metadata; otherwise the metadata scenarios are not applicable.
      Constraint: A selected capability or profile supplies any additional guarantees. Baseline Record reads do not require revision or lifecycle fields, and a representation validator is not presented as a source revision unless the source contract establishes that equivalence.
      Verification: Compare provided metadata with source fixtures and the declared schema, including the meaning of revisions and exposed lifecycle states.
    test: resources/testing.md#core-5
  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: SERVICE_API
    contract: resources/api.yml
    api_operation_id: searchRecords
    applies_when: [consultation-search]
    statement: The Search operation returns a Registry context that resolves through published metadata to the responsible Registry Authority and returns any additional exposed Record provenance with its documented, source-supported meaning.
    documentation: |
      Purpose: A consumer identifies the institutional source and interprets available provenance without fabricated source facts.
      Condition: Additional provenance checks apply only to fields exposed by the Search contract.
      Constraint: A recording time is required only where the selected capability or profile requires it; retrieval time is not substituted for recording time, and unavailable provenance that the capability or profile does not require is omitted rather than inferred.
      Verification: Resolve each Record's Registry context to its published authority and compare every additional exposed provenance value and meaning with source evidence.
    test: resources/testing.md#core-6
  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: FILE
    contract: api/extensions/x-govstack-digital-registries.schema.json
    applies_when: [consultation-search]
    statement: The Digital Registry publishes an OpenAPI contract that declares the Search operation's Registry Identifier, Collection, capability, view, and any selected selectable read features through a valid x-govstack-digital-registries extension, with the Collection equal to the operation path's collectionId or its fixed concrete value, the Registry Identifier resolving to published Registry metadata, the same Record schema used by every operation declaring the same Collection and view, the features array listing only the read features the operation implements, and a valid purpose declaration with its trusted binding when the operation selects purpose-bound.
    documentation: |
      Purpose: A consumer or validator determines from the contract which Registry, logical Collection, and authority the Search operation belongs to, which representation it returns, and which selectable guarantees it supports.
      Prerequisite: Registry metadata and the OpenAPI contract are published.
      Constraint: Each listed feature respects its capability applicability and dependencies. An absent or empty `features` array establishes no selectable feature claim. Caller capability discovery follows its separate cross-Collection schema and is verified under its own requirement.
      Verification: Validate the Search extension against its schema, resolve its Registry Identifier through the metadata, compare its Collection with the path, and compare response schemas for operations sharing the Collection and view. Check each selected feature against the operation's inputs, responses, and declared guarantees, and validate any required purpose object and trusted binding.
    test: resources/testing.md#core-8
  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: SERVICE_API
    contract: resources/api.yml
    api_operation_id: searchRecords
    applies_when: [consultation-search]
    statement: The Search operation returns a representation valid against the declared view schema and exposes only information permitted for the consumer and request context, including through Records, fields, metadata, references, embedded data, counts, errors, continuation information, and other result information.
    documentation: |
      Purpose: A consumer receives the permitted representation without disclosure through adjacent response content.
      Prerequisite: The access policy for the declared view is documented.
      Constraint: Withholding and consumer field selection operate within the declared view schema; neither substitutes another schema nor grants additional disclosure rights.
      Verification: Exercise Search with fixtures for each applicable access policy, including different entitlements where offered, and check representation validity and every permitted information channel.
    test: resources/testing.md#consultation-2
  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: SERVICE_API
    contract: resources/api.yml
    api_operation_id: searchRecords
    applies_when: [consultation-search]
    statement: The Search operation uses a declared deterministic default order with a unique tie-breaker, returns a bounded Page under current authorisation on each request, and advances continuation that preserves the Collection, operation, query, view, and effective field selection where supported to an explicit completion signal, rejecting invalid continuation with 400 invalid-cursor.
    documentation: |
      Purpose: A consumer browses bounded result Pages to an explicit completion signal without silent restarts under the declared source consistency and limit policy.
      Prerequisite: The contract declares cursor expiry, page-size bounds, resource limits, deterministic order, unique tie-breaker, and traversal consistency.
      Constraint: The contract declares resource limits, timeout behaviour, and any limits on the traversable result set. Baseline pagination supports browsing under the declared source consistency and limit policy. It does not establish a complete export or a snapshot; the `complete-traversal` and `snapshot-traversal` features add those guarantees.
      Constraint: Live pagination can observe source changes that move, add, or remove Records and cause omissions or repeats. Disclosure policy governs counts, page sizes, and continuation patterns, including short or empty advancing Pages. Response bounds and timeout controls do not require a particular database pagination technique or a page-size-proportional bound on source work.
      Consumer guidance (informative): Consumers treat cursors as opaque, return them unchanged with the original query inputs, and follow the completion signal, including when an intermediate Page is empty.
      Verification: Traverse multi-page fixtures and check identity, declared order, size bounds, progress, termination, and the published consistency and limit policy. Exercise malformed, expired, and mismatched cursors, source changes, applicable access changes, and the declared timeout outcome. Check permitted page patterns and any total against the full permitted query. Exhaustive membership and snapshot checks apply only to the corresponding selected features.
    test: resources/testing.md#consultation-7
  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: SERVICE_API
    contract: resources/api.yml
    api_operation_id: searchRecords
    applies_when: [consultation-search]
    statement: The Search operation declaring field-selection accepts a non-empty, duplicate-free list of declared top-level data field names and returns only the selected fields that disclosure policy permits, together with any mandatory data fields documented by the view.
    documentation: |
      Purpose: A consumer requests a declared subset of the view's selectable `data` fields without a different view schema or additional disclosure rights.
      Condition: The Search operation declares `field-selection` in its `features` array.
      Prerequisite: The operation publishes its allowed field names, default field set, mandatory fields if any, selection bounds, and omission semantics.
      Constraint: `recordId` and the `data` object remain present even when no selected field can be disclosed. Selectable fields are not required in the view schema so default and selected responses validate against the same schema. Omission of the input uses the declared default field set. Unknown selections and invalid inputs are rejected. Pagination preserves the effective field set.
      Verification: Select one and several supported fields, check schema validity and retained identity, and compare default and selected responses under applicable disclosure policies. Reject empty, duplicate, unknown, and incorrectly typed selections. Check field-selection mismatch on continuation.
    test: resources/testing.md#consultation-9
  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: SERVICE_API
    contract: resources/api.yml
    api_operation_id: searchRecords
    applies_when: [consultation-search]
    statement: The Search operation declaring complete-traversal returns each permitted matching Record once when the declared traversal is followed to completion over unchanged source data and access conditions, without silently omitting results because of an internal result window or limit.
    documentation: |
      Purpose: A consumer that follows a traversal to completion obtains every permitted match once under unchanged source data and access conditions.
      Condition: The Search operation declares `complete-traversal` in its `features` array.
      Prerequisite: The operation publishes its traversal availability and failure conditions.
      Constraint: A limit that prevents complete traversal produces a declared failure rather than a completion signal. This feature does not imply a source snapshot or a bound on database work.
      Verification: Traverse unchanged multi-page fixtures, including tied sort values and filtered-out source candidates, and compare the complete set with the permitted query. Check for missing or repeated Records and exercise limits that prevent completion.
    test: resources/testing.md#consultation-10
  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: SERVICE_API
    contract: resources/api.yml
    api_operation_id: searchRecords
    applies_when: [consultation-search]
    statement: The Search operation declaring snapshot-traversal also declares complete-traversal, fixes source membership, ordering, and represented data at one declared snapshot evaluation point on the first request, and uses that snapshot for every continuation while applying current authorisation and disclosure policy.
    documentation: |
      Purpose: A consumer traverses a result whose source membership, order, and data do not change between Pages.
      Condition: The Search operation declares `snapshot-traversal` in its `features` array.
      Prerequisite: The operation declares both traversal features and the snapshot semantics and availability policy.
      Constraint: The contract defines how the snapshot evaluation point is identified, its availability and expiry, and its failure outcome. An unavailable or expired snapshot produces `400 invalid-cursor`; the service never silently switches to live data or another snapshot. Snapshot traversal fixes one collection traversal; it does not by itself make historical Record states addressable.
      Verification: Establish a snapshot, then insert, change, and remove source fixtures between Pages. Check unchanged snapshot membership, ordering, and source values under unchanged access conditions. Exercise expiry and lost snapshot state, and revoke access between Pages to verify current authorisation.
    test: resources/testing.md#consultation-11
  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: SERVICE_API
    contract: resources/api.yml
    api_operation_id: searchRecords
    applies_when: [consultation-search]
    statement: The Search operation declaring recorded-time accepts recordedAsOf, a date-time cutoff for information accepted by the source, returns a representation based only on source knowledge accepted no later than that cutoff, and echoes the applied recordedAsOf context in a TemporalRecordPage, including an empty Page.
    documentation: |
      Purpose: A consumer reads what the source knew at a declared acceptance cutoff.
      Condition: The Search operation declares `recorded-time` in its `features` array.
      Prerequisite: The operation documents the source event that establishes acceptance, timestamp precision, timezone treatment, inclusivity, retention, and unavailable-history outcome.
      Constraint: The selection is subject to the source's declared recording semantics, corrections, retention, and gaps. Omitting this coordinate selects the latest available source knowledge while still applying any supplied `effectiveAt`; it makes no historical-knowledge claim. Revision operations instead identify history directly by Record and Revision Identifiers and do not accept this selector.
      Verification: Select cutoffs before, at, and after accepted source revisions, including a correction and any declared gap. Compare the result and echoed context with source evidence. Distinguish a successful Search with zero permitted matches (`200` with empty `items` and echoed temporal context) from a source unable to evaluate the requested historical selection (`409 temporal-state-not-available`). Verify that request time, adapter ingestion time, event occurrence time, and registration date are not substituted unless the source contract explicitly defines one as its acceptance time.
    test: resources/testing.md#consultation-14
  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: SERVICE_API
    contract: resources/api.yml
    api_operation_id: searchRecords
    applies_when: [consultation-search]
    statement: The Search operation declaring effective-time accepts effectiveAt, a date or date-time at which the source declares information applicable, returns the source-backed representation selected by that applicability, and echoes the applied effectiveAt context in a TemporalRecordPage, including an empty Page.
    documentation: |
      Purpose: A consumer reads the information the source declares applicable at a date or instant.
      Condition: The Search operation declares `effective-time` in its `features` array.
      Prerequisite: The source has a declared applicability model supporting the accepted selector precision.
      Constraint: The contract defines whether it accepts dates, instants, or both, plus boundary, timezone, overlap, correction, and no-applicable-state semantics. Omitting this coordinate uses the operation's declared default applicability without overriding any supplied `recordedAsOf`; it makes no explicit effective-time claim. Revision operations instead identify history directly by Record and Revision Identifiers and do not accept this selector.
      Constraint: Event occurrence and registration dates are domain facts, not automatically effective-time coordinates. A source can define either as effective time for a particular field or history model, but the service does not infer that equivalence.
      Verification: Exercise date and instant boundaries supported by the contract, overlapping or corrected applicability where possible, and a point with no applicable state. Distinguish a successful Search with zero permitted matches (`200` with empty `items` and echoed temporal context) from a source unable to evaluate the requested historical selection (`409 temporal-state-not-available`). Compare the result and echoed context with source evidence and confirm that occurrence or registration dates are not silently substituted.
    test: resources/testing.md#consultation-15
  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: SERVICE_API
    contract: resources/api.yml
    api_operation_id: searchRecords
    applies_when: [consultation-search]
    statement: The Search operation publishes, for each named Search, a versioned typed criteria schema and applies only the comparison semantics that Search independently declares, where each selected reusable equality, range, set-membership, or prefix semantic defines its applicable fields and types, normalisation and collation, inclusive or exclusive bounds where relevant, empty and null treatment, repeated-value treatment, and how criteria combine.
    documentation: |
      Purpose: A consumer relies on declared typed comparison semantics without inferring a broader query language.
      Prerequisite: The contract publishes at least one named typed Search.
      Constraint: A Search can publish additional domain-specific semantics, but support for one semantic does not imply support for another, fuzzy matching, full-text search, or a universal query language.
      Verification: For every declared Search and semantic, exercise matching and non-matching typed boundaries, invalid operators or fields, normalisation, empty and null cases, and criterion combination. Verify that undeclared semantics are rejected and that the implementation does not advertise a broader query language than it supports.
    test: resources/testing.md#consultation-16
  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: SERVICE_API
    contract: resources/api.yml
    api_operation_id: searchRecords
    applies_when: [consultation-search]
    statement: The Search operation declaring purpose-bound declares a purpose object with required set to true, a non-empty unique allowedPurposes list of controlled bounded non-whitespace codes or absolute URIs, and one trusted binding, obtains the purpose only from that binding, and rejects a missing, untrusted, malformed, or unallowed purpose before Record information is disclosed.
    documentation: |
      Purpose: A deployment enforces a trusted, controlled purpose for the operation without treating it as consent, authority, or proof of use.
      Condition: The Search operation declares `purpose-bound` in its `features` array.
      Prerequisite: The deployment has a trusted purpose binding, and its controlled allowed values and audit treatment are documented.
      Constraint: `access-token-claim` also requires the `claim` name. `trusted-authorization-context` obtains the value from the deployment's authentication and authorisation boundary. Purpose is not accepted from a query parameter or request body.
      Constraint: The effective purpose is bound to cursors, conditional validators, current and historical reads, temporal selection, and the service's audit evidence. A continuation or validator cannot be replayed under another purpose. The contract documents how multiple values and purpose changes are handled.
      Constraint: Declared purpose is distinct from consent, legal or institutional authority, and actual downstream use. One does not prove the others. This feature supplements the inherited authentication and authorisation contract; operations that do not select it retain their inherited security requirements and do not acquire a universal purpose parameter.
      Verification: Exercise missing, malformed, untrusted, allowed, and disallowed purpose contexts; reuse a cursor and conditional validator under another purpose; and compare current, historical, and temporal behaviour. Check rejection before disclosure and verify the recorded effective purpose without treating it as evidence of consent, authority, or downstream use.
    test: resources/testing.md#consultation-18

  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: SERVICE_API
    contract: resources/api.yml
    api_operation_id: listRecordRevisions
    applies_when: [consultation-revision-list]
    statement: The Revision List operation returns every Record representation with a Record Identifier that, together with the unambiguous Registry context defined by the binding, uniquely identifies that Record.
    documentation: |
      Purpose: Consumers distinguish Records from different Registries and refer to one Record without depending on mutable domain attributes.
      Prerequisite: A Record has been accepted into the Registry.
      Constraint: The binding defines how the consumer determines the Registry Identifier from the request, published contract and service metadata, or the representation itself.
      Verification: Obtain revisions of two distinct Record fixtures through Revision List and verify their different Record Identifiers and Registry context. Where several Registries are exposed, verify that identical local identifiers remain distinguishable.
    test: resources/testing.md#core-2
  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: SERVICE_API
    contract: resources/api.yml
    api_operation_id: listRecordRevisions
    applies_when: [consultation-revision-list]
    statement: The Revision List operation returns Record representations in the published format that validate against the operation's unambiguously identified schema and use its documented field meanings.
    documentation: |
      Purpose: Consumers decode, validate, and interpret Revision List representations without knowledge of internal storage.
      Prerequisite: The applicable representation format, schema, and domain documentation are published.
      Verification: Obtain a Revision List representation, identify its format and schema using only the published contract and response context, validate it, and check the published field and nested-value semantics against the fixture.
    test: resources/testing.md#core-4
  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: SERVICE_API
    contract: resources/api.yml
    api_operation_id: listRecordRevisions
    applies_when: [consultation-revision-list]
    statement: The Revision List operation returns exposed revision and lifecycle metadata with the source semantics declared in the representation schema.
    documentation: |
      Purpose: Consumers interpret available revision and lifecycle information without inferring guarantees that the source does not provide.
      Condition: Revision List always exposes the required revision metadata; lifecycle metadata scenarios apply only where the Revision List response exposes lifecycle metadata.
      Constraint: A selected capability or profile supplies any additional guarantees. Baseline Record reads do not require revision or lifecycle fields, and a representation validator is not presented as a source revision unless the source contract establishes that equivalence.
      Verification: Compare provided metadata with source fixtures and the declared schema, including the meaning of revisions and exposed lifecycle states.
    test: resources/testing.md#core-5
  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: SERVICE_API
    contract: resources/api.yml
    api_operation_id: listRecordRevisions
    applies_when: [consultation-revision-list]
    statement: The Revision List operation returns a Registry context that resolves through published metadata to the responsible Registry Authority and returns any additional exposed Record provenance with its documented, source-supported meaning.
    documentation: |
      Purpose: A consumer identifies the institutional source and interprets available provenance without fabricated source facts.
      Condition: Additional provenance checks apply only to fields exposed by the Revision List contract.
      Constraint: A recording time is required only where the selected capability or profile requires it; retrieval time is not substituted for recording time, and unavailable provenance that the capability or profile does not require is omitted rather than inferred.
      Verification: Resolve the Record's Registry context to its published authority and compare every additional exposed provenance value and meaning with source evidence.
    test: resources/testing.md#core-6
  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: FILE
    contract: api/extensions/x-govstack-digital-registries.schema.json
    applies_when: [consultation-revision-list]
    statement: The Digital Registry publishes an OpenAPI contract that declares the Revision List operation's Registry Identifier, Collection, capability, view, and any selected selectable read features through a valid x-govstack-digital-registries extension, with the Collection equal to the operation path's collectionId or its fixed concrete value, the Registry Identifier resolving to published Registry metadata, the same Record schema used by every operation declaring the same Collection and view, the features array listing only the read features the operation implements, and a valid purpose declaration with its trusted binding when the operation selects purpose-bound.
    documentation: |
      Purpose: A consumer or validator determines from the contract which Registry, logical Collection, and authority the Revision List operation belongs to, which representation it returns, and which selectable guarantees it supports.
      Prerequisite: Registry metadata and the OpenAPI contract are published.
      Constraint: A history operation can declare its separate history view. Each listed feature respects its capability applicability and dependencies. An absent or empty `features` array establishes no selectable feature claim. Caller capability discovery follows its separate cross-Collection schema and is verified under its own requirement.
      Verification: Validate the Revision List extension against its schema, resolve its Registry Identifier through the metadata, compare its Collection with the path, and compare response schemas for operations sharing the Collection and view. Check each selected feature against the operation's inputs, responses, and declared guarantees, and validate any required purpose object and trusted binding.
    test: resources/testing.md#core-8
  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: SERVICE_API
    contract: resources/api.yml
    api_operation_id: listRecordRevisions
    applies_when: [consultation-revision-list]
    statement: The Revision List operation returns a representation valid against the declared view schema and exposes only information permitted for the consumer and request context, including through Records, fields, metadata, references, embedded data, counts, errors, continuation information, and other result information.
    documentation: |
      Purpose: A consumer receives the permitted representation without disclosure through adjacent response content.
      Prerequisite: The access policy for the declared view is documented.
      Constraint: Withholding and consumer field selection operate within the declared view schema; neither substitutes another schema nor grants additional disclosure rights.
      Verification: Exercise Revision List with fixtures for each applicable access policy, including different entitlements where offered, and check representation validity and every permitted information channel.
    test: resources/testing.md#consultation-2
  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: SERVICE_API
    contract: resources/api.yml
    api_operation_id: listRecordRevisions
    applies_when: [consultation-revision-list]
    statement: The Revision List operation gives unknown and protected parent Records the same unresolved outcome, including equivalent protocol status, security-relevant metadata, error type, response structure, and non-Record-specific values, without Record-specific or revision-specific data and with independently generated trace and correlation values, so that it does not reveal whether its parent Record exists.
    documentation: |
      Purpose: A caller cannot determine protected Record or history existence from the unresolved outcome.
      Condition: The access policy protects parent Record or history existence.
      Prerequisite: The access policy declares which Records and retained revisions have protected existence. Protected and unknown parent Record fixtures are available under the same consumer context.
      Constraint: The service evaluates protected-existence policy before returning `409 history-not-available`. That diagnostic applies only after the caller is permitted to know the parent Record and requested history context, and only when the source cannot return source-backed retained history. It never distinguishes an unknown resource from a protected one.
      Verification: Compare protected and unknown parent Record fixtures under the same consumer context and check every listed aspect of the outcome and its trace values. Then make source history unavailable for a caller permitted to know the parent and verify `409 history-not-available` only in that post-protection case.
    test: resources/testing.md#consultation-3
  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: SERVICE_API
    contract: resources/api.yml
    api_operation_id: listRecordRevisions
    applies_when: [consultation-revision-list]
    statement: The Revision List operation uses a declared deterministic default order with a unique tie-breaker, returns a bounded Page under current authorisation on each request, and advances continuation that preserves the Collection, operation, query, view, effective field selection where supported, and parent recordId to an explicit completion signal, rejecting invalid continuation with 400 invalid-cursor.
    documentation: |
      Purpose: A consumer browses bounded result Pages to an explicit completion signal without silent restarts under the declared source consistency and limit policy.
      Prerequisite: The contract declares cursor expiry, page-size bounds, resource limits, deterministic order, unique tie-breaker, and traversal consistency. Revision List also declares its parent Record binding.
      Constraint: The contract declares resource limits, timeout behaviour, and any limits on the traversable result set. Baseline pagination supports browsing under the declared source consistency and limit policy. It does not establish a complete export or a snapshot.
      Constraint: Live pagination can observe source changes that move, add, or remove Records and cause omissions or repeats. Disclosure policy governs counts, page sizes, and continuation patterns, including short or empty advancing Pages. Response bounds and timeout controls do not require a particular database pagination technique or a page-size-proportional bound on source work.
      Consumer guidance (informative): Consumers treat cursors as opaque, return them unchanged with the original query inputs, and follow the completion signal, including when an intermediate Page is empty.
      Verification: Traverse multi-page fixtures and check identity, declared order, size bounds, progress, termination, and the published consistency and limit policy. Exercise malformed, expired, and mismatched cursors, source changes, applicable access changes, and the declared timeout outcome. Obtain a cursor under parent Record A and replay it under parent Record B; verify `400 invalid-cursor` without returning either Record's history. Check permitted page patterns and any total against the full permitted query.
    test: resources/testing.md#consultation-7
  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: SERVICE_API
    contract: resources/api.yml
    api_operation_id: listRecordRevisions
    applies_when: [consultation-revision-list]
    statement: The Revision List operation declaring field-selection accepts a non-empty, duplicate-free list of declared top-level data field names and returns only the selected fields that disclosure policy permits, together with any mandatory data fields documented by the view.
    documentation: |
      Purpose: A consumer requests a declared subset of the view's selectable `data` fields without a different view schema or additional disclosure rights.
      Condition: The Revision List operation declares `field-selection` in its `features` array.
      Prerequisite: The operation publishes its allowed field names, default field set, mandatory fields if any, selection bounds, and omission semantics.
      Constraint: `recordId` and the `data` object remain present even when no selected field can be disclosed. Selectable fields are not required in the view schema so default and selected responses validate against the same schema. Omission of the input uses the declared default field set. Unknown selections and invalid inputs are rejected. Pagination preserves the effective field set.
      Verification: Select one and several supported fields, check schema validity and retained identity, and compare default and selected responses under applicable disclosure policies. Reject empty, duplicate, unknown, and incorrectly typed selections. Check field-selection mismatch on continuation.
    test: resources/testing.md#consultation-9
  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: SERVICE_API
    contract: resources/api.yml
    api_operation_id: listRecordRevisions
    applies_when: [consultation-revision-list]
    statement: The Revision List operation declaring purpose-bound declares a purpose object with required set to true, a non-empty unique allowedPurposes list of controlled bounded non-whitespace codes or absolute URIs, and one trusted binding, obtains the purpose only from that binding, and rejects a missing, untrusted, malformed, or unallowed purpose before Record information is disclosed.
    documentation: |
      Purpose: A deployment enforces a trusted, controlled purpose for the operation without treating it as consent, authority, or proof of use.
      Condition: The Revision List operation declares `purpose-bound` in its `features` array.
      Prerequisite: The deployment has a trusted purpose binding, and its controlled allowed values and audit treatment are documented.
      Constraint: `access-token-claim` also requires the `claim` name. `trusted-authorization-context` obtains the value from the deployment's authentication and authorisation boundary. Purpose is not accepted from a query parameter or request body.
      Constraint: The effective purpose is bound to cursors, conditional validators, current and historical reads, temporal selection, and the service's audit evidence. A continuation or validator cannot be replayed under another purpose. The contract documents how multiple values and purpose changes are handled.
      Constraint: Declared purpose is distinct from consent, legal or institutional authority, and actual downstream use. One does not prove the others. This feature supplements the inherited authentication and authorisation contract; operations that do not select it retain their inherited security requirements and do not acquire a universal purpose parameter.
      Verification: Exercise missing, malformed, untrusted, allowed, and disallowed purpose contexts; reuse a cursor and conditional validator under another purpose; and compare current, historical, and temporal behaviour. Check rejection before disclosure and verify the recorded effective purpose without treating it as evidence of consent, authority, or downstream use.
    test: resources/testing.md#consultation-18

  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: SERVICE_API
    contract: resources/api.yml
    api_operation_id: retrieveRecordRevision
    applies_when: [consultation-revision-retrieve]
    statement: The Revision Retrieve operation returns every Record representation with a Record Identifier that, together with the unambiguous Registry context defined by the binding, uniquely identifies that Record.
    documentation: |
      Purpose: Consumers distinguish Records from different Registries and refer to one Record without depending on mutable domain attributes.
      Prerequisite: A Record has been accepted into the Registry.
      Constraint: The binding defines how the consumer determines the Registry Identifier from the request, published contract and service metadata, or the representation itself.
      Verification: Obtain revisions of two distinct Record fixtures through Revision Retrieve and verify their different Record Identifiers and Registry context. Where several Registries are exposed, verify that identical local identifiers remain distinguishable.
    test: resources/testing.md#core-2
  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: SERVICE_API
    contract: resources/api.yml
    api_operation_id: retrieveRecordRevision
    applies_when: [consultation-revision-retrieve]
    statement: The Revision Retrieve operation returns Record representations in the published format that validate against the operation's unambiguously identified schema and use its documented field meanings.
    documentation: |
      Purpose: Consumers decode, validate, and interpret Revision Retrieve representations without knowledge of internal storage.
      Prerequisite: The applicable representation format, schema, and domain documentation are published.
      Verification: Obtain a Revision Retrieve representation, identify its format and schema using only the published contract and response context, validate it, and check the published field and nested-value semantics against the fixture.
    test: resources/testing.md#core-4
  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: SERVICE_API
    contract: resources/api.yml
    api_operation_id: retrieveRecordRevision
    applies_when: [consultation-revision-retrieve]
    statement: The Revision Retrieve operation returns exposed revision and lifecycle metadata with the source semantics declared in the representation schema.
    documentation: |
      Purpose: Consumers interpret available revision and lifecycle information without inferring guarantees that the source does not provide.
      Condition: Revision Retrieve always exposes the required revision metadata; lifecycle metadata scenarios apply only where the Revision Retrieve response exposes lifecycle metadata.
      Constraint: A selected capability or profile supplies any additional guarantees. Baseline Record reads do not require revision or lifecycle fields, and a representation validator is not presented as a source revision unless the source contract establishes that equivalence.
      Verification: Compare provided metadata with source fixtures and the declared schema, including the meaning of revisions and exposed lifecycle states.
    test: resources/testing.md#core-5
  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: SERVICE_API
    contract: resources/api.yml
    api_operation_id: retrieveRecordRevision
    applies_when: [consultation-revision-retrieve]
    statement: The Revision Retrieve operation returns a Registry context that resolves through published metadata to the responsible Registry Authority and returns any additional exposed Record provenance with its documented, source-supported meaning.
    documentation: |
      Purpose: A consumer identifies the institutional source and interprets available provenance without fabricated source facts.
      Condition: Additional provenance checks apply only to fields exposed by the Revision Retrieve contract.
      Constraint: A recording time is required only where the selected capability or profile requires it; retrieval time is not substituted for recording time, and unavailable provenance that the capability or profile does not require is omitted rather than inferred.
      Verification: Resolve the Record's Registry context to its published authority and compare every additional exposed provenance value and meaning with source evidence.
    test: resources/testing.md#core-6
  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: FILE
    contract: api/extensions/x-govstack-digital-registries.schema.json
    applies_when: [consultation-revision-retrieve]
    statement: The Digital Registry publishes an OpenAPI contract that declares the Revision Retrieve operation's Registry Identifier, Collection, capability, view, and any selected selectable read features through a valid x-govstack-digital-registries extension, with the Collection equal to the operation path's collectionId or its fixed concrete value, the Registry Identifier resolving to published Registry metadata, the same Record schema used by every operation declaring the same Collection and view, the features array listing only the read features the operation implements, and a valid purpose declaration with its trusted binding when the operation selects purpose-bound.
    documentation: |
      Purpose: A consumer or validator determines from the contract which Registry, logical Collection, and authority the Revision Retrieve operation belongs to, which representation it returns, and which selectable guarantees it supports.
      Prerequisite: Registry metadata and the OpenAPI contract are published.
      Constraint: A history operation can declare its separate history view. Each listed feature respects its capability applicability and dependencies. An absent or empty `features` array establishes no selectable feature claim. Caller capability discovery follows its separate cross-Collection schema and is verified under its own requirement.
      Verification: Validate the Revision Retrieve extension against its schema, resolve its Registry Identifier through the metadata, compare its Collection with the path, and compare response schemas for operations sharing the Collection and view. Check each selected feature against the operation's inputs, responses, and declared guarantees, and validate any required purpose object and trusted binding.
    test: resources/testing.md#core-8
  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: SERVICE_API
    contract: resources/api.yml
    api_operation_id: retrieveRecordRevision
    applies_when: [consultation-revision-retrieve]
    statement: The Revision Retrieve operation returns a representation valid against the declared view schema and exposes only information permitted for the consumer and request context, including through fields, metadata, references, embedded data, errors, and other result information.
    documentation: |
      Purpose: A consumer receives the permitted representation without disclosure through adjacent response content.
      Prerequisite: The access policy for the declared view is documented.
      Constraint: Withholding and consumer field selection operate within the declared view schema; neither substitutes another schema nor grants additional disclosure rights. Disclosure also governs counts and continuation information where present.
      Verification: Exercise Revision Retrieve with fixtures for each applicable access policy, including different entitlements where offered, and check representation validity and every permitted information channel.
    test: resources/testing.md#consultation-2
  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: SERVICE_API
    contract: resources/api.yml
    api_operation_id: retrieveRecordRevision
    applies_when: [consultation-revision-retrieve]
    statement: The Revision Retrieve operation gives unknown and protected parent Records and revisions the same unresolved outcome, including equivalent protocol status, security-relevant metadata, error type, response structure, and non-Record-specific values, without Record-specific or revision-specific data and with independently generated trace and correlation values, so that it does not reveal whether the parent Record or the named revision is the unavailable resource.
    documentation: |
      Purpose: A caller cannot determine protected Record or revision existence from the unresolved outcome.
      Condition: The access policy protects parent Record or revision existence.
      Prerequisite: The access policy declares which Records and retained revisions have protected existence. Protected and unknown parent Record and Revision Identifier fixtures are available under the same consumer context.
      Constraint: The service evaluates protected-existence policy before returning `409 history-not-available`. That diagnostic applies only after the caller is permitted to know the parent Record and requested history context, and only when the source cannot return source-backed retained history. It never distinguishes an unknown resource from a protected one.
      Verification: Compare protected and unknown fixtures under the same consumer context, separately varying parent Record and Revision Identifier presence and protection, and check every listed aspect of the outcome and its trace values. Then make source history unavailable for a caller permitted to know the parent and verify `409 history-not-available` only in that post-protection case.
    test: resources/testing.md#consultation-3
  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: SERVICE_API
    contract: resources/api.yml
    api_operation_id: retrieveRecordRevision
    applies_when: [consultation-revision-retrieve]
    statement: The Revision Retrieve operation declaring field-selection accepts a non-empty, duplicate-free list of declared top-level data field names and returns only the selected fields that disclosure policy permits, together with any mandatory data fields documented by the view.
    documentation: |
      Purpose: A consumer requests a declared subset of the view's selectable `data` fields without a different view schema or additional disclosure rights.
      Condition: The Revision Retrieve operation declares `field-selection` in its `features` array.
      Prerequisite: The operation publishes its allowed field names, default field set, mandatory fields if any, selection bounds, and omission semantics.
      Constraint: `recordId` and the `data` object remain present even when no selected field can be disclosed. Selectable fields are not required in the view schema so default and selected responses validate against the same schema. Omission of the input uses the declared default field set. Unknown selections and invalid inputs are rejected.
      Verification: Select one and several supported fields, check schema validity and retained identity, and compare default and selected responses under applicable disclosure policies. Reject empty, duplicate, unknown, and incorrectly typed selections.
    test: resources/testing.md#consultation-9
  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: SERVICE_API
    contract: resources/api.yml
    api_operation_id: retrieveRecordRevision
    applies_when: [consultation-revision-retrieve]
    statement: The Revision Retrieve operation declaring purpose-bound declares a purpose object with required set to true, a non-empty unique allowedPurposes list of controlled bounded non-whitespace codes or absolute URIs, and one trusted binding, obtains the purpose only from that binding, and rejects a missing, untrusted, malformed, or unallowed purpose before Record information is disclosed.
    documentation: |
      Purpose: A deployment enforces a trusted, controlled purpose for the operation without treating it as consent, authority, or proof of use.
      Condition: The Revision Retrieve operation declares `purpose-bound` in its `features` array.
      Prerequisite: The deployment has a trusted purpose binding, and its controlled allowed values and audit treatment are documented.
      Constraint: `access-token-claim` also requires the `claim` name. `trusted-authorization-context` obtains the value from the deployment's authentication and authorisation boundary. Purpose is not accepted from a query parameter or request body.
      Constraint: The effective purpose is bound to cursors, conditional validators, current and historical reads, temporal selection, and the service's audit evidence. A continuation or validator cannot be replayed under another purpose. The contract documents how multiple values and purpose changes are handled.
      Constraint: Declared purpose is distinct from consent, legal or institutional authority, and actual downstream use. One does not prove the others. This feature supplements the inherited authentication and authorisation contract; operations that do not select it retain their inherited security requirements and do not acquire a universal purpose parameter.
      Verification: Exercise missing, malformed, untrusted, allowed, and disallowed purpose contexts; reuse a cursor and conditional validator under another purpose; and compare current, historical, and temporal behaviour. Check rejection before disclosure and verify the recorded effective purpose without treating it as evidence of consent, authority, or downstream use.
    test: resources/testing.md#consultation-18
---

## Shared Record model <a href="#core-shared-record-model" id="core-shared-record-model"></a>

### Common Record context <a href="#core-common-record-context" id="core-common-record-context"></a>

Every returned Record representation has the following context. The binding defines where it is conveyed: in the representation, response metadata, or the versioned operational contract and its association with the Registry. The Consultation HTTP binding conveys it through the contract: the `x-govstack-digital-registries` extension on each operation names the Registry, logical Collection, capability, and view, and the operation's response schema is the representation schema. A consumer can determine that context without knowing the source's internal storage. Registry-wide information need not be repeated in every Record or Collection item.

| Concept | Baseline contract |
|---|---|
| Registry Identifier | The operational contract binds the operation to one Registry, or the returned Record explicitly identifies its Registry. |
| Record Identifier | A stable reference unique within that Registry, included in each returned Record. |
| Representation Format | The binding identifies the serialisation or media type. |
| Representation Schema | A resolvable, versioned machine-readable schema identifies the permitted representation; schema selection is unambiguous. |
| Field meanings | Schema descriptions or linked domain documentation explain field meanings, units, code lists, and relevant absence or null semantics. |
| Registry Authority | The Registry context resolves to the authority and authoritative scope published in Registry metadata. |

The applicable capability determines which domain data and metadata the consumer may receive. Each operation has one declared view schema, named in its Consultation Registry context declaration. Access policy can withhold non-required fields within that schema. An operation selecting the selectable Consultation `field-selection` feature can also let consumers request a subset of its declared selectable `data` fields, while retaining Record identity and the `data` object. Its contract documents the default field set and supported selections. Both default and selected responses validate against the same view schema; field selection never grants disclosure rights. A materially different representation uses a separately declared view and operation or API. The HTTP binding uses the same Record envelope and schema for single results and collection members within a declared view.

Collections organise access to Records within the Registry's identity scope. The same Record retains its identifier across Collections, views, revisions, and temporal selections. Distinct Records have distinct identifiers within that Registry, including when their source Collections use overlapping keys. An adapter can qualify such keys with a stable namespace; consumers continue to treat the resulting identifiers as opaque.

A service returning Records from different Registries or schemas makes the distinction explicit for each affected Record. A shared service URL alone does not establish a unique Registry context. An export or portable representation declares any additional context needed when it leaves its original request context.

Record schemas define [structured values and references](#core-structured-values-and-references), including the identity, ownership, and meaning of embedded data.

**Example: resolving Record context.** In the illustrative business binding, `GET https://registry.example/v1/collections/businesses/records/r_42` returns:

```json
{
  "recordId": "r_42",
  "data": {
    "legalName": "Example Ltd",
    "registrationStatus": "DISSOLVED"
  }
}
```

The metadata above associates that service with Registry `https://registry.example/registries/business` and the Business Registration Authority. The Retrieve operation in the linked OpenAPI declares that Registry, the `businesses` collection, and the `business-public` view; its response schema is `BusinessRecord`, whose `data` follows `BusinessData`. A consumer retaining this Record's identity stores the Registry Identifier together with `r_42`.

### Revisions and lifecycle <a href="#core-revisions-and-lifecycle" id="core-revisions-and-lifecycle"></a>

The Record Identifier remains stable when the Record changes. Existing source identifiers may be reused when they satisfy the identity and stability requirements. Core does not require an adapter to introduce revision storage, maintain a journal, or mint aliases for already suitable source identifiers.

Revision identifiers, revision recording times, and lifecycle fields are not required in the baseline. When supplied or required by a selected capability or profile, their schema defines their meaning and availability. A source revision identifies a revision accepted by the source; a response hash or HTTP validator does not by itself establish such an identifier. A response timestamp is not the time a source revision was recorded.

The latest information is the most recent accepted information available through the source interface under its documented currency contract. It need not describe an active entity. Domain status fields retain their documented meaning; omitting a generic lifecycle field does not imply an active state. Consultation revision and temporal capabilities require source-backed history and declared semantics beyond the default latest read. Event occurrence and registration dates are not automatically effective-time coordinates.

**Example: stable identity through a status change.** Two current reads of the same business, before and after its dissolution is accepted by the source, return:

| Read | `recordId` | `data.registrationStatus` |
|---|---|---|
| Before dissolution | `r_42` | `ACTIVE` |
| After dissolution | `r_42` | `DISSOLVED` |

The identifier continues to refer to the same Record; its current domain status changes.

### Domain semantics and extensions <a href="#core-domain-semantics-and-extensions" id="core-domain-semantics-and-extensions"></a>

Adopters should reuse established domain schemas and vocabularies where suitable, including [Schema.org](https://schema.org/), [EU SEMIC Core Vocabularies](https://interoperable-europe.ec.europa.eu/collection/semic-support-centre/solution/core-vocabularies), and schemas defined or adopted by national and sector authorities. The contract identifies adopted models and versions, preserves their concepts' meanings, and documents field meanings, source mappings, local constraints, and extensions. A separately published formal semantic model is not required unless a selected capability or profile requires it. Representations follow the applicable inherited cross-functional requirements.

Extensions preserve the meaning of required Registry and Record metadata. Compatible schema evolution keeps existing fields and context interpretable; an incompatible representation is identified through a new version or an explicitly selected view. The status of broader compatibility rules is documented under [coverage and limitations](../introduction/scope.md#coverage-and-limitations).

#### Structured values and references <a href="#core-structured-values-and-references" id="core-structured-values-and-references"></a>

Domain schemas distinguish values owned by the containing Record, references to other Records, and embedded representations of related Records. Component identifiers have schema-defined scope. Embedded related representations preserve the target Record's identity and Registry context and declare their source currency. Recorded values retain the meaning assigned by their owning source, including its correction rules.

A Record reference identifies its target Record and Registry unambiguously through the field schema or explicit reference context. Adopted domain reference forms can be used with documented identity, target scope, and resolution semantics. When a target read is offered, the field binding identifies the target collection, operational contract and operation, and how the reference supplies the required inputs. A binding with several possible targets defines how to select the applicable read. Target reads follow the Registry's published capabilities and access policy. Profiles declare any referential-integrity guarantees.

Embedded collection schemas declare bounds. Their contracts define complete permitted views, selected subsets, or pages with continuation; omitted, null, and empty values; and overflow outcomes. A collection declared complete contains every component permitted by that view. Each paginated collection has its own continuation context. Disclosure policy applies to references, embedded data, and completeness information.

**Example: related Record identity.** A field using the illustrative `UnscopedRecordReference` [schema](../api/examples/relationship-examples.schema.json) carries the target Registry explicitly:

```json
{
  "recordId": "person_42",
  "registryId": "https://registry.example/registries/individuals"
}
```

The same schema document defines `IndividualReference`, whose target Registry is fixed to that IRI. A field using it can carry `{"recordId": "person_42"}`. Its illustrative field binding maps `recordId` to the path parameter of the target service's `GET /v1/collections/individuals/records/{recordId}` operation. Reading that reference therefore uses `GET https://registry.example/v1/collections/individuals/records/person_42`, subject to the target service's published contract and access conditions. The binding supplies the route; the identifier remains opaque.

## Consultation <a href="#consultation-consultation" id="consultation-consultation"></a>

> **Status:** DRAFT requirements and HTTP binding, for review and implementation trials.

### Purpose and capability model <a href="#consultation-purpose-and-capability-model" id="consultation-purpose-and-capability-model"></a>

Consultation defines read access to Registry Records for independently implemented services and API Consumers. A service selects one or more operation options and publishes its operational contract through [Registry Core metadata](registry-discovery.md#core-api-family-discovery). Consumers use that contract to determine available operations and their inputs.

| Capability | Input | Successful result |
|---|---|---|
| Retrieve | Record Identifier | One Record |
| Lookup | Declared exact selector and its complete key | One Record |
| List | Declared collection and its supported equality filters | Page of Records |
| Search | Declared search and typed criteria | Page of Records |
| Revision List | Record Identifier | Page of retained Record revisions |
| Revision Retrieve | Record Identifier and Revision Identifier | One retained Record revision |

Shared requirements apply to every selected capability; operation requirements apply when that capability is selected. Each operation applies to a declared logical **Collection** with an unambiguous Registry context, representation schema, and access policy. A Collection is an API grouping with declared membership and one stable `collectionId`. It is independent of database tables, source-system modules, governed datasets, and the institutionally defined Registry. One Registry can expose several Collections, and one Record can appear in several Collections without changing its identity. [Selectable read features](#consultation-selectable-read-features) add stronger guarantees only when the operation declares them.

Collection boundaries are adopter choices. For example, a civil-registration service can expose `birth-registrations`, `marriage-registrations`, and `death-registrations` as separate Collections when that arrangement matches its service contract. Those names are illustrative; this specification does not define the legal scope of civil registration or require one Collection per event type.

Consultation interoperates at the level Core defines: operation shapes, the Record envelope, error outcomes, pagination, and discovery are the same for every Registry, while domain fields, selectors, searches, and filters are declared per contract. Consumers can reuse protocol and envelope handling; domain-specific selectors, field meanings, and reference bindings still require integration against the published contract. See the [interoperability boundary](registry-discovery.md#core-purpose-and-applicability) in Core.

### Common read contract <a href="#consultation-common-read-contract" id="consultation-common-read-contract"></a>

A read preserves the source Records. In the absence of an explicit temporal selector, it returns the latest permitted information available under the service's declared currency contract, including replication or cache delay. An operation selecting `recorded-time` or `effective-time` can instead accept the corresponding temporal selector. Snapshot traversal fixes one collection traversal; it does not by itself make historical Record states addressable. The contract documents currency and temporal semantics; verification reviews that documentation and the source arrangement rather than measuring delay. Domain schemas define the meaning of status, validity, event occurrence, and registration fields.

<a id="consultation-retrieve-representation"></a>

**Record representation.** A baseline `Record` contains `recordId` and `data`; a baseline `RecordPage` contains Records and pagination context. Neither baseline schema publishes temporal metadata. A temporally selected response includes the applied `temporal` context at the top level. The canonical `TemporalRecord` and `TemporalRecordPage` wrappers require that metadata; a concrete contract can instead publish one response schema covering current and selected responses when it requires temporal metadata whenever a selector is applied. Page-level echo keeps an empty temporal Search result interpretable without changing the shared item schema. The identifier is stable, unique within its Registry, and never reassigned. It remains the same across Collections, revisions, views, and temporal selections. The [Common Record context](#core-common-record-context) defines how the contract establishes the Registry and the representation schema: each operation declares its Registry, Collection, capability, and view with the `x-govstack-digital-registries` extension, and its response schema defines the view. Retrieve and Lookup return one Record; List and Search use the same Record shape for each item in a Page.

The `data` schema defines domain fields, structured values, references, and their meanings. Revision, lifecycle, and provenance metadata are not required in the baseline; profiles can require source-backed metadata with defined semantics.

**Example: Record representation.** Examples on this page use the [illustrative business Registry binding](../api/examples/business-registry.openapi.yaml), which defines the domain fields, status values, and query names. Its operations declare Registry `https://registry.example/registries/business`, collection `businesses`, and view `business-public`. A Record response contains:

```json
{
  "recordId": "r_42",
  "data": {
    "legalName": "Example Ltd",
    "registrationStatus": "DISSOLVED"
  }
}
```

**Consumer guidance (informative).** Consumers retain Registry context when storing or forwarding Record references, treat Record Identifiers as opaque, and interpret `data` using the declared schema. They accept additional response-envelope members and use only the inputs supported by the published contract. This specification places no conformance requirements on consumers.

### Service declarations <a href="#consultation-service-declarations" id="consultation-service-declarations"></a>

The published service contract supplies the following information for its selected capabilities, directly or through versioned references:

| Topic | Declared information |
|---|---|
| Registry context | Registry Identifier, logical Collection Identifier, capability, view, and selected selectable read features of each operation, through the Core [extension](registry-discovery.md#core-api-composition). |
| Representation | JSON Schemas for the Record view and responses; adopted models and versions; mappings, local constraints, and extensions. |
| Field meanings | Meaning, units, code lists, and omitted, null, or empty values, preserving the semantics of adopted models. |
| Lookup and Search | Names, typed inputs, required components, comparison and normalisation rules, uniqueness scope, and matching semantics. Reusable Search semantics name the supported equality, range, set-membership, and prefix operators without requiring a universal query language. |
| Pagination | Supported equality filters and sorting where offered, deterministic default order with a unique tie-breaker, page-size limits, cursor expiry, source consistency and concurrent-change behaviour, and any complete or snapshot traversal guarantee. |
| Access and currency | Authentication requirements, access policy for the declared view, and source currency, including material replication or cache delay. |
| Resource limits | Request and response bounds, configured timeout behaviour and failure outcome, and any source-query or scan limits. A page-size limit does not establish a bound on source rows examined or database work. |
| Field selection | Supported top-level `data` field names, default field set, mandatory fields if any, selection bounds, omission semantics, and response schema. |
| Revisions and time | Supported revision capabilities, order, retention and gap semantics, schema evolution, recorded-time and effective-time meanings, accepted selector precision, and unavailable-history outcomes. |
| Purpose binding | When selected, the trusted purpose binding, controlled purpose codes or absolute URIs, permitted values, rejection behaviour, cursor and validator binding, and audit treatment. |

A domain profile records reusable agreements about schemas, terminology, and query semantics. A service contract applies those agreements to the operations it exposes. An implementation can adopt an existing profile or publish a concrete domain binding directly. Both preserve the shared Consultation behaviour. Reuse of domain models, the treatment of structured values, Record references, and embedded collections, and schema evolution follow [Registry Core](#core-domain-semantics-and-extensions).

**List and Search.** List and Search both return Pages, and the split between them follows the API design guide. List carries equality filters on declared non-personal fields as query parameters, one parameter per field (guide §12.8). Personal criteria, composite keys, and non-equality matching belong to Search, whose request body keeps them out of URLs and logs (guide §8.6 and §12.9). A contract that needs neither can select List alone; a contract whose every useful criterion is personal selects Search alone.

**Reusable Search semantics.** A contract publishes named searches whose criteria remain typed by versioned schemas. It can reuse the standard equality, range, set-membership, and prefix meanings defined by this specification, independently selecting only those it supports. The field contract states the applicable operator, comparison type, normalisation, null and absence treatment, and combination rule. A deployment is not required to implement fuzzy matching, full-text search, or a universal query language. The [business binding](../api/examples/business-registry.schema.json) illustrates a concrete selection of reusable semantics.

### Selectable read features <a href="#consultation-selectable-read-features" id="consultation-selectable-read-features"></a>

Each operation selects additional read features through the `features` array of its `x-govstack-digital-registries` declaration. Omission or an empty array selects none. The declaration lets a shared client distinguish ordinary reads and browsing from stronger guarantees without changing the Record and Page envelopes.

| Feature | Applicable operations | Additional requirement |
|---|---|---|
| `conditional-read` | Retrieve | #8: ETag and conditional GET. |
| `field-selection` | Any Consultation read | #9: A requested subset of declared `data` fields. |
| `complete-traversal` | List or Search | #10: Each permitted match once under unchanged source data and access conditions. |
| `snapshot-traversal` | List or Search | #11, plus `complete-traversal`: Source membership, order, and data fixed at one evaluation point. |
| `recorded-time` | Retrieve, Lookup, List, or Search | #14: Selection by the source-accepted knowledge cutoff. |
| `effective-time` | Retrieve, Lookup, List, or Search | #15: Selection by declared date or instant applicability. |
| `purpose-bound` | Retrieve, Lookup, List, Search, Revision List, or Revision Retrieve | #18: A trusted, controlled purpose value is required and enforced. |

### Revision and temporal capabilities <a href="#consultation-revision-and-temporal-capabilities" id="consultation-revision-and-temporal-capabilities"></a>

Revision history is selectable and source-backed. A service does not create historical revisions by caching current responses, traversing a collection snapshot, deriving values from event notifications, or assigning identifiers to representations that the source cannot distinguish. Every history request applies current authentication, authorisation, disclosure, and purpose policy. A protected or unavailable revision produces the declared unavailable outcome without revealing whether hidden history exists.

### HTTP binding <a href="#consultation-http-binding" id="consultation-http-binding"></a>

The [canonical OpenAPI](../resources/api.yml) defines the synchronous HTTPS/JSON contract, version `1.0.0-draft`, using API design guide and ruleset `0.3.0-draft`. Its `CollectionId` schema uses the single reference value `records`; concrete examples use literal Collection Identifiers such as `businesses`, `households`, and `birth-registrations`. The `/v1` prefix is the HTTP compatibility line. The BB requirements remain DRAFT. The [read API design decisions](#consultation-consultation) record the binding choices and the shared guide refinements.

#### Deployment contract <a href="#consultation-deployment-contract" id="consultation-deployment-contract"></a>

The server URL identifies the deployment root, which may include a stable routing prefix such as `/registry`. The canonical hierarchy is `/v1/collections/{collectionId}`; with that prefix a household Record is addressed under `/registry/v1/collections/households/records/{recordId}`.

A deployment publishes a concrete OpenAPI contract containing its selected operations and selectable read features, service and authentication endpoints, versioned JSON Schemas for `data` and the complete response, selectors, searches, supported filters and ordering, source currency, access policy, resource limits, temporal and revision semantics where selected, and continuation policy. Every selected Collection-scoped Consultation operation carries the `x-govstack-digital-registries` extension required by [Provide Registry Services](registry-services.md); it names the Registry, Collection, capability, and view, and the operation's response schema defines that view. The `features` array, which can be omitted, declares the additional read guarantees. A `purpose-bound` operation also carries its required `purpose` declaration. The extension is the binding's answer to the Common Record context: the Registry Identifier is not repeated in requests or Records. The cross-Collection caller capability operation uses its own response schema rather than declaring one Collection context.

One API can expose several collections. A shared API can therefore expose:

```http
GET /v1/collections/businesses/records/{recordId}
GET /v1/collections/households/records/{recordId}
GET /v1/collections/birth-registrations/records/{recordId}
POST /v1/collections/households/lookup
POST /v1/collections/households/search
```

These are illustrative Collection names; the published contract defines the supported paths and membership. Collections are logical API resources and need not match tables, source modules, governed datasets, or separate institutional Registries. A Record retains its `(registryId, recordId)` identity across Collections and views within its Registry. [API composition](registry-discovery.md#core-api-composition) describes how Collections and families share an API; Consultation and Write can share a resource URI with separate methods, schemas, and permissions. The [OpenAPI examples](../resources/api-examples/README.md) illustrate concrete Collections, domain schemas, and response payloads.

#### Operations <a href="#consultation-operations" id="consultation-operations"></a>

| Capability | HTTP operation, relative to the deployment root | Successful body | Input contract |
|---|---|---|---|
| Retrieve | `GET /v1/collections/{collectionId}/records/{recordId}` | `Record`, or `TemporalRecord` for selected temporal state | Record Identifier in the path; `recordedAsOf` or `effectiveAt` query selector when its feature is declared. |
| Lookup | `POST /v1/collections/{collectionId}/lookup` | `Record`, or `TemporalRecord` for selected temporal state | `LookupRequest` with `selector`, `values`, and `temporal` when declared. |
| List | `GET /v1/collections/{collectionId}/records` | `RecordPage`, or `TemporalRecordPage` for selected temporal state | Any `pageSize`, `cursor`, declared filters and sort, plus temporal query selectors when declared. |
| Search | `POST /v1/collections/{collectionId}/search` | `RecordPage`, or `TemporalRecordPage` for selected temporal state | `SearchRequest` with `search`, `criteria`, pagination controls, and `temporal` when declared. |
| Revision List | `GET /v1/collections/{collectionId}/records/{recordId}/revisions` | `RevisionPage` | Record Identifier and pagination controls. |
| Revision Retrieve | `GET /v1/collections/{collectionId}/records/{recordId}/revisions/{revisionId}` | `RecordRevision` | Record and Revision Identifiers. |


##### Retrieve <a href="#consultation-retrieve" id="consultation-retrieve"></a>

Retrieve uses `GET /v1/collections/{collectionId}/records/{recordId}` to return the latest permitted Record representation for a stable Record Identifier, or the representation selected by a declared temporal selector.


##### Lookup <a href="#consultation-lookup" id="consultation-lookup"></a>

Lookup uses `POST /v1/collections/{collectionId}/lookup` with a declared exact selector and complete key to resolve at most one permitted Record.


##### List <a href="#consultation-list" id="consultation-list"></a>

List uses `GET /v1/collections/{collectionId}/records` with declared equality filters and ordering to return a bounded Page of permitted Records.


##### Search <a href="#consultation-search" id="consultation-search"></a>

Search uses `POST /v1/collections/{collectionId}/search` with a declared search name and typed criteria to return a bounded Page of permitted matching Records.


##### Revision List <a href="#consultation-revision-list" id="consultation-revision-list"></a>

Revision List uses `GET /v1/collections/{collectionId}/records/{recordId}/revisions` to return a bounded Page of retained revisions of one Record.


##### Revision Retrieve <a href="#consultation-revision-retrieve" id="consultation-revision-retrieve"></a>

Revision Retrieve uses `GET /v1/collections/{collectionId}/records/{recordId}/revisions/{revisionId}` to return one retained revision of one Record.

Lookup and Search are actions on the Collection resource, while item identifiers are under its separate `/records` child. Consequently, `lookup` and `search` do not collide with `{recordId}` and are not reserved Record Identifier values. Lookup and Search are synchronous reads returning `200`; selector and search values remain in the request body. Lookup uses a declared unique key within its documented scope; Search uses declared named typed criteria. The concrete contract defines comparison and normalisation rules and rejects unsupported inputs. The binding also exposes the guide's unversioned `/health` operation.

The canonical contract can also expose `GET /v1/capabilities` with operation ID `getCallerCapabilities`. Its single bounded `CallerCapabilities` response is caller-filtered, advisory, and `no-store`; each operation entry requires a version-specific HTTPS contract, operation ID, capability annotation, and view, and can include `readableFields`, selector, Search, feature, and purpose annotations. `readableFields` does not imply `field-selection`. Capability and feature annotations are extensible as described in requirement #17, while the linked normative operation extension remains closed for its contract version. The document contains at most 64 Collections and 16 operations per Collection. A deployment fails explicitly when the authorised description exceeds a declared bound; it does not truncate or silently omit it. `collections: []` means no operation is visible to the caller, not overflow.

**Example: exact Lookup.** The business binding names its Collection `businesses`. To resolve a business by its declared registration-number key, send this body to `POST /v1/collections/businesses/lookup`:

```json
{
  "selector": "byRegistrationNumber",
  "values": {
    "registrationNumber": "BR-000042"
  }
}
```

For the permitted match, the `200` response is the Record shown above.

**Example: Search and collection result.** To find businesses with a declared registration status, send this body to `POST /v1/collections/businesses/search`:

```json
{
  "search": "byRegistrationStatus",
  "criteria": {
    "registrationStatus": "DISSOLVED"
  },
  "pageSize": 20
}
```

With one permitted match and traversal complete, the `200` response is:

```json
{
  "items": [
    {
      "recordId": "r_42",
      "data": {
        "legalName": "Example Ltd",
        "registrationStatus": "DISSOLVED"
      }
    }
  ],
  "pageInfo": {
    "nextCursor": null
  }
}
```

List uses the same Page shape for its declared collection.

#### Representation and schema context <a href="#consultation-representation-and-schema-context" id="consultation-representation-and-schema-context"></a>

Retrieve and Lookup return baseline `Record` or, when temporal coordinates are applied, `TemporalRecord`. List and Search return baseline `RecordPage` or `TemporalRecordPage`, with each item using the same Record schema for the declared view. Revision Retrieve returns `RecordRevision`; Revision List returns `RevisionPage`. Empty and single-result Collections retain their Page shape. `TemporalRecord` echoes applied coordinates at Record level. `TemporalRecordPage` echoes them at Page level, including when `items` is empty. Baseline `Record` and `RecordPage` omit temporal metadata.

The operation's Registry context declaration and response schema provide Registry and schema context. Additional source metadata follows [Registry Core](#core-common-record-context). A schema linked with `rel="describedby"` describes the complete response, including its envelope. Different operations can declare different views; operations sharing a collection and view use the same Record schema.

**Audience-dependent fields.** A view schema can mark varying fields as not required so access policy and consumer field selection determine which are returned on the same operation. The contract documents the default field set and omission meanings; the schema alone does not guarantee selectable fields will always be present. A materially different view with different required fields or meanings uses a separately declared operation or API. Records retain their identity across those views.

**Field-selection input.** An operation selecting `field-selection` publishes a `fields` input, which clients can omit, restricted to its declared selectable top-level `data` property names. GET operations use a comma-separated query array, for example `GET /v1/collections/businesses/records/r_42?fields=legalName`. Lookup and Search carry a JSON array in the body, for example `"fields": ["legalName"]`. The input selects existing fields; it does not introduce a query language, nested expansion syntax, or a different view schema. Mandatory `data` fields, if any, remain present as documented. Without this feature, an operation does not accept this input.

#### Temporal selection <a href="#consultation-temporal-selection" id="consultation-temporal-selection"></a>

Timestamp selectors and revision recording times use RFC 3339 UTC instants serialised with uppercase `Z`. Calendar-date applicability coordinates use `format: date` and are not converted into instants. The illustrative birth profile accepts calendar dates only for `effectiveAt`, including its response echo, while its recording-time coordinates remain UTC instants.

GET Retrieve and List carry `recordedAsOf` and `effectiveAt` as query parameters only when the corresponding feature is selected. POST Lookup and Search carry the same coordinates inside the closed, non-empty `temporal` object, when supplied. `recordedAsOf` is a date-time; `effectiveAt` is a date or date-time as the concrete contract declares. The operation can accept either or both coordinates. When both are present, it selects the state applicable at `effectiveAt` using only source knowledge accepted no later than `recordedAsOf`. `TemporalRecord` and `TemporalRecordPage` echo every applied source-backed coordinate, including an empty Page. Absence selects the latest representation and omits temporal metadata; a concrete contract can publish a response schema that covers both cases while enforcing that temporal metadata is present whenever a selector is applied. Revision List and Revision Retrieve do not accept these selectors.

Temporal selection is distinct from traversal consistency. `snapshot-traversal` holds one paged result stable but does not provide recorded-time or effective-time history. Conversely, a temporal selector does not make later continuation Pages a snapshot unless `snapshot-traversal` is also selected.

#### Revision history <a href="#consultation-revision-history" id="consultation-revision-history"></a>

Revision operations use a separately declared history view, such as `record-history`. `RecordRevision.revision` always contains `revisionId` and can contain `recordedAt` when that value is source-backed. The deployment documents revision order, retention, gaps, and schema evolution. A declared history view can normalise older source schemas while preserving their values and meanings; a revision that cannot be mapped faithfully produces the declared explicit failure. Current authorisation and disclosure apply to every request and Page. An unavailable historical state fails with the declared protected outcome; the service does not expose an arbitrary raw schema or synthesise it from current data, snapshots, audit events, registration dates, or event occurrence dates.

<a id="consultation-pagination"></a>
<a id="consultation-pagination-contract"></a>

#### Continuation <a href="#consultation-continuation" id="consultation-continuation"></a>

The first request selects `pageSize`, defaulting to 20 and bounded to 100 in the canonical contract. A continuation repeats the original criteria, search name where applicable, sorting, temporal selection, and effective field selection with the cursor. Field order does not change the selected set; omission uses the declared default. It can omit `pageSize` to retain the bound value or supply that same value; a different value produces `400 invalid-cursor`. Cursors are opaque, URL-safe, integrity-protected, and exclude personal data. They bind the operation, Registry, Collection, query, view, temporal context, effective field set and size, effective purpose where required, and applicable access context. A Revision List cursor also binds its parent `recordId`; replay under another parent produces `400 invalid-cursor`. Cursors do not grant authority; every Page is reauthorised. The deployment declares expiry and rejects malformed, expired, or mismatched cursors, including continuations whose declared semantics it can no longer preserve. A short or empty Page can carry a non-null `nextCursor` when source processing advances. An adapter can wrap a source offset, page number, or continuation token while preserving these rules.

A non-null `pageInfo.nextCursor` enables continuation; `null` marks completion of the declared traversal. Baseline completion follows the published consistency and result-limit policy. Only `complete-traversal` establishes exhaustive membership, and only `snapshot-traversal` establishes a fixed source snapshot. When supplied, `pageInfo.total` is the exact count of the full permitted query at the documented evaluation point, before applying the continuation boundary: the current page's evaluation for live reads or the fixed source snapshot evaluated under current disclosure rights for snapshot traversal. Disclosure policy decides whether it is offered at all. Services omit an unavailable total. OpenAPI defines the cursor format, limits, and error responses.

#### Outcomes, errors, and caching <a href="#consultation-outcomes-errors-and-caching" id="consultation-outcomes-errors-and-caching"></a>

OpenAPI defines the status codes and RFC 9457 Problem Details for each operation. Retrieve and Lookup share `404 record-not-available` for unknown Records, Records outside the selected Collection, and Records whose existence is protected under [Provide Registry Services](registry-services.md). Revision List and Revision Retrieve use the same outcome for an unknown or protected parent Record; Revision Retrieve also uses it when the revision is unknown or protected, without distinguishing which resource was unavailable. After these protection checks, an authorised operation whose source cannot return retained history uses `409 history-not-available`.

A successful List or Search with zero permitted matches returns `200` with an empty `items` array, including when policy filters every source match. For a temporal item read, a source-backed determination that no item exists at the selected coordinates uses `404 record-not-available`, subject to protected-existence handling. When the authorised source cannot evaluate the requested temporal state or query, the operation uses `409 temporal-state-not-available` and never substitutes current state. These outcomes distinguish proven absence from unavailable historical evaluation.

Structural input errors, invalid query parameters, and invalid pagination controls use `400`. Empty, duplicate, incorrectly typed, or out-of-bounds field selections also use `400`. Structurally valid Lookup and Search bodies with unknown selector, search, or selectable field names or invalid domain values use `422`. Unknown selectable field names in a query use `400`. Malformed, expired, mismatched, or cross-parent Revision List cursors use `400 invalid-cursor`.

Protected reads and errors use `Cache-Control: no-store`. Deployments may declare caching for public or isolated representations. An operation selecting `conditional-read` publishes `If-None-Match` and `304`; its `200` and `304` responses carry the declared ETag header for the permitted representation, and authorisation precedes evaluation of the validator. The matching `304` is bodyless, while `200` carries the declared response body and headers. A baseline Retrieve operation need not publish ETag, `If-None-Match`, or `304`. Authentication, authorisation, and source failures follow the declared OpenAPI responses and the API design guide. The API catalog's conditional responses are independent of the Consultation feature declaration.

When `purpose-bound` is selected, the operation extension identifies a trusted access-token claim or trusted authorisation context and the controlled allowed purpose values. Purpose never comes from an ordinary request parameter. Missing or unallowed purpose fails before disclosure, and the effective purpose participates in cursor and ETag context. This does not replace inherited security or establish consent, institutional authority, or downstream compliance. Operations without `purpose-bound` continue to use their inherited authentication and authorisation requirements without a purpose input.

#### Record references and expansion <a href="#consultation-record-references-and-expansion" id="consultation-record-references-and-expansion"></a>

The [Core representation rules](#core-structured-values-and-references) govern nested data and related Records. The reusable `RecordReference` schema carries `recordId` and, where the field schema leaves the target Registry open, required `registryId`. A field with a fixed target Registry permits omission of `registryId` and accepts an explicit value only when it matches that target.

When a related read is offered, the field binding identifies its target collection, read operation, and operational contract, including how the reference supplies the operation's inputs. Consumers follow that binding and the target's access requirements. Record Identifiers remain opaque; reference identity is independent of the target's current availability.

Client-selected expansion, where offered, declares its supported paths, bounds, source currency, and disclosure behaviour in the deployment contract. Expansion embeds related representations inside the declared view; it does not select a different view. The [OpenAPI examples](../resources/api-examples/README.md) demonstrate concrete nested schemas and references.

### Conformance <a href="#consultation-conformance" id="consultation-conformance"></a>

Evaluation identifies the service, specification and contract versions, selected capabilities, and any adopted domain profile. The service satisfies the common read contract, service declarations, HTTP binding, and the requirements applicable to each selected capability.

| Selected operation option | Applicable behaviour |
|---|---|
| `consultation-retrieve` | Retrieve by identifier, permitted representation, and protected-existence handling when policy protects existence. |
| `consultation-lookup` | Exact selector resolution, permitted representation, and protected-existence handling when policy protects existence. |
| `consultation-list` | Bounded collection listing, permitted representation, and bounded continuation. |
| `consultation-search` | Declared typed search with reusable Search semantics, permitted representation, and bounded continuation. |
| `consultation-revision-list` | Retained revision listing for one Record, permitted representation, bounded continuation, and protected-existence handling when parent Record or history existence is protected. |
| `consultation-revision-retrieve` | One retained revision of a Record, permitted representation, and protected-existence handling when parent Record or revision existence is protected. |

Each selected selectable read feature additionally applies its requirement: #8 through #11 for conditional, selection, and traversal guarantees; #14 and #15 for temporal selection; and #18 for purpose binding. Offering caller capability discovery applies #17. Capability conformance covers the shared contract and selected operations; additional feature claims establish their stronger guarantees. A shared SDK can handle the common operations, envelopes, errors, and continuation while configuring domain schemas and criteria per Registry. Applications needing complete exports, fixed snapshots, source history, temporal reads, or purpose binding check those declarations explicitly.

Verification checks published contracts and observable exchanges under the stated fixture conditions. The [OpenAPI examples](../resources/api-examples/README.md) and [artifact validation](../resources/testing.md#artifact-validation) support review; deployed behaviour is evaluated separately.

### Resource paths, identity, and API composition <a href="#consultation-resource-paths-identity-and-api-composition" id="consultation-resource-paths-identity-and-api-composition"></a>

Lookup and Search use collection action sub-resources, the convention shared across GovStack BB APIs:

```http
GET /v1/collections/households/records/{recordId}
GET /v1/collections/households/records
POST /v1/collections/households/lookup
POST /v1/collections/households/search
```

Lookup and Search are children of the Collection resource, while Record items are children of its `/records` resource. A Record Identifier equal to `lookup` or `search` therefore remains addressable under `/records/{recordId}` and does not collide with either action. The guide's §5.8 reservation rule does not apply because the action names are not used inside the Record collection's identifier namespace.

This hierarchy exceeds the API Design Guide §5.4 preference for at most two nesting levels after `/v1`. Section 5.4 is a SHOULD, not a MUST. The additional depth is deliberate: this specification selects an explicit logical Collection resource so Collection-level actions, Record items, and Record revision sub-resources remain unambiguous while Record identity stays stable across Collections. The contract documents that rationale; it does not claim an approved guide exception.

Collection membership scopes every read. Retrieve and Lookup use the unavailable-Record outcome for Records outside that Collection, and continuation binds the Collection as well as the query. Identity remains `(registryId, recordId)` across Collections, views, revisions, and temporal selections. Source adapters disambiguate overlapping keys for distinct Records in the same Registry with stable identifiers. Field bindings identify target read operations and input mappings for resolvable references.

### Relationship identity, snapshots, and completeness <a href="#consultation-relationship-identity-snapshots-and-completeness" id="consultation-relationship-identity-snapshots-and-completeness"></a>

The [Core representation rules](#core-structured-values-and-references) distinguish owned components, Record references, and related-data views across API families. The [household contract](../api/examples/household-registry.openapi.yaml) embeds membership attributes and references individual Records. The [birth-registration contract](../api/examples/birth-registration.openapi.yaml) owns recorded parent details, with individual references that may be absent.

Each view declares array bounds and completeness for the permitted representation. A complete array exceeding its bound follows the declared failure contract. A separately paginated relationship collection has its own published operation.

## Write <a href="#write-write" id="write-write"></a>

> **Status:** DRAFT requirements and HTTP binding, for review and implementation trials.

### Purpose and capability model <a href="#write-purpose-and-capability-model" id="write-purpose-and-capability-model"></a>

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


### Published Write contract <a href="#write-published-write-contract" id="write-published-write-contract"></a>

The canonical [Write OpenAPI contract](../resources/write-api.yml) defines the HTTP shapes.
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

### Direct Write semantics <a href="#write-direct-write-semantics" id="write-direct-write-semantics"></a>

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

### Resource path depth <a href="#write-resource-path-depth" id="write-resource-path-depth"></a>

The API Design Guide §5.4 recommends at most two semantic resource levels after `/v1` as a SHOULD, not a MUST.
A named action after the explicit Collection and Record creates three semantic resource levels.
That additional depth is deliberate: it preserves the selected Collection boundary, the addressed Record, and the fixed action meaning without placing an action name in the Record identifier namespace or turning it into a caller-selected generic command.

The non-normative examples use the same rationale for fixed correction and add-member actions.
Supporting paths such as `/v1/change-requests/{changeRequestId}/approve` have only the Change Request and approval-action levels.
The deeper direct action paths retain the guide warning for review; this draft does not claim an approved exception.


### Non-normative domain examples <a href="#write-non-normative-domain-examples" id="write-non-normative-domain-examples"></a>

The [example contracts and payloads](../resources/api-examples/README.md) demonstrate how institution-selected domain models can bind to Write without becoming shared requirements.
Their field names, vocabularies, validation rules, permissions, and review policies are examples only.

A civil-registration declaration or correction can use an operational input shape that differs from the permitted Birth read projection.
Reasons, supporting evidence, requester context, fees, review decisions, and application state remain command, provenance, or workflow information rather than Birth facts.
Only successfully applied authoritative content enters the read projection; a pending, rejected, withdrawn, blocked, or failed proposal does not alter it.

A Household can be created using references to existing people.
A profile can also create people and the Household together only when it separately declares and verifies one atomic transaction within the same authoritative source.
Request-local references resolve to authoritative Record identifiers only after that compound commit succeeds.
The same boundary applies when adding a member later: adding an existing person needs no compound creation guarantee, while creating and adding a new person together requires the declared same-source transaction guarantee.

These examples do not require a civil-registration or household model, combine those domains under one authority, define a generic batch language, or promise a distributed transaction.


### Atomicity and compound changes <a href="#write-atomicity-and-compound-changes" id="write-atomicity-and-compound-changes"></a>

Each operation declares its own component boundary.
Within that boundary, success is all or nothing: a Create does not leave a partial Record, an Update does not commit only some declared components, a Transition does not advance state without its associated committed data, and a Change Request submission does not create a partially stored proposal.

Atomicity across additional Records, Collections, Registries, messages, credentials, or external systems is a stronger guarantee that a deployment declares and verifies separately.
The baseline permits a workflow to coordinate several independently committed components and report an explicit partial or compensating outcome, provided it does not label that sequence atomic.


### Retries and idempotency <a href="#write-retries-and-idempotency" id="write-retries-and-idempotency"></a>

Every selected primary operation accepts the contract's idempotency key and binds it to the authenticated consumer, operation, Registry, Collection, target where present, trusted purpose where required, and canonical request content.
The contract declares key syntax, retention, the replay response, and the conflict returned when the key is reused with different bound content.

A retry with the same key and content cannot create a second committed effect.
The service still applies current authentication and authorisation before executing or disclosing the replayed result.
An idempotency key is neither a credential nor a reservation of future authority.
After the declared retention period, a consumer cannot assume that repeating a mutation is safe and obtains current state before deciding how to recover.


### Concurrency and commit guards <a href="#write-concurrency-and-commit-guards" id="write-concurrency-and-commit-guards"></a>

Update and Transition require a strong opaque precondition for the current target representation.
A Change Request that proposes a change to an existing Record captures the same source precondition at submission.
The service rejects an omitted, malformed, or stale required precondition and checks a matching precondition atomically with commit.

The commit guard protects the current target representation.
It does not require a public revision-history operation, retained historical representations, or reconstruction of a revision sequence.
If two writers start from the same target state, at most one can commit under that guard.


### Authority and purpose <a href="#write-authority-and-purpose" id="write-authority-and-purpose"></a>

Read and Write permissions are separate.
A consumer can be allowed to write information it cannot read back, or to read a Record it cannot change.
Create, Update, Transition, Change Request submission, review, and application each have separately evaluated grants and target scopes.

A deployment that enforces purpose declares one trusted binding and controlled values for each affected operation.
Purpose comes from the trusted authentication or authorisation context, not an ordinary query or body field.
Purpose supplements the operation grant and is not consent, institutional authority, approval, or proof of downstream use.


### Trusted context and client input <a href="#write-trusted-context-and-client-input" id="write-trusted-context-and-client-input"></a>

Actor, reviewer, purpose, approval, and application status are derived from trusted security and workflow context.
The service rejects or ignores client-supplied control fields according to the published schema and never treats them as verified authority.
A domain schema can contain fields with similar names as Record data, but those values do not authenticate an actor, select a reviewer, satisfy a purpose rule, approve a request, or apply a change.


### Acknowledgement, provenance, and audit <a href="#write-acknowledgement-provenance-and-audit" id="write-acknowledgement-provenance-and-audit"></a>

Every accepted Write uses its declared HTTP status, response schema, target URI, `Location`, or validator to identify the target, created resource, or asynchronous Operation and to distinguish authoritative commit, non-authoritative request creation, and accepted asynchronous work.
A bodyless successful response can identify its existing target through the request URI and validator and does not need an invented response body.
The response does not claim that queued work committed, that a submitted proposal was approved, or that an approved request was applied.
Correlation follows the inherited API guidance and the deployment's published policy rather than requiring a new Write-specific identifier in every response.

The service retains provenance and audit evidence for the trusted actor, selected operation, Registry, Collection, Record or Change Request target, trusted purpose where present, validated input identity, precondition, decision, and committed effect.
The deployment declares retention, integrity, clock, redaction, and access boundaries.
Source or recording time is exposed only when the source provides it with documented source-backed semantics; this binding does not require a new history timestamp.
Audit evidence is protected according to its sensitivity and does not prove legal authority, consent, downstream use, or source facts outside the declared validation scope.


### Protected resources <a href="#write-protected-resources" id="write-protected-resources"></a>

An authenticated caller receives the same generic `404` outcome for an unknown resource and a resource whose existence is protected.
This rule covers protected Records, Collections, Change Requests, Operations, and operation availability where the access policy protects them.
The outcome does not reveal the protected resource through body content, security-relevant headers, workflow state, validation detail, conflict detail, precondition detail, timing classes, counts, or continuation behaviour.
Independently generated trace and correlation values can differ.

Authentication can fail before resource resolution.
After protected resolution begins, the service does not return a more specific conflict or workflow outcome unless the caller is permitted to know that resource and context.


### Preview and authoritative state <a href="#write-preview-and-authoritative-state" id="write-preview-and-authoritative-state"></a>

Validation or preview, when offered, is read-only.
Its response is explicitly non-authoritative and states the policy and source evaluation point used.
It does not allocate an authoritative Record Identifier, advance a Change Request, reserve a transition, or guarantee that a later Write will succeed.

A later Write repeats current authentication, authorisation, input validation, source precondition, trusted-purpose, and transition-policy checks.
Clients distinguish preview data from the authoritative acknowledgement and from Consultation of committed Registry state.


### Change Request lifecycle <a href="#write-change-request-lifecycle" id="write-change-request-lifecycle"></a>

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


### Application-time revalidation <a href="#write-application-time-revalidation" id="write-application-time-revalidation"></a>

Application rechecks current authentication, application permission, trusted purpose where required, target availability, the retained source precondition, typed input validity, and transition policy.
These checks are atomic with the authoritative commit.
A stale precondition is not weakened, current content is not silently substituted, and changed proposal content is not applied under an earlier decision.

If any check fails, the service records an explicit unapplied outcome and leaves authoritative state unchanged.
The request's approval decision and application outcome remain separately visible to permitted actors.


### HTTP outcomes <a href="#write-http-outcomes" id="write-http-outcomes"></a>

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


### Change Request listing <a href="#write-change-request-listing" id="write-change-request-listing"></a>

`listChangeRequests`, when offered, returns only requests permitted for the current caller and context.
It uses deterministic ordering with a unique tie-breaker, bounded Pages, a declared default and maximum size, and opaque integrity-protected continuation.
The cursor is bound to caller context, Registry, Collection, filters, order, and effective page size and expires under the published policy.
Every Page reauthorises.

Malformed, tampered, expired, or context-mismatched cursors fail explicitly and never restart silently.
Empty and short advancing Pages retain the Page shape.
A non-null cursor advances, and `null` marks completion under the declared consistency and result-window policy.
Baseline listing does not promise exhaustive traversal or a fixed source snapshot.

### Conformance boundary <a href="#write-conformance-boundary" id="write-conformance-boundary"></a>

The four Write options are DRAFT and independently selectable under the existing `registry-service` variation point.
Only requirements conditioned on a selected option apply to that option.
Conditional facilities such as preview, withdrawal, asynchronous processing, and request listing apply only when offered.
Stronger compound atomicity, exhaustive listing, snapshot listing, multi-approver policy, and domain-specific state machines are not baseline guarantees.

The OpenAPI contract and examples support artifact review.
They do not establish that a deployed implementation enforces authorisation, atomicity, preconditions, idempotency, workflow separation, protected existence, or crash recovery.
Those claims require the pending runtime scenarios in [Write testing](../resources/write-testing.md).

## Service workflows <a href="#workflow-workflows" id="workflow-workflows"></a>

### Retrieve a permitted Record representation <a href="#workflow-retrieve-a-permitted-record-representation" id="workflow-retrieve-a-permitted-record-representation"></a>

This workflow applies to implementations selecting Retrieve. The [HTTP binding](../api/openapi.yaml) defines request and response details.

#### Preconditions <a href="#workflow-preconditions-1" id="workflow-preconditions-1"></a>

1. The published service contract exposes Retrieve and identifies its Registry, collection membership, representation schema, and any selectable features.
2. The consumer has the credentials and request context required by the deployment.

#### Interaction <a href="#workflow-interaction-1" id="workflow-interaction-1"></a>

1. The consumer sends a request to the declared item path, such as `GET /v1/collections/businesses/records/{recordId}`, with a Record Identifier within the Registry. When the operation declares `field-selection`, the consumer may also request declared selectable top-level `data` fields with `fields`. When a temporal feature is declared, the consumer can explicitly supply `recordedAsOf` or `effectiveAt`; omission requests the latest representation.
2. The Registry evaluates authentication, access, and disclosure policy.
3. The Registry resolves the latest or explicitly selected source-backed Record state within the Collection and constructs its permitted baseline `Record` or selected `TemporalRecord` representation. Latest Records may include inactive Records.
4. The Registry returns that representation or the declared unsuccessful outcome.

#### Outcomes <a href="#workflow-outcomes-1" id="workflow-outcomes-1"></a>

| Condition | Observable outcome |
|---|---|
| Latest Record state is accessible without temporal selection | The latest permitted representation is returned without temporal metadata. |
| Explicitly selected Record state is accessible | A `TemporalRecord` echoing the applied temporal context is returned. |
| Consumer has narrower disclosure rights | The returned representation satisfies both disclosure policy and its schema. |
| Identifier is unknown, belongs to a Record outside the collection, or has protected existence | The same `record-not-available` outcome is returned. |
| Source proves no Record exists at the selected temporal coordinates | `404 record-not-available`, subject to protected-existence handling. |
| Authorised source cannot evaluate the selected temporal state | `409 temporal-state-not-available`; current state is not substituted. |
| Operation declares `conditional-read` and an authorised `If-None-Match` validator matches | A bodyless `304` with the selected representation's ETag is returned. |

#### Postconditions <a href="#workflow-postconditions-1" id="workflow-postconditions-1"></a>

- The source Record is unchanged.
- The returned identifier matches the requested identifier.
- Registry, schema, and authority context are unambiguous; any additional source metadata follows the published contract.
- Field selection retains `recordId` and `data`, uses the operation's one declared view schema, and cannot widen disclosure. Unsupported fields produce the declared validation error.

### Look up a Record using an exact selector <a href="#workflow-look-up-a-record-using-an-exact-selector" id="workflow-look-up-a-record-using-an-exact-selector"></a>

This workflow applies to implementations selecting Lookup.

#### Preconditions <a href="#workflow-preconditions-2" id="workflow-preconditions-2"></a>

1. The contract exposes a Lookup operation, such as `POST /v1/collections/businesses/lookup`, and declares the Collection, selectable features, and selector's typed components, comparison rules, and uniqueness scope.
2. The consumer has the required credentials and request context.

#### Interaction <a href="#workflow-interaction-2" id="workflow-interaction-2"></a>

1. The consumer sends `{selector, values}` using the declared schema. A composite selector supplies every key component. When the operation declares `field-selection`, the body may also carry a `fields` array of declared selectable top-level `data` fields. A declared temporal selection is carried in the body `temporal` object.
2. The Registry validates the input and evaluates access and disclosure policy.
3. The Registry resolves the selector within its declared scope, checks uniqueness, and applies collection membership.
4. One permitted match returns the common Record representation. Other outcomes follow the contract, including protected-existence handling and source uniqueness failures.

#### Postconditions <a href="#workflow-postconditions-2" id="workflow-postconditions-2"></a>

- The source Record is unchanged.
- A successful Lookup returns the same Record schema and field meanings as other reads of that view.
- Multiple source matches fail without selecting an arbitrary Record.

### Page through a declared collection or search result <a href="#workflow-page-through-a-declared-collection-or-search-result" id="workflow-page-through-a-declared-collection-or-search-result"></a>

This workflow applies independently to List and Search. For the business example, List uses `GET /v1/collections/businesses/records`; Search uses `POST /v1/collections/businesses/search`.

#### Preconditions <a href="#workflow-preconditions-3" id="workflow-preconditions-3"></a>

1. The contract declares the collection or search, accepted inputs, deterministic ordering with a unique tie breaker, page and resource limits, timeout outcome, cursor lifetime, and any selectable features.
2. The consumer has the required credentials and request context.

#### Interaction <a href="#workflow-interaction-3" id="workflow-interaction-3"></a>

1. The consumer sends the first request without a cursor, supplying the declared criteria and any supported ordering, page size, temporal selection, and field selection. GET List uses query parameters; POST Search carries temporal and field selection in its body.
2. The Registry validates the request and evaluates current access and disclosure policy. A current-state request returns the latest permitted Page without temporal metadata; an applied temporal selection echoes its context at Page level even when `items` is empty. Items use the same Record schema for the selected view.
3. For a non-null `nextCursor`, the consumer repeats the criteria, ordering, temporal selection, and effective field selection with that cursor. It may omit `pageSize` or repeat the effective size established by the first request.
4. The Registry reauthorises the continuation and verifies its cursor binding, including the Collection, query, view, temporal context, effective field set, effective page size, and effective purpose when required. An invalid, expired, or mismatched cursor produces the declared failure.
5. The consumer continues until `nextCursor` is `null`, including after short or empty Pages with a continuing cursor.

#### Outcomes and limits <a href="#workflow-outcomes-and-limits" id="workflow-outcomes-and-limits"></a>

- Every Page respects the effective size bound, every continuation advances, and request processing respects the declared resource limits or returns the declared timeout outcome. The page-size bound does not claim that backend work scales with the number of returned items.
- An evaluable List or Search with zero permitted matches, including one whose source matches are all filtered by policy, returns `200` with an empty `items` array. A source that cannot evaluate a requested temporal query returns `409 temporal-state-not-available`; it does not report an empty successful result.
- Live-data changes follow the published pagination and source-currency policy. Baseline pagination does not promise that one traversal exhaustively observes an unchanged result.
- When the operation declares `complete-traversal`, an unchanged source result and unchanged access conditions yield every permitted match exactly once before completion. An internal result window or limit that prevents this produces the declared failure instead of a completion signal.
- When the operation declares `snapshot-traversal`, the first request fixes source membership, ordering, and Record data at its documented evaluation point. Every Page still applies current authorisation. The service returns `400 invalid-cursor` if it cannot preserve the snapshot, and its contract documents snapshot reference and availability semantics.
- When supplied, `pageInfo.total` is the exact count of the full permitted query at its declared evaluation point. Live traversal evaluates it for the current Page; snapshot traversal uses the fixed source point and filters it through current rights.
- Revoked access applies to subsequent requests. A failed continuation allows the consumer to start a fresh request when permitted.

### Retrieve retained history <a href="#workflow-retrieve-retained-history" id="workflow-retrieve-retained-history"></a>

This workflow applies when Revision List or Revision Retrieve is selected.

1. The consumer inspects the contract's history view, revision ordering, retention, gap, schema-evolution, access, and purpose rules.
2. The consumer requests `GET /v1/collections/{collectionId}/records/{recordId}/revisions` and follows bounded continuation under current authorisation. Every continuation cursor remains bound to that parent `recordId`; replay under another parent returns `400 invalid-cursor`.
3. Each returned `RecordRevision.recordId` equals the parent path identifier and carries a source-backed `revisionId`, plus `recordedAt` only when the source supports it.
4. The consumer can retrieve one retained revision at `GET /v1/collections/{collectionId}/records/{recordId}/revisions/{revisionId}`.
5. Unknown or protected parent Records and revisions use the same `404 record-not-available`, without identifying which resource was unavailable. Only after these protection checks can authorised source inability return `409 history-not-available`. The service does not substitute current state or fabricate a revision.

Revision history and snapshot traversal answer different questions. History exposes source-distinguishable retained states; snapshot traversal holds one collection result stable while it is paged.

### Apply a required purpose <a href="#workflow-apply-a-required-purpose" id="workflow-apply-a-required-purpose"></a>

This workflow applies only to operations declaring `purpose-bound`.

1. The consumer obtains credentials or trusted authorisation context carrying one of the controlled purpose codes or absolute URIs allowed by the operation's `purpose` declaration.
2. The consumer invokes the operation without adding purpose to the URL or request body.
3. The service validates the trusted binding before disclosing Records and rejects missing, malformed, untrusted, or unallowed values.
4. The service binds the effective purpose to continuation, conditional validation, temporal and historical reads, and audit evidence.

Purpose is a declared request context. It is not proof of consent, institutional authority, or actual downstream use. Operations that do not declare `purpose-bound` continue to use their inherited authentication and authorisation contract without this additional requirement.

### Read a household and interpret its relationships <a href="#workflow-read-a-household-and-interpret-its-relationships" id="workflow-read-a-household-and-interpret-its-relationships"></a>

This workflow uses the [household OpenAPI](../api/examples/household-registry.openapi.yaml).

1. The consumer sends `GET /v1/collections/households/records/{recordId}` and receives a household containing its declared address and membership components.
2. The consumer interprets membership attributes as relationship facts. A `membershipId` identifies a component within that household.
3. The `individualRef` field schema fixes the target Individuals Registry, allowing the reference to omit `registryId`.
4. Where an individual read is offered, the consumer follows the field's declared target collection and operation binding through the target Registry's published service contract. The binding explains how to use the reference as input; the consumer follows the operation's access requirements.
5. The related read follows the target's authorisation and source-currency contract. An unavailable target leaves the household's membership facts unchanged.

A predefined household view may instead include permitted individual summaries, with declared fields, bounds, and source currency.

The [birth-registration OpenAPI](../api/examples/birth-registration.openapi.yaml) illustrates recorded parent details. `nameAtRegistration` belongs to the birth-registration Record, with a reference to the individual, which may be absent. Changes to the individual's current Record leave this recorded value unchanged; accepted corrections to the birth-registration source may update it.

### Direct and approval-based Write <a href="#workflow-direct-and-approval-based-write" id="workflow-direct-and-approval-based-write"></a>

The [Write binding](#write-write) describes direct mutations and separately selected change requests. An authorised direct operation commits its declared change and returns a committed result, or acknowledges actual asynchronous processing through an Operation resource. A submitted change request instead remains non-authoritative until the required review and application succeed. Reviewers act on the exact proposal version; commitment rechecks applicable source preconditions and permissions.

The binding's [non-normative domain examples](#write-non-normative-domain-examples) and the [example contracts](../resources/api-examples/README.md) show birth registration, household creation referencing existing individuals, compound household and individual creation, and members added later. Existing references, temporary request-local references, review outcomes, and result mappings have explicit meanings. The [Write test matrix](../resources/write-testing.md) separates artifact checks from required implementation evidence.
