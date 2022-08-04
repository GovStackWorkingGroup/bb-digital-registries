# 8 Service APIs

This section describes external APIs that must be implemented by the building block. Additional APIs may be implemented by the building block (all APIs must adhere to the standards and protocols defined), but the listed APIs define a minimal set that must be provided by any implementation.

Registries BB may contain multiple registries/databases. The dynamic nature of the database structure requires a standard set automatically generated APIs for all databases hosted on the platform. The system generates default API method endpoints automatically after each publish of the database schema. A new API service version is generated after each schema publish. Database schema version and API versions are in sync.

The naming convention and a structure of the API endpoint is the following:

/{information type}/{registry acronym or code}/{version}/{API method as a name}.

Example 1: ​/api/data​/cr​/1.0​/create

Example 2: ​/api/v1/database/modify

Each registry contains a unique set of data and the BB enables an Analyst to change the data storage structure/schema on the fly. In this following example API descriptions are generated for one example dataset for the Postpartum Infant Care Program registry, where Caretaker and infant child is registered and registration ID is issued.

![Example registry database logical data model. ](<.gitbook/assets/Logical datamodel MCTS (1).JPG>)

![Example registry database Json schema.](<.gitbook/assets/image4 (1) (1) (1).png>)

Digital registries BB is expected to host the following API services for each database hosted on the platform

## 8.1 DATA CREATE <a href="#docs-internal-guid-f400fe68-7fff-bffb-3d00-0b067c81eb40" id="docs-internal-guid-f400fe68-7fff-bffb-3d00-0b067c81eb40"></a>

Description: Creates a new record in the registry database.

Request endpoint: POST /data/{code}/{version}/create

Example API: [see in github](https://github.com/ingmarvali/BuildingBlockAPI/blob/main/DigitalRegistriesBB/GovStack\_Digital\_registries\_BB\_Data\_API\_template-1.1.0.json).

{% swagger src="https://raw.githubusercontent.com/ingmarvali/BuildingBlockAPI/main/DigitalRegistriesBB/GovStack_Digital_registries_BB_Data_API_template-1.1.0.json" path="undefined" method="undefined" %}
[https://raw.githubusercontent.com/ingmarvali/BuildingBlockAPI/main/DigitalRegistriesBB/GovStack_Digital_registries_BB_Data_API_template-1.1.0.json](https://raw.githubusercontent.com/ingmarvali/BuildingBlockAPI/main/DigitalRegistriesBB/GovStack_Digital_registries_BB_Data_API_template-1.1.0.json)
{% endswagger %}

## 8.2 DATA UPDATE

Description: Updates one existing record in the registry database.

Request endpoint: PUT /data/{code}/{version}/update

Example API: [see in github](https://github.com/ingmarvali/BuildingBlockAPI/blob/main/DigitalRegistriesBB/GovStack\_Digital\_registries\_BB\_Data\_API\_template-1.1.0.json).

{% swagger src="https://raw.githubusercontent.com/ingmarvali/BuildingBlockAPI/main/DigitalRegistriesBB/GovStack_Digital_registries_BB_Data_API_template-1.1.0.json" path="undefined" method="undefined" %}
[https://raw.githubusercontent.com/ingmarvali/BuildingBlockAPI/main/DigitalRegistriesBB/GovStack_Digital_registries_BB_Data_API_template-1.1.0.json](https://raw.githubusercontent.com/ingmarvali/BuildingBlockAPI/main/DigitalRegistriesBB/GovStack_Digital_registries_BB_Data_API_template-1.1.0.json)
{% endswagger %}

## 8.3 DATA UPDATE-OR-CREATE

Description: API updates existing record if matching with input parameters is successful. If record is not found the API will create a new record.

Request endpoint: POST /data/{code}/{version}/update-or-create

Example API: [see in github](https://github.com/ingmarvali/BuildingBlockAPI/blob/main/DigitalRegistriesBB/GovStack\_Digital\_registries\_BB\_Data\_API\_template-1.1.0.json).

## 8.4 DATA UPDATE-ENTRIES

Description: Updates multiple records in the registry database that match the input query.

Request endpoint: PUT /data/{code}/{version}/update-entries

Example API: [see in github](https://github.com/ingmarvali/BuildingBlockAPI/blob/main/DigitalRegistriesBB/GovStack\_Digital\_registries\_BB\_Data\_API\_template-1.1.0.json).

## 8.5 DATA LIST (Search)

Description: Searches (Regex supported) and returns multiple records as an array-list.

Request endpoint: GET /data/{code}/{version}

Example API: [see in github](https://github.com/ingmarvali/BuildingBlockAPI/blob/main/DigitalRegistriesBB/GovStack\_Digital\_registries\_BB\_Data\_API\_template-1.1.0.json).

## 8.6 DATA READ

Description: Searches and returns one record.

Request endpoint: POST /data/{code}/{version}/read

Example API: [see in github](https://github.com/ingmarvali/BuildingBlockAPI/blob/main/DigitalRegistriesBB/GovStack\_Digital\_registries\_BB\_Data\_API\_template-1.1.0.json).

## 8.7 DATA READ-VALUE

Description: Searches and returns one record’s one field value.

Request endpoint: GET /data/{code}/{version}/{ID}/read-value/{field}.{ext}

Example API: [see in github](https://github.com/ingmarvali/BuildingBlockAPI/blob/main/DigitalRegistriesBB/GovStack\_Digital\_registries\_BB\_Data\_API\_template-1.1.0.json).

## 8.8 DATA EXISTS

Description: Searches records based on input parameters and returns boolean answer (true/false).

Request endpoint: POST /data/{code}/{version}/exists

Example API: [see in github](https://github.com/ingmarvali/BuildingBlockAPI/blob/main/DigitalRegistriesBB/GovStack\_Digital\_registries\_BB\_Data\_API\_template-1.1.0.json).

## 8.9 DATA DELETE

Description: Delete record.

Request endpoint: DELETE /data/{code}/{version}/{ID}/delete

Example API: [see in github](https://github.com/ingmarvali/BuildingBlockAPI/blob/main/DigitalRegistriesBB/GovStack\_Digital\_registries\_BB\_Data\_API\_template-1.1.0.json).

## 8.10 DATA My personal data usage

Description: The purpose of this API is to make personal data protection better and make BB personal data usage transparent by showing who has looked at personal data of the user. Each user can see who has looked at their personal data and when. The definition of personal data is described by each BB owner in the respective country.

Request endpoint: GET /data/MyPersonalDataUsage/{version}

Example API: [see in github](https://github.com/ingmarvali/BuildingBlockAPI/blob/main/DigitalRegistriesBB/GovStack\_Digital\_registries\_BB\_Data\_API\_template-1.1.0.json).

**Database Schema APIs are following:**

## 8.11 DATABASE SCHEMA READ

Description: API reads existing registry database schema.

Request endpoint: GET /api/V1/database/{id}

Example API: [see in github](https://github.com/ingmarvali/BuildingBlockAPI/blob/main/DigitalRegistriesBB/GovStack\_Digital\_registries\_BB\_Database\_API\_template-1.1.0.json).

## 8.12 DATABASE SCHEMA MODIFY

Description: API creates a new registry database schema or updates existing schema if matching with input parameters is successful. If schema is not found the API will create a new schema.

Request endpoint: POST /api/V1/database/modify

Example API: [see in github](https://github.com/ingmarvali/BuildingBlockAPI/blob/main/DigitalRegistriesBB/GovStack\_Digital\_registries\_BB\_Database\_API\_template-1.1.0.json).

## 8.13 DATABASE SCHEMA DELETE

Description: API deletes registry database.

Request endpoint: DELETE /api/v1/database/{id}

Example API: [see in github](https://github.com/ingmarvali/BuildingBlockAPI/blob/main/DigitalRegistriesBB/GovStack\_Digital\_registries\_BB\_Database\_API\_template-1.1.0.json).

## 8.14 DATABASES LIST

Description: API gets all databases and schema versions as a list array.\
Request endpoint: GET /api/v1/databases\
Example API: [see in github](https://github.com/ingmarvali/BuildingBlockAPI/blob/main/DigitalRegistriesBB/GovStack\_Digital\_registries\_BB\_Database\_API\_template-1.1.0.json).\
\
**Standards/Protocols:**

The API is built using representational state transfer (REST) software architectural style ([https://restfulapi.net/](https://restfulapi.net)) and described in Open API 3 standard\
([https://swagger.io/specification/](https://swagger.io/specification/)) using YAML (a human-readable data-serialization language - [http://yaml.org/](http://yaml.org)). Request and response body is in JSON (lightweight data-interchange format - [https://www.json.org/json-en.html](https://www.json.org/json-en.html)).
