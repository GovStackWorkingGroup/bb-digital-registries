---
description: Applicability, covered functionality, relationships, and exclusions of the Digital Registries specification.
---

# Scope

## Subject and applicability

This document specifies the Digital Registries Building Block, a software component that publishes governed Registry descriptions and service contracts and provides permitted Registry information through declared external interfaces.

It applies to software solutions that expose Registry services over records concerning persons, organisations, places, assets, or events. A solution can operate one Registry or many Registries and can be an adaptor over an existing system. The specification concerns externally observable behaviour and required evidence, not the solution's internal architecture.

The Consultation binding can group Records into logical Collections for stable API addressing and declared membership. A Collection is independent of database tables, source modules, governed datasets, and the Registry's institutional boundary. For example, `birth-registrations`, `marriage-registrations`, and `death-registrations` can be separate Collections in one civil-registration service. These are illustrative API choices, not a mandatory definition of civil-registration law or authoritative scope.

All requirements in this alpha draft remain `DRAFT` and unnumbered under the [agreed GovStack Requirements Model](https://github.com/GovStackWorkingGroup/specification-framework/blob/7322f977a6a74127240cbab5ed9d5ad84b9d5c29/chapters/requirements.md). They do not create a certification obligation, and this draft does not support a conformance claim.

## Relationships

This specification extends `govstack-cfr-2.1.0`. Every applicable parent requirement retains its original classifier and applicability conditions unless a Digital Registries requirement identifies a permitted extension or replacement.

The Building Block can participate in government services and domain architectures without transferring institutional authority for Registry records to another component. Reference architectures can define its role in those systems without importing additional requirements into this specification.

## Covered

The core covers both functionalities below. It defines no extensions.

- **Discover Registry Services:** identify a Registry, its responsible authority and authoritative scope, and locate its exposed services and machine-readable contracts.
- **Provide Registry Services:** provide at least one approved Registry service through the operations declared by the Registry's published contract.

Provide Registry Services includes a required Registry-wide variation point. Its currently defined DRAFT options are:

- `consultation-retrieve`: retrieve the current permitted Record representation by stable Record Identifier.
- `consultation-lookup`: resolve one Record through a declared exact selector.
- `consultation-list`: list a bounded declared Record collection.
- `consultation-search`: search through declared typed criteria and return bounded results.
- `consultation-revision-list`: list retained source revisions of one Record.
- `consultation-revision-retrieve`: retrieve one retained source revision.
- `write-create`: create a Record directly under the declared authority and input schema.
- `write-update`: update a Record directly using the declared patch and concurrency contract.
- `write-transition`: apply a published named transition directly.
- `write-change-requests`: submit and manage a proposed change through the declared review and application process.

The other six API families remain informative in this draft. A future version can define service options from those families when their requirements, contracts, and tests are approved; Consultation is not a permanent prerequisite for the Building Block. Only published options count toward the minimum, and adding a published option follows the framework's major-version rule. All options here remain DRAFT, so no current conformance claim is available.

The specification also covers:

- identification and description of a Registry, its authority, authoritative scope, and available services;
- stable identification of Registry Records within an unambiguous Registry context;
- declaration of representation formats, schemas, documented field meanings, and protocol bindings;
- interpretation of source revision, lifecycle, and provenance information when supplied;
- the shared Record envelope, error outcomes, disclosure behaviour, and live cursor pagination contract of the six read operations; and
- the HTTP binding and publication artifacts for the baseline Consultation interface.

The specification separates operations, common Registry and Record context, domain semantics, and protocol bindings. This separation lets national registries, commercial products, open-source platforms, and adaptors expose the same external contract without sharing an internal architecture.

## Not covered

| Excluded | Owned by |
|---|---|
| The legal act or governance process that establishes a Registry Authority | The adopting government's institutional and legal framework |
| A universal domain data model | The applicable sector authority, domain profile, or reference architecture |
| A database management system, storage topology, or internal product architecture | The implementation |
| A no-code registry builder, administrative web interface, or form designer | The implementation or a separate product specification |
| Mandatory multi-tenancy or automatic generation of CRUD APIs | The implementation |
| Citizen-facing intake and approval for registration | The Registration Building Block or the adopting service |
| General-purpose workflow, rules, analytics, reporting, or organisational data exchange | The Workflow, Analytics, or Information Mediator Building Block as applicable |
| Consent policy or the legal basis for disclosure | The Registry Authority and adopting legal framework; a Consent component can supply evidence or policy signals |
| A national foundational identifier | The Identity Building Block and the adopting government's identity architecture |
| Geospatial processing and visualisation | A GIS component or domain implementation guide |
| Jurisdiction-specific legal compliance and security control frameworks | The adopting government |
| Behaviour of API Consumers, Registry Authorities, and Registry Operators outside the defined interfaces | Their owning systems, institutional frameworks, and operating models |
| Provisioning, Evidence, Notification, Aggregate Data, Access Transparency, and Identity Federation conformance | Future requirements and contracts; current pages under [`resources/roadmap/`](../resources/roadmap/) are informative only |

Reference architectures and implementation guides can explain how these concerns are addressed in a domain or jurisdiction without making them part of base Digital Registries conformance.

## Ownership

The GovStack Registries and Registration Working Group owns this draft. Change requests follow the contribution process of the Digital Registries specification repository.

## Write scope

The [Write binding](../resources/write-binding.md) specifies independently selected direct creation, direct update, direct named transitions, and approval-based change requests. Registry-managed review concerns the proposed authoritative change; it does not require a general-purpose intake or workflow engine. Institutions define permissions, review policy, accepted transitions, and domain models. Domain data, legal decisions, and household or civil-registration rules are not standardised here. The [Write examples](../api/examples/README.md) remain non-normative and do not select a required domain schema for shared Write.
