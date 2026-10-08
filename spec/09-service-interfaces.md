---
description: Operational contracts, the Consultation HTTP binding pointer, and protocol options.
---

# 9 Service Interfaces

## 9.1 Operational contracts

[Registry Core](05-api-families/registry-core.md#api-family-discovery) requires each exposed Registry service to publish its family classifications, endpoint, and a link to its machine-readable operational contract. HTTP operations use OpenAPI, or a protocol-native machine-readable description where the selected binding defines one. Consumers locate the contract and the Registry metadata through the [discovery publication](05-api-families/registry-core.md#discovery-publication) rules.

Family classifications identify a service's broad capabilities. The linked contract defines exact operations, parameters, schemas, outcomes, and access requirements. Catalogue descriptions link to these details without reproducing them. A static published description and contract are sufficient; discovery does not require a new runtime service.

Every Consultation operation of an OpenAPI contract declares its Registry context with the `x-govstack-digital-registries` extension defined under [API composition](05-api-families/registry-core.md#api-composition). Each API family owns the HTTP binding of its operations and documents it on its own page.

The [adopter kit](12-other-resources/adopter-kit.md) lists the artifacts an implementation publishes. [Coverage and Limitations](12-other-resources.md#121-coverage-and-limitations) records binding availability. [Requirement Maturity](04-conformance.md#41-requirement-maturity) defines conformance status.

## 9.2 Consultation

[Consultation](05-api-families/consultation.md) defines the independently selectable Retrieve, Lookup, List, and Search capabilities, their [shared Record representation](05-api-families/consultation.md#retrieve-representation), their [pagination contract](05-api-families/consultation.md#pagination-contract), and the [HTTP binding](05-api-families/consultation.md#http-binding) realised by the [canonical OpenAPI](../api/openapi.yaml). The [read API design decisions](12-other-resources/read-api-design-decisions.md) record the binding choices and the shared guide refinements.

## 9.3 Protocol options for additional capabilities

The following standards provide implementation options. The table does not establish a required specification, version, or profile.

| Capability | Protocol options |
|---|---|
| Provisioning and general HTTP operations | OpenAPI |
| Additional Consultation Existence Check, Revision History, and Record Match | OpenAPI |
| GIS Query | OGC API Features |
| Wallet-mediated Evidence | OpenID for Verifiable Credential Issuance and Presentation; W3C Verifiable Credentials |
| Direct Evidence | OpenAPI with a signed credential or attestation format |
| Write | OpenAPI |
| Notification | OpenAPI webhooks for HTTP push; AsyncAPI for event-driven bindings |
| Aggregate Data | OpenAPI; SDMX for statistical exchange |
| Access Transparency | OpenAPI |
| Identity Federation | No protocol option selected; profile ownership and binding remain subject to cross-BB agreement with the Identity team |
