---
description: Programmatic configuration and publication of a Registry service.
---

# Provisioning

> **Status:** Informative. See [Conformance](../04-conformance.md#44-capability-claims).

## Purpose and applicability

Provisioning configures a Registry service and publishes its externally visible contracts. It is useful where schemas, capabilities, bindings, or controlled bulk data flows are administered programmatically.

A Registry can publish its metadata without a Provisioning API. Its authority and schema may be established by law, governance, or an operational process outside an API.

## Capability areas

| Area | Outcome |
|---|---|
| Metadata administration | Creates or revises the Registry's machine-readable identity and capability declarations through an administrative interface. Registry Core separately requires publication of the current Registry metadata. |
| Schema lifecycle | Publishes, revises, or retires a representation schema under defined compatibility rules. |
| Interface publication | Declares supported families, capabilities, bindings, and access conditions. |
| Bulk transfer | Initiates a controlled import or export of data and metadata. |

Provisioning administers service metadata and contracts independently of the storage engine and administrative tooling. Registry Core requires metadata publication whether or not Provisioning is supported. Establishing a Registry Authority remains a legal or governance act outside this API family.

## Adoption considerations

Deployment rules cover administrative authorisation, schema compatibility, publication lifecycle, bulk-operation validation, provenance, and failure recovery.

## Implementation options

Illustrative, non-normative options include synchronous HTTP described by OpenAPI for administrative operations and an asynchronous job or messaging pattern for long-running bulk work.

## Example

A programme administrator publishes a revised benefit-record schema and its compatibility metadata before applications begin sending Records that use the revision.
