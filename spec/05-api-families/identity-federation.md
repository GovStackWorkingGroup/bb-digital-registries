---
description: Sectoral subject authentication and authorised claim release.
---

# Identity Federation

> **Status:** Informative. Cross-Building-Block profile ownership is unresolved. See [Conformance](../04-conformance.md#44-capability-claims) and [Coverage and limitations](../12-other-resources.md#121-coverage-and-limitations).

## Purpose and applicability

Identity Federation enables a sectoral Registry containing Records about people, or a service acting for its authority, to authenticate the person represented by a Registry Record to a Relying Service and release authorised claims. It applies to sector populations such as farmers, students, health-service users, or licensed professionals.

## Relationship to the Identity Building Block

The [Identity Building Block description](https://github.com/GovStackWorkingGroup/bb-identity/blob/main/spec/2-description.md) scopes that Building Block to foundational identity and includes integration with functional identities. Identity Federation concerns authentication and claim release for a functional sector identity.

## Profile scope

A sector identity profile covers the relationship between the authenticated subject and the Registry Record, the lifecycle of the functional identifier, authorised claim release, subject-identifier policy, suspension or termination of the sector relationship, assurance expectations, and issuer topology.

The responsible Registry Authority issues and manages the lifecycle of the functional identifier. Subject-identifier policy addresses issuer-scoped and pairwise identifiers where needed to limit correlation.

## Capability boundary

Identity Federation is an outward-facing service to a Relying Service. It is separate from authentication and authorisation used to protect Registry APIs. It does not issue or replace foundational identity. An Identity service can provide upstream authentication or identity proofing without taking ownership of the sectoral identifier.

## Implementation options

OpenID Connect is an illustrative, non-normative implementation option. No protocol binding is selected for this family.

## Example

A professional Registry authenticates a licensed practitioner to a continuing-education service and releases an authorised claim that identifies the relevant professional sector.
