---
description: Choices and guide refinements behind the first Consultation HTTP binding.
---

# Consultation design rationale

These choices explain the current Consultation HTTP binding. The requirements and [HTTP contract](api.yml) remain DRAFT.

## A practical shared read contract

The binding defines six independently selectable read capabilities. A concrete Registry or sector contract supplies Collection membership, domain fields, views, selectors, searches, source-history semantics, and access policy that map to its source operations.

| Choice | Rationale |
|---|---|
| Record containing `recordId` and `data` | A common identity and data boundary, with Registry and schema context supplied by the endpoint and published contract. |
| Conditional source metadata | Adapters expose available source revisions, lifecycle states, and provenance with documented meanings. |
| Exact Lookup | A declared unique selector supports alternate-key access to one Record. |
| Named, typed Search | Published criteria describe the searches supported by the source. |
| Reusable Search semantics | A named Search selects typed equality, range, set-membership, prefix, or domain-specific semantics independently, without a universal query language. |
| Schema-defined subobjects and relationships | Domain components, references, and related-data views retain their domain meanings. |
| Shared Record and Page shapes | Consumers use the same Record view across operations that declare the same Collection and view. Temporal selection wraps that view with `TemporalRecord` or `TemporalRecordPage`; materially different representations use distinct operations. |
| GET Retrieve/List and POST Lookup/Search | Established HTTP tooling, with selectors and search criteria carried in request bodies. |
| Versioned logical Collections | One API can expose several stable API groupings with explicit Registry, membership, and schema bindings, independently of tables or institutional Registry boundaries. |
| Collection action sub-resources `/lookup` and `/search` | Read actions have distinct routes at the Collection level, while Record Identifiers occupy the separate `/records/{recordId}` namespace. No action-name reservation is needed. |
| Live cursor pagination | Bounded response pages in a deterministic order, adaptable to source continuation mechanisms without claiming exhaustive baseline traversal. |
| Fixed effective page size | Stable page sizing supports adapters over source page or offset mechanisms. |
| Continuing short or empty Pages | Source processing can advance independently of the number of permitted results. Declared resource limits and a timeout outcome bound each request without requiring backend work to scale with page size. |
| Selectable operation features | Conditional caching, caller-selected fields, exhaustive traversal, source snapshots, recorded-time, effective-time, and purpose binding are advertised only where implemented and verified. |
| Selectable revision capabilities | Retained source revisions are exposed only where the source provides stable revision identity and declared retention, gap, order, schema-evolution, and parent-bound continuation semantics. |
| Selectable caller capability discovery | One bounded caller-filtered document points to the versioned contract and operation IDs without granting Record authority. Its capability and feature annotations are extensible; the normative linked operation extension remains closed. |

## Standards reused and alternatives considered

The contract uses [OpenAPI 3.1.2](https://spec.openapis.org/oas/v3.1.2.html), JSON Schema, [HTTP semantics](https://www.rfc-editor.org/rfc/rfc9110.html), and [RFC 9457 Problem Details](https://www.rfc-editor.org/rfc/rfc9457.html) with GovStack extensions. A `rel="describedby"` link follows the [JSON Schema rule](https://json-schema.org/draft/2020-12/json-schema-core#section-9.5.1.1) by identifying a schema for the complete retrieved representation.

The `x-govstack-digital-registries` operation extension has a `features` array that can be omitted. Its closed values include `conditional-read`, `field-selection`, `complete-traversal`, `snapshot-traversal`, `recorded-time`, `effective-time`, and `purpose-bound`; omission or an empty array means none. Capability constraints keep these promises meaningful: conditional reads apply only to Retrieve, complete and snapshot traversal apply only to List or Search, and snapshot traversal includes complete traversal. A purpose-bound operation also declares the trusted purpose binding and controlled values.

| Alternative | Decision |
|---|---|
| [JSON:API 1.1](https://jsonapi.org/format/1.1/) | Select a small Record envelope and the guide's Page convention. Lookup and Search still need domain-specific input contracts. |
| [HTTP QUERY, RFC 10008](https://www.rfc-editor.org/rfc/rfc10008.html) | Use GET and read-only POST for current tooling compatibility; reconsider QUERY with deployment evidence. |
| Common expression language | Select named, typed searches for the baseline. Domain capabilities may adopt an expression language. |
| One universal history model | Publish selectable Revision List, Revision Retrieve, recorded-time, and effective-time contracts separately. Sources need not support all four. |
| Client-supplied purpose parameter | Bind purpose through a trusted token claim or authorisation context. A request field would be an assertion, not a trusted authorisation input. |

## Resource paths, identity, and API composition

The API major version precedes resource Collections, following established conventions illustrated by [Google AIP-185](https://google.aip.dev/185). An OpenAPI server URL supplies the deployment root and any stable routing prefix. For example, server `https://example.org/registry` and path `/v1/collections/households/records/{recordId}` produce `https://example.org/registry/v1/collections/households/records/{recordId}`.

The reference binding constrains `CollectionId` to the example value `records`; concrete contracts use literal domain identifiers such as `businesses`, `households`, and `birth-registrations`. Each Collection declares its Registry association, membership, capabilities, and representation schemas. It is not required to match a database table, source module, governed dataset, or separate institutional Registry. Birth, marriage, and death registration Collections are illustrative choices rather than a mandated civil-registration legal scope. API-family classifications describe operations in metadata and contracts; they impose no URL prefix.

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

An operation declares one view and response schema. Audience policy can withhold non-required fields within that schema, and an operation declaring `field-selection` can let the caller select declared selectable top-level `data` fields without creating another view. Materially different field meanings or schemas remain separate operations or collection paths.

The resource structure supports later family bindings as follows. These are composition principles; each family's contract defines its operations.

| Area | Composition principle |
|---|---|
| Write | Retrieve and update can share a Record URI through different HTTP methods. Write defines its own input schemas and permissions; a permitted read view does not establish an update payload. Governed requests and asynchronous operations can have their own resources. |
| Provisioning and Notification | The API contract coordinates Record collection names with schema, subscription, and other supporting-resource paths. |
| Evidence and events | Record references retain Registry and Record identity. Evidence and event formats use the representations defined by their bindings. |
| Versioning | The major version applies to one API surface. Independently exposed APIs can version separately while retaining stable Registry and Record identity. |
| Protocol-specific families | Bindings such as credential issuance or identity federation follow their protocols' endpoint and versioning conventions. |

## Relationship identity, snapshots, and completeness

The [Core representation rules](registry-core-model.md#structured-values-and-references) distinguish owned components, Record references, and related-data views across API families. The [household contract](../api/examples/household-registry.openapi.yaml) embeds membership attributes and references individual Records. The [birth-registration contract](../api/examples/birth-registration.openapi.yaml) owns recorded parent details, with individual references that may be absent.

Each view declares array bounds and completeness for the permitted representation. A complete array exceeding its bound follows the declared failure contract. A separately paginated relationship collection has its own published operation.

Baseline List and Search are live and make no exhaustive or snapshot claim. `complete-traversal` adds exactly-once exhaustive traversal when source data and access conditions remain unchanged. `snapshot-traversal` additionally fixes source membership, order, and Record data at the first request's documented evaluation point while every Page applies current authorisation. It declares snapshot reference and availability semantics and fails rather than silently weakening to live traversal when the retained snapshot is unavailable.

Snapshot traversal is not a history model. Selectable revision capabilities expose source-distinguishable retained states with declared order, retention, gaps, schema evolution, and pagination bound to the parent Record Identifier. A Revision List cursor issued for parent A fails with `400 invalid-cursor` when replayed under parent B. Selectable `recorded-time` selects the source knowledge accepted by a date-time cutoff; `effective-time` selects information the source declares applicable at a date or instant. Selected responses use `TemporalRecord` or `TemporalRecordPage`; the baseline schemas do not publish temporal metadata. An evaluable Search with zero permitted matches returns `200` empty, a proven absent item returns `404`, and source inability to evaluate requested history returns `409 temporal-state-not-available`. Neither event occurrence nor registration date becomes effective time without an explicit source definition.

The selectable `GET /v1/capabilities` response is a bounded caller-filtered index with at most 64 Collections and 16 operations per Collection. Each operation requires a version-specific HTTPS contract, operation ID, capability annotation, and view, and can list `readableFields`, selectors, named searches, feature annotations, and purpose requirements. `readableFields` states current readable output metadata and does not imply support for the `field-selection` input. For forward compatibility, clients skip entries with unknown capability annotations and ignore unknown advisory feature annotations; unknown metadata never grants authority. The linked normative operation extension remains closed for its contract version. The document does not duplicate complete schemas or promise access to an individual Record. If the authorised description exceeds a schema bound, the service returns its declared explicit error instead of truncating entries or silently returning an empty array. `collections: []` means that no operation is visible to the caller.

Purpose-bound Record and history operations take the effective purpose only from a trusted access-token claim or authorisation context, using controlled codes or absolute URIs. Purpose participates in authorisation context, cursor and validator binding, and audit. Caller capability discovery has no purpose feature or request input; it can filter under a verified purpose already present in trusted context. Declared purpose remains distinct from consent, institutional authority, and actual downstream use, so purpose binding stays selectable rather than changing the inherited security contract for every operation.

## Explicit cross-BB guide refinements

These general refinements were introduced in guide and ruleset `0.2.0-draft` and carried into `0.3.0-draft`; the guide's `draft-changes.md` records their details. Shared schema artifacts remain independently versioned at `0.1.0-draft`.

| Guide area | General refinement | Registry binding choice |
|---|---|---|
| §10.1, identifiers | Stable source-owned keys with documented uniqueness scope. | Non-personal `recordId` unique within its Registry. |
| §9.8, extensibility | Extensible response resources, strict operation arguments, and schema-defined nesting. | Closed Lookup/Search inputs and additive response fields. |
| §2.6 and §5.1, deployment roots and versions | Major version in resource paths; shared API surfaces can expose multiple Collections and families. | Deployment root plus `/v1/collections/businesses`, `/v1/collections/households`, or another declared Collection. |
| §5.4, shallow nesting | Resource paths should normally stay within two levels after `/v1`. | Deliberate documented SHOULD deviation for the explicit Collection, Record, and Revision hierarchy; no approved exception is claimed. |
| §5.3 and §5.8, custom operations | Action sub-resources for custom operations, with kebab-case segments; action names sharing an identifier namespace are excluded from that namespace. | `/v1/collections/records/lookup` and `/v1/collections/records/search`, separate from the `/records/{recordId}` namespace. |
| §6.6, body-based reads | Exact single-result POST Lookup alongside collection Search. | Typed request bodies and synchronous `200` results. |
| §12, pagination | Declared page-size and resource policies, advancing short or empty Pages, and explicit embedded-array completeness. | Fixed effective size, integrity-protected context-bound cursors, exact totals where supplied, and separately declared complete or snapshot traversal. |
| §10, domain schemas | Explicit ownership of adopted domain schemas and applicable inherited requirements. | A data schema and documented field meanings for each view. |
| §2.3 and §3.3, historical artifacts | Explicit separation of legacy contracts from current surfaces. | Previous generated CRUD contracts retained as migration evidence. |
| §4.6 and §20, draft validation | Draft requirement mappings and artifact checks distinguished from active conformance coverage. | DRAFT read coverage and contract/example checks. |

## Verification and follow-up boundary

[Testing](testing.md) separates artifact validation from deployed implementation evidence. The [concrete OpenAPI examples](api-examples/README.md) support contract review. Implementation trials over registries with different source models will provide evidence about Collection mapping, schema publication, history availability, temporal interpretation, purpose binding, declared request limits, continuation, and the cost of selectable guarantees.
