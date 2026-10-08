---
description: Disposition of requirements from the previous 3.0.0-alpha.1 draft.
---

# Migration from the 3.0.0-alpha.1 Draft

## Purpose

The 3.0.0-alpha.2 revision replaces the previous flat `DRS-1` through `DRS-37` requirement set. This ledger preserves traceability and explains whether each concept is retained, moved, inherited, converted to guidance, or retired.

The old identifiers are not reused. New DRAFT requirements use the `govstack-bb-digital-registries-fr-*` namespaces.

The earlier draft also elevated `govstack-cfr-data#req-4` and `govstack-cfr-data#req-7` from RECOMMENDED to REQUIRED. Those elevations are not carried forward. The inherited requirements apply with their `govstack-cfr-2.1.0` classifiers and applicability conditions.

## Requirement disposition

| Previous requirement | Disposition |
|---|---|
| DRS-1 Create Registries | Registry identity, authority, classification, and lifecycle metadata inform Registry Core. Registry creation and schema configuration move to optional Provisioning. Storage-profile choices are retired. |
| DRS-2 Multiple Databases | Mandatory multi-database, foreign-key, graph, and UI-navigation behaviour is retired. Relationships belong to the selected semantic model or implementation guidance. |
| DRS-3 Database Schema | Machine-readable representation schemas and documented field meanings are retained. Registry and schema context may be conveyed through the endpoint, versioned contract, or response as the binding specifies. Schema authoring and field configuration move to optional Provisioning. The fixed field-type and UI-widget catalogue is retired. |
| DRS-4 Publishing and Versioning | Schema lifecycle and compatibility remain relevant to future Provisioning. Schema publication is decoupled from automatic endpoint-version generation. Deletion of old schemas is not carried forward. |
| DRS-5 APIs | Split across Consultation, Write, Notification, and Provisioning. Automatic creation, copying, hiding, and deletion of CRUD endpoints is retired. |
| DRS-6 Authorisation and Access Control | General authentication and access control inherit from GovStack CFR. Policy-based permitted representations are retained in Consultation. RBAC, ABAC, PBAC, consent, and anonymous-role internals are not prescribed. |
| DRS-7 Logging and Auditing | Registry Core defines the meaning of supplied source revision and provenance metadata; it does not require an adapter to invent missing values. Principal-facing access history moves to Access Transparency. Generic security logging inherits from CFR. Blockchain is not a conformance mechanism. |
| DRS-8 Personal Data Usage | Access-event concepts move to Access Transparency. The fixed `PersonalDataID` log structure and optional device fingerprint are not retained. |
| DRS-9 Database Views | Defined views inform the independently optional List and Search capabilities, which now have DRAFT requirements and a shared pagination contract. Open-data publication requires an explicit disclosure policy and is not equated with anonymous access. |
| DRS-10 Export Schema | Moves to optional Provisioning. File formats will be defined by an applicable binding or guide. |
| DRS-11 Import Schema | Moves to optional Provisioning. File formats will be defined by an applicable binding or guide. |
| DRS-12 Service Usage Statistics | Generic monitoring inherits from CFR. Administrative analytics are implementation guidance. Logging every search term is not a default requirement. |
| DRS-13 Personal Data Field | Sensitivity and classification metadata remain relevant through CFR and declared schemas. UI-specific field marking is retired. |
| DRS-14 Personal Data Identifier | Stable identifier concepts are retained, including suitable source identifiers unique within an unambiguous Registry context. Record, foundational, functional, and domain identifiers remain distinct. Federation behaviour is tracked under the candidate Identity Federation family pending a cross-BB ownership decision. |
| DRS-15 Secret Field | Classification, encryption, and transport security inherit from CFR. Policy-driven redaction is retained in Consultation. The credit-card and mandatory Information Mediator examples are removed. |
| DRS-16 Read Schema in UI | Machine-readable schema declaration is retained. Administrative UI presentation is implementation guidance. |
| DRS-17 Field Properties and Triggers | Validation constraints inform schemas and optional Provisioning. UI widgets, database relationships, and embedded trigger scripting are implementation choices. |
| DRS-18 Per-Database Encryption Key | Retired. Applications must not need a Registry encryption key to read data. Cryptography, key management, and rotation inherit from CFR. |
| DRS-19 Automated Data Exchange | Change events move to Notification. Cross-system orchestration and mapping tools belong to neighbouring BBs or implementation guidance. |
| DRS-20 Schema Templates | Registry templates and marketplaces are implementation guidance, not interoperability requirements. |
| DRS-21 View Data | Record access moves to Consultation and audit visibility to Access Transparency. Grid, detail, and document views are implementation choices. |
| DRS-22 Edit Data | Record mutation moves to Write. Deletion inherits CFR lifecycle rules where applicable. Editing UI behaviour is implementation guidance. |
| DRS-23 Search Helpers | Declared filters, search criteria, and ordering move to independently optional List and Search capabilities with DRAFT requirements. Exact domain-identifier resolution is Lookup. Full-text or approximate matching and a general query language are not mandatory. UI behaviour is not retained. |
| DRS-24 Import Data | Bulk import moves to optional Provisioning or an applicable Write profile. CSV and spreadsheet UI behaviour is guidance. |
| DRS-25 Export Data | Bulk export moves to optional Provisioning or Consultation profiles. General portability inherits from CFR. |
| DRS-26 Statistical Queries | Moves to optional Aggregate Data. Dashboards and report designers are implementation guidance. |
| DRS-27 Share Data | Controlled disclosure informs Consultation, Evidence, and consent integration. Email, links, QR codes, watermarks, and anonymous sharing are implementation choices. |
| DRS-28 Create Registry by API | Duplicate of the provisioning aspect of DRS-1. Moves to optional Provisioning. |
| DRS-29 Multiple Registries by API | Duplicate of DRS-2. Mandatory multi-tenancy is retired. |
| DRS-30 Publish Registry by API | Duplicate of DRS-4. Moves to optional Provisioning. |
| DRS-31 Modify APIs | Duplicate of DRS-5. Capability declaration and linked operational contracts are retained in Core; generated-API product behaviour is retired. |
| DRS-32 Schema and API Discovery | Machine-readable Registry and service metadata publication is required by the DRAFT Core requirements, including API-family classifications, endpoints, and linked operational contracts. Full schema administration is optional Provisioning. The [Registry Core metadata model](../05-api-families/registry-core.md#registry-metadata) defines the metadata document and the [metadata vocabulary appendix](metadata-vocabulary.md) records its DCAT composition; executable conformance validation is not published in this release. |
| DRS-33 Applicant CRUD | Split across independently optional Consultation Retrieve, Lookup, List, and Search, and optional Write. The Applicant CRUD framing is retired. |
| DRS-34 Swagger Service List | Machine-readable service contracts are retained, including a canonical draft Consultation OpenAPI contract. Swagger UI and live production examples are not conformance requirements. Other protocol-native bindings depend on the applicable GovStack framework rules. |
| DRS-35 Personal Data Usage API | Duplicate of DRS-8. Moves to Access Transparency and is generalised from a person-specific identifier to a Record Principal. |
| DRS-36 Statistical Queries API | Moves to optional Aggregate Data. |
| DRS-37 Data Owner Access Log | Duplicate of DRS-8 and DRS-35. Moves to Access Transparency and is generalised to a Record Principal. |

## Replacement index

The following DRAFT requirements carry forward the interoperability intent in Registry Core and independently optional Consultation Retrieve, Lookup, List, and Search. Core requirements for returned Records apply when a selected capability returns Records. A previous requirement can map to more than one replacement because the earlier product-oriented clauses combined several concerns.

| Current target | Principal predecessors |
|---|---|
| `fr-core#req-1` Registry metadata | DRS-1, DRS-32, DRS-34 |
| `fr-core#req-2` Record identification within Registry context | DRS-14, DRS-33 |
| `fr-core#req-3` Record Identifier stability | DRS-14, DRS-33 |
| `fr-core#req-4` Representation schema and field meanings | DRS-3, DRS-4, DRS-16, DRS-17, DRS-32, DRS-34 |
| `fr-core#req-5` Meaning of supplied revision and lifecycle metadata | DRS-4, DRS-7, DRS-14 |
| `fr-core#req-6` Meaning of supplied Record provenance | DRS-7, DRS-21, DRS-33 |
| `fr-core#req-7` Service discovery | DRS-5, DRS-31, DRS-32, DRS-34 |
| `fr-consultation#req-1` Retrieve by identifier | DRS-5, DRS-21, DRS-33 |
| `fr-consultation#req-2` Permitted representation | DRS-6, DRS-15, DRS-21, DRS-27, DRS-33 |
| `fr-consultation#req-3` Protected-existence handling | DRS-6, DRS-15, DRS-33 |
| `fr-consultation#req-4` Exact selector Lookup | DRS-5, DRS-14, DRS-23, DRS-33 |
| `fr-consultation#req-5` Bounded List | DRS-9, DRS-21, DRS-23, DRS-33 |
| `fr-consultation#req-6` Search using declared criteria | DRS-9, DRS-23, DRS-33 |
| `fr-consultation#req-7` Bounded result continuation | DRS-9, DRS-23, DRS-25, DRS-33 |

Concepts moved to capability families without requirements in this release retain no normative force. Provisioning carries DRS-1, DRS-3, DRS-4, DRS-10, DRS-11, DRS-17, DRS-24, DRS-28, and DRS-30. Write carries DRS-22 and relevant parts of DRS-24. Notification carries DRS-19. Aggregate Data carries DRS-26 and DRS-36. Access Transparency carries DRS-8, DRS-35, and DRS-37. Evidence carries the relevant disclosure aspects of DRS-27. The candidate Identity Federation family tracks relevant identifier-federation aspects of DRS-14 and DRS-27 pending agreement with the Identity team on profile ownership.

All remaining retired or guidance-only clauses have the exact disposition recorded in the table above.

## Current draft read contract

The [canonical Consultation OpenAPI contract](../../api/openapi.yaml) replaces the legacy generated CRUD interface for the current draft. Retrieve and List use GET; exact Lookup and Search use POST request bodies. The four capabilities are independently optional. No QUERY method, CQL2 implementation, or general query engine is required.

The common Record shape is `{recordId, data}`. A Page contains `{items, pageInfo: {nextCursor, total?}}` and reuses that Record shape for the same response view. Continuation repeats the criteria and ordering with a fixed effective page size. Live pagination does not promise a source snapshot; totals are optional and, when supplied, exact for the current authorized result at the declared evaluation point.

These choices accompany the API Design Guide `0.2.0-draft` work and remain part of `3.0.0-alpha.2`. No release or conformance certification is implied. Draft contract and example checks validate artifacts; an end-to-end implementation conformance suite is not yet published.

## Legacy service contracts and tests

The previous artifacts are not suitable as contracts for this release:

- there is no Retrieve-by-Identifier operation; `POST /read` performs search-by-example;
- embedded API versions disagree with filenames and with one another;
- JSON, YAML, documentation, and tests disagree on endpoint names and casing;
- tests send an Information Mediator-specific header while the contracts declare different security metadata;
- examples and fixtures assume one postpartum-care schema; and
- tests do not cover authorisation-sensitive errors, redaction, lifecycle states, revisions, or provenance.

Their behavioural intent is preserved where useful in the workflow and testing chapters. The old paths and schemas have no conformance effect in this release.
