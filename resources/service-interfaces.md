---
description: Operational contracts, the Consultation HTTP binding pointer, and protocol options.
---

# Service Interfaces

## Operational contracts

[Registry Core](registry-core-model.md#api-family-discovery) requires each exposed Registry service to publish its family classifications, endpoint, and a link to its machine-readable operational contract. HTTP operations use OpenAPI, or a protocol-native machine-readable description where the selected binding defines one. Consumers locate the contract and the Registry metadata through the [discovery publication](registry-core-model.md#discovery-publication) rules.

Family classifications identify a service's broad capabilities. The linked contract defines exact operations, parameters, schemas, outcomes, and access requirements. Catalogue descriptions link to these details without reproducing them. A static published description and contract are sufficient; discovery does not require a new runtime service.

Every Collection-scoped Consultation operation of an OpenAPI contract declares its Registry context with the `x-govstack-digital-registries` extension defined under [API composition](registry-core-model.md#api-composition). The extension also declares any selectable operation features; omission or an empty `features` array declares none. Cross-Collection caller capability discovery uses its bounded response schema and references those operations. Each API family owns the HTTP binding of its operations and documents it on its own page.

The [adopter kit](adopter-kit.md) lists the artifacts an implementation publishes. [Coverage and limitations](README.md#coverage-and-limitations) records binding availability. [Requirement maturity](conformance.md#requirement-maturity) defines conformance status.

## Consultation

[Consultation](consultation-binding.md) defines independently selectable Retrieve, Lookup, List, Search, Revision List, and Revision Retrieve operation options, their [shared Record representation](consultation-binding.md#retrieve-representation), their [pagination contract](consultation-binding.md#pagination), and the [HTTP binding](consultation-binding.md#http-binding) realised by the [canonical OpenAPI](api.yml). Operations can additionally declare conditional reads, field selection, complete traversal, snapshot traversal, recorded-time, effective-time, or purpose binding. The selectable caller capability document describes caller-available operations without granting record-level authority. The [read API design decisions](read-api-design-decisions.md) record the binding choices and the shared guide refinements.

The [generated Consultation API reference](api-reference.md) presents the canonical DRAFT read operations and links to separate illustrative birth-registration, business, and household bindings.

## Protocol options for roadmap families

The following standards provide implementation options. The table does not establish a required specification, version, or profile.

| Capability | Protocol options |
|---|---|
| Provisioning and general HTTP operations | OpenAPI |
| Additional Consultation Existence Check and Record Match | OpenAPI |
| GIS Query | OGC API Features |
| Wallet-mediated Evidence | OpenID for Verifiable Credential Issuance and Presentation; W3C Verifiable Credentials |
| Direct Evidence | OpenAPI with a signed credential or attestation format |
| Notification | OpenAPI webhooks for HTTP push; AsyncAPI for event-driven bindings |
| Aggregate Data | OpenAPI; SDMX for statistical exchange |
| Access Transparency | OpenAPI |
| Identity Federation | No protocol option selected; profile ownership and binding remain subject to cross-BB agreement with the Identity team |

## Write

The [Write binding](write-binding.md) and [canonical Write OpenAPI](write-api.yml) define separately selected direct creation, update, named transition, and approval-based change-request operations. Each operation publishes its input schema and grants. Change-request submission creates a request resource; it does not commit the proposed Record change. Approval and application outcomes remain distinct. Current source preconditions and authorisation are checked when a change commits.

The [Write API reference](write-api-reference.md) links the transport contract. The [non-normative Write examples](../api/examples/README.md) illustrate direct and governed birth registration, household creation with existing or newly created individuals, and later membership additions. The adopting institution selects the domain model and policy. The Write operation extension is distinct from the closed Consultation extension.
