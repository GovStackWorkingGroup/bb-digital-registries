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

- **Architects and procurement teams:** read the [overview](introduction/overview.md)
  and [scope](introduction/scope.md) for purpose, boundaries, draft maturity, and
  conformance conditions.
- **Implementers:** use [Discover Registry Services](requirements/registry-discovery.md)
  for metadata and discovery, then [Provide Registry Services](requirements/registry-services.md)
  for the Record model, Consultation, Write, and workflows.
- **API consumers:** use the [Consultation](resources/api-reference.md) and
  [Write](resources/write-api-reference.md) references. The
  [API examples](resources/api-examples/README.md) illustrate deployment choices
  and add no requirements to the shared contracts.
- **Assessors:** use the [verification procedures](resources/testing.md),
  [Write verification](resources/write-testing.md), and the applicability
  declarations in the functionality files.

## Source and contributions

The [Digital Registries repository](https://github.com/GovStackWorkingGroup/bb-digital-registries)
contains the source, contributor instructions, validation tools, and Git history.

## Attribution

Current coordinating authors are Sebastian Leidig, Jeremi Joslin, and David Higgins.
The repository release history retains historical authors, coordinators,
editors, reviewers, and changes.

The [repository licence](LICENSE) applies to the specification source.
