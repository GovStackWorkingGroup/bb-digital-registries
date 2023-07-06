---
description: This section lists the technical capabilities of this Building Block.
---

# 6 Functional Requirements

## 6.1 Administrative/Analyst Functions <a href="#docs-internal-guid-d85f59a4-7fff-1564-6ae2-86d67f36a258" id="docs-internal-guid-d85f59a4-7fff-1564-6ae2-86d67f36a258"></a>

* DRS-1: Analysts have the option to create a new registry database by filling in the following information (REQUIRED):
  1. Name of the database;
  2. A short name;
  3. Schema of the database (see DRS-3).
* DRS-2: Analysts can create multiple databases in one system instance. Databases must be linkable with foreign keys. See the foreign key API description example in [Appendix 2](.gitbook/assets/appendix2.json). Analysts can configure which databases and which fields are linked. In this document and foreign key function, we consider databases as database tables that can be linked with one another. See the [example illustration](.gitbook/assets/Database%20Foreign%20key.png). User story: As a user, I can browse database content (Data) in the user interface and when databases are linked, then I can click and move from one database/table to another where the corresponding linked data will open in the user interface. In the Digital Registries Data user interface, it should be possible to open another database by clicking on the record ID in one database and all corresponding records from the other Database will open. It is required to have at least two levels of IDs (database ID and field ID) to link the databases. See the example API in[ Appendix 2](.gitbook/assets/appendix2.json). Example: In one registry database we store information about Mother and Child records. In the second registry database, we store information about payments made for the mother. The system must enable a foreign key link between the payment database to the Mother and child record database. Users can click in the payment database record user interface to the Mother ID field and the system user interface should open the corresponding record in the Mother and Child database. (REQUIRED)
*   DRS-3: Analysts have the option to add fields to the database schema. Fields of the database must contain at least the following elements (REQUIRED):

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
       9. Block container (optional, to group fields visually);
       10. List of Values/Catalog (holding value and key).

    3\. Field properties (see more in DRS-33)
* DRS-4:  Analysts have the option to publish the database. Publishing will reveal the database to users. (REQUIRED)
  * Publish uses versioning. Each publish creates a new version of the database schema and API services;
  * Old database schemas must be available to the users;
  * Data stored in the old database versions must be usable in old versions and in new versions;
  * Analysts can delete database schema versions. Same version API services must be deleted at the same time.
* DRS-5: Analysts must be able to configure the API services per registry database. (REQUIRED)
  * The system automatically creates API services to:
    * create data;
    * read data;
    * update data;
    * delete data;
    * validate data (if exists);
    * update or create data.
  * Analysts can hide/disable API services;
  * Analysts can delete API services;
  * Analysts can copy API services;
  * Analysts can create custom API services;
  * The system generates the API data structure from the dynamic database structure automatically each time a publish is done.
*   DRS-6: Authorization to (REQUIRED)

    1. create and manage databases;
    2. API usage per service, per record, per data field;
    3. access to DATA.

    Analysts have the option to manage user rights of a database and data via API and via a user interface.

    * "Any logged-in user" role must be available;
    * "Anonymous" user role must be available;
    * Attribute Based Access Control (ABAC) logic could be used (API, Schema, data fields, record filter, users);
    * Per user, per group of users option must be available.
      * Group is a set of users in a role.
      * Role is a set of rights.
* DRS-7: The system must log all data processing in the database. (REQUIRED)
  * Schema changes must be logged;
  * Data processing (Create, Read, Update, Delete) must be logged;
  * Logs must be visible and searchable to the Analyst via the User Interface;
  * Every data owner (e.g. physical person) has the option to see who has processed his/her data (PersonalData). The function is a standard function for all registries ([DRS-14 API example](../api/GovStack\_Digital\_registries\_BB\_Data\_API\_template-1.3.0.json)).
  * Change logs are protected with the highest level of integrity (chaining of logs)
  * Database logs could be logged with an external blockchain for additional security (optional).
*   DRS-8: Personal Data usage. (REQUIRED)

    System must automatically store all data read requests and store these in the log table.

    * Covers data read events via User Interface and via APIs.&#x20;
    * Personal Data logs are stored with PersonalData data tag, storing at least the following information.
      * Log ID;
      * Data record ID;
      * Field ID;
      * PersonalDataID (unique and unchangeable identifier of a person);
      * Reader ID- who read the data;
      * Reader name- name or initial of a person;
      * When- the moment when the Personal Data was read.
    * The Personal Data report is visible only for Analysts to see all data read logs and Data Owners (physical persons) to see their own personal data usage log. Input is PersonalDataID field.
    * PersonalData report is usable as an API service (read)
    * System has API for PersonalData reports. API is per registry(database)
    * System must log Personal Data log read events to the log table.
* DRS-9: Analysts must be able to create views of a database. (OPTIONAL)
  * View is a selection of data from a database;
  * View can be opened as OPEN DATA (anonymous user);
  * View can be created and it can be as a base for an API service (Custom API);
  * View is not for changing or deleting data, only for reading;
  * View rights are managed by the user rights management system.
* DRS-10: The option export database schema to JSON file, (optional: XLS file format). (REQUIRED)
* DRS-11: The option to import database schema from JSON file. (REQUIRED); The option to import database schema from XLS file. (OPTIONAL)
* DRS-12: Service usage statistics (OPTIONAL)
  * System must record all API service usage information.
  * System must record all searches made in the Registry User Interface and via APIs.
* DRS-13: An analyst must be able to mark a field as PersonalData log object (This field contains personal data). (OPTIONAL)
* DRS-14: An analyst must be able to mark a field as PersonalDataID. This is the data owner’s ID. (OPTIONAL)
*   DRS-15: An analyst must be able to mark a field as secret- This field contains secret data (credit card number). E.g. secret data (card data) must be encrypted while at REST.

    Information in transit between the Building Blocks is secured with encryption. Information in Transit is described and governed by Information Mediator Building Block. (REQUIRED)
* DRS-16: Analyst has the option to read database schema in the web User Interface. (REQUIRED)
*   DRS-33: Analyst has capabilities to configure database field properties (REQUIRED)

    1\. API-related field properties:&#x20;

    * Validation options: required, unique, max, min.&#x20;
    * blinded/encrypted (DRS-15, DRS-18);&#x20;

    2\. User Interface related field properties:&#x20;

    * field mask, format,&#x20;
    * read-only,&#x20;
    * personal data,&#x20;
    * enum list selection;&#x20;
    * blinded/encrypted (DRS-18);&#x20;
    * multiple value/array. User can add more values (e.g. multi select from catalog list) to the same field. Multiple values are:
      * array type field;
      * validation options- Required, Unique, max, min.
      * Foreign keys (to link other databases in the same ecosystem). See the example schema in [Appendix 2](.gitbook/assets/appendix2.json).&#x20;
    * Triggers to automate field content-related actions:&#x20;
      * create IDs,&#x20;
      * merge fields,&#x20;
      * add prefix,&#x20;
      * suffix,&#x20;
      * conditional logic,&#x20;
      * trigger will be activated if certain condition(s) are true,
      * transform-upper/lower case/ javascript);&#x20;
      * Triggers are automated when a record is created/changed. A trigger is a record-level automation.
*   DRS-34: Analyst has the capability to add an encryption key per database. (REQUIRED)

    * Encryption key is used to encrypt and decrypt data (DRS-17).&#x20;
    * Encryption key can be used by applications to read encrypted data. Each database has a unique encryption key defined by the analyst.&#x20;
    * Encryption key is blinded in the User Interface.&#x20;

    If applications want to read encrypted data via API they must know the encryption key. Data is decrypted in the user interface.
*   DRS-35: Analyst has the capabilities to automate data exchange between databases internally and externally via API. (REQUIRED)

    * Automation is triggered automatically after a pre-configured time interval as a loop (finishes when all corresponding records have been processed).&#x20;
    * Automation processes one record at a time.&#x20;
    * Automation has configurable conditions (business rules in Rules Engine). E.g. IF field A = 123 then true. Conditions can be grouped with AND and OR operators.
    *   Automation is configured by mapping (input, output) registry data fields to:&#x20;

        * another database in the same instance.&#x20;
        * API in an external database.

        Mapping involves:&#x20;
    * query part (input)&#x20;
    * answer part (output)&#x20;

    Mapping can be done from many to one and one to many. Mapping may have a transformation option to convert data to another format. E.g. est->EST;\
    Expected outcome: Automation can be activated automatically when certain conditions are true and the system sends data to another database or to an external API.
* DRS-36: Analyst may have capabilities to use database schema templates so that the registry creation is faster. (OPTIONAL)
  * Schema templates can be shared in the same instance (internal marketplace).&#x20;
  * Schema templates can be shared in a marketplace.&#x20;
  * Schema templates can be imported and exported.
*   DRS-17: Analyst has a view to see all data in the registry. (REQUIRED)

    Two main views:

    * Main registry records grid view.
    * Record detail view.
      * See data;
      * See documents(open if image, download if other type);
      * Data log view (changes (create, update, delete). Data before and after).
      * Data read view (information about who has looked at/exported the data). Data and data reader information is stored in the log registry.
* DRS-18: Analyst has a view to edit data in the registry. (REQUIRED) Two main views:
  * Main grid (inline editing).
  *   Detail record edit view:

      * Edit data;
      * Remove/add documents (upload).

      All data changes are logged.
  * Analyst has option to delete data in the registry.
    * All data changes are logged.
* DRS-19: Analyst can use additional functions to simplify data searching (REQUIRED)
  * Filtering by search criteria by field content.
  * Full-text data search.
  * Order by each data field.
* DRS-20: Import data to the registry. Analyst has the option to import information into the database. Import formats are: JSON, CSV, XLS. (REQUIRED)
* DRS-21: Export data from the registry. Analyst has the option to export selected/filtered data from a registry to CSV/XLS, JSON. (REQUIRED)
* DRS-22: Statistical queries. The system should have the ability to (REQUIRED):
  1. Produce standard statistical reports
     * System must show statistics of all registered items in the registry, with various criteria for filtering. For example:
       * Details of registered people
       * Details of registered services
       * Time series: Change in registration of people/services over time
       * Details of change to data elements (audit logs)
     * Generate customizable reports based on the fields registered in the registry.
  2. Allow the analyst/user to analyze data collected in the system in various ways:
     * (Option) Develop functionality to allow custom dashboards for analysts to analyze data within databases.
     * Provide APIs for extracting data from databases to analyze in external data analytics systems (e.g. Tableau).
* DRS-33: Users can share data with other users. Share data with other users via e-mail, or via a unique and secure URL. Sharing must be at a record level and field level. Data sharing can be turned off in the authorization module. Data can be shared with anonymous users. The data shared with anonymous users is Open Data. (REQUIRED)
* DRS-28: Developer has the option to create a new registry database by sending data via API (REQUIRED). Developer is a user who is using API interface.&#x20;
  1. Name of the database;
  2. A short name;
  3. Schema of the database (see DRS-3).
* DRS-29: Developer can create multiple registry databases into one system instance. (REQUIRED)
* DRS-30: Developer has the option to publish the database. Publishing will reveal the database to users. (REQUIRED)
* DRS-31: Developer must be able to modify API services per registry database. (REQUIRED)
  * The system generates the API data structure from the dynamic database structure automatically each time a publish is done.
  * The system automatically creates API services to:
    * create data;
    * read data;
    * update data;
    * delete data;
    * validate data (if exists);
    * update or create data.
  * Developer can hide API services;
  * Developer can delete API services;
  * Developer can copy API services;
  * Developer can create custom API services.
* DRS-32: Developer has the option to read database schema via API. Developer has the option to read the list API services available per Database. (REQUIRED)

## 6.2 Applicant Functions <a href="#docs-internal-guid-d85f59a4-7fff-1564-6ae2-86d67f36a258" id="docs-internal-guid-d85f59a4-7fff-1564-6ae2-86d67f36a258"></a>

*   DRS-23: Building Block must enable client systems to process (CRUD) the database records via Open API services. (REQUIRED)

    * Applicant can search data;
    * Applicant can create data;
    * Applicant can read data;
    * Applicant can update data;
    * Applicant can delete data;
    * Applicant can create or update data.

    Building Block authorizes client systems and users to process data.
*   DRS-24: Building Block has the Open API service list (Swagger) to visualize all API services and API service versions. (REQUIRED)



    Client systems must be able to see all API service descriptions including:

    * Description of each field.
    * Example data of each field.

    If possible then the example must be real so that whoever is looking at the API specifications can test the example data in the service (try it).
* DRS-25: System has an API for PersonalData usage report. (REQUIRED)
  * API input must be configurable by the analyst. Input must be a unique identifier of the data owner(e.g. personal identification number).
  * If the registry database schema is designed to store personal data then the analyst must be able to link the personal data to the owner of personal data (e.g. citizen).
* DRS-26: Statistical queries via API. (OPTIONAL)
  * System should make data accessible through the API:
    * Registration Data;
    * Program Data.
  * API should allow querying data with multiple parameters:
    * Date, time ranges;
    * Registered Program.
  * Only authorized data should be available through the API.
* DRS-27: Using viewing event logs- every data owner has the right to see who has looked at their personal data. (REQUIRED)
  * Data owner is a physical person whose personal data is stored in the registry.
  * Data owner has the right to access data reading/processing event logs of the personal data they own. Personal data in a registry is marked accordingly (PersonalData) by the analyst.
  * PersonalData logs are visible via API or via User Interface (PersonalData report).

## Building Block Components

The Building Block has a user interface to query and consult the registry data but in most cases, the Applicants are using the end client applications like Registration Building Block to access the registry. Any Building Block can query data from Digital Registries Building Block via APIs if authorization is given.

![Digital registries functional components](<.gitbook/assets/image3 (1) (1).png>)
