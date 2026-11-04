---
description: Terms with a specific meaning in this specification.
---

# Terminology

This specification uses the [GovStack Common Terminology](https://specs.govstack.global/architecture/2-common-terminology). The following terms have a specific meaning for Digital Registries.

| Term | Definition |
|---|---|
| API Consumer | A system authorised to invoke a Registry service interface. |
| API Family | A coherent group of related Registry operations. |
| Authoritative Source | A source for which a named authority accepts responsibility within a declared domain and scope. Authoritative does not imply error-free. |
| Authoritative State | Record state that the Registry has committed within its declared authoritative scope. A permitted read projection can omit, transform, or combine this state. |
| Binding | A mapping of abstract operations to a transport or established protocol. |
| Binding Capability | An operation pattern named by `capability` in the normative operation extension, such as `retrieve` or `create`. The defined values map to operation option keys. |
| Capability | An informative business outcome declared in `metadata.yml` and realised by one or more functionalities. A capability does not carry requirements. |
| Conformance Declaration | An implementation's statement of its selected operation options and any claimed extensions. This draft defines no standard declaration format or approved conformance target. |
| Collection | A logical API grouping of Records with declared membership and a stable Collection Identifier. It need not correspond to one database table, governed dataset, source module, or institutionally separate Registry. |
| Effective At | When selected, the date or instant at which the source declares represented information applicable. Event occurrence and registration dates are not automatically effective-time coordinates. |
| Functionality | A service provided to an external actor and realised by a set of requirements. Its file contains the requirement metadata and explains the service, workflows, and data structures. |
| Functional Identifier | An identifier issued and lifecycle-managed for a sector-specific purpose, such as a farmer, student, health, or professional identifier. |
| Lifecycle State | When supplied, the state of a Record under a documented vocabulary. A current Record is not necessarily active. |
| Lookup | Resolution of a Record using a declared exact selector, such as a registration number or a defined combination of fields. It does not imply general search or approximate matching. |
| Option | A choice permitted by a variation point. Its key identifies the selection and determines which conditional requirements apply. |
| Permitted Representation | The record data and metadata an API consumer is authorised to receive. It may be filtered or redacted and need not contain the complete stored record. |
| Read Projection | A permitted representation produced under a declared view, access policy, and source-currency contract. It is not necessarily the Registry's complete authoritative state or a Write input shape. |
| Record | The Registry's representation of an entity, place, asset, or event within its declared scope. |
| Record Identifier | A stable identifier unique within its Registry. It may reuse a suitable source identifier; the Registry context and identifier together identify the Record. |
| Record Principal | A person or organisation with a recognised relationship to a record, such as its subject, owner, title holder, director, or credential holder. |
| Record Reference | A value identifying another Record and its target Registry through explicit or schema-defined context. It does not guarantee that the Record can be retrieved or disclosed. |
| Record Revision | A representation of a record at a defined point in its change history. |
| Recorded As Of | When selected, the source-accepted knowledge cutoff used to choose represented information. It is not the adapter request or retrieval time. |
| Representation Format | The serialisation or media type used to encode a returned representation, identified through the applicable binding. |
| Registry Authority | The institution accountable for the Registry and its declared authoritative scope. |
| Registry Core | The common behaviour and metadata required of Registry implementations, with Record-related requirements applied according to their applicability. |
| Registry Identifier | A globally unique and stable identifier for a Registry. |
| Registry Operator | The organisation that operates an implementation on behalf of, or as, the Registry Authority. |
| Relying Service | A service that relies on authentication or claims provided through the Identity Federation family. |
| Schema | A machine-readable definition of the structure and validation constraints of records or messages. |
| Search | Retrieval of a bounded collection using criteria declared by the service contract or applicable domain profile. It does not imply a generic query engine. |
| Semantic Model | A published vocabulary or domain model for interpreting Registry data. A formal semantic-model reference is not required unless the selected profile requires it; field meanings remain documented. |
| Source Recorded At | When supplied, the time at which the source recorded the represented information or revision, with the precise meaning declared by the contract. It is not the time at which an adapter retrieved the information. |
