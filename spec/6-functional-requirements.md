---
description: This section lists the technical capabilities of this Building Block.
---

# 6 Functional Requirements

## Introduction <a href="#docs-internal-guid-d85f59a4-7fff-1564-6ae2-86d67f36a258" id="docs-internal-guid-d85f59a4-7fff-1564-6ae2-86d67f36a258"></a>

This page translates the key functionalities of the Digital Registries Building Block into a clear set of functional requirements. These are the specific capabilities that any implementation of the building block must support to be considered compliant with the GovStack standard

For technical teams, these requirements serve as a specification for development. For government stakeholders, they provide a checklist to evaluate solutions.

In short, this list describes what a **Digital Registry** must be able to _do_. It’s the checklist for building or buying a system that meets GovStack standards.

## 6.1 Administrative/Analyst Functions <a href="#docs-internal-guid-d85f59a4-7fff-1564-6ae2-86d67f36a258" id="docs-internal-guid-d85f59a4-7fff-1564-6ae2-86d67f36a258"></a>

1. **DRS-1:** **Create Registries** - The Digital Registry BB shall enable authorised users to create new registry schemas, each identified by: (REQUIRED):
   1. Name of the database;
   2. A unique short code / name;
   3. A structured schema definition as specified in (see DRS-3).
   4. Registry metadata (domain, owner department, retention policy, classification Open/Restricted/Confidential)
   5. Lifecycle state: Draft-> Published ->Archived
   6. Default indexing & Storage profile (row store / column store / document store)
2. **DRS-2: Multiple Databases**
   * Analysts can create multiple databases in one system instance.&#x20;
     * Links can be:
       * **Foreign key** (Strict)
       * **Soft link** (UUID reference; no FK constraint)
       * **Graph relationship** (NEW: parent-child, many-to-many edges)
   * Analysts can configure which databases and which fields are linked. In this document and foreign key function, we consider databases as database tables that can be linked with one another. See the [example illustration](https://github.com/GovStackWorkingGroup/bb-digital-registries/blob/23Q4/spec/.gitbook/assets/Database%20Foreign%20key.png).
     * **User story**: As a user, I can browse database content (Data) in the user interface and when databases are linked, then I can click and move from one database/table to another where the corresponding linked data will open in the user interface.
   * In the Digital Registries Data user interface, it should be possible to open another database by clicking on the record ID in one database and all corresponding records from the other Database will open.
   * It is required to have at least two levels of IDs (database ID and field ID) to link the databases. See the example API in [Appendix 2](https://github.com/GovStackWorkingGroup/bb-digital-registries/blob/23Q4/spec/.gitbook/assets/appendix2.json).
     * **Example**: In one registry database we store information about Mother and Child records. In the second registry database, we store information about payments made for the mother. The system must enable a foreign key link between the payment database to the Mother and child record database. Users can click in the payment database record user interface to the Mother ID field and the system user interface should open the corresponding record in the Mother and Child database. (REQUIRED)
   * **Reference Integrity Rules**:
     * Cascade delete
     * Restrict delete
     * Orphan tolerance
3. **DRS-3: Database Schema**
   *   Analysts have the option to add fields to the database schema. Fields of the database must contain at least the following elements (REQUIRED):

       1. Field name;
       2. Field type, at least with the following types:
          1. Text;
          2. Number;
          3. Boolean;
          4. Date/time;
          5. Date;
          6. Time;
          7. File (pdf, doc, etc.). File extensions/types must be configurable;
          8. List/Array/Edit grid (sub-table/array of values inside a field);
          9. JSON object / Block container (optional, to group fields visually);
          10. List of Values/Catalog (holding value and key).
          11. Database/Cluster encoding UTF-8 for multi language support (Optional)
          12. GeoPoint (lat/long) (optional)
          13. GeoShape (polygon, boundary)(optional)

       3\. Field properties (see more in DRS-17)
4. **DRS-4:** **Publishing and Versioning**
   * Analysts have the option to publish the database. Publishing will reveal the database to users. (REQUIRED)
   * Publish uses versioning. Each publish request creates a new version of the database schema and API services.
   * Old database schemas must be made available to the users.
   * Data stored in the old database versions must be usable in old versions and in new versions.
   * Analysts can delete database schema versions. Same version API services must be deleted at the same time.
   * Change impact analysis:
     * Breaking changes identified automatically
     * Warnings shown to analyst
5. **DRS-5: APIs**
   * Analysts must be able to configure the API services per registry database. (REQUIRED)
     * The system automatically creates API services to:
       * create data.
       * read data.
       * update data.
       * delete data.
       * Bulk operations (batch create/update/delete)
       * validate data (if exists).
       * update or create data.
       * archive data
       * Schema Introspection (replies with the schema (tables/fields/types/relations) in a machine-readable form)
   * Analysts can hide/disable API services.
   * Analysts can delete API services.
   * Analysts can copy API services.
   * Analysts can create view (Read data) custom API services.
   * Field-level masking applied dynamically (Optional) (DRS-9)
   * Subscription API (event-based)
   * An analyst must be able to mark a field as secret (DRS-15)
   * An analyst must be able to mark a field as PersonalDataID (DRS-14)
   * The system generates the API data structure from the dynamic database structure automatically each time a publish is done.
6. **DRS-6: Authorization and Access Control**
   *   Authorization to (REQUIRED)

       1. create and manage databases.
       2. API usage per service, per record, per data field.
       3. access to DATA.

       Analysts have the option to manage user rights of a database and data via API and via a user interface.
   * RBAC (roles)
   * ABAC (attributes)
   * PBAC (policy-based access control)
   * Consent-based access
   * **Delegated access** (guardian, parent, representative)
   * **Cross-registry access templates**
   * **Data minimization rules** (only minimum required fields returned)
   * **Condition-based dynamic restrictions** Example: Show fields only if “CaseStatus=APPROVED”
   * "Any logged-in user" role must be available
   * "Anonymous" user role must be available
   * Attribute Based Access Control (ABAC) logic could be used (API, Schema, data fields, record filter, users)
   * Per user, per group of users option must be available.
     * Group is a set of users in a role
     * Role is a set of rights
7. **DRS-7: Logging and Auditing**
   1. The system must log all data processing in the database. (REQUIRED)
      1. Schema changes must be logged
      2. Data processing (Create, Read, Update, Delete) must be logged
      3. Logs must be visible and searchable to the Analyst via the User Interface
      4. Every data owner (e.g. physical person) has the option to see who has processed his/her data (PersonalData). The function is a standard function for all registries ([DRS-14 API example](https://github.com/GovStackWorkingGroup/bb-digital-registries/blob/23Q4/api/GovStack_Digital_registries_BB_Data_API_template-1.3.0.json))
   2. Change logs are protected with the highest level of integrity (chaining of logs)
   3. Database logs could be logged with an external blockchain for additional security (optional)
8. **DRS-8: Personal Data usage. (REQUIRED)**
   1. The System must automatically store all data read requests and store these in the log table.
      * Covers data read events via User Interface and via APIs
      * Personal Data logs are stored with PersonalData data tag, storing at least the following information.
        * Log ID
        * Data record ID
        * Field ID
        * PersonalDataID (unique and unchangeable identifier of a person)
        * Reader ID- who read the data
        * Reader name- name or initial of a person
        * When - the moment when the Personal Data was read
      * The Personal Data report is visible only for Analysts to see all data read logs and Data Owners (physical persons) to see their own personal data usage log. Input is PersonalDataID field
      * PersonalData report is usable as an API service (read)
      * System has API for PersonalData reports. API is per registry(database)
      * System must log Personal Data log read events to the log table.
      * Legal justification (if required by law)
      * Consent reference (if applicable)
      * Data viewer’s role, org, location, Device fingerprint (optional)
9. **DRS-9: Analysts must be able to create views of a database. (OPTIONAL)**
   * View is a selection of data from a database
   * View can be opened as OPEN DATA (anonymous user)
   * View can be created, and it can be as a base for an API service (Custom API)
   * View is not for changing or deleting data, only for reading
   * View rights are managed by the user rights management system
10. **DRS-10:** The option export database schema to JSON/YAML file, (optional: XLS file format) (REQUIRED)
11. **DRS-11:** The option to import database schema from JSON/YAML file. (REQUIRED); The option to import database schema from XLS file. (OPTIONAL)
12. **DRS-12:** Service usage statistics (OPTIONAL)
    * System must record all API service usage information.
    * System must record all searches made in the Registry User Interface and via APIs.
13. **DRS-13:** An analyst must be able to mark a field as PersonalData log object (This field contains personal data). (OPTIONAL)
14. **DRS-14:** An analyst must be able to mark a field as PersonalDataID. This is the data owner’s ID. (OPTIONAL)
    * Multiple identifiers (national ID, passport, local ID)
    * Identifier validation rules
    * Identifier linking to external registries
    * Immutable identifier enforcement
15. **DRS-15:** An analyst must be able to mark a field as secret
    * This field contains secret data (credit card number). E.g. secret data (card data) must be encrypted while at REST.
    * Information in transit between the Building Blocks is secured with encryption. Information in Transit is described and governed by Information Mediator Building Block. (REQUIRED)
16. **DRS-16:** Analyst has the option to read database schema in the web User Interface. (REQUIRED)
17. **DRS-17:** Analyst has capabilities to configure database field properties (REQUIRED)
    1. API-related field properties
       1. Validation options: required, unique, max, min
       2. blinded/encrypted (DRS-15, DRS-22)
    2. User Interface related field properties:
       * field mask, format
       * read-only
       * personal data
       * enum list selection
       * blinded/encrypted (DRS-22)
       * multiple value/array. User can add more values (e.g. multi select from catalog list) to the same field. Multiple values are
         * array type field
         * validation options- Required, Unique, max, min
         * Foreign keys (to link other databases in the same ecosystem). See the example schema in [Appendix 2](https://github.com/GovStackWorkingGroup/bb-digital-registries/blob/23Q4/spec/.gitbook/assets/appendix2.json)
       * Triggers to automate field content-related actions
         * create IDs
         * merge fields
         * add prefix
         * suffix
         * conditional logic
         * trigger will be activated if certain condition(s) are true
         * transform-upper/lower case/ javascript)
         * Triggers are automated when a record is created/changed. A trigger is a record-level automation
18. **DRS-18:** Analyst has the capability to add an encryption key per database. (REQUIRED)
    * Encryption key is used to encrypt and decrypt data (DRS-17).
    * Encryption key can be used by applications to read encrypted data. Each database has a unique encryption key defined by the analyst.
    * Encryption key is blinded in the User Interface.
    * If applications want to read encrypted data via API they must know the encryption key. Data is decrypted in the user interface.
19. **DRS-19:** Analyst has the capabilities to automate data exchange between databases internally and externally via API. (REQUIRED)
    1. Automation is triggered automatically after a pre-configured time interval as a loop (finishes when all corresponding records have been processed).
    2. Automation processes one record at a time.
    3. Automation has configurable conditions (business rules in Rules Engine). E.g. IF field A = 123 then true. Conditions can be grouped with AND and OR operators.
    4. Automation is configured by mapping (input, output) registry data fields to:
       1. another database in the same instance.
       2. API in an external database.
    5. Mapping involves:
       1. query part (input)
       2. answer part (output)
    6. Webhook triggers (Multi-Registry Orchestration )

Mapping can be done from many to one and one to many. Mapping may have a transformation option to convert data to another format. E.g. est->EST; Expected outcome: Automation can be activated automatically when certain conditions are true and the system sends data to another database or to an external API.

20. **DRS-20:** Analyst may have capabilities to use database schema templates so that the registry creation is faster. (OPTIONAL)
    1. Schema templates can be shared in the same instance (internal marketplace).
    2. Schema templates can be shared in a marketplace.
    3. Schema templates can be imported and exported.
    4. Full registry + schema + views + API configs
    5. Domain templates: Health Registry, Business Registry, Farmer Registry (Optional)
    6. Versioned template repository
21. **DRS-21:** Analyst has a view to see all data in the registry. (REQUIRED)
    1. Two main views:
       1. Main registry records grid view.
       2. Record detail view.
    2. See data;
    3. See documents(open if image, download if other type);
    4. Data log view (changes (create, update, delete). Data before and after).
    5. Data read view (information about who has looked at/exported the data). Data and data reader information is stored in the log registry.
22. **DRS-22:** Analyst has a view to edit data in the registry. (REQUIRED) Two main views:
    1. Main grid (inline editing).
    2. Detail record edit view:
       1. Edit data;
       2. Remove/add documents (upload).
       3. blinded/encrypted

Analyst has option to delete data in the registry. All data changes are logged.

23. **DRS-23:** Analyst can use additional functions to simplify data searching (REQUIRED)
    * Filtering by search criteria by field content.
    * Full-text data search.
    * Order by each data field.
24. **DRS-24:** Import data to the registry. Analyst has the option to import information into the database. Import formats are: JSON, CSV, XLS. (REQUIRED)
25. **DRS-25:** Export data from the registry. Analyst has the option to export selected/filtered data from a registry to CSV/XLS, JSON. (REQUIRED)
26. **DRS-26:** Statistical queries. The system should have the ability to (REQUIRED):
    1. Produce standard statistical reports
       1. System must show statistics of all registered items in the registry, with various criteria for filtering. For example:
          1. Details of registered people
          2. Details of registered services
          3. Time series: Change in registration of people/services over time
          4. Details of change to data elements (audit logs)
       2. Generate customizable reports based on the fields registered in the registry.
    2. Allow the analyst/user to analyze data collected in the system in various ways:
       1. (Option) Develop functionality to allow custom dashboards for analysts to analyze data within databases.
       2. Provide APIs for extracting data from databases to analyze in external data analytics systems (e.g. Tableau).
27. **DRS-27:** Users can share data with other users. Share data with other users via e-mail, or via a unique and secure URL. Sharing must be at a record level and field level. Data sharing can be turned off in the authorization module. Data can be shared with anonymous users. The data shared with anonymous users is Open Data. (REQUIRED)
    1. Time-bound secure links
    2. Consent-required links
    3. Role-restricted link sharing
    4. QR code sharing
    5. Download watermarking
    6. View-only mode (no export)
28. **DRS-28:** Developer has the option to create a new registry database by sending data via API (REQUIRED). Developer is a user who is using API interface.
    1. Name of the database;
    2. A short name;
    3. Schema of the database (see DRS-3).
29. **DRS-29:** Developer can create multiple registry databases into one system instance. (REQUIRED)
30. **DRS-30:** Developer has the option to publish the database. Publishing will reveal the database to users. (REQUIRED)
31. **DRS-31:** Developer must be able to modify API services per registry database. (REQUIRED)
    1. The system generates the API data structure from the dynamic database structure automatically each time a publish is done.
    2. The system automatically creates API services to:
       1. create data;
       2. read data;
       3. update data;
       4. delete data;
       5. validate data (if exists);
       6. update or create data.
    3. Developer can hide API services;
    4. Developer can delete API services;
    5. Developer can copy API services;
    6. Developer can create custom API services.
32. **DRS-32:** Developer has the option to read database schema via API. Developer has the option to read the list API services available per Database. (REQUIRED)

## 6.2 Applicant Functions <a href="#docs-internal-guid-d85f59a4-7fff-1564-6ae2-86d67f36a258" id="docs-internal-guid-d85f59a4-7fff-1564-6ae2-86d67f36a258"></a>

33. **DRS-33:** Building Block must enable client systems to process (CRUD) the database records via Open API services. (REQUIRED)
    * Applicant can search data
    * Applicant can create data
    * Applicant can read data
    * Applicant can update data
    * Applicant can delete data
    * Applicant can create or update data.

Building Block authorizes client systems and users to process data

34. **DRS-34:** Building Block has the Open API service list (Swagger) to visualize all API services and API service versions. (REQUIRED)

Client systems must be able to see all API service descriptions including:

* Description of each field.
* Example data of each field.

If possible then the example must be real so that whoever is looking at the API specifications can test the example data in the service (try it).

35. **DRS-35:** System has an API for PersonalData usage report. (REQUIRED)
    1. API input must be configurable by the analyst. Input must be a unique identifier of the data owner(e.g. personal identification number)
    2. If the registry database schema is designed to store personal data then the analyst must be able to link the personal data to the owner of personal data (e.g. citizen).
36. **DRS-36:** Statistical queries via API. (OPTIONAL)
    1. System should make data accessible through the API
       1. Registration Data
       2. Program Data
    2. API should allow querying data with multiple parameters
       1. Date, time ranges
       2. Registered Program
    3. Only authorized data should be available through the API.
37. **DRS-37:** Using viewing event logs- every data owner has the right to see who has looked at their personal data. (REQUIRED)
    1. Data owner is a physical person whose personal data is stored in the registry
    2. Data owner has the right to access data reading/processing event logs of the personal data they own. Personal data in a registry is marked accordingly (PersonalData) by the analyst
    3. PersonalData logs are visible via API or via User Interface (PersonalData report).

## Building Block Components

The Building Block has a user interface to query and consult the registry data but in most cases, the Applicants are using the end client applications like Registration Building Block to access the registry. Any Building Block can query data from Digital Registries Building Block via APIs if authorization is given.

![Digital registries functional components](<.gitbook/assets/image3 (1) (1).png>)
