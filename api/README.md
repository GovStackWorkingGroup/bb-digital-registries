# API artifacts

[openapi.yaml](openapi.yaml) defines the DRAFT Consultation HTTP contract:
OpenAPI **3.1.2**, API version **1.0.0-draft**, targeting API Design Guide and
ruleset **0.2.0-draft**. The `/v1` path identifies the HTTP compatibility line;
the Building Block specification has its own version.

| Capability | HTTP path | Success |
| --- | --- | --- |
| Retrieve | `GET /v1/records/{recordId}` | Record |
| List | `GET /v1/records` | RecordPage |
| Exact Lookup | `POST /v1/records:lookup` | Record |
| Named Search | `POST /v1/records:search` | RecordPage |

`records` is the reference collection name, and
`https://registry.example/registries/records` is a placeholder Registry Identifier.
Deployments publish concrete names, such as `/v1/businesses` or `/v1/households`,
declare the Registry Identifier from their Registry metadata, and select
capabilities for each collection. One API can expose several collections, each
with a declared Registry, membership scope, and operation schemas. Success responses share
`Record {recordId, data}` and `RecordPage {items, pageInfo}`.
Lookup and Search are synchronous reads. `/health` provides operational liveness.
`GET` and `HEAD /.well-known/api-catalog` serve the RFC 9727 linkset at the origin
root, outside any routing prefix.

The server URL identifies the deployment root, optionally with a stable prefix
such as `/registry`. The major version precedes the collection in each operation
path. API-family labels describe capabilities; families can share resource paths
with distinct HTTP methods, schemas, and access requirements.

The shared Record schemas apply the [Registry Core](../spec/05-api-families/registry-core.md)
representation rules. Core metadata is published as a JSON-LD document that the
RFC 9727 `/.well-known/api-catalog` linkset locates. It identifies the Registry and
its authority and links each service to its deployed OpenAPI contract. Every
Consultation operation declares its Registry, collection, capability, and view
with the `x-govstack-digital-registries` extension. Together, the metadata and
selected Consultation operations provide the Core + Consultation contract.

[extensions/](extensions/) holds the JSON Schemas for the extension and for the
compacted metadata document.

A deployment publishes its selected operations with concrete schemas for
`data`, selector values, search criteria, and supported sorting. Its contract
declares collection scope, source currency, security, limits, and continuation rules.
The [OpenAPI examples](examples/README.md) show business reads, household
memberships, and birth-registration parent details.

[coverage.yaml](coverage.yaml) maps DRAFT requirements to operations or review
evidence. [Common component provenance](common/README.md) pins the vendored
schemas for local reference resolution.

## Validation

From the repository root, validate the four OpenAPI documents, domain schemas,
inline examples, positive and negative fixtures, the Registry context extension
of every operation, and the discovery examples against their schemas and the
Registry Core page:

```sh
uv run --with-requirements tools/requirements-api.txt python tools/validate_consultation.py
```

With the sibling `bb-template` checkout at guide/ruleset `0.2.0-draft` and its
documented linter dependencies installed, run the canonical artifact gate:

```sh
uv run --with-requirements tools/requirements-api.txt node ../bb-template/api-design-guide/linter/cli.mjs --repo-root .
```

The checks validate current artifacts and local dependencies. Registry Identifiers
are resolved against the metadata example only in the business contract, the one
contract that example describes; the canonical, household, and birth-registration
contracts use illustrative identifiers. The guide gate checks canonical discovery,
requirement coverage, and the OpenAPI and Spectral rules for the canonical
contract and the example contracts.
[Implementation tests](../spec/11-testing.md) cover runtime authorization,
source behavior, and cursor guarantees.

## Historical artifacts

`legacy/generated-crud/` preserves APIs from earlier releases for migration
analysis. Release context and contributor credits are in the
[legacy API README](legacy/generated-crud/README.md). Current Consultation
validation uses the artifacts listed above.
