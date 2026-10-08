---
description: Terms with a specific meaning in this specification.
---

# 3 Terminology

This specification uses the [GovStack Common Terminology](https://specs.govstack.global/architecture/2-common-terminology). The following terms have a specific meaning for Digital Registries.

| Term | Definition |
|---|---|
| API Consumer | A system authorised to invoke a Registry service interface. |
| API Family | A coherent group of related Registry capabilities and operations. |
| Authoritative Source | A source for which a named authority accepts responsibility within a declared domain and scope. Authoritative does not imply error-free. |
| Binding | A mapping of abstract operations to a transport or established protocol. |
| Capability | An independently selectable operation pattern within an API family, such as Retrieve or Search. |
| Capability Claim | A declaration that an implementation supports a specified API family, capability, and binding and meets the requirements attached to that claim. |
| Functional Identifier | An identifier issued and lifecycle-managed for a sector-specific purpose, such as a farmer, student, health, or professional identifier. |
| Lifecycle State | When supplied, the state of a Record under a documented vocabulary. A current Record is not necessarily active. |
| Lookup | Resolution of a Record using a declared exact selector, such as a registration number or a defined combination of fields. It does not imply general search or approximate matching. |
| Permitted Representation | The record data and metadata an API consumer is authorised to receive. It may be filtered or redacted and need not contain the complete stored record. |
| Record | The Registry's representation of an entity, place, asset, or event within its declared scope. |
| Record Identifier | A stable identifier unique within its Registry. It may reuse a suitable source identifier; the Registry context and identifier together identify the Record. |
| Record Principal | A person or organisation with a recognised relationship to a record, such as its subject, owner, title holder, director, or credential holder. |
| Record Reference | A value identifying another Record and its target Registry through explicit or schema-defined context. It does not guarantee that the Record can be retrieved or disclosed. |
| Record Revision | A representation of a record at a defined point in its change history. |
| Representation Format | The serialisation or media type used to encode a returned representation, identified through the applicable binding. |
| Registry Authority | The institution accountable for the Registry and its declared authoritative scope. |
| Registry Core | The common behaviour and metadata required of Registry implementations, with Record-related requirements applied according to their applicability. |
| Registry Identifier | A globally unique and stable identifier for a Registry. |
| Registry Operator | The organisation that operates an implementation on behalf of, or as, the Registry Authority. |
| Relying Service | A service that relies on authentication or claims provided through the Identity Federation family. |
| Schema | A machine-readable definition of the structure and validation constraints of records or messages. |
| Search | Retrieval of a bounded collection using criteria declared by the service contract or applicable domain profile. It does not imply a generic query engine. |
| Semantic Model | A published vocabulary or domain model for interpreting Registry data. A formal semantic-model reference is optional unless the selected profile requires it; field meanings remain documented. |
| Source Recorded At | When supplied, the time at which the source recorded the represented information or revision, with the precise meaning declared by the contract. It is not the time at which an adapter retrieved the information. |
