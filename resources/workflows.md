---
description: Registry service discovery, latest and historical Record reads, exact lookup, and declared Collection pagination guarantees.
---

# Workflows

## Discover Registry services and their contracts

This workflow applies to every Registry BB implementation. The publisher serves the Registry metadata document and locates it, with each contract, through the RFC 9727 `/.well-known/api-catalog` linkset at the API origin.

### Preconditions

1. The consumer knows the API origin or has a configured metadata document URI.
2. The consumer has any access needed to read the metadata and linked contracts.
3. The publisher provides the Registry metadata and service discovery required by Registry Core.

### Interaction

1. The consumer requests `/.well-known/api-catalog` at the API origin, follows its `service-meta` link to the Registry metadata document, and selects the Registry by its stable identifier.
2. The consumer inspects its authority, authoritative scope statement, and referenced Digital Registries specification version.
3. The consumer follows the Registry's service associations and reads each service's identifier, API-family labels, endpoint URL, and operational-contract reference for the services available to that consumer's audience.
4. The consumer follows the operational contract to determine the logical Collections, the Registry context declared on each operation, exact operations, selectable features, named searches, inputs, outputs, limits, temporal and purpose requirements, and access requirements. For HTTP APIs, this is an OpenAPI description unless the applicable binding defines an established protocol-native description.
5. When the service offers caller capability discovery, the consumer can request `GET /v1/capabilities` to obtain a bounded, caller-filtered advisory view of authorised Collection operations and their required views, plus readable fields, selectors, searches, features, and purpose requirements. Filtering uses current trusted context, including a verified purpose when present, and can omit operations whose required purpose is absent. Discovery creates no new purpose input. The consumer still follows the versioned contract and does not treat this document as authority for any Record. If the caller-available description exceeds a declared bound, the service fails explicitly rather than truncating or silently omitting it.
6. The consumer selects a suitable operation, or determines that the required operation is unavailable.

### Outcomes

The linked contract, not the family label, tells the consumer which operations exist. Discovery is not satisfied when an exposed service is missing from the Registry description or lacks its identifier, valid family labels, endpoint, or machine-readable contract, or when the origin serves no `/.well-known/api-catalog` linkset with a `service-meta` link to the metadata document.

### Postconditions

- The consumer can distinguish the governed Registry, its authority, and its technical services.
- The consumer knows which operations are available from each service's operational contract.
- Family labels classify the service's operations. Selected operation options follow the [draft conformance model](conformance.md#draft-conformance-model).

## Retrieve a permitted Record representation

This workflow applies to implementations selecting Retrieve. The [HTTP binding](../api/openapi.yaml) defines request and response details.

### Preconditions

1. The published service contract exposes Retrieve and identifies its Registry, collection membership, representation schema, and any selectable features.
2. The consumer has the credentials and request context required by the deployment.

### Interaction

1. The consumer sends a request to the declared item path, such as `GET /v1/collections/businesses/records/{recordId}`, with a Record Identifier within the Registry. When the operation declares `field-selection`, the consumer may also request declared selectable top-level `data` fields with `fields`. When a temporal feature is declared, the consumer can explicitly supply `recordedAsOf` or `effectiveAt`; omission requests the latest representation.
2. The Registry evaluates authentication, access, and disclosure policy.
3. The Registry resolves the latest or explicitly selected source-backed Record state within the Collection and constructs its permitted baseline `Record` or selected `TemporalRecord` representation. Latest Records may include inactive Records.
4. The Registry returns that representation or the declared unsuccessful outcome.

### Outcomes

| Condition | Observable outcome |
|---|---|
| Latest Record state is accessible without temporal selection | The latest permitted representation is returned without temporal metadata. |
| Explicitly selected Record state is accessible | A `TemporalRecord` echoing the applied temporal context is returned. |
| Consumer has narrower disclosure rights | The returned representation satisfies both disclosure policy and its schema. |
| Identifier is unknown, belongs to a Record outside the collection, or has protected existence | The same `record-not-available` outcome is returned. |
| Source proves no Record exists at the selected temporal coordinates | `404 record-not-available`, subject to protected-existence handling. |
| Authorised source cannot evaluate the selected temporal state | `409 temporal-state-not-available`; current state is not substituted. |
| Operation declares `conditional-read` and an authorised `If-None-Match` validator matches | A bodyless `304` with the selected representation's ETag is returned. |

### Postconditions

- The source Record is unchanged.
- The returned identifier matches the requested identifier.
- Registry, schema, and authority context are unambiguous; any additional source metadata follows the published contract.
- Field selection retains `recordId` and `data`, uses the operation's one declared view schema, and cannot widen disclosure. Unsupported fields produce the declared validation error.

## Look up a Record using an exact selector

This workflow applies to implementations selecting Lookup.

### Preconditions

1. The contract exposes a Lookup operation, such as `POST /v1/collections/businesses/lookup`, and declares the Collection, selectable features, and selector's typed components, comparison rules, and uniqueness scope.
2. The consumer has the required credentials and request context.

### Interaction

1. The consumer sends `{selector, values}` using the declared schema. A composite selector supplies every key component. When the operation declares `field-selection`, the body may also carry a `fields` array of declared selectable top-level `data` fields. A declared temporal selection is carried in the body `temporal` object.
2. The Registry validates the input and evaluates access and disclosure policy.
3. The Registry resolves the selector within its declared scope, checks uniqueness, and applies collection membership.
4. One permitted match returns the common Record representation. Other outcomes follow the contract, including protected-existence handling and source uniqueness failures.

### Postconditions

- The source Record is unchanged.
- A successful Lookup returns the same Record schema and field meanings as other reads of that view.
- Multiple source matches fail without selecting an arbitrary Record.

## Page through a declared collection or search result

This workflow applies independently to List and Search. For the business example, List uses `GET /v1/collections/businesses/records`; Search uses `POST /v1/collections/businesses/search`.

### Preconditions

1. The contract declares the collection or search, accepted inputs, deterministic ordering with a unique tie breaker, page and resource limits, timeout outcome, cursor lifetime, and any selectable features.
2. The consumer has the required credentials and request context.

### Interaction

1. The consumer sends the first request without a cursor, supplying the declared criteria and any supported ordering, page size, temporal selection, and field selection. GET List uses query parameters; POST Search carries temporal and field selection in its body.
2. The Registry validates the request and evaluates current access and disclosure policy. A current-state request returns the latest permitted Page without temporal metadata; an applied temporal selection echoes its context at Page level even when `items` is empty. Items use the same Record schema for the selected view.
3. For a non-null `nextCursor`, the consumer repeats the criteria, ordering, temporal selection, and effective field selection with that cursor. It may omit `pageSize` or repeat the effective size established by the first request.
4. The Registry reauthorises the continuation and verifies its cursor binding, including the Collection, query, view, temporal context, effective field set, effective page size, and effective purpose when required. An invalid, expired, or mismatched cursor produces the declared failure.
5. The consumer continues until `nextCursor` is `null`, including after short or empty Pages with a continuing cursor.

### Outcomes and limits

- Every Page respects the effective size bound, every continuation advances, and request processing respects the declared resource limits or returns the declared timeout outcome. The page-size bound does not claim that backend work scales with the number of returned items.
- An evaluable List or Search with zero permitted matches, including one whose source matches are all filtered by policy, returns `200` with an empty `items` array. A source that cannot evaluate a requested temporal query returns `409 temporal-state-not-available`; it does not report an empty successful result.
- Live-data changes follow the published pagination and source-currency policy. Baseline pagination does not promise that one traversal exhaustively observes an unchanged result.
- When the operation declares `complete-traversal`, an unchanged source result and unchanged access conditions yield every permitted match exactly once before completion. An internal result window or limit that prevents this produces the declared failure instead of a completion signal.
- When the operation declares `snapshot-traversal`, the first request fixes source membership, ordering, and Record data at its documented evaluation point. Every Page still applies current authorisation. The service returns `400 invalid-cursor` if it cannot preserve the snapshot, and its contract documents snapshot reference and availability semantics.
- When supplied, `pageInfo.total` is the exact count of the full permitted query at its declared evaluation point. Live traversal evaluates it for the current Page; snapshot traversal uses the fixed source point and filters it through current rights.
- Revoked access applies to subsequent requests. A failed continuation allows the consumer to start a fresh request when permitted.

## Retrieve retained history

This workflow applies when Revision List or Revision Retrieve is selected.

1. The consumer inspects the contract's history view, revision ordering, retention, gap, schema-evolution, access, and purpose rules.
2. The consumer requests `GET /v1/collections/{collectionId}/records/{recordId}/revisions` and follows bounded continuation under current authorisation. Every continuation cursor remains bound to that parent `recordId`; replay under another parent returns `400 invalid-cursor`.
3. Each returned `RecordRevision.recordId` equals the parent path identifier and carries a source-backed `revisionId`, plus `recordedAt` only when the source supports it.
4. The consumer can retrieve one retained revision at `GET /v1/collections/{collectionId}/records/{recordId}/revisions/{revisionId}`.
5. Unknown or protected parent Records and revisions use the same `404 record-not-available`, without identifying which resource was unavailable. Only after these protection checks can authorised source inability return `409 history-not-available`. The service does not substitute current state or fabricate a revision.

Revision history and snapshot traversal answer different questions. History exposes source-distinguishable retained states; snapshot traversal holds one collection result stable while it is paged.

## Apply a required purpose

This workflow applies only to operations declaring `purpose-bound`.

1. The consumer obtains credentials or trusted authorisation context carrying one of the controlled purpose codes or absolute URIs allowed by the operation's `purpose` declaration.
2. The consumer invokes the operation without adding purpose to the URL or request body.
3. The service validates the trusted binding before disclosing Records and rejects missing, malformed, untrusted, or unallowed values.
4. The service binds the effective purpose to continuation, conditional validation, temporal and historical reads, and audit evidence.

Purpose is a declared request context. It is not proof of consent, institutional authority, or actual downstream use. Operations that do not declare `purpose-bound` continue to use their inherited authentication and authorisation contract without this additional requirement.

## Read a household and interpret its relationships

This workflow uses the [household OpenAPI](../api/examples/household-registry.openapi.yaml).

1. The consumer sends `GET /v1/collections/households/records/{recordId}` and receives a household containing its declared address and membership components.
2. The consumer interprets membership attributes as relationship facts. A `membershipId` identifies a component within that household.
3. The `individualRef` field schema fixes the target Individuals Registry, allowing the reference to omit `registryId`.
4. Where an individual read is offered, the consumer follows the field's declared target collection and operation binding through the target Registry's published service contract. The binding explains how to use the reference as input; the consumer follows the operation's access requirements.
5. The related read follows the target's authorisation and source-currency contract. An unavailable target leaves the household's membership facts unchanged.

A predefined household view may instead include permitted individual summaries, with declared fields, bounds, and source currency.

The [birth-registration OpenAPI](../api/examples/birth-registration.openapi.yaml) illustrates recorded parent details. `nameAtRegistration` belongs to the birth-registration Record, with a reference to the individual, which may be absent. Changes to the individual's current Record leave this recorded value unchanged; accepted corrections to the birth-registration source may update it.

## Direct and approval-based Write

The [Write binding](write-binding.md) describes direct mutations and separately selected change requests. An authorised direct operation commits its declared change and returns a committed result, or acknowledges actual asynchronous processing through an Operation resource. A submitted change request instead remains non-authoritative until the required review and application succeed. Reviewers act on the exact proposal version; commitment rechecks applicable source preconditions and permissions.

The binding's [non-normative domain examples](write-binding.md#non-normative-domain-examples) and the [example contracts](../api/examples/README.md) show birth registration, household creation referencing existing individuals, compound household and individual creation, and members added later. Existing references, temporary request-local references, review outcomes, and result mappings have explicit meanings. The [Write test matrix](write-testing.md) separates artifact checks from required implementation evidence.
