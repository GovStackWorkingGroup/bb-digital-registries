---
description: Purpose, value, system boundary, functionalities, actors, and interfaces of the Digital Registries Building Block.
---

# Digital Registries Building Block

## Purpose

### Value

The Digital Registries Building Block exists so that governments and authorised service providers can discover governed registries and obtain permitted Registry information through consistent external contracts. A named Registry Authority remains institutionally responsible for each Registry within its declared scope. Authoritative means that the authority accepts responsibility for maintaining the Record in that scope; completeness and accuracy are separate data-quality properties.

| Capability | Value |
|---|---|
| Registry Service Discovery | An API consumer can identify a Registry, its responsible authority and authoritative scope, and locate the services and machine-readable contracts available to that consumer. |
| Authoritative Registry Services | An authorised consumer uses the Registry's declared services within its responsible authority's scope and access policy. |

Without a common specification, every consuming service must learn a different discovery mechanism, representation envelope, error model, and pagination contract. The common agreement supports interoperability between independently operated systems, makes implementations more replaceable, and gives buyers and assessors a stable basis for comparing externally observable behaviour.

### Place in larger systems

A Digital Registries implementation exposes services over records for which a named authority accepts responsibility. Examples include business registrations, land titles, vehicle registrations, professional licences, programme enrolments, and civil events. A Registry can operate independently. Where other GovStack Building Blocks are deployed, they can provide complementary citizen-facing intake, workflow orchestration, organisational data exchange, consent management, digital signatures, wallets, identity services, or geospatial processing.

The Registry Authority decides the authoritative scope and the applicable information-sharing and access policy. The implementation enforces the resulting decisions for each request. Neighbouring components do not acquire responsibility for the Registry's authoritative records merely because they collect, route, process, sign, hold, or visualise related information.

| Neighbouring Building Block | Boundary |
|---|---|
| Registration | Registration can collect submissions and manage an intake process. The Registry accepts an approved result, a governed change request, or declared state transitions according to an applicable Write profile. |
| Workflow | Workflow coordinates a process across components. The Registry controls which Record transitions it accepts and remains responsible for the resulting authoritative state. |
| Information Mediator | Information Mediator can provide cross-organisation addressing, routing, and transport controls. The Registry owns its operations, disclosure decisions, and records. |
| Consent | Consent can provide evidence or policy signals used in a disclosure decision. The Registry enforces the decision applicable to each request and supports other lawful bases where relevant. |
| E-Signature | E-Signature can perform signing operations. The Registry remains responsible for the meaning, issuance, status, and lifecycle of Registry Evidence. |
| Wallet | A Wallet can hold and present credentials issued through Evidence. The Registry remains the source of the asserted facts and is not required to operate a Wallet. |
| Identity | The [Identity Building Block](https://github.com/GovStackWorkingGroup/bb-identity/blob/main/spec/2-description.md) defines foundational identity services and describes integration with functional identities. A sectoral Registry owns its functional identifiers. [Identity Federation](../resources/roadmap/identity-federation.md) addresses authentication to Relying Services; Registry API access control is a separate responsibility. |
| GIS | GIS can provide geospatial processing and visualisation. A spatial Registry remains responsible for its records and can expose an OGC-aligned GIS Query capability. |

Reference architectures and domain or jurisdictional implementation guides can place the Digital Registries Building Block in larger systems without changing this specification's conformance contract.

## Description

### System under test

The system under test is a software component that publishes the identity, authority, scope, services, and contracts of one or more Registries and provides permitted Registry information through declared interfaces. It is assessed as a black box through those interfaces and through auditable evidence where a property, such as Record Identifier non-reassignment, cannot be established from one exchange.

The interoperability contract is independent of database technology, internal modules, administrative tools, deployment model, and whether an adaptor fronts an existing Registry. An implementation can be centralised or distributed and can use relational, document, graph, event-sourced, or other storage approaches. Those choices affect conformance only when they change observable behaviour or required evidence.

### Functionalities

| Functionality | Realises | Conformance | Description | Requirements |
|---|---|---|---|---|
| Discover Registry Services | Registry Service Discovery | Core | An API consumer identifies a Registry, its responsible authority and authoritative scope, and locates the Registry services and machine-readable contracts available to that consumer. | [`requirements/registry-discovery.md`](../requirements/registry-discovery.md) |
| Provide Registry Services | Authoritative Registry Services | Core | An API consumer uses the Registry service operations declared in the Registry's published contract. | [`requirements/registry-services.md`](../requirements/registry-services.md) |

Both functionalities are core, and this specification defines no extensions. Discover Registry Services prevents a metadata-free or contract-free service claim. Provide Registry Services contains the required `registry-service` variation point: a solution selects at least one operation. The six Consultation and four Write options currently defined are independently selectable; discovery metadata alone cannot satisfy the intended model. This is the Registry-wide service choice; future versions can add options from other API families when their requirements, contracts, and tests are approved. Consultation is not a permanent universal requirement. Publishing another option follows the framework's major-version rule.

The wire contract retains `capability` as its established field name. In that binding vocabulary, the values map to framework option keys as follows:

| Binding `capability` value | Framework option key | OpenAPI operation |
|---|---|---|
| `retrieve` | `consultation-retrieve` | `retrieveRecord` |
| `lookup` | `consultation-lookup` | `lookupRecord` |
| `list` | `consultation-list` | `listRecords` |
| `search` | `consultation-search` | `searchRecords` |
| `revision-list` | `consultation-revision-list` | `listRecordRevisions` |
| `revision-retrieve` | `consultation-revision-retrieve` | `retrieveRecordRevision` |
| Write `create` | `write-create` | `createRecord` |
| Write `update` | `write-update` | `updateRecord` |
| Write `transition` | `write-transition` | `applyRecordTransition` |
| Write `change-requests` | `write-change-requests` | `submitChangeRequest` |

The Write values belong to the separate Write operation extension; the existing Consultation extension remains closed to its six read capabilities. The binding field does not declare a framework capability. The framework capabilities are the informative outcomes Registry Service Discovery and Authoritative Registry Services.

### Actors

| Actor | Kind | Boundary | Reaches the Building Block through | Specified where |
|---|---|---|---|---|
| API Consumer | System or software component | Outside | Discover Registry Services; Provide Registry Services | The consumer is outside this specification. Its use of the exposed interfaces follows the linked operational contract. |
| Registry Authority | Organisation | Outside | Named by Discover Registry Services; it does not become part of the software under test | The adopting government's institutional and legal framework. |
| Registry Operator | Organisation | Outside | Operates the deployment through mechanisms that this specification does not define | The adopting government's operating model and implementation documentation. |

The Registry Authority and Registry Operator can be the same organisation or different organisations. The catalogue publisher can also be separate. Publication of an authority declaration does not by itself establish institutional responsibility; the adopting ecosystem determines how that declaration is accepted or verified.

### Interfaces

| Interface | Counterpart | Direction | Functionality | Type | Contract defined in |
|---|---|---|---|---|---|
| Registry service discovery | API Consumer | Inbound request, outbound response | Discover Registry Services | Service API | [`resources/api.yml`](../resources/api.yml), realised by [`requirements/registry-discovery.md`](../requirements/registry-discovery.md) |
| Registry metadata and operational contracts | API Consumer | Outbound published documents | Discover Registry Services | File | [Registry Core model](../resources/registry-core-model.md#registry-metadata) and the schemas and contracts linked from `resources/api.yml` |
| Registry consultation | API Consumer | Inbound request, outbound response | Provide Registry Services | Service API | [`resources/api.yml`](../resources/api.yml), realised by [`requirements/registry-services.md`](../requirements/registry-services.md) |
| Registry writes and approval requests | API Consumer | Inbound request, outbound response | Provide Registry Services | Service API | [`resources/write-api.yml`](../resources/write-api.yml), realised by the selected Write options in [`requirements/registry-services.md`](../requirements/registry-services.md) |
| Record schemas and field meanings | API Consumer | Outbound published documents | Provide Registry Services | File | The deployment's linked operational contract and schemas, constrained by the [Registry Core model](../resources/registry-core-model.md#domain-semantics-and-extensions) |

Logging, monitoring, deployment, and other interfaces inherited from the cross-functional requirements are not repeated here.
