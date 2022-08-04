# 4  Key Digital Functionalities



The Key Digital Functionalities describe the core (required) functions that this building block must be able to perform. These functionalities are described as business processes as opposed to technical specifications or API definitions.&#x20;

The first user of the BB is an **Administrator/Analyst** who is building a new registry.  The Analyst is the person who is building the new registry database, changing the existing database configuration or simply administering the API user authorization. The Administrator/analyst is using a web user interface. The main functions and UI of the BB for Analysts are:&#x20;

1. Create a new register/database (API or Web user interface);
2. Create and configure schema of the register(API or Web user interface);&#x20;
3. Change schema configuration and publish new version of the database and API services (API or Web user interface);
4. Enter data to the register (API or Web user interface);
5. View data records in the register (API or Web user interface);
6. Update data in the register (API or Web user interface);&#x20;
7. Import/export data from/to external files;
8. Import/export registry database schema;
9. Create  API services;&#x20;
10. View statistics(API or Web user interface);
11. Inspect transaction log of registry data operations (API or Web user interface).
12. Manage access to registry data. Authorize users to see and edit registry records or data field (ABAC based access management).&#x20;
13. Share data with other users via e-mail, or via unique and secure URL. sharing can be field level or record level.

The second main user is an **Applicant** who is consuming registry data via other BB (e.g. Registration BB) screen flow or via Information Mediator BB API services. The main functions of the BB for Applicants are:&#x20;

1. Search data from the register (API service);
2. Read/pull data from the register (API service);
3. Create data in the register(API service);
4. Update data in the register(API service);
5. Delete data in the register (API service);
6. Validate if given content exists in specified register (API service);  &#x20;
7. Read statistics (API service).

The BB has a user interface to query and consult the registry data but in most cases the Applicants are using the end client applications like Registration BB to access the registry. Any building block can query data from Digital Registries BB via APIs if authorization is given.

![Digital registries functional components](<.gitbook/assets/image3 (1) (1).png>)

## 4.1 Out of Scope Assumptions

* Distributed database architecture; Blockchain solutions; integrations with distributed architecture solutions.&#x20;
* Automated data migration from Digital Registries solution to external databases.
* Event notification to external endpoints.  &#x20;
