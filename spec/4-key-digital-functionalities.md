---
description: >-
  Key Digital Functionalities describe the core (required) functions that this
  Building Block must be able to perform.
---

# 4 Key Digital Functionalities

The building block is an application meant to offer fast and intuitive database management functionalities to entities without the need of database experts. Digital Registries is simple to use like online Excel with advanced data management and connectivity options for advanced users. Digital Registries BB is a multi tenant platform where users can create and manage new registry databases. Each registry database created in the system will have automatically REST services generated.&#x20;

## 4.1 Administrative/Analyst Functions <a href="#docs-internal-guid-d85f59a4-7fff-1564-6ae2-86d67f36a258" id="docs-internal-guid-d85f59a4-7fff-1564-6ae2-86d67f36a258"></a>

The first user of the Building Block is an **Administrator/Analyst** who is building a new registry. The Analyst is the person who is building the new registry database, changing the existing database configuration, or simply administering the API user authorization. The Administrator/analyst is using a web user interface. The main functions of the Building Block for Analysts are:

1. Create a new register/database (API or Web user interface);
2. Create and configure the schema of the register (API or Web user interface);
3. Change schema configuration and publish the new version of the database and API services (API or Web user interface);
4. Enter data to the register (API or Web user interface);
5. View data records in the register (API or Web user interface);
6. Update data in the register (API or Web user interface);
7. Import/export data from/to external files;
8. Import/export registry database schema;
9. Create API services;
10. View statistics (API or Web user interface);
11. Inspect transaction log of registry data operations (API or Web user interface);
12. Manage access to registry data. Authorize users to see and edit registry records or data fields (Attribute-Based Access Control management);
13. Share data with other users via e-mail, or via a unique and secure Uniform Resource Locator (URL) sharing can be field level or record level.

## 4.2 Applicant Functions <a href="#docs-internal-guid-d85f59a4-7fff-1564-6ae2-86d67f36a258" id="docs-internal-guid-d85f59a4-7fff-1564-6ae2-86d67f36a258"></a>

The second main user is an **Applicant** who is consuming registry data via other Building Block (e.g. Registration Building Block) screen flow or via Information Mediator Building Block API services. The main functions of the Building Block for Applicants are:

1. Search data from the register (API service);
2. Read/pull data from the register (API service);
3. Create data in the register (API service);
4. Update data in the register (API service);
5. Delete data in the register (API service);
6. Validate if given content exists in specified register (API service);
7. Read statistics (API service).

The Building Block has a user interface to query and consult the registry data but in most cases, the Applicants are using the end client applications like Registration Building Block to access the registry. Any Building Block can query data from Digital Registries Building Block via APIs if authorization is given.

![Digital registries functional components](<.gitbook/assets/image3 (1) (1).png>)

## 4.3 Out of Scope Assumptions

* Distributed database architecture; Blockchain solutions; integrations with distributed architecture solutions.
* Automated data migration from Digital Registries solutions to external databases.
* Event notification to external endpoints.
