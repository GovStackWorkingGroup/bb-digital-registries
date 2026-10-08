---
description: Interoperable read access to Registry Records.
---

# Consultation

> **Status:** DRAFT requirements and HTTP binding, for review and implementation trials.

## Purpose and capability model

Consultation defines read access to Registry Records for independently implemented services and API Consumers. A service selects one or more capabilities and publishes its operational contract through [Registry Core metadata](registry-core.md#api-family-discovery). Consumers use that contract to determine available operations and their inputs.

| Capability | Input | Successful result |
|---|---|---|
| Retrieve | Record Identifier | One Record |
| Lookup | Declared exact selector and its complete key | One Record |
| List | Declared collection and its supported equality filters | Page of Records |
| Search | Declared search and typed criteria | Page of Records |

Shared requirements apply to every selected capability; operation requirements apply when that capability is selected. Each operation applies to a declared collection with an unambiguous Registry context, representation schema, and access policy.

Consultation interoperates at the level Core defines: operation shapes, the Record envelope, error outcomes, pagination, and discovery are the same for every Registry, while domain fields, selectors, searches, and filters are declared per contract. Consumers can reuse protocol and envelope handling; domain-specific selectors, field meanings, and reference bindings still require integration against the published contract. See the [interoperability boundary](registry-core.md#purpose-and-applicability) in Core.

## Common read contract

A read preserves the source Records. Current information is the information accepted by the authoritative source and available under the service's declared currency contract, including replication or cache delay. The contract documents currency; verification reviews that documentation and the source arrangement rather than measuring delay. Domain schemas define the meaning of status and validity fields.

<a id="retrieve-representation"></a>

**Record representation.** A Record contains `recordId` and `data`. The identifier is stable, unique within its Registry, and never reassigned. The [Common Record context](registry-core.md#common-record-context) defines how the contract establishes the Registry and the representation schema: each operation declares its Registry, collection, capability, and view with the `x-govstack-digital-registries` extension, and its response schema defines the view. Retrieve and Lookup return one Record; List and Search use the same Record shape for each item in a Page.

The `data` schema defines domain fields, structured values, references, and their meanings. Revision, lifecycle, and provenance metadata are optional in the baseline; profiles can require source-backed metadata with defined semantics.

**Example: Record representation.** Examples on this page use the [illustrative business Registry binding](../../api/examples/business-registry.openapi.yaml), which defines the domain fields, status values, and query names. Its operations declare Registry `https://registry.example/registries/business`, collection `businesses`, and view `business-public`. A Record response contains:

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
| Registry context | Registry Identifier, collection, capability, and view of each operation, through the Core [extension](registry-core.md#api-composition). |
| Representation | JSON Schemas for the Record view and responses; adopted models and versions; mappings, local constraints, and extensions. |
| Field meanings | Meaning, units, code lists, and omitted, null, or empty values, preserving the semantics of adopted models. |
| Lookup and Search | Names, typed inputs, required components, comparison and normalization rules, uniqueness scope, and matching semantics. |
| List | Supported equality filters and sorting, deterministic order, page-size limits, and cursor expiry. |
| Access and currency | Authentication requirements, access policy for the declared view, and source currency, including material replication or cache delay. |

A domain profile records reusable agreements about schemas, terminology, and query semantics. A service contract applies those agreements to the operations it exposes. An implementation can adopt an existing profile or publish a concrete domain binding directly. Both preserve the shared Consultation behaviour. Reuse of domain models, the treatment of structured values, Record references, and embedded collections, and schema evolution follow [Registry Core](registry-core.md#domain-semantics-and-extensions).

**List and Search.** List and Search both return Pages, and the split between them follows the API design guide. List carries equality filters on declared non-personal fields as query parameters, one parameter per field (guide §12.8). Personal criteria, composite keys, and non-equality matching belong to Search, whose request body keeps them out of URLs and logs (guide §8.6 and §12.9). A contract that needs neither can select List alone; a contract whose every useful criterion is personal selects Search alone.

**Field-equality Search (informative).** A contract whose searches need only exact matches on fields of its view can declare one search for them. Its criteria schema lists those fields as optional properties, requires at least one, and rejects any other; every supplied field must match, and omitted fields do not constrain the result. An adapter can derive this search from the view schema instead of authoring one search per field combination. Access policy still governs the results, including combinations of personal criteria. The [business binding](../../api/examples/business-registry.schema.json) declares `byFields` over `legalName` and `registrationStatus` this way.

## Read requirements

<a id="retrieve-functional-requirements"></a>

### #1 Retrieve the current Record by identifier (DRAFT EXTENSIBLE OBSERVABLE)

`govstack-bb-digital-registries-fr-consultation#req-1`

`KF: Consultation`

Given a valid Record Identifier for a Record in the selected collection and a permitted request, Retrieve returns the current representation of that Record. An unknown identifier or a Record outside that collection receives the binding's unavailable-Record outcome, subject to protected-existence handling.

**Prerequisite:** Retrieve is selected and the collection declares its Registry context and view.

**Verification:** Retrieve a known source fixture and check its identity, schema, currency documentation, and declared metadata. Confirm that the source Record is unchanged; exercise an unknown identifier and, where applicable, an identifier belonging to another collection.

### #2 Apply disclosure rules to the returned representation (DRAFT EXTENSIBLE OBSERVABLE)

`govstack-bb-digital-registries-fr-consultation#req-2`

`KF: Consultation`

For every selected read, the service returns a representation valid against the declared view schema and containing only the Records, fields, metadata, and result information permitted for the consumer and request context. Disclosure applies to references, embedded data, counts, errors, and continuation information. Withholding applies to optional fields of the declared view; it does not substitute another schema.

**Prerequisite:** The access policy for the declared view is documented.

**Verification:** Exercise each selected read with fixtures for the service's applicable access policies. Check representation validity and permitted information, including different entitlements where offered.

### #3 Hide protected Record existence (DRAFT EXTENSIBLE OBSERVABLE)

`govstack-bb-digital-registries-fr-consultation#req-3`

`KF: Consultation`

When policy protects Record existence, Retrieve and Lookup return the same unresolved outcome for unknown and protected Records. Equivalence covers protocol status, security-relevant metadata, error type, response structure, and non-Record-specific values. Trace and correlation values are generated independently of Record existence; the outcome contains no Record-specific data. A Lookup failure caused by a source uniqueness violation on a protected key is indistinguishable from the unresolved outcome.

**Prerequisite:** The access policy declares which Records or keys have protected existence.

**Verification:** Compare protected and unknown fixtures under the same consumer context for each selected operation, including a uniqueness violation on a protected key where Lookup is selected. Check equivalent outcomes and independent trace values.

### #4 Resolve a Record by a declared exact selector (DRAFT EXTENSIBLE OBSERVABLE)

`govstack-bb-digital-registries-fr-consultation#req-4`

`KF: Consultation`

Lookup accepts a published selector and all required key components. The key can be composite. Its declared comparison and normalization rules resolve at most one Record within the uniqueness scope. A permitted unique match in the selected collection returns that Record; zero matches in the collection produce the unresolved outcome. A source uniqueness violation produces a failure governed by disclosure policy.

Invalid, incomplete, or unsupported inputs are rejected. A **context-derived Lookup** derives some or all key components from verified consumer context, such as the authenticated subject, when its selector contract defines that mode; a fully context-derived selector accepts an empty caller-supplied `values` object.

**Prerequisite:** Lookup is selected and each selector declares its key components, comparison rules, uniqueness scope, and any context-derived components.

**Verification:** Exercise known, unknown, incomplete, incorrectly typed, and unsupported inputs, plus a source uniqueness violation. Verify comparison rules, composite keys where supported, context-derived components where declared, and protected-existence handling.

### #5 List a bounded Record collection (DRAFT EXTENSIBLE OBSERVABLE)

`govstack-bb-digital-registries-fr-consultation#req-5`

`KF: Consultation`

List returns a bounded Page of permitted Records from its declared collection, applying its supported equality filters and ordering. Filters address declared non-personal fields only. Zero and single-result collections retain the Page shape. Unsupported filters or sorting produce a validation error.

**Prerequisite:** List is selected and the collection declares its order, tie-breaker, filters, and sorting.

**Verification:** Use fixtures with zero, one, and multiple results, including tied sort values where applicable. Check membership, schemas, order, size bounds, and rejection of unsupported inputs.

### #6 Search using declared criteria (DRAFT EXTENSIBLE OBSERVABLE)

`govstack-bb-digital-registries-fr-consultation#req-6`

`KF: Consultation`

Search accepts a published search name and its typed criteria. It applies the declared matching rules to the selected collection and returns a bounded Page of permitted matching Records, retaining the Page shape for zero or one result. Unsupported searches, unknown criteria, and invalid inputs produce a validation error.

**Prerequisite:** Search is selected and each search declares its criteria schema and matching rules.

**Verification:** Execute declared searches with valid and invalid inputs. Check matching results, empty Pages, applicable disclosure contexts, and use of the binding's protected request locations for personal criteria.

<a id="pagination-contract"></a>

### #7 Continue bounded result pages (DRAFT EXTENSIBLE OBSERVABLE)

`govstack-bb-digital-registries-fr-consultation#req-7`

`KF: Consultation`

List and Search use a declared deterministic order with a unique tie-breaker. Each request performs bounded source work, returns a bounded Page, and applies current authorization. Continuation preserves the collection, query, and view and advances traversal to explicit completion. Invalid continuation produces an error.

A completed traversal over unchanged data and access conditions contains each permitted matching Record once.

Pagination observes live data: source changes can move, add, or remove Records and cause repeated results. A profile can define stronger snapshot guarantees. Disclosure policy governs counts, page sizes, and continuation patterns, including short or empty advancing Pages.

Consumers treat cursors as opaque and return them unchanged with the original query inputs. They follow the completion signal, including when an intermediate Page is empty. The [HTTP binding](#http-binding) defines the continuation fields and fixed page-size policy.

**Prerequisite:** List or Search is selected and the collection declares its cursor expiry and page-size bounds.

**Verification:** Traverse unchanged multi-page fixtures to completion, checking complete membership without duplicates, identity, order, size bounds, progress, and termination. Exercise malformed, expired, and mismatched cursors, source changes, and applicable access changes. Check permitted page patterns and any total against the full permitted query.

## HTTP binding

The [canonical OpenAPI](../../api/openapi.yaml) defines the synchronous HTTPS/JSON contract, version `1.0.0-draft`, using API design guide and ruleset `0.2.0-draft`. It uses `records` as the reference collection name and `/v1` as the HTTP compatibility line. The BB requirements remain DRAFT. The [read API design decisions](../12-other-resources/read-api-design-decisions.md) record the binding choices and the shared guide refinements.

### Deployment contract

The server URL identifies the deployment root, optionally including a stable routing prefix such as `/registry`. The major version precedes each collection: `/v1/households` or, with that prefix, `/registry/v1/households`.

A deployment publishes a concrete OpenAPI contract containing its selected operations, service and authentication endpoints, versioned JSON Schemas for `data` and the complete response, selectors, searches, supported filters and ordering, source currency, access policy, and continuation policy. Every selected Consultation operation carries the `x-govstack-digital-registries` extension required by [Core requirement #8](registry-core.md#registry-core-functional-requirements); it names the Registry, collection, capability, and view, and the operation's response schema defines that view. The extension is the binding's answer to the Common Record context: the Registry Identifier is not repeated in requests or Records.

One API can expose several collections. A shared API can therefore expose:

```http
GET /v1/individuals/{recordId}
GET /v1/households/{recordId}
GET /v1/land-parcels/{recordId}
POST /v1/households:lookup
POST /v1/households:search
```

These are illustrative collection names; the published contract defines the supported paths. Different collections can belong to the same Registry or to different Registries. A Record retains its `(registryId, recordId)` identity across collections and views within its Registry. [API composition](registry-core.md#api-composition) describes how collections and families share an API; Consultation and Write can share a resource URI with separate methods, schemas, and permissions. The [OpenAPI examples](../../api/examples/README.md) illustrate concrete collections, domain schemas, and response payloads.

### Operations

| Capability | HTTP operation, relative to the deployment root | Successful body | Input contract |
|---|---|---|---|
| Retrieve | `GET /v1/records/{recordId}` | `{recordId, data}` | Record Identifier encoded as one path segment. |
| Lookup | `POST /v1/records:lookup` | `{recordId, data}` | JSON object with `selector` and `values`. |
| List | `GET /v1/records` | `{items, pageInfo}` | Optional `pageSize`, `cursor`, declared equality filters as query parameters, and declared sort parameters. |
| Search | `POST /v1/records:search` | `{items, pageInfo}` | JSON object with `search`, `criteria`, and optional `pageSize`, `cursor`, and declared `sort`. |

The `:lookup` and `:search` suffixes distinguish collection methods from item identifiers, including valid IDs such as `lookup` and `search`. Lookup and Search are synchronous reads returning `200`; selector and search values remain in the request body. Lookup uses a declared unique key within its documented scope; Search uses declared typed criteria. The concrete contract defines comparison and normalization rules and rejects unsupported inputs. The binding also exposes the guide's unversioned `/health` operation.

**Example: exact Lookup.** The business binding names its collection `businesses`. To resolve a business by its declared registration-number key, send this body to `POST /v1/businesses:lookup`:

```json
{
  "selector": "byRegistrationNumber",
  "values": {
    "registrationNumber": "BR-000042"
  }
}
```

For the permitted match, the `200` response is the Record shown above.

**Example: Search and collection result.** To find businesses with a declared registration status, send this body to `POST /v1/businesses:search`:

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

Retrieve and Lookup return `{recordId, data}`. List and Search return `{items, pageInfo}`, with each item using the same Record schema for the declared view. Empty and single-result collections retain the Page shape.

The operation's Registry context declaration and response schema provide Registry and schema context. Additional source metadata follows [Registry Core](registry-core.md#common-record-context). A schema linked with `rel="describedby"` describes the complete response, including its envelope. An operation exposing a different view is a separate operation with its own declared schema and field meanings.

**Audience-dependent fields (informative).** When access policies release different fields of the same Records, a contract can take one of two approaches. It can publish one view whose schema marks the varying fields optional, so each caller receives the fields its policy permits; the schema then cannot guarantee those fields to a caller entitled to all of them. Or it can publish each field set as its own view with its own required fields. Because an operation's declared collection equals its path segment, a second view of the same Records uses its own collection path, such as `/v1/businesses` for `business-public` and `/v1/business-extracts` for a fuller `business-extract` view, or a separate API. Records keep their identifiers in both collections.

### Continuation

The first request selects `pageSize`, defaulting to 20 and bounded to 100 in the canonical contract. A continuation repeats the original criteria, search name where applicable, sorting, and view with the cursor. It can omit `pageSize` to retain the bound value or supply that same value; a different value produces `400 invalid-cursor`. Cursors bind the operation, Registry, collection, query, view, effective size, and applicable access context. The deployment declares expiry and rejects malformed, expired, or mismatched cursors, including continuations whose declared semantics it can no longer preserve. A short or empty Page can carry a non-null `nextCursor` when source processing advances.

A non-null `pageInfo.nextCursor` enables continuation; `null` marks completion. Optional `pageInfo.total` is the exact count of the full permitted query at the documented page evaluation time, before applying the continuation boundary. Because the count is of permitted Records only, disclosure policy decides whether it is offered at all. Services omit an unavailable total. OpenAPI defines the cursor format, limits, and error responses.

### Outcomes, errors, and caching

OpenAPI defines the status codes and RFC 9457 Problem Details for each operation. Retrieve and Lookup share `404 record-not-available` for unknown Records, Records outside the selected collection, and Records whose existence is protected under [requirement #3](#retrieve-functional-requirements). Structural input errors, invalid query parameters, and invalid pagination controls use `400`. Structurally valid Lookup and Search bodies with unknown selector or search names or invalid domain values use `422`. Malformed, expired, or mismatched cursors use `400 invalid-cursor`.

Protected reads and errors use `Cache-Control: no-store`. Deployments may declare caching for public or isolated representations. Retrieve supports conditional requests: its `200` and `304` responses carry an ETag that validates the selected HTTP representation, and the service evaluates authorization before `If-None-Match` can produce `304`. Authentication, authorization, and source failures follow the declared OpenAPI responses and the API design guide.

### Record references and expansion

The [Core representation rules](registry-core.md#structured-values-and-references) govern nested data and related Records. The reusable `RecordReference` schema carries `recordId` and, where the field schema leaves the target Registry open, required `registryId`. A field with a fixed target Registry permits omission of `registryId` and accepts an explicit value only when it matches that target.

When a related read is offered, the field binding identifies its target collection, read operation, and operational contract, including how the reference supplies the operation's inputs. Consumers follow that binding and the target's access requirements. Record Identifiers remain opaque; reference identity is independent of the target's current availability.

Optional client-selected expansion declares its supported paths, bounds, source currency, and disclosure behaviour in the deployment contract. Expansion embeds related representations inside the declared view; it does not select a different view. The [OpenAPI examples](../../api/examples/README.md) demonstrate concrete nested schemas and references.

## Conformance

Evaluation identifies the service, specification and contract versions, selected capabilities, and any adopted domain profile. The service satisfies the common read contract, service declarations, HTTP binding, and the requirements applicable to each selected capability.

| Selected capability | Applicable Consultation requirements |
|---|---|
| Retrieve | #1, #2; also #3 when existence is protected |
| Lookup | #2, #4; also #3 when existence is protected |
| List | #2, #5, #7 |
| Search | #2, #6, #7 |

Verification checks published contracts and observable exchanges under the stated fixture conditions. The [OpenAPI examples](../../api/examples/README.md) and [artifact validation](../../api/README.md#validation) support review; deployed behaviour is evaluated separately.
