---
description: Draft verification of mandatory Registry discovery and selected capabilities.
---

# 11 Testing

## 11.1 Test maturity

The scenarios below define verification intent for the [draft requirements](04-conformance.md#41-requirement-maturity). The [Consultation artifact checks](../api/README.md#validation) validate OpenAPI documents and schema fixtures. Implementation conformance requires separate evaluation of a deployed Registry; an executable suite is pending. Legacy Cucumber tests under `test/openAPI` remain migration evidence for the previous generated CRUD interface.

## 11.2 Applicability and required fixtures

Verification starts with an inventory of the Registry BB capabilities and services the implementation exposes to each intended metadata audience. Every evaluation covers Registry identity, authoritative scope, specification-version metadata, and service discovery. Capability-specific verification follows the implementation's selected capabilities and the [conformance model](04-conformance.md#43-conformance-model).

Common Record representation requirements are evaluated through each implemented operation that returns Records, using that operation to obtain the fixtures. Identifier lifecycle evidence applies wherever the implementation assigns or maintains Record Identifiers.

An implementation being evaluated provides non-production fixtures according to the following applicability rules:

| Fixture or evidence | Required when |
|---|---|
| Machine-readable Registry metadata, the inventory of exposed Registry BB services, and their linked machine-readable operational contracts | Every evaluation. |
| Two distinct current Records in the same Registry, with expected scoped identity, declared schema, and field meanings | An implemented operation returns Record representations. |
| Record fixtures covering each exposed lifecycle state | An implemented operation returns Record representations in those states. |
| Identifier policy and stability/non-reassignment evidence across source changes and retirement where supported | The implementation assigns or maintains Record Identifiers. |
| Source revision, lifecycle, and provenance evidence for metadata actually exposed | The operation or selected profile exposes or requires this metadata. |
| Consumer contexts and expected permitted representations | An implemented operation returns Record representations. |
| The same Record accessible to consumers with different disclosure rights | The applicable policy provides different disclosure entitlements. |
| An unknown Record Identifier and a known Record outside the selected collection where applicable | Retrieve is selected. |
| Distinct Records in different collections | A Registry exposes multiple collections. |
| One Record available through multiple collections or views | Collections overlap or expose distinct views of one Record. |
| Known, unknown, invalid, and composite selector inputs where supported; a simulated source uniqueness failure | Lookup is selected. |
| A protected and an unknown identifier or selector for the same consumer context | Retrieve or Lookup is selected and the applicable policy protects Record existence. |
| Zero-, one-, and multi-result collections; typed search criteria and invalid inputs; duplicate sort values where applicable | List or Search is selected, using fixtures relevant to each selected operation. |
| Continuations covering completion, mismatch, expiry, and access changes; a short or empty advancing page where supported | List or Search is selected. |
| Nested components, same-target and mixed-target references, and collection-boundary fixtures | A selected view exposes subobjects, references, or embedded collections. |
| Recorded related details and a separately changed current target Record; a parent without an individual reference where supported | A selected view exposes recorded related details or optional references. |

Use synthetic fixtures and record the applicability rationale for each omitted conditional fixture.

## 11.3 Requirement traceability

| Requirement | Applicability | Verification item | Expected result |
|---|---|---|---|
| `fr-core#req-1` | Every implementation | Access machine-readable Registry metadata as an intended consumer and inspect identifier evidence | Globally unique and stable Registry Identifier, Registry name, Registry Authority, authoritative scope statement, and Digital Registries specification-version reference are present; the publication URI and access conditions are available to intended consumers. |
| `fr-core#req-2` | Each implemented operation returning Records | Obtain two distinct Record representations through that operation; compare collections where supported | Each representation includes a different Record Identifier and has unambiguous Registry context; each identifier pair is unique across the Registry, including its collections, without requiring repeated Registry fields. |
| `fr-core#req-3` | Implementations assigning or maintaining Record Identifiers | Inspect the identifier policy and lifecycle evidence | A Record Identifier remains unchanged across revisions and lifecycle states, is not shared, and is not reassigned after retirement. |
| `fr-core#req-4` | Each implemented operation returning Records | Validate a returned representation | The binding identifies the format and versioned resolvable schema, field meanings are documented, and validation succeeds. A separate formal semantic model is checked only when declared. Nested component and reference meanings, target Registry scope, related-read bindings where offered, and collection completeness are unambiguous. |
| `fr-core#req-5` | Source revision or lifecycle metadata is exposed or required by the selected profile | Obtain relevant Record fixtures and source evidence | Provided metadata has documented meaning, matches the source, and is not fabricated from an ETag or adapter fetch. Absence is valid for a profile that does not require it. |
| `fr-core#req-6` | Each implemented operation returning Records, with conditional checks for extra provenance | Obtain a known accessible Record and resolve its Registry context | Registry Authority resolves through metadata. Any additional provenance has documented semantics and matches source evidence; a recording timestamp is not fabricated from fetch time. |
| `fr-core#req-7` | Every implementation | Request `/.well-known/api-catalog` at each HTTP service origin, follow its `service-meta` link to the metadata document, and compare services exposed to each intended metadata audience with their published discovery metadata and linked operational contracts | Every exposed Registry BB service is identified, associated with its Registry, and declares valid API-family concepts, an endpoint URL, and a resolvable machine-readable operational contract. The contract describes the advertised endpoint and operations from each declared family; declarations reflect currently available services. |
| `fr-core#req-8` | Implementations selecting Consultation capabilities | Validate the `x-govstack-digital-registries` extension of every selected Consultation operation against its schema and compare it with the published metadata and the operation path | Every such operation declares a Registry Identifier present in the metadata, the collection segment of its path, its capability, and a view; operations sharing a collection and view use one Record schema. |
| `fr-consultation#req-1` | Retrieve selected | Retrieve a known accessible Record and a Record outside the collection where applicable | A current permitted collection member returns its required Record context; a Record outside the collection returns `record-not-available`. |
| `fr-consultation#req-2` | Every selected Consultation read | Invoke fixtures under applicable consumer contexts; compare responses where entitlements differ | Each response contains only the projection permitted to that consumer, validates against its schema, and does not expose omitted values through related references, embedded fields, errors, or collection metadata. |
| `fr-consultation#req-3` | Retrieve or Lookup selected and policy protects Record existence | Resolve unknown and protected fixtures as the same consumer through each selected operation | Status or protocol outcome, security-relevant response metadata, stable error type, response structure, and non-Record-specific values match; any differing trace or correlation values are independent of Record existence; neither response contains Record-specific data. |
| `fr-consultation#req-4` | Lookup selected | Exercise each declared exact selector with known, unknown, invalid, and ambiguous source fixtures | One collection member resolves uniquely within the selector's declared scope; missing components and unknown inputs fail; no permitted collection match gives the declared unresolved outcome; multiple matches never return an arbitrary Record. |
| `fr-consultation#req-5` | List selected | List declared collections, including zero and one result and unsupported inputs | Results retain the Page shape, satisfy membership and disclosure, respect the page bound and declared order, and reject unsupported filters or sort. |
| `fr-consultation#req-6` | Search selected | Execute each declared search with valid, empty-result, and invalid criteria | Matching permitted Records use the same declared view; empty results retain the Page shape; unsupported searches and fields fail. |
| `fr-consultation#req-7` | List or Search selected | Traverse unchanged fixtures; test changed collection or criteria, expiry, page-size mismatch, and authorization changes | Traversal advances to a null cursor, preserves collection, query, and view, respects the fixed effective size, reauthorizes, and never silently restarts. Optional totals match the full permitted query at evaluation. |

The abbreviated references in this table use the full `govstack-bb-digital-registries` namespaces defined under [Registry Core](05-api-families/registry-core.md#registry-core-functional-requirements) and [Consultation](05-api-families/consultation.md#retrieve-functional-requirements).

## 11.4 Behaviour scenarios

Discovery is verified through `fr-core#req-7` in the traceability table: every exposed service is reachable through the linkset and the metadata document, a family label does not by itself establish that any particular operation exists, and a service without a machine-readable contract fails the requirement. Read scenarios apply to their selected capabilities. Disclosure differences, protected existence, exposed metadata, and bounded-scan behavior additionally require the corresponding conditions in section 11.2.

The following cases apply to the selected read capabilities. Run them against each operation and view to which their fixtures apply.

| Case | Exercise | Expected evidence |
|---|---|---|
| Current Retrieve | Read a known accessible Record, including an exposed inactive state. | Stable identifier, valid permitted representation, declared source currency, and an unchanged source Record. |
| Collection scope | Retrieve a known Record through a collection that excludes it. | The same `record-not-available` outcome as an unknown identifier. |
| Identity across collections | Read one Record through multiple collections or views, and compare distinct Records across collections in the same Registry. | The same Record retains its identifier; distinct Records have different identifiers within the Registry. |
| Collection methods | Retrieve Records whose identifiers are `lookup`, `lookups`, or `search`, where the identifier syntax permits them, and invoke the collection's `:lookup` or `:search` operation. | Item retrieval and collection methods route independently. |
| Disclosure | Read the same Record under different disclosure entitlements. | Each response matches the permitted fields and metadata for its consumer. |
| Protected existence | Retrieve and Look up unknown and protected fixtures as the same consumer. | Both produce the same contract-defined unresolved outcome and security-relevant content; independently generated trace values may differ. |
| Exact Lookup | Submit known, unknown, incomplete, incorrectly typed, and unsupported selector inputs, including composite keys where declared. | One permitted Record for a valid unique match; declared unresolved or validation errors otherwise. |
| Selector uniqueness failure | Supply source data with multiple matches for a unique selector. | The declared failure, with protected-existence policy applied and no arbitrary Record selected. |
| Empty and single-result collections | List and Search fixtures containing zero and one permitted match. | The Page shape is retained; completed results have `nextCursor: null`. |
| Complete traversal | Traverse an unchanged collection with duplicate primary sort values. | Every matching permitted Record appears once in the declared order; every Page respects the size bound and the last cursor is null. |
| Bounded source scan | Process a bounded source region with no permitted matches and unprocessed source state remaining. | A short or empty Page may carry a cursor that advances source processing. |
| Cursor binding | Change collection, criteria, search, ordering, view, or effective page size while reusing a cursor. | The invalid-cursor outcome, with no silent restart. |
| Continuation size | Omit `pageSize`, then repeat the original effective size on another continuation. | Both retain the bound size. |
| Cursor validity | Submit malformed, tampered, and expired cursors. | The invalid-cursor outcome. |
| Authorization change | Revoke access between Pages. | Subsequent requests enforce current authorization before releasing results. |
| Total | Compare any reported `total` on a later Page with the full permitted query. | An exact count at that Page's evaluation time, including matches before the cursor. |
| Live source changes | Insert, update, and remove source Records between Pages. | Observed results match the published currency and pagination policy. |
| Query disclosure | Compare unknown and protected-only query fixtures where match existence is protected. | Items, counts, and continuation patterns preserve the disclosure policy. |
| Unsupported input | Submit undeclared Search names, criteria, List parameters, and sort choices. | The declared validation error. |

Relationship cases apply to views exposing the corresponding shapes. The [household](../api/examples/household-registry.openapi.yaml) and [birth-registration](../api/examples/birth-registration.openapi.yaml) contracts provide concrete examples; their [fixtures](../api/examples/relationship-exchanges.json) cover schema validation.

| Case | Exercise | Expected evidence |
|---|---|---|
| Nested components | Read a household with an address and memberships. | Components validate with their declared field meanings and local identifier scope. |
| Fixed-target reference | Validate an individual reference with omitted, matching, and conflicting `registryId`. | Omitted or matching values resolve to the schema-declared Registry; a conflicting value fails validation. |
| Mixed-target reference | Validate a reference whose field allows multiple Registries. | The reference identifies its target Registry; omission fails validation. |
| Related read binding | Follow a reference for which the contract offers a related read. | The declared target collection, operation contract, and input mapping determine the request without parsing the opaque Record Identifier. |
| Recorded parent details | Change the individual's current name while leaving the birth registration unchanged. | The birth registration retains `nameAtRegistration`; a permitted parent component may omit its individual reference. |
| Complete array boundary | Exceed the response bound of a view declaring a complete memberships array. | The declared failure, with no truncated array presented as complete. |
| Related disclosure | Read a household with restricted individual or relationship fields. | References, embedded values, omissions, arrays, and completeness metadata satisfy the consumer's disclosure policy. |

## 11.5 Evidence retained for audit

Retain the specification version, selected capabilities, exposed services, published metadata and contracts, and a requirement traceability report with pass, fail, or not-applicable results and applicability rationales. Applicable evidence includes fixtures, requests and responses, schema-validation results, source mapping and currency, pagination and disclosure outcomes, and identifier lifecycle evidence.

Record artifact validation separately from deployed implementation results.
