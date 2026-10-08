---
description: The four artifacts an implementation publishes, with the files to start from.
---

# Adopter kit

An implementation of Registry Core with Consultation publishes four artifacts. The rest of this specification explains what they mean; this page lists them so that an implementer knows what to produce.

| Artifact | Where it is served | Start from | Defined by |
|---|---|---|---|
| OpenAPI contract, one per API | A stable URL chosen by the deployment | [Business Registry example](../../api/examples/business-registry.openapi.yaml), which reuses the shared components of the [canonical Consultation OpenAPI](../../api/openapi.yaml) | [Consultation HTTP binding](../05-api-families/consultation.md#http-binding) and [API composition](../05-api-families/registry-core.md#api-composition) |
| Registry metadata document | A stable document URI, served as `application/ld+json` | [Registry metadata example](../../api/examples/registry-metadata.jsonld), validated by the [metadata document schema](../../api/extensions/registry-metadata.schema.json) | [Registry metadata](../05-api-families/registry-core.md#registry-metadata) |
| API catalog linkset | `/.well-known/api-catalog` at the API origin, served as `application/linkset+json` | [API catalog example](../../api/examples/api-catalog.linkset.json) and the `/.well-known/api-catalog` path of the [canonical Consultation OpenAPI](../../api/openapi.yaml) | [Discovery publication](../05-api-families/registry-core.md#discovery-publication) |
| Health endpoint | `/health` relative to the OpenAPI server URL, including any routing prefix | The `/health` path of the [canonical Consultation OpenAPI](../../api/openapi.yaml) | GovStack API Design Guide, unversioned health endpoint |

## Producing the artifacts

1. **Contract.** Copy the business example, rename its collection and Record schema, and keep the `$ref` links into the canonical OpenAPI for shared parameters, headers, responses, and security schemes. Every selected Consultation operation keeps its `x-govstack-digital-registries` declaration, with `registry` set to your Registry Identifier and `collection` equal to the path segment.
2. **Metadata document.** Describe one Registry (`@id`, `title`, `description`, `authority`, `specification`, `dataService`) and one data service per API (`serviceType`, `endpointURL`, `endpointDescription` pointing at the contract). Validate the document against the metadata document schema with any JSON Schema validator. The document is plain JSON; RDF tooling is not needed unless a catalogue integrator wants it, in which case the [metadata vocabulary appendix](metadata-vocabulary.md) explains the mapping.
3. **Linkset.** Serve the API catalog with one `service-desc` link per contract and one `service-meta` link to the metadata document.
4. **Health.** Expose `/health` relative to the OpenAPI server URL, for example `/registry/health` when that URL includes `/registry`.

## Checking the artifacts

The repository's [artifact validator](../../tools/validate_consultation.py) checks the example contracts, schemas, fixtures, metadata document, and linkset shipped with this specification; the [validation commands](../../api/README.md#validation) show how to run it and how to lint a contract with the GovStack API Design Guide linter. Adopters run the same linter against their own contract and validate their metadata document against the schema. [Testing](../11-testing.md) covers verification of a deployed implementation.

## What is not needed

- A catalogue API or Provisioning API: static documents satisfy discovery.
- Every API family: minimum conformance is Registry Core plus one declared capability, as defined in [Conformance](../04-conformance.md#43-conformance-model).
- Revision, lifecycle, or provenance metadata, unless a selected capability or profile requires it.
