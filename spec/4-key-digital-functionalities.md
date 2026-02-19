---
description: >-
  Key Digital Functionalities describe the core (required) functions that this
  Building Block must be able to perform.
---

# 4 Key Digital Functionalities

The Digital Registries Building Block (BB) provides foundational capabilities to create and manage authoritative registries in a modular, domain-agnostic way. It enables storage, management, and governance of records about entities (persons, organisations, places, assets, events) with standardised CRUD operations, schema and record versioning (audit trails), and interoperability.

Digital Registries Building Block is a multi-tenant platform where users can create and manage new registry databases. Each registry created within the system automatically generates OpenAPI-compliant services for interoperability.

The Digital Registry System does not contain data capturing and workﬂow functionality, however, if a user interface for making new registration requests and processing such requests is needed, then Digital Registries can be combined with other GovStack building blocks (e.g. the [Registration Building Block](https://github.com/GovStackWorkingGroup/bb-registration/tree/1.0-QA)) in a plug-and-play fashion.

## 4.1 Administrative/Analyst Functions <a href="#docs-internal-guid-d85f59a4-7fff-1564-6ae2-86d67f36a258" id="docs-internal-guid-d85f59a4-7fff-1564-6ae2-86d67f36a258"></a>

The first user of the Building Block is an **Administrator/Analyst** who is building a new registry. The Analyst is the person who is building the new registry database, changing the existing database configuration, or simply administering the API user authorization. The Administrator/analyst is using a web user interface.

The key functions of the Building Block for Analysts are:

### Registry lifecycle management

1. Create a new registry/database (via API or Web UI).
2. Publish, deprecate, or archive registry versions.
3. Create and configure the schema of the register and publish (API or Web UI);
4. Modify schema and publish a new schema/API version with backward-compatibility guidance.
5. Define validation rules, deduplication, and data quality controls.
6. Import/export registry database schema;

### Data management

8. Enter, view, and update records (via API or Web UI).
9. Support soft deletion and archival of records.
10. Bulk import/export of data from/to external files.
11. Policy-based masking and redaction for sensitive attributes.
12. Share data with other users via e-mail, or via a unique and secure Uniform Resource Locator (URL) sharing can be field level or record level.

### Interoperability

12. Auto-generate REST/GraphQL/OpenAPI services per registry.
13. Integrate with external systems through the Information Mediator BB.
14. Emit domain events (create/update/delete) via Pub/Sub for downstream consumers.

### Monitoring and analytics

15. View statistics on registry usage, performance, and data quality.
16. Generate dashboards and administrative reports.
17. Inspect transaction log of registry data operations (API or Web user interface);

## 4.2 Applicant Functions <a href="#docs-internal-guid-d85f59a4-7fff-1564-6ae2-86d67f36a258" id="docs-internal-guid-d85f59a4-7fff-1564-6ae2-86d67f36a258"></a>

**Applicants** do not access the Registry BB directly. They interact via sectoral applications or other GovStack BBs:

* Registration BB (UI for data capture, modification, validation).
* Workflow BB (approvals/authorisations).
* Information Mediator BB (secure API mediation).
* Security & Consent BB (authentication, authorisation, consent).

The key functions of the Building Block for Applicants through those applications are:

1. Search and query data from the register;
2. Read authoritative records (with policy-driven masking).
3. Request creation, update, or deletion of records where allowed; mediated services invoke Registry APIs on their behalf.
4. Validate record existence in a specified registry (e.g., verify an identifier or ownership).
5. Access statistics when exposed to external users.
6. Subscribe to registry events via mediated services (e.g., External or cross-domain consumers must subscribe to registry events via mediated services exposed through the Information Mediator BB (or an IM-managed Event Gateway); internal consumers within the same trust boundary may subscribe directly to the internal event bus, subject to RBAC/ABAC policy, tenant isolation, and audit).
