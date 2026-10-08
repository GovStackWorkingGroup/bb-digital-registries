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

The 6 September 2026 revision of the `3.0.0-alpha.2` draft replaces universal Consultation Retrieve with a target conformance model of mandatory Registry Core plus at least one declared Registry capability. It strengthens Core metadata publication and service discovery, while leaving all API families optional. This is a revision of the same alpha draft, not a new release; no conformance claim is available.

The revision adds DRAFT requirements and a [canonical HTTP contract](../api/openapi.yaml) for four independently optional Consultation capabilities: Retrieve, Lookup, List, and Search. GET serves Retrieve and List; POST carries exact Lookup and Search criteria. All four share a Record representation. List and Search use live cursor pagination with repeated criteria and a fixed effective page size.

The Record model accepts stable source identifiers within a Registry and permits Registry and schema context through the endpoint, versioned contract, or response. Source revision, lifecycle, and recording time are optional unless a selected capability or profile requires them. Field meanings remain documented.

The [household](../api/examples/household-registry.openapi.yaml) and [birth-registration](../api/examples/birth-registration.openapi.yaml) contracts illustrate nested components, Record references, recorded related details, and bounded arrays with declared completeness. API Design Guide `0.2.0-draft` accompanies these choices. Contract and example validation is published separately from implementation conformance testing.

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

The detailed change record is preserved in the [Release Notes](01-version-history/release-notes.md).
