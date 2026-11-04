# API artifacts

[openapi.yaml](openapi.yaml) defines the single DRAFT Registry HTTP contract:
OpenAPI **3.1.2**, API version **1.0.0-draft**, targeting API Design Guide and
ruleset **0.3.0-draft**. The `/v1` path identifies the HTTP compatibility line;
the Building Block specification has its own version.

[write.openapi.yaml](write.openapi.yaml) is a compatibility alias to
`openapi.yaml`, not a second Write contract. The publication entry points
[`resources/api.yml`](../resources/api.yml) and
[`resources/write-api.yml`](../resources/write-api.yml) resolve to the same
canonical contract.

## Operation groups

The contract groups operations by their role. A deployment publishes only the
Registry service options and supporting operations it implements.

| Group | Operations | Primary resources or results |
| --- | --- | --- |
| Read | Retrieve, List, exact Lookup, named Search, Revision List, and Revision Retrieve | Record, RecordPage, RecordRevision, and RevisionPage |
| Write | Create, Update, and named Transition | Authoritative Record commit or separately identified asynchronous work |
| Change Requests | Submit, list, retrieve, approve, reject, and optional withdraw | Immutable proposal, review decision, and application outcome |
| Operations | Retrieve asynchronous status | Operation execution status |

Discovery and Health are common groups. Discovery includes the API catalog and
caller capability operations; Health contains operational liveness.

Direct Create, Update, Transition, and Change Requests remain independently
selectable. A deployment does not have to offer every operation or both reads and
writes. Read, mutation, submission, review, application, and Operation-status
permissions remain separate.

`records` is the reference Collection name, and
`https://registry.example/registries/records` is a placeholder Registry
Identifier. Deployments publish concrete Collection names, declare the Registry
Identifier from their Registry metadata, and select operations for each
Collection. One API can expose several Collections, each with a declared Registry,
membership scope, operation schemas, and access requirements.
Read and Write resources use the same broad opaque `RecordId` schema. A Record
keeps that identifier across Collections and views within its Registry.

The server URL identifies the deployment root, which may include a stable prefix
such as `/registry`. The major version precedes the Collection in each versioned
operation path. `/health` provides operational liveness. `GET` and `HEAD
/.well-known/api-catalog` serve the RFC 9727 linkset at the origin root, outside
any routing prefix.

The default response language is English (`en`). A deployment may select another
default or localise Problem `title` and `detail`; it then declares that default
and follows API Design Guide §19 for `Accept-Language`, `Content-Language`, and
`Vary`.

## Registry and operation declarations

The shared Record schemas apply the [Registry Core](../requirements/registry-discovery.md#core-registry-core)
representation rules. Core metadata is published as a JSON-LD document that the
RFC 9727 API catalog locates. It identifies the Registry and its authority and
links each service to the deployed OpenAPI contract.

Every Collection-scoped read operation declares its Registry, Collection,
capability, view, and any selectable features with
`x-govstack-digital-registries`. Every selected primary Write operation declares
its Registry, Collection where applicable, capability, input schema, and
operation-specific binding metadata with
`x-govstack-digital-registries-write`. The operation contract also publishes its
input mapping and grant. The two extension vocabularies remain closed for the
versioned contract. They coexist in one API;
one does not widen the other. [extensions/](extensions/) holds their JSON Schemas
and the compacted metadata-document schema.

An Update or Transition declares a `companionRead` that identifies the shared
`retrieveRecord` operation for the exact same Registry, Collection, and view. Only
that designated use is a current authoritative guard view. Its body and strong
ETag come from one evaluation under the effective authorisation, disclosure,
purpose, and field-selection context. The tag is a valid strong validator for the
permitted representation and also invalidates when any authoritative field or
source condition changes in a way that can alter that mutation's validation,
mapping, or committed effect. Unrelated hidden state need not invalidate it.

The guard is opaque, encodes no source value, grants no authority, and does not
identify which state changed. A deployment cannot designate the view as a
companion when policy forbids disclosure of the tag or its change cadence. The API
publishes one `GET` for the Record resource, not a separate writable-only
retrieval operation. Read access remains separately authorised and is not a
prerequisite for granting Write access. Ordinary non-companion reads can retain
their declared source currency, including material lag, and need not publish a
strong validator.

Write inputs are operation-specific. They can differ from permitted read
projections and can carry evidence, reasons, or workflow context that is not
Record output. Accepted values map as declared to authoritative state, retained
provenance, or workflow-only context. A successful commit receipt establishes
the declared commit. It does not grant the caller read access, require automatic
field echo, guarantee immediate projection visibility or currency, or create a
revision-history guarantee.
A matching tag is expected only when a later companion Retrieve has reached
companion currency and observes that exact committed state, with no intervening
mutation-relevant change, under the same effective authorisation, disclosure,
purpose, and field-selection context. A shared view name alone does not establish
validator equality, and the contract does not promise that any future Retrieve
will eventually return the mutation success tag.

## Read behaviour

A deployment publishes concrete schemas for `data`, selector values, search
criteria, supported sorting, source currency, limits, continuation, access policy,
and any selected read features. Omitted or empty `features` declares none.

Temporal GET inputs use `recordedAsOf` and `effectiveAt` query parameters. POST
Lookup and Search carry the same coordinates in a closed `temporal` request
object. Omission selects current state. A temporal response echoes the applied
source-backed selection and does not substitute current state when the selected
state is unavailable. Timestamp coordinates and revision recording times use UTC
instants serialised with `Z`; calendar dates remain dates.

Revision operations publish only retained source history and apply current
authorisation and disclosure to every returned revision. `revision.revisionId`
is required, while `revision.recordedAt` is included only when source-backed. A
Revision List cursor is bound to its parent `recordId` and complete request.

Caller discovery is authenticated, caller-filtered, bounded, advisory, and served
with `Cache-Control: no-store`. Authentication uses the caller's trusted context
without requiring a universal Record-read scope merely to discover visible Write
operations. Collection-scoped entries appear under `collections`; cross-Collection
Change Request and asynchronous Operation entries appear in the optional root
`operations` array with their Registry context. Every operation entry identifies
its capability, contract, and operation ID. A recognised Consultation entry
requires its view and can carry read features, fields, selectors, searches, and
purpose annotations. Existing recognised read entries can omit `family`, which
means Consultation; new Write and supporting entries explicitly use
`family: write` and cannot carry those read annotations. Update and Transition
instead identify their `write.companionRead`. Unknown future capabilities remain
skippable and do not acquire read-view requirements. Current authorisation remains
decisive for every invocation. Discovery never promises access to a particular
Record or grants mutation, review, application, or status authority. Empty
`collections` with omitted or empty root `operations` means that no operation is
visible.

Purpose-bound operations accept purpose only from the declared trusted binding,
never from a request URI, query, body, or ad hoc header.

## Examples and coverage

The [OpenAPI examples](../resources/api-examples/README.md) show business reads,
household memberships, birth-registration parent details, direct commits, and
approval-based proposals. The examples select institution-specific domain models
and add no requirements to the shared contract.

Requirement front matter provides operation links. [coverage.yaml](coverage.yaml)
and [write-coverage.yaml](write-coverage.yaml) record the current artifact mappings.
[Common component provenance](common/README.md) pins the vendored schemas used for
local reference resolution.

## Validation

From the repository root, run:

```sh
uv run --with-requirements tools/requirements-api.txt python tools/validate_consultation.py
uv run python tools/validate_write.py
```

These gates validate the canonical contract, operation extensions, domain schemas,
examples, positive and negative fixtures, required headers, request and result
identity, and declared relationships. They do not execute authorisation,
approvals, source transactions, cursor behaviour, idempotency, or deployed source
semantics. Runtime scenarios are in [read verification](../resources/testing.md)
and [Write verification](../resources/write-testing.md).

With the sibling `govstack-api-design-guide` checkout at guide and ruleset
`0.3.0-draft` and its documented dependencies installed, run:

```sh
uv run --with-requirements tools/requirements-api.txt node ../govstack-api-design-guide/linter/cli.mjs --repo-root .
```

The guide's shallow-path recommendation (§5.4) reports the selected Collection,
Record, revision, and transition hierarchies. The
[binding rationale](../requirements/registry-services.md#consultation-resource-paths-identity-and-api-composition)
explains the deliberate depth. These warnings are retained for review; no approved
guide exception is claimed.

The guide driver's reference-origin pass over the non-normative
[Write example contract](examples/write-examples.openapi.yaml) can exit with
`Maximum call stack size exceeded` on its valid recursive domain-schema graph.
This is a tool limitation, not a passing example-guide result. Offline OpenAPI,
domain-schema, mirror-equivalence, and exchange checks validate the examples
separately.

## Historical artifacts

`legacy/generated-crud/` preserves APIs from earlier releases for migration
analysis. Release context and contributor credits are in the
[legacy API README](legacy/generated-crud/README.md). Current validation uses the
unified artifacts described above.
