---
description: Coverage, reader guidance, migration material, and references.
---

# 12 Other Resources

## 12.1 Coverage and limitations

The 3.0.0-alpha.2 specification provides the Registry model, DRAFT Core requirements, and DRAFT requirements and an HTTP contract for Consultation Retrieve, Lookup, List, and Search. Additional capabilities remain informative. [Requirement Maturity](04-conformance.md#41-requirement-maturity) defines its conformance status and dependency on the GovStack Common Requirements Framework.

| Area | Published material | Not specified or published |
|---|---|---|
| Conformance | DRAFT model of Registry Core plus at least one declared capability, with capability-specific applicability | Approved conformance claims and named multi-family conformance profiles |
| Registry Core | DRAFT requirements for metadata, scoped Record identity, schema context, documented field meanings, and the interpretation of optional source metadata | Complete schema lifecycle and domain-specific compatibility policies |
| Metadata and discovery | JSON metadata document with schema, RFC 9727 discovery linkset, OpenAPI Registry context extension, examples, and an informative DCAT vocabulary appendix | Vocabulary, context, and schema publication at the assigned `vocab.govstack.global` IRIs; canonical specification-version IRIs |
| Authority | Registry Authority identity and declared authoritative scope | Delegation, shared responsibility, and a machine-readable mandate model |
| Capabilities | DRAFT Consultation Retrieve, Lookup, List, and Search requirements; informative descriptions of other capabilities | Requirements, contracts, and tests for other capabilities, including Revision History |
| Service interfaces | [Canonical draft Consultation OpenAPI](../api/openapi.yaml), shared schemas, and [concrete example contracts](../api/examples/README.md) | Canonical contracts for other API families |
| Verification | Discovery, Retrieve, Lookup, and pagination workflows; verification scenarios; contract and example checks | End-to-end implementation conformance suite |
| Migration | Disposition of every previous DRS requirement | None |

Domain-specific semantic models and jurisdiction-specific governance or legal compliance are outside the Building Block's standardisation scope. Registry Authorities and adopting ecosystems supply these as appropriate to their services. Field meanings must be documented even when no formal semantic model is selected. Source revision, lifecycle state, and source recording time remain optional unless a selected profile or capability requires them.

Identity Federation profile ownership and binding remain subject to agreement with the Identity team.

## 12.2 Reading guide

| Topic | Reference |
|---|---|
| Service boundary, implementation choices, and neighbouring Building Blocks | [Description and Scope](02-description-and-scope.md) |
| Minimum conformance and capability claims | [Conformance](04-conformance.md) |
| The artifacts an implementation publishes | [Adopter kit](12-other-resources/adopter-kit.md) |
| Registry identity, authoritative scope, and metadata keys | [Registry Core metadata](05-api-families/registry-core.md#registry-metadata) |
| DCAT, RDF vocabulary, and JSON-LD context | [Metadata vocabulary](12-other-resources/metadata-vocabulary.md) (informative) |
| Service discovery and linked operational contracts | [API family discovery](05-api-families/registry-core.md#api-family-discovery) and [Service Interfaces](09-service-interfaces.md) |
| Shared Record context and domain semantics | [Registry Core](05-api-families/registry-core.md#common-record-context) |
| Capability boundaries and selection | [API Families](05-key-functionalities.md) |
| Retrieve, exact Lookup, List, Search, and additional read patterns | [Consultation](05-api-families/consultation.md) |
| HTTP contract and shared representation/pagination rules | [Consultation HTTP binding](05-api-families/consultation.md#http-binding) and [canonical OpenAPI](../api/openapi.yaml) |
| Structured values and references | [Core representation rules](05-api-families/registry-core.md#structured-values-and-references) and [OpenAPI examples](../api/examples/README.md) |
| Concrete adopter schema and fixtures | [Business Registry schema](../api/examples/business-registry.schema.json) and [request/response fixtures](../api/examples/consultation-exchanges.json) |
| Sectoral authentication and cross-Building-Block ownership | [Identity Federation](05-api-families/identity-federation.md) |
| Verification scenarios | [Testing](11-testing.md) |

## 12.3 Migration and history

- [Migration from the 3.0.0-alpha.1 Draft](12-other-resources/migration-from-3.0.md) records the disposition of every previous DRS requirement.
- [Release Notes](01-version-history/release-notes.md) preserve detailed historical contributors and changes.

The OpenAPI files under `api/legacy/generated-crud/` and Cucumber scenarios under `test/openAPI/` describe the previous generated CRUD interface. They are legacy artifacts and are not service contracts or conformance tests for this release. The legacy OpenAPI files do not contain a Retrieve-by-Identifier operation.

The [Testing chapter](11-testing.md) distinguishes artifact validation from deployed implementation evidence.

## 12.4 Reference architecture and implementation guidance

Actors, organisational responsibilities, domain governance, semantic choices, and multi-Building-Block deployment patterns belong in a Registry Reference Architecture or implementation guide. They are useful to adopters but do not alter the technical conformance contract in this specification.

See [References](12-other-resources/references.md) for standards and related GovStack material.
