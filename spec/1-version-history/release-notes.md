# Release Notes

## Version 3 <a href="#version-3" id="version-3"></a>

***

### **v3.0.0-alpha** <a href="#v3.0.0" id="v3.0.0"></a>

_Release date: June 2025_

_Authors: David Higgins, Ali González_

#### **Release Overview:**

This release is the result of the consolidation of a new Registries and Registration Working Group that worked between July 2025 and February 2026; The team discussed terminology and scope of the Registries Building Block and reviewed the current BB structure to reflect GovSpecs 2.0 Architecture. Since February, the team have discussed a re-scope of both the Registries and Registration BB and [opened articles for public comment](https://govstack.global/news/how-to-define-digital-registries-and-registration-in-the-govstack-context/). \
\
This early release represents the direction in which the Working Group will take the Registries and Registration solutions' space.&#x20;

Changelog per section is as follows:

| Section                                                            | Title                         | Change Level                                                           |
| ------------------------------------------------------------------ | ----------------------------- | ---------------------------------------------------------------------- |
| [Section 1](release-notes.md#section-1-version-history)            | Version History               | 🔴 Significant – Complete restructure and alignment to standard format |
| [Section 2](release-notes.md#section-2-description)                | Description                   | ⚠️ Moderate – Structural & content change                              |
| [Section 3](release-notes.md#section-3-terminology)                | Terminology                   | ⚠️ Moderate – Structural & content change                              |
| Section 4                                                          | Key Digital Functionalities   | ✅ No changes                                                           |
| [Section 5](release-notes.md#section-5-cross-cutting-requirements) | Cross-Functional Requirements | 🔴 Significant – Updated to reflect GovSpec Architecture 2.0           |
| Section 6                                                          | Functional Requirements       | ✅ No changes                                                           |
| Section 7                                                          | Data Structures               | ✅ No changes                                                           |
| Section 8                                                          | Service APIs                  | ✅ No changes                                                           |
| Section 9                                                          | Internal Workflows            | ✅ No changes                                                           |
| Section 10                                                         | Other Resources               | ✅ No changes                                                           |

#### Section 1: Version History

Significant changes to Version History. Now updated to include and versions and inclusion of detailed release notes page for all past versions.  Numbering aligned to semantic version numbering denoting previous 23Q4 as v2.0.0

#### Section 2: Description

Update to both text and diagrams to clarify current understanding of Digital Registries

#### Section 3: Terminology

Updated to point to GovStack General Terminology this has removed the following terms which are now in the GovStack General Terminology

* Claim
* Entity
* Registry

#### Section 5: Cross-Cutting Requirements

Significant change. This section has changed to now be referred to as Cross Functional Requirements in line with  GovSpecs Architecture 2.1.  All Cross Cutting requirements have been reviewed on this basis and the text is completely re-drafted including all requirements



***

## Version 2.0 <a href="#version-3" id="version-3"></a>

***

### **v2.0.0 (previously known as 23Q4)** <a href="#v3.0.0" id="v3.0.0"></a>

_Release date: December 2023_

#### **Release Overview:**

| Section                                                            | Title                       | Change Level                                                |
| ------------------------------------------------------------------ | --------------------------- | ----------------------------------------------------------- |
| Section 2                                                          | Description                 | ✅ No changes                                                |
| Section 3                                                          | Terminology                 | ✅ No changes                                                |
| Section 4                                                          | Key Digital Functionalities | ✅ No changes                                                |
| [Section 5](release-notes.md#section-5-cross-cutting-requirements) | Cross-Cutting Requirements  | ⚠️ Moderate – Structural & content changes                  |
| Section 6                                                          | Functional Requirements     | 🔵 Minor – Whitespace only                                  |
| [Section 7](release-notes.md#section-7-data-structures)            | Data Structures             | ⚠️ Moderate – Section removed                               |
| [Section 8](release-notes.md#section-8-service-apis)               | Service APIs                | 🔴 Significant – Multiple endpoint & infrastructure changes |
| Section 9                                                          | Internal Workflows          | ✅ No changes                                                |
| Section 10                                                         | Other Resources             | ✅ No changes                                                |

#### **Section 5 Cross-Cutting Requirements:**

The `5.1 Requirements` parent wrapper section was added in v2.0.0 (v23Q4), causing all sections to be renumbered and removing numbering conflicts that previously existed:

| v2.0.0(previously 23Q4)                                       | v.1.0                                                       | Notes                                                          |
| ------------------------------------------------------------- | ----------------------------------------------------------- | -------------------------------------------------------------- |
| 5.1 Requirements _(parent)_                                   | _did not exist_                                             | Parent wrapper added                                           |
| 5.1.1 Citizen-Centric (RECOMMENDED)                           | 5.1 Citizen-Centric (RECOMMENDED)                           | Renumbered                                                     |
| 5.1.2 Open (RECOMMENDED)                                      | 5.2 Open (RECOMMENDED)                                      | Renumbered                                                     |
| 5.1.3 Robust (RECOMMENDED)                                    | 5.3 Robust (RECOMMENDED)                                    | Renumbered                                                     |
| 5.1.4 Databases must not include business logic (RECOMMENDED) | 5.3 Databases must not include business logic (RECOMMENDED) | Renumbered — **⚠️ numbering conflict: 5.3 used twice in v1.0** |
| 5.1.5 Privacy and protection of user data (REQUIRED)          | 5.4 Privacy and protection of user data (REQUIRED)          | Renumbered                                                     |

v2.0.0 contains **5.2 Standards** and **5.2.1 OpenAPI** (referencing versions 3.0.0, 3.0.1, 3.1.0).

* This content is **absent from Section 5 in v1.0** — it was relocated to Section 7 (see below).



#### **Section 7 - Data Structures:**

v2.0.0 (23Q4) removed **Standards/Protocols** section:

> _"The following standards are applicable to data structures in the Digital Registries Building Block: OpenAPI Version 3.0.0, 3.0.1, 3.1.0."_

* **Note:** This is the same content that was moved to Section 5 (5.2 Standards / 5.2.1 OpenAPI in v2.0.0 (v23Q4). It has been **relocated** from Section 7 to Section 5.

#### **Section 8 - Service APIs:**

This section underwent significant changes with changes to API Endpoints and APIs

All API source file references have been updated from the **GitHub raw content CDN** to the **GitBook file storage CDN**, and the GitBook **space ID** has changed. This affects every single OpenAPI block in the document.

|                            | v1.0                                  | v2.0 (23Q4)                                                |
| -------------------------- | ------------------------------------- | ---------------------------------------------------------- |
| **Host**                   | `1641505654-files.gitbook.io`         | `834113276-files.gitbook.io`                               |
| **Space ID**               | `bOCHHFq0hQOuzuQ1QBAK`                | `Wox5PaYnPAhN0reOEf4y`                                     |
| **File format (Data API)** | Mixed: `.yaml` and `.json` references | Consistently `.json` (Data API) and `.yaml` (Database API) |

**API ENDPOINT PATH PARAMETER NAMING – Standardised to camelCase**

Path parameter names have been updated from `kebab-case` / lowercase to `camelCase` across all endpoints.

| v1.0 Path         | v2.0 (23Q4) Path  |
| ----------------- | ----------------- |
| `{registryname}`  | `{registryName}`  |
| `{versionnumber}` | `{versionNumber}` |
| `{ID}`            | `{id}`            |

**SECTION 8.1 Administrative/Analyst Functions – API Order & Endpoints Changed**

Order of APIs Reorganised and duplicate API that existed in v1.0 removed

| Type | v1.0                                                             | Type | v2.0 (23Q4)                                                                       |
| ---- | ---------------------------------------------------------------- | ---- | --------------------------------------------------------------------------------- |
| GET  | `/data/{registryname}/{versionnumber}` (YAML source)             | GET  | `/data/{registryName}/{versionNumber}`                                            |
|      |                                                                  | POST | `/data/{registryName}/{versionNumber}/read` _(moved up from position 6)_          |
| PUT  | `/data/{registryname}/{versionnumber}/update`                    | PUT  | `/data/{registryName}/{versionNumber}/update`                                     |
| POST | `/data/{registryname}/{versionnumber}/update-or-create`          | PUT  | `/data/{registryName}/{versionNumber}/updateEntries` _(moved up from position 5)_ |
| GET  | `/data/{registryname}/{versionnumber}` (JSON source — duplicate) |      | _(duplicate removed)_                                                             |
| POST | `/data/{registryname}/{versionnumber}/read`                      | POST | `/data/{registryName}/{versionNumber}/updateOrCreate` _(moved from position 3)_   |

Endpoint Path Changes in 8.1

| v1.0 Endpoint              | v2.0 (23Q4) Endpoint     | Change                          |
| -------------------------- | ------------------------ | ------------------------------- |
| `/update-entries` (PUT)    | `/updateEntries` (PUT)   | Renamed: kebab-case → camelCase |
| `/update-or-create` (POST) | `/updateOrCreate` (POST) | Renamed: kebab-case → camelCase |

**SECTION 8.2 Applicant Functions – API Order & Endpoints Changed**

Order of APIs Reorganised

| Type   | v1.0                                        | Type   | v2.0 (23Q4)                                                                   |
| ------ | ------------------------------------------- | ------ | ----------------------------------------------------------------------------- |
| GET    | `/{uuid}/read-value/{field}.{ext}`          | POST   | `/exists` _(moved up from postion 2)_                                         |
| POST   | `/exists`                                   | DELETE | `/{id}/delete` _(moved up from position 3)_                                   |
| DELETE | `/{ID}/delete`                              | GET    | `/{uuid}/readValue/{field}.{ext}` _(renamed and moved from position 1)_       |
| GET    | `/data/MyPersonalDataUsage/1.0`             | GET    | `/data/mypersonalDataUsage` _(renamed)_                                       |
| GET    | `/database/{id}`                            | GET    | `/database/{id}`                                                              |
| POST   | `/database/modify`                          | DELETE | `/database/{id}` _(moved from position 7)_                                    |
| DELETE | `/database/{id}`                            | POST   | `/database/modify` _(moved from position 6)_                                  |
| GET    | `/databases`                                | GET    | `/databases`                                                                  |
| POST   | `/data/mcts/1.4/create-entries`             | GET    | `/data/{registryName}/{versionNumber}` _(moved from position 10 and renamed)_ |
| GET    | `/data/{registryname}/{versionnumber}`      | POST   | `/data/mcts/createEntries` _(moved from position 9 and renamed)_              |
| POST   | `/data/{registryname}/{versionnumber}/read` | POST   | `/data/{registryName}/{versionNumber}/read` _(renamed)_                       |



**Endpoint Path Changes in 8.2**

| v1.0 Endpoint                               | v2.0 (23Q4) Endpoint                        | Change                                                          |
| ------------------------------------------- | ------------------------------------------- | --------------------------------------------------------------- |
| GET `/{uuid}/read-value/{field}.{ext}`      | GET `/{uuid}/readValue/{field}.{ext}`       | Renamed: kebab-case → camelCase                                 |
| GET `/data/MyPersonalDataUsage/1.0`         | GET `/data/mypersonalDataUsage`             | Renamed: removed version number `/1.0`, changed casing          |
| POST `/data/mcts/1.4/create-entries`        | POST `/data/mcts/createEntries`             | Renamed: removed version number `/1.4/`, kebab-case → camelCase |
| POST `/data/{registryname}/{versionnumber}` | POST `/data/{registryName}/{versionNumber}` | Renamed: kebab-case → camelCase                                 |
| GET `/data/{registryname}/{versionnumber}`  | GET `/data/{registryName}/{versionNumber}`  | Renamed: kebab-case → camelCase                                 |

**IMAGE URLs – Updated to New GitBook Space**

Both diagram image URLs have been updated to reflect the new GitBook space, consistent with the API source file hosting change.

|                          | v1.0                                                              | v2.0 (23Q4)                                                      |
| ------------------------ | ----------------------------------------------------------------- | ---------------------------------------------------------------- |
| Logical data model image | `1641505654-files.gitbook.io/.../spaces/bOCHHFq0hQOuzuQ1QBAK/...` | `834113276-files.gitbook.io/.../spaces/Wox5PaYnPAhN0reOEf4y/...` |
| JSON schema image        | Same old space                                                    | Same new space                                                   |



***

## Version 1 <a href="#version-1" id="version-1"></a>

***

### **v1.0.0** <a href="#v1.0.0" id="v1.0.0"></a>

_Released date: August 2022_

#### **Overview**

Digital Registries Building Block was first published in TBC by the Registries Working Group as reference specification for implementers.
