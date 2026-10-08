---
description: Purpose, scope, architecture, and exclusions of the Digital Registries Building Block.
---

# 2 Description and Scope

## 2.1 Purpose

The GovStack Common Terminology defines the general concept of a Registry. A Digital Registries implementation exposes services over records for which a named authority accepts responsibility within a defined scope. Examples include business registrations, land titles, vehicle registrations, professional licences, programme enrolments, and civil events. A service can provide a permitted Record representation, signed evidence, approved statistics, or another declared Registry capability.

The Digital Registries Building Block defines the external behaviour that allows applications and other Building Blocks to use those records consistently. Its interoperability contract is independent of database technology, internal modules, administrative tools, and deployment model.

Authoritative means that a named Registry Authority is institutionally responsible for maintaining a Record within the declared scope. Completeness and accuracy are separate data-quality properties.

## 2.2 Scope

This specification covers:

- identification and description of a registry, its authority and scope, and its available services;
- stable identification of Registry Records within a declared scope;
- independently optional Retrieve, exact Lookup, List, and Search of permitted Record representations;
- declaration of representation formats, schemas, documented field meanings, supported capabilities, and protocol bindings;
- interpretation of source revision, lifecycle, and provenance information when supplied; and
- optional capabilities for provisioning, consultation, evidence, writing, notifications, aggregate data, access transparency, and identity federation.

The specification applies to registries containing records about persons, organisations, places, assets, or events. Their contracts document the domain-specific field meanings and can reference a formal semantic model. A selected profile or capability can require additional source metadata or a specific semantic model.

The [conformance model](04-conformance.md) combines Registry Core with at least one selected capability. Every implementation publishes discovery metadata for its exposed Registry services. Each capability defines its result, which can be a Record representation or another form of Registry information.

## 2.3 Architectural approach

The specification separates four concerns:

1. **Operations** describe what an API consumer can ask the registry to do.
2. **Common context** identifies the Registry, scoped Record reference, representation format, and schema through the endpoint, versioned contract, or response as the binding specifies. Supplied source revision, lifecycle, and provenance metadata have documented meanings.
3. **Domain semantics** document field meanings and can use a published semantic model.
4. **Bindings** map operations to HTTP, event-driven messaging, or an established industry protocol.

This separation lets an existing national registry, a commercial product, an open-source platform, or an adaptor conform to the same external contract without sharing an internal architecture.

## 2.4 Deployment and composition

An implementation may operate one registry or many registries. It may be centralised or distributed, and may use relational, document, graph, event-sourced, or other storage approaches. These choices do not affect conformance unless they change externally observable behaviour.

A Registry can operate independently. Where other GovStack Building Blocks are deployed, they can provide complementary capabilities such as citizen-facing intake, workflow orchestration, organisational data exchange, consent management, digital signatures, wallets, identity services, or geospatial processing.

## 2.5 Boundaries with neighbouring Building Blocks

A Registry can integrate with neighbouring Building Blocks without transferring its responsibility for authoritative records.

| Neighbouring Building Block | Boundary |
|---|---|
| Registration | Registration can collect submissions and manage an intake process. The Registry accepts an approved result, a governed change request, or declared state transitions according to its Write profile. |
| Workflow | Workflow coordinates a process across components. The Registry controls which record transitions it accepts and remains responsible for the resulting authoritative state. |
| Information Mediator | Information Mediator can provide cross-organisation addressing, routing, and transport controls. The Registry owns its operations, disclosure decisions, and records. |
| Consent | Consent can provide evidence or policy signals used in a disclosure decision. The Registry enforces the decision applicable to each request and supports other lawful bases where relevant. |
| E-Signature | E-Signature can perform signing operations. The Registry remains responsible for the meaning, issuance, status, and lifecycle of Registry Evidence. |
| Wallet | A Wallet can hold and present credentials issued through Evidence. The Registry remains the source of the asserted facts and is not required to operate a Wallet. |
| Identity | The [Identity Building Block](https://github.com/GovStackWorkingGroup/bb-identity/blob/main/spec/2-description.md) defines foundational identity services and describes integration with functional identities. A sectoral Registry owns its functional identifiers. [Identity Federation](05-api-families/identity-federation.md) addresses authentication to Relying Services; Registry API access control is a separate responsibility. |
| GIS | GIS can provide geospatial processing and visualisation. A spatial Registry remains responsible for its records and can expose an OGC-aligned GIS Query capability. |

These integrations are optional unless a selected capability profile states otherwise.

## 2.6 Out of scope

This specification does not prescribe:

- the legal act or governance process that establishes a Registry Authority;
- a universal domain data model;
- a database management system or storage topology;
- a no-code registry builder, administrative web interface, or form designer;
- mandatory multi-tenancy or automatic generation of CRUD APIs;
- the citizen-facing intake and approval process for registration;
- a general-purpose workflow, rules, analytics, reporting, or data-exchange platform;
- a national foundational identifier; or
- jurisdiction-specific legal compliance or security control frameworks.

Reference architectures and implementation guides may explain how these concerns are addressed in particular domains or jurisdictions without making them part of base Registry conformance.
