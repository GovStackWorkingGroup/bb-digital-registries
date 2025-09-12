---
description: This section provides context for this Building Block.
---

# 2 Description

The Digital Registries Building Block provides services to other Building Blocks and to external systems, to store and manage data/claims on any entity (persons, places, and things) in forms of uniquely identiﬁable records in a database.

The Digital Registries Building Block (BB) is a trusted, authoritative service that stores, manages, and provides access to uniquely identifiable records about entities such as persons, organizations, places, assets, and events. It is designed to act as the single source of truth within the GovStack ecosystem, ensuring consistency, reliability, and accountability in the use of registry data.

A registry is not limited to a database table but can be viewed as a document, logically assembled from one or multiple underlying databases or sources. This document-centric view allows the registry to be queried to provide authoritative answers, ensuring interoperability and consistency across systems.

The Digital Registries BB enables other Building Blocks, government institutions, and external systems to capture, validate, store, search, distribute, and present registry record in a secure and standardised and uniquely identiﬁable manner. By abstracting the complexity of underlying databases, it exposes consistent service APIs that allow seamless integration and reuse across multiple domains and applications.

The Digital Registries BB provides a generic, domain-agnostic solution to create and maintain registries that serve as authoritative sources of information. It can be applied across multiple sectors and contexts, including but not limited to:

* Health and medical information
* Ownership of property, vehicles, and other assets
* Banking and commercial transactions
* Civil registration (births, deaths, marriages, etc.)
* Education and qualifications
* Land surveys and manufacturing details

The Building Block provides the capability to capture, store, search, distribute, and present data with zero or minimal need for software development. It also maintains and reports logs of all operations taking place on database schemas and data. It contains various functional components, and data resources to abstract away all the details and complexity, and to expose capabilities as service-APIs to external Building Blocks/applications.

The Digital Registries BB works in close coordination with other GovStack components:

* Registration BB – for onboarding and managing entity lifecycle.
* Foundational ID BB – for uniquely identifying entities.
* Workflow BB – for orchestrating business processes tied to registry data.
* Information Mediator / Consent & Authorisation – for secure, policy-driven data exchange across organisations.

The Digital Registries Building Block is an optional Building Block for other GovStack Building Blocks that have the need to store information. Any traditional database platform could be used alone or in combination with Digital Registries Building Block. The Digital Registries Building Block can operate as a standalone service and could be implemented as one centralized instance per domain, containing multiple registries in one instance, or many instances per domain, each database in its own server.

![Illustration 1- Digital Registries Building Block in GovStack sandbox](<.gitbook/assets/Illustration 1- Digital Registries BB in GovStack sandbox.png>)
