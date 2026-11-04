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
    contract: resources/write-binding.md#published-write-contract
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
    contract: resources/write-binding.md#atomicity-and-compound-changes
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
    contract: resources/write-binding.md#retries-and-idempotency
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
    contract: resources/write-binding.md#concurrency-and-commit-guards
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
    contract: resources/write-binding.md#authority-and-purpose
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
    contract: resources/write-binding.md#trusted-context-and-client-input
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
    contract: resources/write-binding.md#acknowledgement-provenance-and-audit
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
    contract: resources/write-binding.md#protected-resources
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
    contract: resources/write-binding.md#preview-and-authoritative-state
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
    contract: resources/write-binding.md#change-request-lifecycle
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
    contract: resources/write-binding.md#change-request-lifecycle
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
    contract: resources/write-binding.md#application-time-revalidation
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
    contract: resources/write-binding.md#http-outcomes
    applies_when: [write-create, write-update, write-transition, write-change-requests]
    statement: A selected Write operation returns `201 Created` only when it creates the identified resource, including a newly submitted Change Request, and returns `202 Accepted` only when it accepts separately identifiable asynchronous work whose Operation status can be retrieved without implying a committed Record change or approved request.
    documentation: |
      Purpose: A consumer can distinguish a created resource from queued work and from an authoritative commit.
      Prerequisite: Every asynchronous path publishes an Operation representation, status retrieval, terminal outcomes, and retention policy.
      Constraint: A `202` acknowledgement is not success of the requested mutation. A Change Request created synchronously uses `201` even though its later review or application can be asynchronous. A direct Write can use a synchronous successful outcome defined by its contract when the authoritative commit is complete.
      Verification: Exercise synchronous creation, Change Request submission, asynchronous acceptance, processing success, processing failure, and status expiry. Correlate each response with the resource or Operation and authoritative state.
    test: resources/write-testing.md#write-18
  - id:
    status: DRAFT
    level: REQUIRED
    observability: OBSERVABLE
    mutability: EXTENSIBLE
    interaction: PROTOCOL
    contract: resources/write-binding.md#change-request-listing
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
    contract: resources/registry-core-model.md#domain-semantics-and-extensions
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

# Consultation workflow (informative)

The requirement front matter defines conformance. In a consultation workflow, an implementation selects one or more consultation options. A consumer uses [Retrieve](../resources/consultation-binding.md#retrieve) for a known Record Identifier, [Lookup](../resources/consultation-binding.md#lookup) for a declared exact selector, [List](../resources/consultation-binding.md#list) for an ordered collection, [Search](../resources/consultation-binding.md#search) for declared typed criteria, [Revision List](../resources/consultation-binding.md#revision-list) for the retained revisions of one Record, or [Revision Retrieve](../resources/consultation-binding.md#revision-retrieve) for one identified retained revision. List, Search, and Revision List share the [pagination model](../resources/consultation-binding.md#pagination).

An operation can also declare [selectable read features](../resources/consultation-binding.md#selectable-read-features) in its `features` array: conditional reads, field selection, complete or snapshot traversal, recorded or effective time selection, and purpose binding. Each declared feature adds its own requirements to the claim. Features, and the selectable caller capability discovery operation, do not by themselves satisfy the minimum Registry service choice.

All selected operations use the Registry identity, schemas, field meanings, disclosure policy, and source semantics described in the [Registry Core model](../resources/registry-core-model.md#domain-semantics-and-extensions). The source Registry remains authoritative; consultation observes information and does not change the source Record.
