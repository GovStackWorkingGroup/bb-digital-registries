# OpenAPI examples

These illustrative deployments specialize the [Consultation contract](../openapi.yaml).

| OpenAPI | Collection | Capabilities | Record view |
| --- | --- | --- | --- |
| [Business registry](business-registry.openapi.yaml) | `/v1/businesses` | Retrieve, Lookup, List, Search | Legal name and registration status |
| [Household registry](household-registry.openapi.yaml) | `/v1/households` | Retrieve | Address, memberships, and individual references |
| [Birth registration](birth-registration.openapi.yaml) | `/v1/birth-registrations` | Retrieve | Birth details and recorded parent information |

Each contract declares its Registry, collection, capability, and view on every
operation with `x-govstack-digital-registries`, and publishes schemas, source
currency, access policy, limits, and response examples. The business contract also defines exact
and composite selectors, a typed status search, a field-equality search, and live
cursor pagination.

The examples use `https://registry.example` as their API root. A deployment can
combine several collections under that root and associate each with its Registry.
Business Lookup and Search use `/v1/businesses:lookup` and
`/v1/businesses:search`; item identifiers remain in `/v1/businesses/{recordId}`.

Household memberships are embedded components with household-scoped identifiers.
Their individual references inherit the target Registry from the field schema.
Birth-registration parent details carry their recorded meaning and can include
an individual reference. The concrete schemas declare each view's array bounds
and completeness.

`IndividualReference` illustrates a binding to a target Individual service and
maps the referenced identifier to its Retrieve operation. That target contract is
not included in these artifacts; validation covers the reference shape and the
containing Record views.

## Schemas and fixtures

| Schema | Fixtures |
| --- | --- |
| [Business Record and request schemas](business-registry.schema.json) | [Consultation exchanges](consultation-exchanges.json) |
| [Household, birth-registration, and reference schemas](relationship-examples.schema.json) | [Relationship exchanges](relationship-exchanges.json) |

## Discovery

| Artifact | Purpose |
| --- | --- |
| [Registry metadata](registry-metadata.jsonld) | Compacted JSON-LD document for the business Registry, validated against the [metadata document schema](../extensions/registry-metadata.schema.json) |
| [API catalog linkset](api-catalog.linkset.json) | RFC 9727 `/.well-known/api-catalog` response linking the three contracts and the metadata document |

The Registry Core page embeds both documents; the validator checks that the
embedded copies and these files are identical.

Named exchanges represent independent fixture states, except
`emptySearchContinuation` and `finalSearchPage`, which form one traversal.
Example cursors are illustrative values.

The [artifact validator](../../tools/validate_consultation.py) checks operation
schemas, examples, and valid and invalid inputs. Run it using the
[validation commands](../README.md#validation).
