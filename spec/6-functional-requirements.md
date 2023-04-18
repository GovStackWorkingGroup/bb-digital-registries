---
description: This section lists the technical capabilities of this Building Block.
---

# 6 Functional Requirements

## 6.1 Administrative/Analyst Functions <a href="#docs-internal-guid-d85f59a4-7fff-1564-6ae2-86d67f36a258" id="docs-internal-guid-d85f59a4-7fff-1564-6ae2-86d67f36a258"></a>

The main functions of the Building Block for Analysts are:

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

## 6.2 Applicant Functions <a href="#docs-internal-guid-d85f59a4-7fff-1564-6ae2-86d67f36a258" id="docs-internal-guid-d85f59a4-7fff-1564-6ae2-86d67f36a258"></a>

The main functions of the Building Block for Applicants are:

1. Search data from the register (API service);
2. Read/pull data from the register (API service);
3. Create data in the register (API service);
4. Update data in the register (API service);
5. Delete data in the register (API service);
6. Validate if given content exists in specified register (API service);
7. Read statistics (API service).

## Building Block Components

The Building Block has a user interface to query and consult the registry data but in most cases, the Applicants are using the end client applications like Registration Building Block to access the registry. Any Building Block can query data from Digital Registries Building Block via APIs if authorization is given.

![Digital registries functional components](<.gitbook/assets/image3 (1) (1).png>)
