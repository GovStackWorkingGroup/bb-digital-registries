---
description: Choices and guide refinements behind the first Consultation HTTP binding.
---

# Read API design decisions

Status: accepted direction for the September 2026 draft. The requirements and [HTTP contract](../../api/openapi.yaml) remain DRAFT.

## A practical shared read contract

The binding defines four independently selectable read capabilities. A concrete Registry or sector contract supplies domain fields, views, selectors, and searches that map to its source operations.

| Choice | Rationale |
|---|---|
| Record containing `recordId` and `data` | A common identity and data boundary, with Registry and schema context supplied by the endpoint and published contract. |
| Conditional source metadata | Adapters expose available source revisions, lifecycle states, and provenance with documented meanings. |
| Exact Lookup | A declared unique selector supports alternate-key access to one Record. |
| Named, typed Search | Published criteria describe the searches supported by the source. |
| Schema-defined subobjects and relationships | Domain components, references, and related-data views retain their domain meanings. |
| Shared Record and Page shapes | Consumers use the same Record view across selected operations. |
| GET Retrieve/List and POST Lookup/Search | Established HTTP tooling, with selectors and search criteria carried in request bodies. |
| Versioned, typed collections | One API can expose several domain collections with explicit Registry and schema bindings. |
| Collection methods `:lookup` and `:search` | Read actions have distinct routes while all valid Record Identifiers remain addressable. |
| Live cursor pagination | Bounded traversal in a deterministic order, adaptable to source continuation mechanisms. |
| Fixed effective page size | Stable page sizing supports adapters over source page or offset mechanisms. |
| Continuing short or empty Pages | Bounded source processing can advance independently of the number of permitted results. |

## Standards reused and alternatives considered

The contract uses [OpenAPI 3.1.2](https://spec.openapis.org/oas/v3.1.2.html), JSON Schema, [HTTP semantics](https://www.rfc-editor.org/rfc/rfc9110.html), and [RFC 9457 Problem Details](https://www.rfc-editor.org/rfc/rfc9457.html) with GovStack extensions. A `rel="describedby"` link follows the [JSON Schema rule](https://json-schema.org/draft/2020-12/json-schema-core#section-9.5.1.1) by identifying a schema for the complete retrieved representation.

| Alternative | Decision |
|---|---|
| [JSON:API 1.1](https://jsonapi.org/format/1.1/) | Select a small Record envelope and the guide's Page convention. Lookup and Search still need domain-specific input contracts. |
| [HTTP QUERY, RFC 10008](https://www.rfc-editor.org/rfc/rfc10008.html) | Use GET and read-only POST for current tooling compatibility; reconsider QUERY with deployment evidence. |
| Common expression language | Select named, typed searches for the baseline. Domain capabilities may adopt an expression language. |

## Resource paths, identity, and API composition

The API major version precedes resource collections, following established conventions illustrated by [Google AIP-185](https://google.aip.dev/185). An OpenAPI server URL supplies the deployment root and any stable routing prefix. For example, server `https://example.org/registry` and path `/v1/households/{recordId}` produce `https://example.org/registry/v1/households/{recordId}`.

The reference binding uses the collection name `records`; concrete contracts publish domain names such as `businesses`, `individuals`, `households`, and `land-parcels`. Each collection declares its Registry association, membership, capabilities, and representation schemas. API-family classifications describe operations in metadata and contracts; they impose no URL prefix.

Lookup and Search use the collection custom-method notation from [Google AIP-136](https://google.aip.dev/136):

```http
GET /v1/households/{recordId}
GET /v1/households
POST /v1/households:lookup
POST /v1/households:search
```

This keeps collection methods distinct from item paths: a Record whose identifier is `search` remains available at `/v1/households/search`. OpenAPI gives [concrete paths precedence over templated paths](https://spec.openapis.org/oas/v3.1.2.html#paths-object), making a concrete `/households/search` route problematic for such identifiers. The broader guide permits both custom methods and action sub-resources; Consultation selects custom methods for Lookup and Search.

Collection membership scopes every read. Retrieve and Lookup use the unavailable-Record outcome for Records outside that collection, and continuation binds the collection as well as the query. Identity remains `(registryId, recordId)` across collections and views. Source adapters disambiguate overlapping keys for distinct Records in the same Registry with stable identifiers. Field bindings identify target read operations and input mappings for resolvable references.

The resource structure supports later family bindings as follows. These are composition principles; each family's contract defines its operations.

| Area | Composition principle |
|---|---|
| Write | Retrieve and update can share a Record URI through different HTTP methods. Write defines its own input schemas and permissions; a permitted read view does not establish an update payload. Governed requests and asynchronous operations can have their own resources. |
| Provisioning and Notification | The API contract coordinates Record collection names with schema, subscription, and other supporting-resource paths. |
| Evidence and events | Record references retain Registry and Record identity. Evidence and event formats use the representations defined by their bindings. |
| Versioning | The major version applies to one API surface. Independently exposed APIs can version separately while retaining stable Registry and Record identity. |
| Protocol-specific families | Bindings such as credential issuance or identity federation follow their protocols' endpoint and versioning conventions. |

## Relationship identity, snapshots, and completeness

The [Core representation rules](../05-api-families/registry-core.md#structured-values-and-references) distinguish owned components, Record references, and related-data views across API families. The [household contract](../../api/examples/household-registry.openapi.yaml) embeds membership attributes and references individual Records. The [birth-registration contract](../../api/examples/birth-registration.openapi.yaml) owns recorded parent details, with optional individual references.

Each view declares array bounds and completeness for the permitted representation. A complete array exceeding its bound follows the declared failure contract. A separately paginated relationship collection has its own published operation.

## Explicit cross-BB guide refinements

These general refinements belong to guide and ruleset `0.2.0-draft`; the guide's `draft-changes.md` records their details. Shared schema artifacts remain independently versioned at `0.1.0-draft`.

| Guide area | General refinement | Registry binding choice |
|---|---|---|
| §10.1, identifiers | Stable source-owned keys with documented uniqueness scope. | Non-personal `recordId` unique within its Registry. |
| §9.8, extensibility | Extensible response resources, strict operation arguments, and schema-defined nesting. | Closed Lookup/Search inputs and additive response fields. |
| §2.6 and §5.1, deployment roots and versions | Major version in resource paths; shared API surfaces can expose multiple collections and families. | Deployment root plus `/v1/businesses`, `/v1/households`, or another declared collection. |
| §5.3 and §5.8, custom methods | Colon custom methods alongside action sub-resources, with distinct resource and method naming conventions. | `/v1/records:lookup` and `/v1/records:search` in the reference binding. |
| §6.6, body-based reads | Exact single-result POST Lookup alongside collection Search. | Typed request bodies and synchronous `200` results. |
| §12, pagination | Declared page-size policy, advancing short or empty Pages, and explicit embedded-array completeness. | Fixed size within a live traversal; optional exact totals. |
| §10, domain schemas | Explicit ownership of adopted domain schemas and applicable inherited requirements. | A data schema and documented field meanings for each view. |
| §2.3 and §3.3, historical artifacts | Explicit separation of legacy contracts from current surfaces. | Previous generated CRUD contracts retained as migration evidence. |
| §4.6 and §20, draft validation | Draft requirement mappings and artifact checks distinguished from active conformance coverage. | DRAFT read coverage and contract/example checks. |

## Verification and follow-up boundary

[Testing](../11-testing.md) separates artifact validation from deployed implementation evidence. The [concrete OpenAPI examples](../../api/examples/README.md) support contract review. Implementation trials over registries with different source models will provide evidence about mapping effort, schema publication, and bounded continuation.
