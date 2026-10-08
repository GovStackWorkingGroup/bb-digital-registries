---
description: Capability families provided by the Digital Registries Building Block.
---

# 5 Key Functionalities: API Families

The Digital Registries Building Block groups its externally visible capabilities into eight families. A family describes an adopter outcome and a coherent trust boundary. It does not prescribe an internal module, product architecture, or transport.

The [conformance model](04-conformance.md#43-conformance-model) requires Registry Core and at least one declared Registry capability. All API families and operations, including Consultation Retrieve, are optional.

<figure><img src=".gitbook/assets/api-families.svg" alt="Digital Registries Building Block capability families"><figcaption>Registry Core provides the mandatory shared foundation. Implementations select capabilities from optional families.</figcaption></figure>

## 5.1 Reading capability requirements

Requirements are placed with the capability to which they apply. Shared requirements are defined under [Registry Core](05-api-families/registry-core.md), while family-specific requirements are defined on the applicable family page.

[Requirement Maturity](04-conformance.md#41-requirement-maturity) defines requirement classification, governance dependencies, and conformance status. Informative capability descriptions do not create requirements.

## 5.2 Registry Core

Registry Core provides the identity, metadata, discovery, stable Record references, schema context, and field meanings shared by every API family. It also defines how supplied revision, lifecycle, and provenance metadata are described. It is not itself an API family. Each selected capability inherits the applicable [Registry Core model and requirements](05-api-families/registry-core.md). Requirements for returned Records apply when a capability returns Records.

Registry Core requires publication of machine-readable Registry and service metadata. Service descriptions identify exposed API families, endpoints, and operational contracts. This publication can use static metadata and does not require a Provisioning API. Paths, methods, parameters, schemas, and security details belong in the linked operational contract, such as OpenAPI.

## 5.3 Family catalogue

Consultation is the only family with requirements and a contract in this release.

| Family | Adopter outcome | Capabilities | Status in this release |
|---|---|---|---|
| [Consultation](05-api-families/consultation.md) | Obtain a permitted representation of Registry information. | Retrieve, Lookup, List, Search | DRAFT requirements and a draft HTTP contract. Existence Check, Revision History, Record Match, and GIS Query are described informatively. |

The remaining families are informative roadmap descriptions. They have no requirements, contracts, or tests in this release.

| Family | Adopter outcome | Capabilities |
|---|---|---|
| [Provisioning](05-api-families/provisioning.md) | Configure a Registry service and publish its externally visible contracts. | Metadata administration, schemas, capability publication, bulk transfer |
| [Evidence](05-api-families/evidence.md) | Obtain a signed assertion derived from authoritative Registry information. | Direct attestation, wallet-mediated credential, status |
| [Write](05-api-families/write.md) | Create a Record or accept a new authoritative revision. | Direct write, governed write, correction |
| [Notification](05-api-families/notification.md) | Inform authorised subscribers that Registry state changed. | Subscribe, filter, deliver, retry, replay |
| [Aggregate Data](05-api-families/aggregate-data.md) | Obtain approved statistics derived from Registry Records. | Aggregate query, dataset metadata, published release |
| [Access Transparency](05-api-families/access-transparency.md) | Obtain a permitted view of access to a related Record. | Access-history consultation |
| [Identity Federation](05-api-families/identity-federation.md) | Authenticate a person represented by a sectoral Registry Record to a Relying Service and release authorised claims. | Profile ownership and binding to be decided with the Identity team; cross-BB ownership unresolved |

## 5.4 Selecting families

An adopter selects capabilities from the Registry's institutional responsibilities, domain model, and consumer needs, not from the feature list of a particular product. Useful questions include:

- Do consumers know Record Identifiers, need exact lookup by a domain identifier, or need collection browsing or search?
- Does the Registry expose historical revisions, mutation, events, evidence, statistics, or subject authentication?
- Which actors can invoke each capability, and what may each actor learn?
- Does the Registry own an approval process, or accept an approved result from another service?
- Does the consumer need live Registry information, a portable proof, or notification that state changed?
- Which sector semantic model and protocol binding fit the participating systems?

Each family page states its boundary and maturity. A registry or sector profile supplies domain-specific schemas, field meanings, declared selectors and search criteria, and other constraints needed by its selected capabilities. It defines lifecycle and revision semantics when those are provided or required. [Capability Claims](04-conformance.md#44-capability-claims) defines the requirements for claiming a selected capability.
