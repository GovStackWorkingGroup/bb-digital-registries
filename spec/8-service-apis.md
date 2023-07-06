---
description: >-
  This section provides a reference for APIs that should be implemented by this
  Building Block.
---

# 8 Service APIs

The APIs defined here establish a blueprint for how the Building Block will interact with other Building Blocks. Additional APIs may be implemented by the Building Block, but the listed APIs define a minimal set of functionality that should be provided by any implementation of this Building Block.&#x20;

The [GovStack non-functional requirements document](https://govstack.gitbook.io/specification/v/1.0/architecture-and-nonfunctional-requirements/6-onboarding) provides additional information on how 'adaptors' may be used to translate an existing API to the patterns described here. This section also provides guidance on how candidate products are tested and how GovStack validates a product's API against the API specifications defined here.&#x20;

The tests for the Digital Registries Building Block can be found in [this GitHub repository](https://github.com/GovStackWorkingGroup/bb-digital-registries/tree/main/test/openAPI).

The Digital Registries Building Block may contain multiple registries/databases. The dynamic nature of the database structure requires a standard set of automatically generated APIs for all databases hosted on the platform. The system generates default API method endpoints automatically after each publication of the database schema. A new API service version is generated after each schema publish. Database schema version and API versions are in sync.

The naming convention and structure of the API endpoint are the following:

/{information type}/{registry acronym or code}/{version}/{API method as a name}.

Example 1: ​/api/data​/cr​/1.0​/create

Example 2: ​/api/v1/database/modify

Each registry contains a unique set of data and the Building Block enables an Analyst to change the data storage structure/schema on the fly. In the following example API descriptions are generated for one example dataset for the Postpartum Infant Care Program registry, where the Caretaker and infant child are registered and a registration ID is issued.

![Example registry database logical data model.](<.gitbook/assets/Logical datamodel MCTS (1).JPG>)

![Example registry database Json schema.](<.gitbook/assets/image4 (1) (1) (1).png>)

Digital Registries Building Block is expected to host the following API services for each database hosted on the platform.

The API is built using a representational state transfer ([REST](https://restfulapi.net/)) software architectural style and described in [Open API 3 standard](https://swagger.io/specification/) using [YAML](https://yaml.org/) (a human-readable data-serialization language). Request and response body is in [JSON](https://www.json.org/json-en.html) (lightweight data-interchange format).

## 8.1 Administrative/Analyst Functions <a href="#docs-internal-guid-d85f59a4-7fff-1564-6ae2-86d67f36a258" id="docs-internal-guid-d85f59a4-7fff-1564-6ae2-86d67f36a258"></a>

{% swagger src="https://raw.githubusercontent.com/GovStackWorkingGroup/bb-digital-registries/main/api/GovStack_Digital_registries_BB_Data_API_template-1.3.0.yaml" path="/data/{registryname}/{versionnumber}" method="get" %}
[https://raw.githubusercontent.com/GovStackWorkingGroup/bb-digital-registries/main/api/GovStack_Digital_registries_BB_Data_API_template-1.3.0.yaml](https://raw.githubusercontent.com/GovStackWorkingGroup/bb-digital-registries/main/api/GovStack_Digital_registries_BB_Data_API_template-1.3.0.yaml)
{% endswagger %}

{% swagger src="https://raw.githubusercontent.com/GovStackWorkingGroup/bb-digital-registries/main/api/GovStack_Digital_registries_BB_Data_API_template-1.3.0.json" path="/data/{registryname}/{versionnumber}/update" method="put" %}
[https://raw.githubusercontent.com/GovStackWorkingGroup/bb-digital-registries/main/api/GovStack_Digital_registries_BB_Data_API_template-1.3.0.json](https://raw.githubusercontent.com/GovStackWorkingGroup/bb-digital-registries/main/api/GovStack_Digital_registries_BB_Data_API_template-1.3.0.json)
{% endswagger %}

{% swagger src="https://raw.githubusercontent.com/GovStackWorkingGroup/bb-digital-registries/main/api/GovStack_Digital_registries_BB_Data_API_template-1.3.0.json" path="/data/{registryname}/{versionnumber}/update-or-create" method="post" %}
[https://raw.githubusercontent.com/GovStackWorkingGroup/bb-digital-registries/main/api/GovStack_Digital_registries_BB_Data_API_template-1.3.0.json](https://raw.githubusercontent.com/GovStackWorkingGroup/bb-digital-registries/main/api/GovStack_Digital_registries_BB_Data_API_template-1.3.0.json)
{% endswagger %}

{% swagger src="https://raw.githubusercontent.com/GovStackWorkingGroup/bb-digital-registries/main/api/GovStack_Digital_registries_BB_Data_API_template-1.3.0.json" path="/data/{registryname}/{versionnumber}/update-entries" method="put" %}
[https://raw.githubusercontent.com/GovStackWorkingGroup/bb-digital-registries/main/api/GovStack_Digital_registries_BB_Data_API_template-1.3.0.json](https://raw.githubusercontent.com/GovStackWorkingGroup/bb-digital-registries/main/api/GovStack_Digital_registries_BB_Data_API_template-1.3.0.json)
{% endswagger %}

{% swagger src="https://raw.githubusercontent.com/GovStackWorkingGroup/bb-digital-registries/main/api/GovStack_Digital_registries_BB_Data_API_template-1.3.0.json" path="/data/{registryname}/{versionnumber}" method="get" %}
[https://raw.githubusercontent.com/GovStackWorkingGroup/bb-digital-registries/main/api/GovStack_Digital_registries_BB_Data_API_template-1.3.0.json](https://raw.githubusercontent.com/GovStackWorkingGroup/bb-digital-registries/main/api/GovStack_Digital_registries_BB_Data_API_template-1.3.0.json)
{% endswagger %}

{% swagger src="https://raw.githubusercontent.com/GovStackWorkingGroup/bb-digital-registries/main/api/GovStack_Digital_registries_BB_Data_API_template-1.3.0.json" path="/data/{registryname}/{versionnumber}/read" method="post" %}
[https://raw.githubusercontent.com/GovStackWorkingGroup/bb-digital-registries/main/api/GovStack_Digital_registries_BB_Data_API_template-1.3.0.json](https://raw.githubusercontent.com/GovStackWorkingGroup/bb-digital-registries/main/api/GovStack_Digital_registries_BB_Data_API_template-1.3.0.json)
{% endswagger %}

## 8.2 Applicant Functions <a href="#docs-internal-guid-d85f59a4-7fff-1564-6ae2-86d67f36a258" id="docs-internal-guid-d85f59a4-7fff-1564-6ae2-86d67f36a258"></a>

{% swagger src="https://raw.githubusercontent.com/GovStackWorkingGroup/bb-digital-registries/main/api/GovStack_Digital_registries_BB_Data_API_template-1.3.0.json" path="/data/{registryname}/{versionnumber}/{uuid}/read-value/{field}.{ext}" method="get" %}
[https://raw.githubusercontent.com/GovStackWorkingGroup/bb-digital-registries/main/api/GovStack_Digital_registries_BB_Data_API_template-1.3.0.json](https://raw.githubusercontent.com/GovStackWorkingGroup/bb-digital-registries/main/api/GovStack_Digital_registries_BB_Data_API_template-1.3.0.json)
{% endswagger %}

{% swagger src="https://raw.githubusercontent.com/GovStackWorkingGroup/bb-digital-registries/main/api/GovStack_Digital_registries_BB_Data_API_template-1.3.0.json" path="/data/{registryname}/{versionnumber}/exists" method="post" %}
[https://raw.githubusercontent.com/GovStackWorkingGroup/bb-digital-registries/main/api/GovStack_Digital_registries_BB_Data_API_template-1.3.0.json](https://raw.githubusercontent.com/GovStackWorkingGroup/bb-digital-registries/main/api/GovStack_Digital_registries_BB_Data_API_template-1.3.0.json)
{% endswagger %}

{% swagger src="https://raw.githubusercontent.com/GovStackWorkingGroup/bb-digital-registries/main/api/GovStack_Digital_registries_BB_Data_API_template-1.3.0.json" path="/data/{registryname}/{versionnumber}/{ID}/delete" method="delete" %}
[https://raw.githubusercontent.com/GovStackWorkingGroup/bb-digital-registries/main/api/GovStack_Digital_registries_BB_Data_API_template-1.3.0.json](https://raw.githubusercontent.com/GovStackWorkingGroup/bb-digital-registries/main/api/GovStack_Digital_registries_BB_Data_API_template-1.3.0.json)
{% endswagger %}

{% swagger src="https://raw.githubusercontent.com/GovStackWorkingGroup/bb-digital-registries/main/api/GovStack_Digital_registries_BB_Data_API_template-1.3.0.json" path="/data/MyPersonalDataUsage/1.0" method="get" %}
[https://raw.githubusercontent.com/GovStackWorkingGroup/bb-digital-registries/main/api/GovStack_Digital_registries_BB_Data_API_template-1.3.0.json](https://raw.githubusercontent.com/GovStackWorkingGroup/bb-digital-registries/main/api/GovStack_Digital_registries_BB_Data_API_template-1.3.0.json)
{% endswagger %}

{% swagger src="https://raw.githubusercontent.com/GovStackWorkingGroup/bb-digital-registries/main/api/GovStack_Digital_registries_BB_Database_API_template-1.3.0.json" path="/database/{id}" method="get" %}
[https://raw.githubusercontent.com/GovStackWorkingGroup/bb-digital-registries/main/api/GovStack_Digital_registries_BB_Database_API_template-1.3.0.json](https://raw.githubusercontent.com/GovStackWorkingGroup/bb-digital-registries/main/api/GovStack_Digital_registries_BB_Database_API_template-1.3.0.json)
{% endswagger %}

{% swagger src="https://raw.githubusercontent.com/GovStackWorkingGroup/bb-digital-registries/main/api/GovStack_Digital_registries_BB_Database_API_template-1.3.0.json" path="/database/modify" method="post" %}
[https://raw.githubusercontent.com/GovStackWorkingGroup/bb-digital-registries/main/api/GovStack_Digital_registries_BB_Database_API_template-1.3.0.json](https://raw.githubusercontent.com/GovStackWorkingGroup/bb-digital-registries/main/api/GovStack_Digital_registries_BB_Database_API_template-1.3.0.json)
{% endswagger %}

{% swagger src="https://raw.githubusercontent.com/GovStackWorkingGroup/bb-digital-registries/main/api/GovStack_Digital_registries_BB_Database_API_template-1.3.0.json" path="/database/{id}" method="delete" %}
[https://raw.githubusercontent.com/GovStackWorkingGroup/bb-digital-registries/main/api/GovStack_Digital_registries_BB_Database_API_template-1.3.0.json](https://raw.githubusercontent.com/GovStackWorkingGroup/bb-digital-registries/main/api/GovStack_Digital_registries_BB_Database_API_template-1.3.0.json)
{% endswagger %}

{% swagger src="https://raw.githubusercontent.com/GovStackWorkingGroup/bb-digital-registries/main/api/GovStack_Digital_registries_BB_Database_API_template-1.3.0.json" path="/databases" method="get" %}
[https://raw.githubusercontent.com/GovStackWorkingGroup/bb-digital-registries/main/api/GovStack_Digital_registries_BB_Database_API_template-1.3.0.json](https://raw.githubusercontent.com/GovStackWorkingGroup/bb-digital-registries/main/api/GovStack_Digital_registries_BB_Database_API_template-1.3.0.json)
{% endswagger %}

{% swagger src="https://raw.githubusercontent.com/GovStackWorkingGroup/bb-digital-registries/main/api/GovStack_Digital_registries_BB_Data_API_template-1.3.0.json" path="/data/mcts/1.4/create-entries" method="post" %}
[https://raw.githubusercontent.com/GovStackWorkingGroup/bb-digital-registries/main/api/GovStack_Digital_registries_BB_Data_API_template-1.3.0.json](https://raw.githubusercontent.com/GovStackWorkingGroup/bb-digital-registries/main/api/GovStack_Digital_registries_BB_Data_API_template-1.3.0.json)
{% endswagger %}

{% swagger src="https://raw.githubusercontent.com/GovStackWorkingGroup/bb-digital-registries/main/api/GovStack_Digital_registries_BB_Data_API_template-1.3.0.json" path="/data/{registryname}/{versionnumber}" method="get" %}
[https://raw.githubusercontent.com/GovStackWorkingGroup/bb-digital-registries/main/api/GovStack_Digital_registries_BB_Data_API_template-1.3.0.json](https://raw.githubusercontent.com/GovStackWorkingGroup/bb-digital-registries/main/api/GovStack_Digital_registries_BB_Data_API_template-1.3.0.json)
{% endswagger %}

{% swagger src="https://raw.githubusercontent.com/GovStackWorkingGroup/bb-digital-registries/main/api/GovStack_Digital_registries_BB_Data_API_template-1.3.0.json" path="/data/{registryname}/{versionnumber}/read" method="post" %}
[https://raw.githubusercontent.com/GovStackWorkingGroup/bb-digital-registries/main/api/GovStack_Digital_registries_BB_Data_API_template-1.3.0.json](https://raw.githubusercontent.com/GovStackWorkingGroup/bb-digital-registries/main/api/GovStack_Digital_registries_BB_Data_API_template-1.3.0.json)
{% endswagger %}
