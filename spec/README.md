---
description: Version 3.0.0-alpha.2
---

# Digital Registries Building Block Specification

`govstack-bb-digital-registries-3.0.0-alpha.2 extends govstack-cfr-2.1.0`

The Digital Registries Building Block defines interoperable behaviour for software that maintains authoritative records about persons, organisations, places, assets, or events. It specifies a mandatory Registry Core and a catalogue of optional capabilities that an implementation may support.

The conformance model combines Registry Core, including machine-readable Registry and service metadata, with at least one declared Registry capability. API families and operations are optional. The specification does not prescribe a database product, administrative user interface, storage model, deployment topology, or domain data model.

The current draft defines Consultation Retrieve, Lookup, List, and Search as independently optional capabilities, with a common Record representation and bounded collection pagination. [Service Interfaces](09-service-interfaces.md) introduces the canonical draft HTTP contract. The HTTP binding supplies Registry and schema context through a declaration on each operation of the versioned contract. Source revision, lifecycle, and recording-time metadata are optional unless a selected profile or capability requires them.

For this alpha's maturity and conformance status, see [Requirement Maturity](04-conformance.md#41-requirement-maturity). [Coverage and Limitations](12-other-resources.md#121-coverage-and-limitations) describes the available specifications and artifacts.

## How to use this specification

- **Government architects** should begin with [Description and Scope](02-description-and-scope.md) and [Conformance](04-conformance.md) to determine where a Registry fits within a digital government architecture.
- **Procurement teams** should use [Conformance](04-conformance.md) to understand capability claims and cite an approved specification version in a tender or acceptance contract.
- **Implementers** should begin with the [Adopter kit](12-other-resources/adopter-kit.md), which lists the four artifacts to publish, then read [Registry Core](05-api-families/registry-core.md), the selected [API families](05-key-functionalities.md), and [Service Interfaces](09-service-interfaces.md). The [illustrative business Registry contract](../api/examples/business-registry.openapi.yaml) shows a concrete mapping.
- **Conformance testers** should use [Testing](11-testing.md) for verification scenarios and their applicability.

## Authorship

Contributions, authors, coordinators, editors, and reviewers are recorded in the [Version History](01-version-history.md) and [Release Notes](01-version-history/release-notes.md).

_**Coordinating authors (3.0.0-alpha.2):**_ Sebastian Leidig, Jeremi Joslin, and David Higgins

<figure><img src=".gitbook/assets/api-families.svg" alt="Digital Registries Building Block capability families"><figcaption>The conformance model combines mandatory Registry Core with at least one selected capability.</figcaption></figure>
