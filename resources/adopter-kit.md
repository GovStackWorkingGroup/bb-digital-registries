---
description: The four artifacts an implementation publishes, with the files to start from.
---

# Adopter kit

An implementation of Registry Core with selected Consultation or Write services publishes four artifacts. The rest of this specification explains what they mean; this page lists them so that an implementer knows what to produce.

| Artifact | Where it is served | Start from | Defined by |
|---|---|---|---|
| OpenAPI contract, one per API | A stable URL chosen by the deployment | The [example matching the selected capabilities](../api/examples/README.md), using the [Consultation](api.yml) or [Write](write-api.yml) contract as applicable | [Consultation HTTP binding](consultation-binding.md#http-binding) and [API composition](registry-core-model.md#api-composition) |
| Registry metadata document | A stable document URI, served as `application/ld+json` | [Registry metadata example](../api/examples/registry-metadata.jsonld), validated by the [metadata document schema](../api/extensions/registry-metadata.schema.json) | [Registry metadata](registry-core-model.md#registry-metadata) |
| API catalog linkset | `/.well-known/api-catalog` at the API origin, served as `application/linkset+json` | [API catalog example](../api/examples/api-catalog.linkset.json) and the `/.well-known/api-catalog` path of the [canonical Consultation OpenAPI](api.yml) | [Discovery publication](registry-core-model.md#discovery-publication) |
| Health endpoint | `/health` relative to the OpenAPI server URL, including any routing prefix | The `/health` path of the [canonical Consultation OpenAPI](api.yml) | GovStack API Design Guide, unversioned health endpoint |

## Producing the artifacts

1. **Contract.** Choose the example matching the capabilities and features you need. The household and birth-registration examples show concrete logical Collections; the business example selects additional Consultation behaviour. Replace the literal `collectionId` and Record schema while preserving the `/v1/collections/{collectionId}` hierarchy and shared `$ref` links for parameters, headers, responses, and security schemes. Every selected Collection-scoped Consultation operation keeps its `x-govstack-digital-registries` declaration, with `registry` set to your Registry Identifier and `collection` equal to its path value. Add only the capabilities and selectable `features` the operation implements and can verify; an omitted or empty array declares none. A `purpose-bound` operation also requires its trusted `purpose` declaration. Caller capability discovery uses its separate bounded response schema. Align each selection with its inputs, response headers, schemas, responses, and guarantees.
2. **Metadata document.** Describe one Registry (`@id`, `title`, `description`, `authority`, `specification`, `dataService`) and one data service per API (`serviceType`, `endpointURL`, `endpointDescription` pointing at the contract). Validate the document against the metadata document schema with any JSON Schema validator. The document is plain JSON; RDF tooling is not needed unless a catalogue integrator wants it, in which case the [metadata vocabulary appendix](metadata-vocabulary.md) explains the mapping.
3. **Linkset.** Serve the API catalog with one `service-desc` link per contract and one `service-meta` link to the metadata document.
4. **Health.** Expose `/health` relative to the OpenAPI server URL, for example `/registry/health` when that URL includes `/registry`.

## Checking the artifacts

The repository's [artifact validator](../tools/validate_consultation.py) checks the example contracts, schemas, fixtures, metadata document, and linkset shipped with this specification; the [validation commands](../api/README.md#validation) show how to run it and how to lint a contract with the GovStack API Design Guide linter. Adopters run the same linter against their own contract and validate their metadata document against the schema. [Testing](testing.md) covers verification of a deployed implementation.

## What is not needed

- A catalogue API or Provisioning API: static documents satisfy discovery.
- All Consultation or Write operations: the draft variation point selects at least one, as described in [Conformance](conformance.md#draft-conformance-model). Direct writes and approval-based writes remain independently selectable.
- Conditional requests, caller-selected fields, exhaustive traversal, or source snapshots unless the operation declares the corresponding feature.
- Revision history, recorded-time or effective-time selection, caller capability discovery, or purpose binding unless the corresponding capability or feature is selected.
- Revision, lifecycle, or provenance metadata, unless a selected profile requires it.

## Adopting Write

Select the direct operations or approval-based route the source and policy support, using the [Write contract](write-api.yml) and [binding](write-binding.md). Publish the concrete input schemas, named transitions, grants, trusted purpose rules where selected, strong validator source, idempotency replay contract, and commit boundaries. Approval-only deployments publish request and review operations without granting direct write access. Returned acknowledgements do not imply permission to retrieve every resulting Record.

The [non-normative Write examples](../api/examples/README.md) show one possible set of domain bindings, not a required data model. Document the institution's chosen model version, mappings, extensions, and licence attribution. Validate Write artifacts with `uv run python tools/validate_write.py`; use [Write verification](write-testing.md) for implementation scenarios.
