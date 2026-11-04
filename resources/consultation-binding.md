---
description: Interoperable read access to Registry Records.
---

# Consultation

> **Status:** DRAFT requirements and HTTP binding, for review and implementation trials.

## Purpose and capability model

Consultation defines read access to Registry Records for independently implemented services and API Consumers. A service selects one or more operation options and publishes its operational contract through [Registry Core metadata](registry-core-model.md#api-family-discovery). Consumers use that contract to determine available operations and their inputs.

| Capability | Input | Successful result |
|---|---|---|
| Retrieve | Record Identifier | One Record |
| Lookup | Declared exact selector and its complete key | One Record |
| List | Declared collection and its supported equality filters | Page of Records |
| Search | Declared search and typed criteria | Page of Records |
| Revision List | Record Identifier | Page of retained Record revisions |
| Revision Retrieve | Record Identifier and Revision Identifier | One retained Record revision |

Shared requirements apply to every selected capability; operation requirements apply when that capability is selected. Each operation applies to a declared logical **Collection** with an unambiguous Registry context, representation schema, and access policy. A Collection is an API grouping with declared membership and one stable `collectionId`. It is independent of database tables, source-system modules, governed datasets, and the institutionally defined Registry. One Registry can expose several Collections, and one Record can appear in several Collections without changing its identity. [Selectable read features](#selectable-read-features) add stronger guarantees only when the operation declares them.

Collection boundaries are adopter choices. For example, a civil-registration service can expose `birth-registrations`, `marriage-registrations`, and `death-registrations` as separate Collections when that arrangement matches its service contract. Those names are illustrative; this specification does not define the legal scope of civil registration or require one Collection per event type.

Consultation interoperates at the level Core defines: operation shapes, the Record envelope, error outcomes, pagination, and discovery are the same for every Registry, while domain fields, selectors, searches, and filters are declared per contract. Consumers can reuse protocol and envelope handling; domain-specific selectors, field meanings, and reference bindings still require integration against the published contract. See the [interoperability boundary](registry-core-model.md#purpose-and-applicability) in Core.

## Common read contract

A read preserves the source Records. In the absence of an explicit temporal selector, it returns the latest permitted information available under the service's declared currency contract, including replication or cache delay. An operation selecting `recorded-time` or `effective-time` can instead accept the corresponding temporal selector. Snapshot traversal fixes one collection traversal; it does not by itself make historical Record states addressable. The contract documents currency and temporal semantics; verification reviews that documentation and the source arrangement rather than measuring delay. Domain schemas define the meaning of status, validity, event occurrence, and registration fields.

<a id="retrieve-representation"></a>

**Record representation.** A baseline `Record` contains `recordId` and `data`; a baseline `RecordPage` contains Records and pagination context. Neither baseline schema publishes temporal metadata. A temporally selected response includes the applied `temporal` context at the top level. The canonical `TemporalRecord` and `TemporalRecordPage` wrappers require that metadata; a concrete contract can instead publish one response schema covering current and selected responses when it requires temporal metadata whenever a selector is applied. Page-level echo keeps an empty temporal Search result interpretable without changing the shared item schema. The identifier is stable, unique within its Registry, and never reassigned. It remains the same across Collections, revisions, views, and temporal selections. The [Common Record context](registry-core-model.md#common-record-context) defines how the contract establishes the Registry and the representation schema: each operation declares its Registry, Collection, capability, and view with the `x-govstack-digital-registries` extension, and its response schema defines the view. Retrieve and Lookup return one Record; List and Search use the same Record shape for each item in a Page.

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

## Service declarations

The published service contract supplies the following information for its selected capabilities, directly or through versioned references:

| Topic | Declared information |
|---|---|
| Registry context | Registry Identifier, logical Collection Identifier, capability, view, and selected selectable read features of each operation, through the Core [extension](registry-core-model.md#api-composition). |
| Representation | JSON Schemas for the Record view and responses; adopted models and versions; mappings, local constraints, and extensions. |
| Field meanings | Meaning, units, code lists, and omitted, null, or empty values, preserving the semantics of adopted models. |
| Lookup and Search | Names, typed inputs, required components, comparison and normalisation rules, uniqueness scope, and matching semantics. Reusable Search semantics name the supported equality, range, set-membership, and prefix operators without requiring a universal query language. |
| Pagination | Supported equality filters and sorting where offered, deterministic default order with a unique tie-breaker, page-size limits, cursor expiry, source consistency and concurrent-change behaviour, and any complete or snapshot traversal guarantee. |
| Access and currency | Authentication requirements, access policy for the declared view, and source currency, including material replication or cache delay. |
| Resource limits | Request and response bounds, configured timeout behaviour and failure outcome, and any source-query or scan limits. A page-size limit does not establish a bound on source rows examined or database work. |
| Field selection | Supported top-level `data` field names, default field set, mandatory fields if any, selection bounds, omission semantics, and response schema. |
| Revisions and time | Supported revision capabilities, order, retention and gap semantics, schema evolution, recorded-time and effective-time meanings, accepted selector precision, and unavailable-history outcomes. |
| Purpose binding | When selected, the trusted purpose binding, controlled purpose codes or absolute URIs, permitted values, rejection behaviour, cursor and validator binding, and audit treatment. |

A domain profile records reusable agreements about schemas, terminology, and query semantics. A service contract applies those agreements to the operations it exposes. An implementation can adopt an existing profile or publish a concrete domain binding directly. Both preserve the shared Consultation behaviour. Reuse of domain models, the treatment of structured values, Record references, and embedded collections, and schema evolution follow [Registry Core](registry-core-model.md#domain-semantics-and-extensions).

**List and Search.** List and Search both return Pages, and the split between them follows the API design guide. List carries equality filters on declared non-personal fields as query parameters, one parameter per field (guide §12.8). Personal criteria, composite keys, and non-equality matching belong to Search, whose request body keeps them out of URLs and logs (guide §8.6 and §12.9). A contract that needs neither can select List alone; a contract whose every useful criterion is personal selects Search alone.

**Reusable Search semantics.** A contract publishes named searches whose criteria remain typed by versioned schemas. It can reuse the standard equality, range, set-membership, and prefix meanings defined by this specification, independently selecting only those it supports. The field contract states the applicable operator, comparison type, normalisation, null and absence treatment, and combination rule. A deployment is not required to implement fuzzy matching, full-text search, or a universal query language. The [business binding](../api/examples/business-registry.schema.json) illustrates a concrete selection of reusable semantics.

## Requirements

The requirements that use this binding are in [Provide Registry Services](../requirements/registry-services.md). Verification procedures remain in [Testing](testing.md#requirement-traceability).

## Selectable read features

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

## Revision and temporal capabilities

Revision history is selectable and source-backed. A service does not create historical revisions by caching current responses, traversing a collection snapshot, deriving values from event notifications, or assigning identifiers to representations that the source cannot distinguish. Every history request applies current authentication, authorisation, disclosure, and purpose policy. A protected or unavailable revision produces the declared unavailable outcome without revealing whether hidden history exists.

## HTTP binding

The [canonical OpenAPI](api.yml) defines the synchronous HTTPS/JSON contract, version `1.0.0-draft`, using API design guide and ruleset `0.3.0-draft`. Its `CollectionId` schema uses the single reference value `records`; concrete examples use literal Collection Identifiers such as `businesses`, `households`, and `birth-registrations`. The `/v1` prefix is the HTTP compatibility line. The BB requirements remain DRAFT. The [read API design decisions](read-api-design-decisions.md) record the binding choices and the shared guide refinements.

### Deployment contract

The server URL identifies the deployment root, which may include a stable routing prefix such as `/registry`. The canonical hierarchy is `/v1/collections/{collectionId}`; with that prefix a household Record is addressed under `/registry/v1/collections/households/records/{recordId}`.

A deployment publishes a concrete OpenAPI contract containing its selected operations and selectable read features, service and authentication endpoints, versioned JSON Schemas for `data` and the complete response, selectors, searches, supported filters and ordering, source currency, access policy, resource limits, temporal and revision semantics where selected, and continuation policy. Every selected Collection-scoped Consultation operation carries the `x-govstack-digital-registries` extension required by [Provide Registry Services](../requirements/registry-services.md); it names the Registry, Collection, capability, and view, and the operation's response schema defines that view. The `features` array, which can be omitted, declares the additional read guarantees. A `purpose-bound` operation also carries its required `purpose` declaration. The extension is the binding's answer to the Common Record context: the Registry Identifier is not repeated in requests or Records. The cross-Collection caller capability operation uses its own response schema rather than declaring one Collection context.

One API can expose several collections. A shared API can therefore expose:

```http
GET /v1/collections/businesses/records/{recordId}
GET /v1/collections/households/records/{recordId}
GET /v1/collections/birth-registrations/records/{recordId}
POST /v1/collections/households/lookup
POST /v1/collections/households/search
```

These are illustrative Collection names; the published contract defines the supported paths and membership. Collections are logical API resources and need not match tables, source modules, governed datasets, or separate institutional Registries. A Record retains its `(registryId, recordId)` identity across Collections and views within its Registry. [API composition](registry-core-model.md#api-composition) describes how Collections and families share an API; Consultation and Write can share a resource URI with separate methods, schemas, and permissions. The [OpenAPI examples](api-examples/README.md) illustrate concrete Collections, domain schemas, and response payloads.

### Operations

| Capability | HTTP operation, relative to the deployment root | Successful body | Input contract |
|---|---|---|---|
| Retrieve | `GET /v1/collections/{collectionId}/records/{recordId}` | `Record`, or `TemporalRecord` for selected temporal state | Record Identifier in the path; `recordedAsOf` or `effectiveAt` query selector when its feature is declared. |
| Lookup | `POST /v1/collections/{collectionId}/lookup` | `Record`, or `TemporalRecord` for selected temporal state | `LookupRequest` with `selector`, `values`, and `temporal` when declared. |
| List | `GET /v1/collections/{collectionId}/records` | `RecordPage`, or `TemporalRecordPage` for selected temporal state | Any `pageSize`, `cursor`, declared filters and sort, plus temporal query selectors when declared. |
| Search | `POST /v1/collections/{collectionId}/search` | `RecordPage`, or `TemporalRecordPage` for selected temporal state | `SearchRequest` with `search`, `criteria`, pagination controls, and `temporal` when declared. |
| Revision List | `GET /v1/collections/{collectionId}/records/{recordId}/revisions` | `RevisionPage` | Record Identifier and pagination controls. |
| Revision Retrieve | `GET /v1/collections/{collectionId}/records/{recordId}/revisions/{revisionId}` | `RecordRevision` | Record and Revision Identifiers. |

<a id="retrieve"></a>

#### Retrieve

Retrieve uses `GET /v1/collections/{collectionId}/records/{recordId}` to return the latest permitted Record representation for a stable Record Identifier, or the representation selected by a declared temporal selector.

<a id="lookup"></a>

#### Lookup

Lookup uses `POST /v1/collections/{collectionId}/lookup` with a declared exact selector and complete key to resolve at most one permitted Record.

<a id="list"></a>

#### List

List uses `GET /v1/collections/{collectionId}/records` with declared equality filters and ordering to return a bounded Page of permitted Records.

<a id="search"></a>

#### Search

Search uses `POST /v1/collections/{collectionId}/search` with a declared search name and typed criteria to return a bounded Page of permitted matching Records.

<a id="revision-list"></a>

#### Revision List

Revision List uses `GET /v1/collections/{collectionId}/records/{recordId}/revisions` to return a bounded Page of retained revisions of one Record.

<a id="revision-retrieve"></a>

#### Revision Retrieve

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

### Representation and schema context

Retrieve and Lookup return baseline `Record` or, when temporal coordinates are applied, `TemporalRecord`. List and Search return baseline `RecordPage` or `TemporalRecordPage`, with each item using the same Record schema for the declared view. Revision Retrieve returns `RecordRevision`; Revision List returns `RevisionPage`. Empty and single-result Collections retain their Page shape. `TemporalRecord` echoes applied coordinates at Record level. `TemporalRecordPage` echoes them at Page level, including when `items` is empty. Baseline `Record` and `RecordPage` omit temporal metadata.

The operation's Registry context declaration and response schema provide Registry and schema context. Additional source metadata follows [Registry Core](registry-core-model.md#common-record-context). A schema linked with `rel="describedby"` describes the complete response, including its envelope. Different operations can declare different views; operations sharing a collection and view use the same Record schema.

**Audience-dependent fields.** A view schema can mark varying fields as not required so access policy and consumer field selection determine which are returned on the same operation. The contract documents the default field set and omission meanings; the schema alone does not guarantee selectable fields will always be present. A materially different view with different required fields or meanings uses a separately declared operation or API. Records retain their identity across those views.

**Field-selection input.** An operation selecting `field-selection` publishes a `fields` input, which clients can omit, restricted to its declared selectable top-level `data` property names. GET operations use a comma-separated query array, for example `GET /v1/collections/businesses/records/r_42?fields=legalName`. Lookup and Search carry a JSON array in the body, for example `"fields": ["legalName"]`. The input selects existing fields; it does not introduce a query language, nested expansion syntax, or a different view schema. Mandatory `data` fields, if any, remain present as documented. Without this feature, an operation does not accept this input.

### Temporal selection

Timestamp selectors and revision recording times use RFC 3339 UTC instants serialised with uppercase `Z`. Calendar-date applicability coordinates use `format: date` and are not converted into instants. The illustrative birth profile accepts calendar dates only for `effectiveAt`, including its response echo, while its recording-time coordinates remain UTC instants.

GET Retrieve and List carry `recordedAsOf` and `effectiveAt` as query parameters only when the corresponding feature is selected. POST Lookup and Search carry the same coordinates inside the closed, non-empty `temporal` object, when supplied. `recordedAsOf` is a date-time; `effectiveAt` is a date or date-time as the concrete contract declares. The operation can accept either or both coordinates. When both are present, it selects the state applicable at `effectiveAt` using only source knowledge accepted no later than `recordedAsOf`. `TemporalRecord` and `TemporalRecordPage` echo every applied source-backed coordinate, including an empty Page. Absence selects the latest representation and omits temporal metadata; a concrete contract can publish a response schema that covers both cases while enforcing that temporal metadata is present whenever a selector is applied. Revision List and Revision Retrieve do not accept these selectors.

Temporal selection is distinct from traversal consistency. `snapshot-traversal` holds one paged result stable but does not provide recorded-time or effective-time history. Conversely, a temporal selector does not make later continuation Pages a snapshot unless `snapshot-traversal` is also selected.

### Revision history

Revision operations use a separately declared history view, such as `record-history`. `RecordRevision.revision` always contains `revisionId` and can contain `recordedAt` when that value is source-backed. The deployment documents revision order, retention, gaps, and schema evolution. A declared history view can normalise older source schemas while preserving their values and meanings; a revision that cannot be mapped faithfully produces the declared explicit failure. Current authorisation and disclosure apply to every request and Page. An unavailable historical state fails with the declared protected outcome; the service does not expose an arbitrary raw schema or synthesise it from current data, snapshots, audit events, registration dates, or event occurrence dates.

<a id="pagination"></a>
<a id="pagination-contract"></a>

### Continuation

The first request selects `pageSize`, defaulting to 20 and bounded to 100 in the canonical contract. A continuation repeats the original criteria, search name where applicable, sorting, temporal selection, and effective field selection with the cursor. Field order does not change the selected set; omission uses the declared default. It can omit `pageSize` to retain the bound value or supply that same value; a different value produces `400 invalid-cursor`. Cursors are opaque, URL-safe, integrity-protected, and exclude personal data. They bind the operation, Registry, Collection, query, view, temporal context, effective field set and size, effective purpose where required, and applicable access context. A Revision List cursor also binds its parent `recordId`; replay under another parent produces `400 invalid-cursor`. Cursors do not grant authority; every Page is reauthorised. The deployment declares expiry and rejects malformed, expired, or mismatched cursors, including continuations whose declared semantics it can no longer preserve. A short or empty Page can carry a non-null `nextCursor` when source processing advances. An adapter can wrap a source offset, page number, or continuation token while preserving these rules.

A non-null `pageInfo.nextCursor` enables continuation; `null` marks completion of the declared traversal. Baseline completion follows the published consistency and result-limit policy. Only `complete-traversal` establishes exhaustive membership, and only `snapshot-traversal` establishes a fixed source snapshot. When supplied, `pageInfo.total` is the exact count of the full permitted query at the documented evaluation point, before applying the continuation boundary: the current page's evaluation for live reads or the fixed source snapshot evaluated under current disclosure rights for snapshot traversal. Disclosure policy decides whether it is offered at all. Services omit an unavailable total. OpenAPI defines the cursor format, limits, and error responses.

### Outcomes, errors, and caching

OpenAPI defines the status codes and RFC 9457 Problem Details for each operation. Retrieve and Lookup share `404 record-not-available` for unknown Records, Records outside the selected Collection, and Records whose existence is protected under [Provide Registry Services](../requirements/registry-services.md). Revision List and Revision Retrieve use the same outcome for an unknown or protected parent Record; Revision Retrieve also uses it when the revision is unknown or protected, without distinguishing which resource was unavailable. After these protection checks, an authorised operation whose source cannot return retained history uses `409 history-not-available`.

A successful List or Search with zero permitted matches returns `200` with an empty `items` array, including when policy filters every source match. For a temporal item read, a source-backed determination that no item exists at the selected coordinates uses `404 record-not-available`, subject to protected-existence handling. When the authorised source cannot evaluate the requested temporal state or query, the operation uses `409 temporal-state-not-available` and never substitutes current state. These outcomes distinguish proven absence from unavailable historical evaluation.

Structural input errors, invalid query parameters, and invalid pagination controls use `400`. Empty, duplicate, incorrectly typed, or out-of-bounds field selections also use `400`. Structurally valid Lookup and Search bodies with unknown selector, search, or selectable field names or invalid domain values use `422`. Unknown selectable field names in a query use `400`. Malformed, expired, mismatched, or cross-parent Revision List cursors use `400 invalid-cursor`.

Protected reads and errors use `Cache-Control: no-store`. Deployments may declare caching for public or isolated representations. An operation selecting `conditional-read` publishes `If-None-Match` and `304`; its `200` and `304` responses carry the declared ETag header for the permitted representation, and authorisation precedes evaluation of the validator. The matching `304` is bodyless, while `200` carries the declared response body and headers. A baseline Retrieve operation need not publish ETag, `If-None-Match`, or `304`. Authentication, authorisation, and source failures follow the declared OpenAPI responses and the API design guide. The API catalog's conditional responses are independent of the Consultation feature declaration.

When `purpose-bound` is selected, the operation extension identifies a trusted access-token claim or trusted authorisation context and the controlled allowed purpose values. Purpose never comes from an ordinary request parameter. Missing or unallowed purpose fails before disclosure, and the effective purpose participates in cursor and ETag context. This does not replace inherited security or establish consent, institutional authority, or downstream compliance. Operations without `purpose-bound` continue to use their inherited authentication and authorisation requirements without a purpose input.

### Record references and expansion

The [Core representation rules](registry-core-model.md#structured-values-and-references) govern nested data and related Records. The reusable `RecordReference` schema carries `recordId` and, where the field schema leaves the target Registry open, required `registryId`. A field with a fixed target Registry permits omission of `registryId` and accepts an explicit value only when it matches that target.

When a related read is offered, the field binding identifies its target collection, read operation, and operational contract, including how the reference supplies the operation's inputs. Consumers follow that binding and the target's access requirements. Record Identifiers remain opaque; reference identity is independent of the target's current availability.

Client-selected expansion, where offered, declares its supported paths, bounds, source currency, and disclosure behaviour in the deployment contract. Expansion embeds related representations inside the declared view; it does not select a different view. The [OpenAPI examples](api-examples/README.md) demonstrate concrete nested schemas and references.

## Conformance

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

Verification checks published contracts and observable exchanges under the stated fixture conditions. The [OpenAPI examples](api-examples/README.md) and [artifact validation](testing.md#artifact-validation) support review; deployed behaviour is evaluated separately.
