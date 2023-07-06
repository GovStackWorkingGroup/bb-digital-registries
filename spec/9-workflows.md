---
description: >-
  This section provides a detailed view of how this Building Block will interact
  with other Building Blocks to support common use cases.
---

# 9 Internal Workflows

## 9.1 Administrative/Analyst Functions <a href="#docs-internal-guid-d85f59a4-7fff-1564-6ae2-86d67f36a258" id="docs-internal-guid-d85f59a4-7fff-1564-6ae2-86d67f36a258"></a>

The Digital Registries building block facilitates the foloowing main internal workflows:

\
9.1.1 Create a registry database in User Interface

9.1.2 Process registry data in User Interface

9.1.3 Create registry database in API interface

### 9.1.1 User Story 1 - Create registry database in user interface <a href="#docs-internal-guid-51953ef5-7fff-4062-e282-1719dbc98029" id="docs-internal-guid-51953ef5-7fff-4062-e282-1719dbc98029"></a>

As an Administrator/Analyst I want to use a web user interface to create a register database (example registry use case - social security program) so that I can configure and launch the registry database instantly to be used by internet users and client systems (e.g. Registration Building Block, Information Mediator Building Block) via web interface and API.

**Actors**: Analyst - An administrator user who is creating/changing the registry database schema. The main actor/user in these requirements is the Analyst.

**Preconditions**:

1. User is authenticated;
2. User is authorized as an admin;
3. User interface is a web interface;
4. User has internet;
5. System has electricity.

**Process:**

1. Create a new registry database project.
2. Define the database fields.
3. Publish the database.
4. Validate/configure the API services.
5. Manage user rights to access the database and APIs.



**Post conditions:**

1. System contains a database that is ready to process new data.
2. System has API services to CRUD (Create, Read, Update, Delete) data (and API to validate if data exist).
3. User can enter data to the registry via web user interface (UI).
4. User can see log information in the UI.
5. User can see statistics in the UI.
6. User can give authorization to use the database and process data.
7. System contains a database that is ready to process new data.
8. System has API services to CRUD data (and API to validate if data exist).
9. User can enter data to the registry via web UI.
10. User can see log information in the UI.
11. User can see statistics in the UI.
12. User can give authorization to use the database and process data.

### 9.1.2 User Story 2 - Process registry data in User Interface <a href="#docs-internal-guid-31701a28-7fff-8c98-6f59-06d5eed22cd9" id="docs-internal-guid-31701a28-7fff-8c98-6f59-06d5eed22cd9"></a>

As an Administrator/Analyst, I want to process (Create, Read, Update, Delete) registry data so that I do not have to know the query language.

**Actors**

* Analyst: the main actor in these requirements is the Analyst/Administrator.
* Data owner: a physical person whose personal data is stored in the registry.

**Preconditions:**

1. Analyst is authenticated and authorized to use the Building Block and process data in the database;
2. The user interface is a web interface;
3. User has internet;
4. System has electricity.

**Process**:

1. Analyst searches a record via search or filter function;
2. Analyst selects a record;
3. Analyst processes a record;
4. System stores changes to the Change Log database.

**Postconditions**:

Processing changes by Analyst are done and log for change is created.

### 9.1.3 User Story 3- Create registry database in API interface <a href="#docs-internal-guid-49b62261-7fff-0ca4-5ac9-2267b594ffc6" id="docs-internal-guid-49b62261-7fff-0ca4-5ac9-2267b594ffc6"></a>

As an IT developer, I want to Create/update/delete registry database schema via API services.

**Actors**

* IT developer (Developer): Main actor in these requirements is planning to open a new business program and web form to capture applicants' data. Captured data must be registered in the registry. In this use case, a Developer is any user who is using API services to create and manage registries database.

**Preconditions**:

1. Developer is using API with a client system or a script that is connected to Information Mediator Building Block. Client system is any Building Block that is using API services via Information Mediator;
2. IT Developer (Information Mediator organization) has been given authorization to Create/update/delete database schema via API services.
3. Developer has internet;
4. System has electricity.

**Process**:

1. Developer uses a client system to edit the registry database in the Building Block. Developer can:
   1. Create database schema;
   2. Read database schema;
   3. Modify database schema;
   4. Delete database schema and all data in it.

**Postconditions**:

1. When Developer is authorized to use Building Block API then the Digital Registries Building Block allows processing CRUD (Create, Read, Update, Delete) schema of a registry, and all authorized users can;
2. When Developer is not authorized to process/CRUD the database schema, the system allows to process schema of all databases where an anonymous user has been allowed to edit the database schema (simplification for GovStack Sandbox instance);
3. When a user has no authorization, one can not create nor change (CRUD) any schema in the Building Block.



## 9.2 Applicant Functions <a href="#docs-internal-guid-d85f59a4-7fff-1564-6ae2-86d67f36a258" id="docs-internal-guid-d85f59a4-7fff-1564-6ae2-86d67f36a258"></a>

9.2.1 Process data in API interface

### 9.2.1 User Story 4 - Process data in API interface

As an Applicant, I want to process CRUD (Create, Read, Update, Delete) data in the registry database.

**Actors**:

* Applicant - The main actor in these requirements is an applicant via the client system. In this use case applicant is any user who is using a client system (Registration Building Block). For example, a Health Care worker is an applicant in this user story; a mother, using the Registration Building Block. An example client system in this document is Registration Building Block.

**Preconditions**:

1. Applicant is using client system (e.g. Registration Building Block) that is connected to Information Mediator Building Block;
2. Client system has been given authorization to access Registry to process (CRUD) information;
3. Applicant has been given authorization to access Registry to process (CRUD) information;
4. Applicants are registered in the system and able to use authentication. Applicant is Authenticated by client system or Security Building Block (Authentication).
5. Applicant has internet;
6. System has electricity.

**Process**:

1. Applicant uses a client system to process data in the registry
   * Applicant can create data;
   * Applicant can read data;
   * Applicant can update data;
   * Applicant can delete data;
   * Applicant can create or update data;
   * Applicant can validate data.
2. System logs all processing events in the dedicated audit registry.

**Postconditions**:

1. When Applicant is authenticated by a client system (e.g. Registration Building Block) the registry allows processing (CRUD) information from the registry. All users who are authenticated can read data.
2. When a user is not authenticated in the system, the system allows processing (CRUD) data from all databases where an anonymous user has been allowed to process data.
3. When a user has no authorization, one can not process (CRUD) any information in the registry.

### &#x20;<a href="#docs-internal-guid-49b62261-7fff-0ca4-5ac9-2267b594ffc6" id="docs-internal-guid-49b62261-7fff-0ca4-5ac9-2267b594ffc6"></a>

