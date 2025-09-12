---
description: >-
  Key Digital Functionalities describe the core (required) functions that this
  Building Block must be able to perform.
---

# 4 Key Digital Functionalities

“The Digital Registries Building Block (BB) provides foundational capabilities to create and manage authoritative registries in a domain-agnostic way”. It enables storage, management, and governance of records about entities (persons, organisations, places, assets, events) with standardised CRUD operations, schema and record versioning (audit trails), and interoperability.

Digital Registries Building Block is a multi-tenant platform where users can create and manage new registry databases. Each registry created within the system automatically generates OpenAPI-compliant services for interoperability.

The Digital Registry System does not contain data capturing and workﬂow functionality, however, if a user interface for creating the new register and data storage & processing is needed then Digital Registries can be combined with other GovStack building blocks (e.g. the [Registration Building Block](https://github.com/GovStackWorkingGroup/bb-registration/tree/1.0-QA)) as a plug-and-play.

## 4.1 Administrative/Analyst Functions <a href="#docs-internal-guid-d85f59a4-7fff-1564-6ae2-86d67f36a258" id="docs-internal-guid-d85f59a4-7fff-1564-6ae2-86d67f36a258"></a>

The first user of the Building Block is an **Administrator/Analyst** who is building a new registry. The Analyst is the person who is building the new registry database, changing the existing database configuration, or simply administering the API user authorization. The Administrator/analyst is using a web user interface.&#x20;

The key functions of the Building Block for Analysts are:

### Registry lifecycle management
1. Create a new registry/database (via API or Web UI).
2. Publish, deprecate, or archive registry versions.
3. Support soft deletion and archival of records.
4. Create and configure the schema of the register and publish (API or Web UI);
5. Modify schema and publish a new schema/API version with backward-compatibility guidance.
6. Define validation rules, deduplication, and data quality controls.
7. Import/export registry database schema;

### Data management
8. Enter, view, and update records (via API or Web UI).
9. Bulk import/export of data from/to external files.
10. Policy-based masking and redaction for sensitive attributes.
11. Share data with other users via e-mail, or via a unique and secure Uniform Resource Locator (URL) sharing can be field level or record level.

### Interoperability
12. Auto-generate REST/GraphQL/OpenAPI services per registry.
13. Integrate with external systems through the Information Mediator BB.
14. Emit domain events (create/update/delete) via Pub/Sub for downstream consumers.

### Monitoring and analytics
15. View statistics on registry usage, performance, and data quality.
16. Generate dashboards and administrative reports.
17. Inspect transaction log of registry data operations (API or Web user interface);

## 4.2 Applicant Functions <a href="#docs-internal-guid-d85f59a4-7fff-1564-6ae2-86d67f36a258" id="docs-internal-guid-d85f59a4-7fff-1564-6ae2-86d67f36a258"></a>

The second main user is an **Applicant** who is consuming registry data via other Building Block (e.g. Registration Building Block) screen flow or via Information Mediator Building Block API services.&#x20;

The key functions of the Building Block for Applicants are:

1. Search data from the register;
2. Read data from the register;
3. Create data in the register;
4. Update data in the register;
5. Delete data in the register;
6. Validate if given content exists in specified register;
7. Read statistics.
