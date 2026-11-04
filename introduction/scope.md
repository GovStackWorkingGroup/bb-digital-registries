---
description: Applicability, covered functionality, relationships, exclusions, and draft conformance boundaries of the Digital Registries specification.
---

# Scope

## Subject and applicability

API consumers need a consistent way to discover Registry services and use permitted Registry operations without depending on each solution's internal design. This Building Block Specification defines the external behaviour of software that publishes governed Registry descriptions and service contracts and provides read, direct Write, and approval-based operations through declared external interfaces.

It applies to software solutions that expose Registry services over records concerning persons, organisations, places, assets, or events. A solution can operate one Registry or many Registries and can be an adaptor over an existing system. A Registry can operate independently; other GovStack Building Blocks are complementary when a deployment uses them. The specification concerns externally observable behaviour and required evidence, not the solution's internal architecture, institutional model, or product design.

The Registry API can group Records into logical Collections for stable API addressing and declared membership. A Collection is independent of database tables, source modules, governed datasets, and the Registry's institutional boundary. For example, `birth-registrations`, `marriage-registrations`, and `death-registrations` can be separate Collections in one civil-registration service. These are illustrative API choices, not a mandatory definition of civil-registration law or authoritative scope.

## Relationships

This specification extends `govstack-cfr-2.1.0`. A Digital Registries implementation can participate in government services and domain architectures without transferring institutional authority for Registry records to another component. Reference architectures can define the implementation's role in those systems without importing additional requirements into this specification.

### Inherited cross-functional requirements <a href="#conformance-inherited-cross-functional-requirements" id="conformance-inherited-cross-functional-requirements"></a>

Every applicable parent requirement retains its original classifier and applicability conditions unless a Digital Registries requirement explicitly identifies a permitted extension or replacement under the GovStack Requirements Model. This draft defines no Registry-specific cross-functional extension or replacement. It does not impose a jurisdiction-specific security framework, a universal legal basis for data processing, or one deletion policy on every type of Registry.

## Covered

The current alpha material covers Registry Core plus selected read and Write operations in one Registry API contract. The specification's core covers both functionalities below and defines no extensions.

- **Discover Registry Services:** identify a Registry, its responsible authority and authoritative scope, and locate its exposed services and machine-readable contracts.
- **Provide Registry Services:** provide at least one approved Registry service through the operations declared by the Registry's published contract.

### Draft conformance model <a href="#conformance-draft-conformance-model" id="conformance-draft-conformance-model"></a>

Provide Registry Services contains the REQUIRED `registry-service` variation point with `select.min: 1`. Its ten currently defined DRAFT options are independently selectable:

| Option key | Operation | Behaviour | Binding `capability` value |
|---|---|---|---|
| `consultation-retrieve` | `retrieveRecord` | Retrieve the current permitted Record representation by stable Record Identifier | `retrieve` |
| `consultation-lookup` | `lookupRecord` | Resolve one Record through a declared exact selector | `lookup` |
| `consultation-list` | `listRecords` | List a bounded declared Record Collection | `list` |
| `consultation-search` | `searchRecords` | Search through declared typed criteria and return bounded results | `search` |
| `consultation-revision-list` | `listRecordRevisions` | List retained source revisions of one Record | `revision-list` |
| `consultation-revision-retrieve` | `retrieveRecordRevision` | Retrieve one retained source revision | `revision-retrieve` |
| `write-create` | `createRecord` | Create a Record directly under the declared authority and input schema | Write `create` |
| `write-update` | `updateRecord` | Update a Record directly using the declared patch and concurrency contract | Write `update` |
| `write-transition` | `applyRecordTransition` | Apply a published named transition directly | Write `transition` |
| `write-change-requests` | `submitChangeRequest` | Submit and manage a proposed change through the declared review and application process | Write `change-requests` |

A future claim against a published version will meet both core functionalities and at least one published option of this variation point. Only `PUBLISHED` options count toward `select.min`. Because every option in this alpha is DRAFT, no solution can yet satisfy the published-option rule. Publishing an additional option is a major change under the agreed framework; adding DRAFT options does not publish a new release.

Direct creation, update, and named transition options are selectable independently from approval-based change requests. An implementation offering only the approval route need not expose the corresponding direct mutation endpoints. The other six API families, Provisioning, Evidence, Notification, Aggregate Data, Access Transparency, and Identity Federation, remain informative and cannot satisfy the minimum. A future version can define options from those families when their requirements, contracts, and tests are approved. Consultation is not a permanent prerequisite for the Building Block.

Conditions are machine-readable. Each operation-specific requirement names its option key in `applies_when`; requirements that apply regardless of the selected option carry no selection condition. Conditions concerning source data or access policy are recorded in the requirement's `documentation`. This model does not depend on the former provisional capability-namespace approach.

Core requirements concerning returned Records apply through each selected option. Retrieve resolves a stable Record Identifier; Lookup resolves a declared exact selector; List and Search return bounded Pages; revision operations return source-backed retained history. Search also defines reusable typed comparison semantics that a named search can select independently. An authorised API consumer receives the permitted representation under the operation's declared currency, temporal, and traversal semantics, or a policy-appropriate unsuccessful outcome. Current access policy governs the permitted representation. Consumer guidance in binding and workflow descriptions is informative; conformance applies to implementations only.

An operation can also declare selectable Consultation features. `conditional-read` applies only to Retrieve; `field-selection` can apply to a declared read; `complete-traversal` and `snapshot-traversal` apply only to List or Search, and `snapshot-traversal` includes the `complete-traversal` guarantee. `recorded-time` and `effective-time` add temporal selectors only to Retrieve, Lookup, List, or Search. `purpose-bound` adds a required trusted purpose binding to the inherited security contract of a Record or history operation. An absent or empty `features` member declares none of these selectable guarantees.

Features are not options of the variation point. Each feature requirement carries its operation option in `applies_when` and its feature condition in `documentation`. Declaring a feature brings its applicable requirement, contract, and tests into a future claim. The normative operation extensions remain closed to the capability and feature values of their contract version. Caller capability discovery is separately offered supporting metadata for caller-visible Consultation, Write, and supporting workflow operations. It does not satisfy the minimum Registry service choice, grant record-level or mutation authority, or select `purpose-bound`. Its capability and feature annotations are extensible advisory metadata. A recognised Consultation entry requires its read `view`; a Write or supporting workflow entry cannot carry one. Existing recognised read entries can omit `family` and are interpreted as Consultation, while new Write entries declare `family: write`. Unknown future capability entries remain skippable without being forced into either known family's fields.

Registry metadata can describe a Registry for directory participation without establishing Digital Registries conformance. A specification reference, API-family classification, binding `capability` value, or linked operational contract is not by itself a conformance claim.

The specification also covers:

- identification and description of a Registry, its authority, authoritative scope, and available services;
- stable identification of Registry Records within an unambiguous Registry context;
- declaration of representation formats, schemas, documented field meanings, and protocol bindings;
- interpretation of source revision, lifecycle, and provenance information when supplied;
- the shared Record envelope, error outcomes, disclosure behaviour, and live cursor pagination contract of the six Consultation operations;
- one HTTP binding and its publication artifacts for the selected read, direct Write, and approval-based change-request operations.

The specification separates operations, common Registry and Record context, domain semantics, and protocol bindings. This separation allows national registries, commercial products, open-source platforms, and adaptors to expose the same external contract without sharing an internal architecture or adopting a product-specific or universal domain model.

## Coverage and limitations <a href="#coverage-and-limitations" id="coverage-and-limitations"></a>

This section describes the material available in `3.0.0-alpha.2`; it does not add contract requirements.

| Area | Material in this alpha | Limitation |
|---|---|---|
| Registry Core | DRAFT requirements for metadata, scoped Record identity across logical Collections, schema context, documented field meanings, and interpretation of supplied source metadata | Complete schema lifecycle and domain-specific compatibility policies are not specified |
| Metadata and discovery | A JSON metadata document and schema, RFC 9727 discovery linkset, OpenAPI Registry context extension, examples, and an informative DCAT vocabulary appendix | The vocabulary, context, and schema are not published at their assigned `vocab.govstack.global` IRIs; canonical specification-version IRIs are not published |
| Authority | Registry Authority identity and declared authoritative scope | Delegation, shared responsibility, and a machine-readable mandate model are not specified |
| Service interfaces | One canonical draft Registry OpenAPI contract, shared schemas, and concrete example contracts | No canonical contracts exist for Provisioning, Evidence, Notification, Aggregate Data, Access Transparency, or Identity Federation; Consultation operation patterns described only informatively are not current options |
| Verification | Discovery, Consultation, and Write artifact validation, requirement-to-operation mapping, and Write implementation scenarios | No end-to-end implementation conformance suite or deployed runtime evidence is published; artifact checks do not establish runtime behaviour |

Domain-specific semantic models and jurisdiction-specific governance or legal compliance remain outside the Building Block's standardisation scope. Registry Authorities and adopting ecosystems supply them as appropriate. Field meanings must be documented even when no formal semantic model is selected. Source revision, lifecycle state, recording time, and effective-time history are not required unless a selected option or feature requires them.

Identity Federation remains informative. This draft selects no protocol binding for it, and cross-Building-Block ownership of its profile remains unresolved. An adopter therefore cannot rely on this draft for an Identity Federation conformance target.

## Conformance status <a href="#conformance-requirement-maturity" id="conformance-requirement-maturity"></a>

All requirements and options in `3.0.0-alpha.2` are `DRAFT` and unnumbered. Under the [agreed GovStack Requirements Model](https://github.com/GovStackWorkingGroup/specification-framework/blob/7322f977a6a74127240cbab5ed9d5ad84b9d5c29/chapters/requirements.md), a DRAFT requirement has `id: null`, takes no part in compliance, and can change before acceptance. Previous `fr-core#req-*` and `fr-consultation#req-*` labels are historical aliases, not current requirement identifiers. Previous requirement text remains available in Git history.

Requirement levels and other classifiers are interpreted according to that model. Lowercase modal verbs have their ordinary English meaning; this specification does not use BCP 14 keywords to assign requirement levels.

No implementation, operation, or functionality can claim conformance with this alpha. The unified Registry HTTP binding is also DRAFT, and no executable implementation conformance suite is published. The canonical contract, requirement-to-operation mappings, and example-validation checks support artifact review and prototyping only; they do not establish deployed runtime behaviour. Procurement and certification should reference an approved specification version. No approval or certification obligation is claimed here.

## Conformance declaration and binding vocabulary <a href="#conformance-conformance-declaration-and-binding-vocabulary" id="conformance-conformance-declaration-and-binding-vocabulary"></a>

The GovStack framework requires a future conformance declaration to list the options a solution claims. A claim also names any features declared by its claimed operations; every applicable requirement, contract, and test for those features forms part of the claim. The framework has not yet defined the declaration's serialisation, so this specification does not invent one.

The Consultation OpenAPI extension retains `capability` as a wire-level field name. Its six values bind operations to the six Consultation option keys above. The Write extension binds operations to the four Write options; it does not add Write values to the closed Consultation extension. Both extensions are used in the same canonical contract. These binding values are not informative framework capabilities. The informative capabilities declared for this specification are Registry Service Discovery and Authoritative Registry Services.

## Adaptors <a href="#conformance-adaptors" id="conformance-adaptors"></a>

An existing Registry does not need to replace its internal software to implement the draft contract. An adaptor can translate an existing interface into the operations, metadata, outcomes, and bindings described here. Assessment concerns the resulting external behaviour and required evidence.

The adaptor documents source currency, identifier mapping where needed, Collection membership, supported selectors and searches, and representation mappings. It does not fabricate source revisions, recording or effective times, history, or lifecycle facts to fill an envelope. A service offering latest reads does not need to implement revision operations, temporal features, caller capability discovery, purpose binding, or a general query engine.

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
| Provisioning, Evidence, Notification, Aggregate Data, Access Transparency, and Identity Federation conformance | Future requirements and contracts; these families are not current conformance targets |

Reference architectures and implementation guides can explain how these concerns are addressed in a domain or jurisdiction without making them part of base Digital Registries conformance.

## Ownership

The GovStack Registries and Registration Working Group owns this draft. Change requests follow the contribution process of the Digital Registries specification repository.

## Write scope <a href="#conformance-write-applicability" id="conformance-write-applicability"></a>

The [Write requirements](../requirements/registry-services.md) and [Write verification matrix](../resources/write-testing.md) apply to selected Write options. Their canonical transport entry point is the unified [Registry API](../resources/api.yml); [write-api.yml](../resources/write-api.yml) remains a compatibility alias. A direct Write selection does not require change requests or manual review; a change-request selection does not grant direct mutation authority. Compound changes are available only when the published operation declares their supported boundary and guarantees. Pending review and approval do not establish commitment.

Registry-managed review concerns the proposed authoritative change; it does not require a general-purpose intake or workflow engine. Adopting institutions define permissions, review policy, accepted transitions, and domain models. Birth registration, Household, Person, membership, and other payloads in the [Write examples](../resources/api-examples/README.md) are non-normative profiles. Their fields, vocabularies, local reference mappings, bounds, domain models, and policy rules are not requirements of shared Write.
