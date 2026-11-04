---
description: Illustrative Registry API read and Write bindings, schemas, and exchanges.
---

# API examples

The read examples below specialise the read operations in the unified [Registry API contract](../api-reference.md). The independently selectable Write examples are listed separately below.

| OpenAPI | Collection | Capabilities | Selectable features | Record view |
| --- | --- | --- | --- | --- |
| [Business registry](business.md) | `/v1/collections/businesses` | Retrieve, Lookup, List, Search | Field selection on all operations; conditional Retrieve; complete List and Search traversal | Legal name and registration status |
| [Household registry](household.md) | `/v1/collections/households` | Retrieve | None | Address, memberships, and individual references |
| [Birth registration](birth-registration.md) | `/v1/collections/birth-registrations` | Retrieve, Search, Revision List, Revision Retrieve | Recorded time, effective time, and purpose binding on current-state reads; purpose binding on history reads | Birth details, Record applicability, recorded parent information, and retained revisions |

Each contract declares its Registry, collection, capability, and view on every
operation with `x-govstack-digital-registries`, and publishes schemas, source
currency, access policy, limits, and response examples. The business contract also defines exact
and composite selectors, a typed status search, a field-equality search, projected response
examples, and live cursor pagination with a complete-traversal claim.

The examples use `https://registry.example` as their API root. A deployment can
combine several collections under that root and associate each with its Registry.
Business Lookup and Search use `/v1/collections/businesses/lookup` and
`/v1/collections/businesses/search`; item identifiers remain under
`/v1/collections/businesses/records/{recordId}`.

Household memberships are embedded components with household-scoped identifiers.
Their individual references inherit the target Registry from the field schema.
Birth-registration parent details carry their recorded meaning and can include
an individual reference. Its `dateOfBirth` is the civil-registration event date,
while `registrationEffectiveFrom` and `effectiveAt` describe Record applicability.
This birth profile accepts calendar dates only for `effectiveAt`, with an inclusive
`registrationEffectiveFrom` boundary and no timezone conversion. Its `recordedAsOf`
and available revision recording times remain UTC instants serialised with `Z`.
The birth contract also illustrates a typed `byOccurrencePeriodAndPlace` Search,
before-and-after recording-time reads, an evaluated empty temporal Search, a
source-unavailable temporal Search, and retained revision list/detail reads. The
selectable exchange set also pairs Business Retrieve `200` and bodyless `304`
responses and shows a caller-filtered capability document spanning Business and
birth-registration operations.
The concrete schemas declare each view's array bounds and completeness.

`IndividualReference` illustrates a binding to a target Individual service and
maps the referenced identifier to its Retrieve operation. That target contract is
not included in these artifacts; validation covers the reference shape and the
containing Record views.

## Schemas and fixtures

| Schema | Fixtures |
| --- | --- |
| [Business Record and request schemas](../../api/examples/business-registry.schema.json) | [Consultation exchanges](../../api/examples/consultation-exchanges.json) |
| [Household, birth-registration, and reference schemas](../../api/examples/relationship-examples.schema.json) | [Relationship exchanges](../../api/examples/relationship-exchanges.json) |
| [Read operation extension schema](../../api/extensions/x-govstack-digital-registries.schema.json) | [Positive and negative schema fixtures](../../api/examples/consultation-extension-fixtures.json) and [history, temporal, search, and discovery exchanges](../../api/examples/consultation-extension-exchanges.json) |

## Discovery

| Artifact | Purpose |
| --- | --- |
| [Registry metadata](../../api/examples/registry-metadata.jsonld) | Compacted JSON-LD document for the business Registry, validated against the [metadata document schema](../../api/extensions/registry-metadata.schema.json) |
| [API catalog linkset](../../api/examples/api-catalog.linkset.json) | RFC 9727 `/.well-known/api-catalog` response linking the unified Registry contract, the informative Evidence contract, and the metadata document |

[Discover Registry Services](../../requirements/registry-discovery.md#core-api-family-discovery) includes both discovery examples. The artifact checks verify that the embedded examples match these files.

Named exchanges represent independent fixture states, except
`emptySearchContinuation` and `finalSearchPage`, which form one traversal.
Example cursors are illustrative values.

## Non-normative Write examples

[Write example OpenAPI](write.md), [input and result schemas](../../api/examples/write-examples.schema.json), and [request/response exchanges](../../api/examples/write-exchanges.json) illustrate the Write operations in the shared [Registry API contract](../api-reference.md) using birth registration, households, and individuals. Both direct commits and approval-based proposals are shown. These are example deployment choices, not additional conformance requirements.

Birth declaration and correction commands carry proposed facts, reasons, and evidence references. A successful authoritative commit maps accepted facts into authoritative state as declared by the operation. A permitted Birth read projection can omit, transform, or combine that state and is governed by its own access and currency contract. Command annotations remain outside that projection. Pending and rejected proposals do not change authoritative facts. The HTTP idempotency key and source transaction identifier have separate roles.

| Household case | Example relationship input |
| --- | --- |
| Create with existing individuals | Existing individual Record URIs |
| Create individuals together with the household | Embedded individuals identified by request-local URIs |
| Add an existing individual later | Named `add-member` transition with an existing Record URI |
| Create and add an individual later | Named `add-member` transition with an embedded individual |

The compound cases explicitly assume one source transaction across the household and newly created individuals. A deployment without that guarantee can use existing individual references. The example makes no distributed transaction guarantee. Successful results map request-local URIs to authoritative Record identifiers; unapplied proposals cannot provide those resolutions.

Selected domain fields use [PublicSchema](https://publicschema.org/) as a reference. The source schemas and their CC BY 4.0 attribution, plus the transitive GeoJSON MIT notice, are retained with the [schema attribution](schema-attribution.md). This vocabulary choice is local to these examples; Write inputs and Consultation views are chosen by the deployment.

The [domain-neutral Write fixtures](../../api/examples/write-contract-fixtures.json) distinguish immediate commit, background execution (`202` plus Operation polling), and a created Change Request awaiting approval (`201`). The successful and failed background outcomes are alternative fixture states. Background processing is optional and does not replace review or application state.
