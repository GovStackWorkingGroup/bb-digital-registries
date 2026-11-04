---
description: Major changes to the Digital Registries Building Block specification.
---

# 1 Version History

| Version | Contributors | Comment |
|---|---|---|
| 0.7, 0.8, and 0.9 | Initial authors and reviewers listed below | Initial drafts and technical review. |
| 1.0, May 2023 | Ingmar Vali; reviewers Steve Conrad, Wes Brown, and Valeria Tafoya | First GovStack 1.0-aligned release. |
| 2.0, November 2023 | Authors and editors listed below | Updated cross-cutting requirements, service APIs, and the test suite. Breaking change. |
| 3.0.0-alpha.1, June 2026 | Coordinators, authors, and editors listed below | Expanded scope and alignment work for GovStack Architecture 2.x. Public alpha release. |
| 3.0.0-alpha.2, August 2026 | Digital Registries Working Group | Reframed the alpha as a domain-neutral Registry Core with mandatory Consultation Retrieve and additional capability families. Breaking prerelease change. |

## Current alpha draft revision

The 6 September 2026 revision of the `3.0.0-alpha.2` draft replaced universal Consultation Retrieve with mandatory Registry Core plus at least one selected Registry service operation. The format migration expresses that rule as two core functionalities and the REQUIRED `registry-service` variation point with `select.min: 1`. This remains a revision of the same alpha draft, not a new release; no conformance claim is available.

The revision adds DRAFT requirements and a [canonical HTTP contract](api.yml) for four independently selectable Consultation operation options: Retrieve, Lookup, List, and Search. GET serves Retrieve and List; POST carries exact Lookup and Search criteria. All four share a Record representation. List and Search use live cursor pagination with repeated criteria and a fixed effective page size.

The 8 October 2026 revision distinguishes baseline pagination from selectable stronger operation features. Baseline List and Search publish bounded responses, deterministic ordering, fixed-size context-bound continuation, resource limits, and timeout behaviour without claiming exhaustive backend traversal. Operations can separately declare conditional Retrieve, field selection, complete traversal, or snapshot traversal; omitted features make no such promise.

The 29 October 2026 revision makes logical Collections explicit in the canonical `/v1/collections/{collectionId}` hierarchy and keeps Record identity stable across Collections. It adds selectable source-backed Revision List and Revision Retrieve capabilities, recorded-time and effective-time selection, reusable named Search semantics, caller-filtered capability discovery, and trusted purpose binding. The revision does not mandate a civil-registration legal model, a universal query language, historical storage, or purpose on every operation.

The Record model accepts stable source identifiers within a Registry and permits Registry and schema context through the endpoint, versioned contract, or response. Source revision, lifecycle, and recording time are not required unless a selected capability or profile requires them. Field meanings remain documented.

The [household](../api/examples/household-registry.openapi.yaml) and [birth-registration](../api/examples/birth-registration.openapi.yaml) contracts illustrate nested components, Record references, recorded related details, and bounded arrays with declared completeness. API Design Guide `0.3.0-draft` accompanies these choices. Contract and example validation is published separately from implementation conformance testing.

## Contributors by release

### Versions 0.7 and 0.8

Authors: Frank Grozel, Ingmar Vali, Tambet Artma, Saurav Bhattarai, Dr. P. S. Ramkumar, and Rauno Kulla.

Version 0.8 reviewers: Neil Roy, Aare Lapõnin, and Amy Darling.

### Version 0.9

Authors: Ingmar Vali, Sebastian Leidig, Frank Grozel, and Tambet Artma.

Technical reviewers: Tony Shannon, Saša Kovačević, Riham Moawad, Riham Fahmi, Aare Laponin, Manish Srivastava, Palab Saha, Surendra Singh Sucharia, Arvind Gupta, Gayatri P., Shivank Singh Chauhan, and Gavin Lyons.

Reviewers: Steve Conrad, Wes Brown, and Valeria Tafoya.

### Version 2.0

Authors: Sebastian Leidig, Steve Conrad, Łukasz Ruzicki, Damian Borowiecki, Karolina Kopacz, and Paweł Gesek.

Reviewer: Sebastian Leidig. Editors: Steve Conrad and Valeria Tafoya.

### Version 3.0.0-alpha.1

Coordinators: Dr. Bimal Kumar, Xilene Siquero, and Sebastian Leidig.

Authors: Janet Ngugi, Vivek Rana, Chinenye Ifebirinachi, Ananya Jha, Umang Gupta, Leonora Smart-Abbey, and Jeremi Joslin.

Editors: Ali González-García and David Higgins.

The detailed change record is preserved in the [Release Notes](history/release-notes.md).

## 4 November 2026 Write draft revision

The same unreleased alpha now defines separately selectable direct creation, direct update, direct named transitions, and approval-based change requests. The DRAFT [Write binding](write-binding.md) and [contract](write-api.yml) distinguish proposal review from authoritative application, protect source and proposal versions separately, and declare retry, disclosure, and compound-operation guarantees. The [birth and household examples](../api/examples/README.md) remain non-normative and do not select a required domain model. No release, implementation conformance claim, or deployed workflow is established by these artifacts.
