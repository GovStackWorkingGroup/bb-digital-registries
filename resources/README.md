---
description: Draft coverage, limitations, and reading guidance for adopters.
---

# Coverage and reading guide

## Coverage and limitations

The `3.0.0-alpha.2` specification provides the Registry model, two core functionality files with unnumbered DRAFT requirements, and an HTTP contract for the independently selectable Retrieve, Lookup, List, Search, Revision List, and Revision Retrieve operation options. It also specifies selectable recorded-time, effective-time, caller capability discovery, reusable Search semantics, and purpose-bound behaviour. The [Write binding](write-binding.md) additionally defines four independently selectable DRAFT options for direct creation, update, named transitions, and approval-based change requests. The other six API-family pages remain informative roadmap material. [Requirement maturity](conformance.md#requirement-maturity) defines the current status.

| Area | Published material | Not specified or published |
|---|---|---|
| Conformance | DRAFT core with Discover Registry Services, Provide Registry Services, and the REQUIRED `registry-service` variation point selecting at least one operation option | Approved conformance claims and a standardised conformance-declaration serialisation |
| Registry Core | DRAFT requirements for metadata, scoped Record identity across logical Collections, schema context, documented field meanings, and interpretation of source metadata that is not required | Complete schema lifecycle and domain-specific compatibility policies |
| Metadata and discovery | JSON metadata document with schema, RFC 9727 discovery linkset, OpenAPI Registry context extension, examples, and an informative DCAT vocabulary appendix | Vocabulary, context, and schema publication at the assigned `vocab.govstack.global` IRIs; canonical specification-version IRIs |
| Authority | Registry Authority identity and declared authoritative scope | Delegation, shared responsibility, and a machine-readable mandate model |
| Operation options | DRAFT Consultation Retrieve, Lookup, List, Search, Revision List, and Revision Retrieve options and requirements, with selectable conditional-read, field-selection, complete-traversal, snapshot-traversal, recorded-time, effective-time, and purpose-bound features; reusable Search semantics and selectable caller capability discovery; four separately selected [Write options](write-binding.md) | Requirements, contracts, and tests for the six roadmap families and Consultation capabilities still described informatively |
| Service interfaces | [Canonical draft Consultation OpenAPI](api.yml), [Write OpenAPI](write-api.yml), shared schemas, and [concrete example contracts](api-examples/README.md) | Canonical contracts for the other six API families |
| Verification | Discovery, Consultation, and Write artifact validation; requirement-to-operation mapping; [Write implementation scenarios](write-testing.md) | End-to-end implementation conformance suite and deployed runtime evidence; artifact checks do not establish runtime behaviour |

Domain-specific semantic models and jurisdiction-specific governance or legal compliance are outside the Building Block's standardisation scope. Registry Authorities and adopting ecosystems supply these as appropriate to their services. Illustrative Collections such as birth, marriage, and death registrations do not define or constrain legal civil-registration scope. Field meanings must be documented even when no formal semantic model is selected. Source revision, lifecycle state, recording time, and effective-time history are not required unless a selected capability or feature requires them.

The Identity Federation family remains informative. This draft selects no protocol binding for that family.

## Reading guide

| Topic | Reference |
|---|---|
| Purpose, system boundary, functionalities, actors, and interfaces | [Overview](../introduction/overview.md) |
| Applicability and exclusions | [Scope](../introduction/scope.md) |
| Draft conformance and option declarations | [Conformance](conformance.md) |
| The artifacts an implementation publishes | [Adopter kit](adopter-kit.md) |
| Registry identity, authoritative scope, and metadata keys | [Registry Core metadata](registry-core-model.md#registry-metadata) |
| DCAT, RDF vocabulary, and JSON-LD context | [Metadata vocabulary](metadata-vocabulary.md) (informative) |
| Service discovery and linked operational contracts | [API family discovery](registry-core-model.md#api-family-discovery) and [Service Interfaces](service-interfaces.md) |
| Shared Record context and domain semantics | [Registry Core](registry-core-model.md#common-record-context) |
| API-family boundaries and roadmap | [API Family Catalogue](family-catalogue.md) |
| Retrieve, exact Lookup, List, Search, revisions, temporal selection, caller discovery, and purpose binding | [Consultation](consultation-binding.md) |
| HTTP contract, shared representation and pagination rules, and selectable operation features | [Consultation HTTP binding](consultation-binding.md#http-binding) and [canonical OpenAPI](api.yml) |
| Direct writes, approval requests, concurrency, and compound changes | [Write binding](write-binding.md), [canonical Write contract](write-api.yml), and [Write verification](write-testing.md) |
| Non-normative birth registration, households, individuals, and memberships | [Write examples](api-examples/README.md) and their [binding context](write-binding.md#non-normative-domain-examples) |
| Structured values and references | [Core representation rules](registry-core-model.md#structured-values-and-references) and [OpenAPI examples](api-examples/README.md) |
| Concrete adopter schema and fixtures | [Business Registry schema](../api/examples/business-registry.schema.json) and [request/response fixtures](../api/examples/consultation-exchanges.json) |
| Sectoral authentication and cross-Building-Block ownership | [Identity Federation](roadmap/identity-federation.md) |
| Verification scenarios | [Testing](testing.md) |

## Version history

The [version history](version-history.md) and [release notes](history/release-notes.md)
record specification changes and historical contributors. Previous requirement
text is available in the
[repository's Git history](https://github.com/GovStackWorkingGroup/bb-digital-registries/commits/main/).

The OpenAPI files under `api/legacy/generated-crud/` and Cucumber scenarios under `test/openAPI/` describe the previous generated CRUD interface. They are legacy artifacts and are not service contracts or conformance tests for this release. The legacy OpenAPI files do not contain a Retrieve-by-Identifier operation.

The [Testing resource](testing.md) distinguishes artifact validation from deployed implementation evidence.

## Reference architecture and implementation guidance

Actors, organisational responsibilities, domain governance, semantic choices, and multi-Building-Block deployment patterns belong in a Registry Reference Architecture or implementation guide. They are useful to adopters but do not alter the technical conformance contract in this specification.

See [References](../introduction/references.md) for standards and related GovStack material.
