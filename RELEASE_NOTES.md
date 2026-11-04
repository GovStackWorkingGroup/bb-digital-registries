# Release history

Release records and contributor credits are retained in the repository. The current `3.0.0-alpha.2` content remains an unreleased draft.

## 1 Version History <a href="#versions-1-version-history" id="versions-1-version-history"></a>

| Version | Contributors | Comment |
|---|---|---|
| 0.7, 0.8, and 0.9 | Initial authors and reviewers listed below | Initial drafts and technical review. |
| 1.0, May 2023 | Ingmar Vali; reviewers Steve Conrad, Wes Brown, and Valeria Tafoya | First GovStack 1.0-aligned release. |
| 2.0, November 2023 | Authors and editors listed below | Updated cross-cutting requirements, service APIs, and the test suite. Breaking change. |
| 3.0.0-alpha.1, June 2026 | Coordinators, authors, and editors listed below | Expanded scope and alignment work for GovStack Architecture 2.x. Public alpha release. |
| 3.0.0-alpha.2, August 2026 | Digital Registries Working Group | Reframed the alpha as a domain-neutral Registry Core with mandatory Consultation Retrieve and additional capability families. Breaking prerelease change. |

### Current alpha draft revision <a href="#versions-current-alpha-draft-revision" id="versions-current-alpha-draft-revision"></a>

The 6 September 2026 revision of the `3.0.0-alpha.2` draft replaced universal Consultation Retrieve with mandatory Registry Core plus at least one selected Registry service operation. The current requirement model expresses that rule as two core functionalities and the REQUIRED `registry-service` variation point with `select.min: 1`. This remains a revision of the same alpha draft, not a new release; no conformance claim is available.

The revision adds DRAFT requirements and a [canonical HTTP contract](resources/api.yml) for four independently selectable Consultation operation options: Retrieve, Lookup, List, and Search. GET serves Retrieve and List; POST carries exact Lookup and Search criteria. All four share a Record representation. List and Search use live cursor pagination with repeated criteria and a fixed effective page size.

The 8 October 2026 revision distinguishes baseline pagination from selectable stronger operation features. Baseline List and Search publish bounded responses, deterministic ordering, fixed-size context-bound continuation, resource limits, and timeout behaviour without claiming exhaustive backend traversal. Operations can separately declare conditional Retrieve, field selection, complete traversal, or snapshot traversal; omitted features make no such promise.

The 29 October 2026 revision makes logical Collections explicit in the canonical `/v1/collections/{collectionId}` hierarchy and keeps Record identity stable across Collections. It adds selectable source-backed Revision List and Revision Retrieve capabilities, recorded-time and effective-time selection, reusable named Search semantics, caller-filtered capability discovery, and trusted purpose binding. The revision does not mandate a civil-registration legal model, a universal query language, historical storage, or purpose on every operation.

The Record model accepts stable source identifiers within a Registry and permits Registry and schema context through the endpoint, versioned contract, or response. Source revision, lifecycle, and recording time are not required unless a selected capability or profile requires them. Field meanings remain documented.

The [household](api/examples/household-registry.openapi.yaml) and [birth-registration](api/examples/birth-registration.openapi.yaml) contracts illustrate nested components, Record references, recorded related details, and bounded arrays with declared completeness. API Design Guide `0.3.0-draft` accompanies these choices. Contract and example validation is published separately from implementation conformance testing.

### Contributors by release <a href="#versions-contributors-by-release" id="versions-contributors-by-release"></a>

#### Versions 0.7 and 0.8 <a href="#versions-versions-07-and-08" id="versions-versions-07-and-08"></a>

Authors: Frank Grozel, Ingmar Vali, Tambet Artma, Saurav Bhattarai, Dr. P. S. Ramkumar, and Rauno Kulla.

Version 0.8 reviewers: Neil Roy, Aare Lapõnin, and Amy Darling.

#### Version 0.9 <a href="#versions-version-09" id="versions-version-09"></a>

Authors: Ingmar Vali, Sebastian Leidig, Frank Grozel, and Tambet Artma.

Technical reviewers: Tony Shannon, Saša Kovačević, Riham Moawad, Riham Fahmi, Aare Laponin, Manish Srivastava, Palab Saha, Surendra Singh Sucharia, Arvind Gupta, Gayatri P., Shivank Singh Chauhan, and Gavin Lyons.

Reviewers: Steve Conrad, Wes Brown, and Valeria Tafoya.

#### Version 2.0 <a href="#versions-version-20" id="versions-version-20"></a>

Authors: Sebastian Leidig, Steve Conrad, Łukasz Ruzicki, Damian Borowiecki, Karolina Kopacz, and Paweł Gesek.

Reviewer: Sebastian Leidig. Editors: Steve Conrad and Valeria Tafoya.

#### Version 3.0.0-alpha.1 <a href="#versions-version-300-alpha1" id="versions-version-300-alpha1"></a>

Coordinators: Dr. Bimal Kumar, Xilene Siquero, and Sebastian Leidig.

Authors: Janet Ngugi, Vivek Rana, Chinenye Ifebirinachi, Ananya Jha, Umang Gupta, Leonora Smart-Abbey, and Jeremi Joslin.

Editors: Ali González-García and David Higgins.

The detailed change record is preserved in the [Release Notes](#release-release-notes).

### 4 November 2026 Write draft revision <a href="#versions-4-november-2026-write-draft-revision" id="versions-4-november-2026-write-draft-revision"></a>

The same unreleased alpha now defines separately selectable direct creation, direct update, direct named transitions, and approval-based change requests. The DRAFT [Write binding](requirements/registry-services.md#write-write) and [contract](resources/write-api.yml) distinguish proposal review from authoritative application, protect source and proposal versions separately, and declare retry, disclosure, and compound-operation guarantees. The [birth and household examples](resources/api-examples/README.md) remain non-normative and do not select a required domain model. No release, implementation conformance claim, or deployed workflow is established by these artifacts.

## Release Notes <a href="#release-release-notes" id="release-release-notes"></a>

### Version 3 <a href="#release-version-3" id="release-version-3"></a>

***

#### **v3.0.0-alpha.1** <a href="#release-v300-alpha1" id="release-v300-alpha1"></a>

_Release date: June 2026_

_Authors: David Higgins, Ali González-García_

##### **Release Overview:** <a href="#release-release-overview-1" id="release-release-overview-1"></a>

This release is the result of the consolidation of a new Registries and Registration Working Group that worked between July 2025 and June 2026; The team discussed terminology and scope of the Registries Building Block and reviewed the current BB structure to reflect GovSpecs 2.0 Architecture. Since February, the team have discussed a re-scope of both the Registries and Registration BB and [opened articles for public comment](https://govstack.global/news/how-to-define-digital-registries-and-registration-in-the-govstack-context/). \
\
This early release represents the direction in which the Working Group will take the Registries and Registration solutions' space.&#x20;

Change-log per section is as follows:

| Section                                                            | Title                         | Change Level                                                           |
| ------------------------------------------------------------------ | ----------------------------- | ---------------------------------------------------------------------- |
| [Section 1](#release-section-1-version-history)            | Version History               | 🔴 Significant – Complete restructure and alignment to standard format |
| [Section 2](#release-section-2-description)                | Description                   | ⚠️ Moderate – Structural & content change                              |
| [Section 3](#release-section-3-terminology)                | Terminology                   | ⚠️ Moderate – Structural & content change                              |
| Section 4                                                          | Key Digital Functionalities   | ✅ No changes                                                           |
| [Section 5](#release-section-5-cross-cutting-requirements) | Cross-Functional Requirements | 🔴 Significant – Updated to reflect GovSpec Architecture 2.0           |
| Section 6                                                          | Functional Requirements       | ✅ No changes                                                           |
| Section 7                                                          | Data Structures               | ✅ No changes                                                           |
| Section 8                                                          | Service APIs                  | ✅ No changes                                                           |
| Section 9                                                          | Internal Workflows            | ✅ No changes                                                           |
| Section 10                                                         | Other Resources               | ✅ No changes                                                           |

##### Section 1: Version History <a href="#release-section-1-version-history" id="release-section-1-version-history"></a>

Significant changes to Version History. Now updated to include and versions and inclusion of detailed release notes page for all past versions.  Numbering aligned to semantic version numbering denoting previous 23Q4 as v2.0.0

##### Section 2: Description <a href="#release-section-2-description" id="release-section-2-description"></a>

Update to both text and diagrams to clarify current understanding of Digital Registries

##### Section 3: Terminology <a href="#release-section-3-terminology" id="release-section-3-terminology"></a>

Updated to point to GovStack General Terminology this has removed the following terms which are now in the GovStack General Terminology

* Claim
* Entity
* Registry

##### Section 5: Cross-Cutting Requirements <a href="#release-section-5-cross-cutting-requirements" id="release-section-5-cross-cutting-requirements"></a>

Significant change. This section has changed to now be referred to as Cross Functional Requirements in line with  GovSpecs Architecture 2.1.  All Cross Cutting requirements have been reviewed on this basis and the text is completely re-drafted including all requirements



***

### Version 2.0 <a href="#release-version-20" id="release-version-20"></a>

***

#### **v2.0.0 (previously known as 23Q4)** <a href="#release-v200-previously-known-as-23q4" id="release-v200-previously-known-as-23q4"></a>

_Release date: December 2023_

##### **Release Overview:** <a href="#release-release-overview-1" id="release-release-overview-1"></a>

| Section                                                            | Title                       | Change Level                                                |
| ------------------------------------------------------------------ | --------------------------- | ----------------------------------------------------------- |
| Section 2                                                          | Description                 | ✅ No changes                                                |
| Section 3                                                          | Terminology                 | ✅ No changes                                                |
| Section 4                                                          | Key Digital Functionalities | ✅ No changes                                                |
| [Section 5](#release-section-5-cross-cutting-requirements) | Cross-Cutting Requirements  | ⚠️ Moderate – Structural & content changes                  |
| Section 6                                                          | Functional Requirements     | 🔵 Minor – Whitespace only                                  |
| [Section 7](#release-section-7---data-structures)            | Data Structures             | ⚠️ Moderate – Section removed                               |
| [Section 8](#release-section-8---service-apis)               | Service APIs                | 🔴 Significant – Multiple endpoint & infrastructure changes |
| Section 9                                                          | Internal Workflows          | ✅ No changes                                                |
| Section 10                                                         | Other Resources             | ✅ No changes                                                |

##### **Section 5 Cross-Cutting Requirements:** <a href="#release-section-5-cross-cutting-requirements-1" id="release-section-5-cross-cutting-requirements-1"></a>

The `5.1 Requirements` parent wrapper section was added in v2.0.0 (v23Q4), causing all sections to be renumbered and removing numbering conflicts that previously existed:

| v2.0.0(previously 23Q4)                                       | v.1.0                                                       | Notes                                                          |
| ------------------------------------------------------------- | ----------------------------------------------------------- | -------------------------------------------------------------- |
| 5.1 Requirements _(parent)_                                   | _did not exist_                                             | Parent wrapper added                                           |
| 5.1.1 Citizen-Centric (RECOMMENDED)                           | 5.1 Citizen-Centric (RECOMMENDED)                           | Renumbered                                                     |
| 5.1.2 Open (RECOMMENDED)                                      | 5.2 Open (RECOMMENDED)                                      | Renumbered                                                     |
| 5.1.3 Robust (RECOMMENDED)                                    | 5.3 Robust (RECOMMENDED)                                    | Renumbered                                                     |
| 5.1.4 Databases must not include business logic (RECOMMENDED) | 5.3 Databases must not include business logic (RECOMMENDED) | Renumbered , **⚠️ numbering conflict: 5.3 used twice in v1.0** |
| 5.1.5 Privacy and protection of user data (REQUIRED)          | 5.4 Privacy and protection of user data (REQUIRED)          | Renumbered                                                     |

v2.0.0 contains **5.2 Standards** and **5.2.1 OpenAPI** (referencing versions 3.0.0, 3.0.1, 3.1.0).

* This content is **absent from Section 5 in v1.0** , it was relocated to Section 7 (see below).



##### **Section 7 - Data Structures:** <a href="#release-section-7---data-structures" id="release-section-7---data-structures"></a>

v2.0.0 (23Q4) removed **Standards/Protocols** section:

> _"The following standards are applicable to data structures in the Digital Registries Building Block: OpenAPI Version 3.0.0, 3.0.1, 3.1.0."_

* **Note:** This is the same content that was moved to Section 5 (5.2 Standards / 5.2.1 OpenAPI in v2.0.0 (v23Q4). It has been **relocated** from Section 7 to Section 5.

##### **Section 8 - Service APIs:** <a href="#release-section-8---service-apis" id="release-section-8---service-apis"></a>

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
| GET  | `/data/{registryname}/{versionnumber}` (JSON source , duplicate) |      | _(duplicate removed)_                                                             |
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

### Version 1 <a href="#release-version-1" id="release-version-1"></a>

***

#### **v1.0.0** <a href="#release-v100" id="release-v100"></a>

_Released date: August 2022_

##### **Overview** <a href="#release-overview" id="release-overview"></a>

Digital Registries Building Block was first published in TBC by the Registries Working Group as reference specification for implementers.
