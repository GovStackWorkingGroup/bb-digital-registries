# API artifacts

[openapi.yaml](openapi.yaml) defines the DRAFT Consultation HTTP contract:
OpenAPI **3.1.2**, API version **1.0.0-draft**, targeting API Design Guide and
ruleset **0.3.0-draft**. The `/v1` path identifies the HTTP compatibility line;
the Building Block specification has its own version.

| Capability | HTTP path | Success |
| --- | --- | --- |
| Retrieve | `GET /v1/collections/{collectionId}/records/{recordId}` | Record |
| List | `GET /v1/collections/{collectionId}/records` | RecordPage |
| Exact Lookup | `POST /v1/collections/{collectionId}/lookup` | Record |
| Named Search | `POST /v1/collections/{collectionId}/search` | RecordPage |
| Revision List | `GET /v1/collections/{collectionId}/records/{recordId}/revisions` | RevisionPage |
| Revision Retrieve | `GET /v1/collections/{collectionId}/records/{recordId}/revisions/{revisionId}` | RecordRevision |
| Caller Discovery | `GET /v1/capabilities` | CallerCapabilities |

`records` is the reference collection name, and
`https://registry.example/registries/records` is a placeholder Registry Identifier.
Deployments publish concrete names, such as `/v1/collections/businesses/records`
or `/v1/collections/households/records`,
declare the Registry Identifier from their Registry metadata, and select
capabilities for each collection. One API can expose several collections, each
with a declared Registry, membership scope, and operation schemas. Success responses share
`Record {recordId, data}` and `RecordPage {items, pageInfo}`.
Lookup and Search are synchronous reads. `/health` provides operational liveness.
`GET` and `HEAD /.well-known/api-catalog` serve the RFC 9727 linkset at the origin
root, outside any routing prefix.

The server URL identifies the deployment root, which may include a stable prefix
such as `/registry`. The major version precedes the collection in each operation
path. API-family labels describe capabilities; families can share resource paths
with distinct HTTP methods, schemas, and access requirements.

The default response language is English (`en`). A deployment may select another
default or localise Problem `title` and `detail`; it then declares that default and
follows API Design Guide §19 for `Accept-Language`, `Content-Language`, and `Vary`.

The shared Record schemas apply the [Registry Core](../requirements/registry-discovery.md#core-registry-core)
representation rules. Core metadata is published as a JSON-LD document that the
RFC 9727 `/.well-known/api-catalog` linkset locates. It identifies the Registry and
its authority and links each service to its deployed OpenAPI contract. Every
Collection-scoped Consultation read declares its Registry, collection, capability, view,
and any selectable features with the `x-govstack-digital-registries` extension.
Omitting `features` or publishing an empty array declares none. Together, the metadata and selected
Consultation operations provide the Core + Consultation contract.

[extensions/](extensions/) holds the JSON Schemas for the extension and for the
compacted metadata document.

A deployment publishes its selected operations with concrete schemas for
`data`, selector values, search criteria, and supported sorting. Its contract
declares collection scope, source currency, security, limits, continuation
rules, and any conditional-read, field-selection, complete-traversal, or
snapshot-traversal feature it implements. A deployment can additionally select
recorded-time, effective-time, or purpose-bound on an applicable operation.
Temporal GET inputs use `recordedAsOf` and `effectiveAt` query parameters; POST
Lookup and Search bindings carry the same coordinates in a closed `temporal`
request object. Omission selects current state. A temporal response echoes the
selection in source-backed top-level `temporal` metadata and never substitutes
current state when the selected state is unavailable.
Timestamp coordinates and revision recording times use UTC instants serialised
with `Z`. Calendar dates stay dates. The shared `effectiveAt` schema supports dates
or UTC instants; the birth profile narrows it to calendar dates in requests and
response metadata.

Revision operations publish only retained source history and apply current
authorisation and disclosure to every returned revision. `revision.revisionId`
is required and `revision.recordedAt` is included only when source-backed. A
Revision List cursor is bound to its parent `recordId` and the complete request;
cross-Record replay returns `400 invalid-cursor`.
The selectable caller capability document is authenticated, caller-filtered,
bounded, served with `Cache-Control: no-store`, and does not promise access to
any particular Record. Capability and feature annotations are open advisory
vocabularies: clients skip unknown capability entries and ignore unknown feature
annotations on recognised capabilities. Current authorisation remains decisive.
Purpose-bound operations accept purpose only from the declared trusted binding,
never from a request URI, query, body, or ad hoc header.
The [OpenAPI examples](../resources/api-examples/README.md) show business reads, household
memberships, and birth-registration parent details.

[coverage.yaml](coverage.yaml) contains no numbered DRAFT claims in the current draft. Requirement front matter
provides operation links. Previous numbered mappings remain in Git history. [Common component provenance](common/README.md) pins the vendored
schemas for local reference resolution.

## Validation

From the repository root, validate the four OpenAPI documents, domain schemas,
inline examples, positive and negative fixtures, the Registry context extension
of every operation, and the discovery examples against their schemas and the
Registry Core page:

```sh
uv run --with-requirements tools/requirements-api.txt python tools/validate_consultation.py
```

With the sibling `govstack-api-design-guide` checkout at guide/ruleset `0.3.0-draft` and its
documented linter dependencies installed, run the canonical artifact gate:

```sh
uv run --with-requirements tools/requirements-api.txt node ../govstack-api-design-guide/linter/cli.mjs --repo-root .
```

The checks validate current artifacts and local dependencies. Registry Identifiers
are resolved against the metadata example only in the business contract, the one
contract that example describes; the canonical, household, and birth-registration
contracts use illustrative identifiers. The guide gate checks canonical discovery,
requirement coverage, and the OpenAPI and Spectral rules for the canonical
contract and the example contracts.
[Implementation tests](../resources/testing.md) cover runtime authorisation,
source behaviour, and cursor guarantees.

The guide's shallow-path recommendation (§5.4) reports the selected Collection,
Record, and revision hierarchy on the canonical and concrete Revision List and
Revision Retrieve paths. The [binding rationale](../requirements/registry-services.md#consultation-resource-paths-identity-and-api-composition)
explains that deliberate depth. These warnings are retained for review; no
approved guide exception is claimed.

## Historical artifacts

`legacy/generated-crud/` preserves APIs from earlier releases for migration
analysis. Release context and contributor credits are in the
[legacy API README](legacy/generated-crud/README.md). Current Consultation
validation uses the artifacts listed above.

## Write contract

[write.openapi.yaml](write.openapi.yaml) defines the DRAFT Write transport separately from the unchanged Consultation contract. Direct creation, update, named transitions, and approval-based change requests are independently selectable. [Write binding](../requirements/registry-services.md#write-write) documents shared guarantees; [write-coverage.yaml](write-coverage.yaml) maps DRAFT keys to verification and operations. The separate [Write operation extension](extensions/x-govstack-digital-registries-write.schema.json) does not widen the closed Consultation extension.

The [non-normative Write examples](../resources/api-examples/README.md#non-normative-write-examples) illustrate birth registration, household creation using existing and newly created individuals, and later membership additions. Their domain models are illustrative choices and add no requirements to the shared contract.

Run the Write artifact gate with:

```sh
uv run python tools/validate_write.py
```

The gate validates schemas, examples, required headers, request/result identity, and declared relationships. It does not execute authorisation, approvals, source transactions, or idempotency enforcement. Runtime scenarios are in [Write verification](../resources/write-testing.md).

### Guide validation of Write

The normative Write reference can be checked independently:

```sh
uv run node ../govstack-api-design-guide/linter/cli.mjs --repo-root . --openapi api/write.openapi.yaml
```

The canonical Write reference retains a documented shallow-path SHOULD warning for the Collection, Record, and transition hierarchy; no approved guide exception is claimed. The current guide driver's reference-origin pass over the non-normative [Write example contract](examples/write-examples.openapi.yaml) exits with `Maximum call stack size exceeded` on a valid recursive domain-schema graph. This is a tool limitation, not a passing example-guide result. Offline OpenAPI, domain-schema, mirror-equivalence, and exchange checks validate the examples separately. Example fields borrowed from an external model retain their source spellings under the guide's external-model naming rules.
