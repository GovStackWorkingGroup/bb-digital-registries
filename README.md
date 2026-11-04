# Digital Registries Building Block Specification

Version **3.0.0-alpha.2**, an authoring draft. The specification inherits
`govstack-cfr-2.1.0`. Its requirements remain DRAFT and do not establish an
implementation conformance or certification claim.

The Digital Registries Building Block defines interoperable behaviour for software
that maintains authoritative records about persons, organisations, places, assets,
or events. It specifies Registry identity, authority, metadata, discovery, stable
Record references, and permitted representations without prescribing a database
product, administrative user interface, storage model, deployment topology, or
domain data model.

The target conformance model combines Registry Core with at least one declared
Registry operation. This draft defines six independently selectable Consultation options and four
Write options: direct creation, direct update, direct named transition, and
approval-based change requests. No particular operation is universal. A deployment
can offer direct writes, approval-based writes, both, or only declared reads.
The other six API families remain informative roadmap material until their
requirements, contracts, and tests are defined.
Business-outcome capabilities in `metadata.yml` are informative and are realised
by the functionalities; operation choices are declared by option key.

The six Consultation operations share a Record representation and bounded
pagination over explicit logical Collections. Operations can separately declare
conditional reads, field selection, complete traversal, snapshot traversal,
recorded-time, effective-time, or purpose binding; caller capability discovery is
also selectable. The HTTP binding supplies Registry, Collection, schema, capability,
and selectable feature declarations through each operation's versioned contract.
Source history, revision, lifecycle, recording-time, and effective-time metadata
remain conditional on the source and the selected capability or feature.

## Reading guide

- **Government architects:** start with the [overview](introduction/overview.md)
  and [scope](introduction/scope.md) for the system boundary and neighbouring
  Building Blocks.
- **Procurement teams:** read [conformance](resources/conformance.md) and
  [coverage and limitations](resources/README.md#coverage-and-limitations).
  Cite an approved specification version when one is available.
- **Implementers:** start with the [adopter kit](resources/adopter-kit.md), then
  [Discover Registry Services](requirements/registry-discovery.md),
  [Provide Registry Services](requirements/registry-services.md), and the
  [Consultation HTTP binding](resources/consultation-binding.md) or
  [Write HTTP binding](resources/write-binding.md). The
  [non-normative Write examples](resources/api-examples/README.md) illustrate birth
  registration and household creation without imposing a domain model.
- **Assessors:** use the [verification procedures](resources/testing.md) and the
  applicability declarations in each functionality file.

<figure><img src="assets/api-families.svg" alt="Digital Registries API-family catalogue"><figcaption>The catalogue retains the previous draft's API-family terminology; selected operations are represented as options in the requirement model.</figcaption></figure>

## API references

The [Consultation API](resources/api-reference.md) and
[Write API](resources/write-api-reference.md) describe the draft transport contracts.
The [API examples](resources/api-examples/README.md) show illustrative deployment
bindings and do not add requirements to those contracts.

## Source and contributions

The [Digital Registries repository](https://github.com/GovStackWorkingGroup/bb-digital-registries)
contains the source, contributor instructions, validation tools, and Git history.

## Attribution

Current coordinating authors are Sebastian Leidig, Jeremi Joslin, and David Higgins.
The [version history](resources/version-history.md) and
[release notes](resources/history/release-notes.md) retain historical authors,
coordinators, editors, reviewers, and changes.

The [repository licence](LICENSE) applies to the specification source.
