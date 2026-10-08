---
description: Draft minimum conformance and capability model for Digital Registries.
---

# 4 Conformance

## 4.1 Requirement maturity

All requirements in the 3.0.0-alpha.2 specification are classified as DRAFT. They do not create a certification obligation.

Each requirement follows the [GovStack Requirements Model](https://specs.govstack.global/architecture/development/5-specification-framework/5.3-requirements-model). Requirement levels and other classifiers are interpreted according to that model. Lowercase modal verbs have their ordinary English meaning; this specification does not use BCP 14 keywords to assign requirement levels. Requirement identifiers are permanently reserved even while the requirement is DRAFT. Cross-family requirements are defined under [Registry Core](05-api-families/registry-core.md#registry-core-functional-requirements), while family-specific requirements are defined on the applicable API-family page.

The conformance model and capability-specific requirement namespaces remain provisional pending support for conditional capability applicability in the GovStack Common Requirements Framework. [GovStack CFR issue #7](https://github.com/GovStackWorkingGroup/cfr-architecture/issues/7) tracks that dependency.

No implementation or capability can claim conformance with this alpha. Its requirements and Consultation HTTP binding are DRAFT, and no executable implementation conformance suite is published. The canonical Consultation contract and example-validation checks support prototyping and review. Procurement and certification should reference an approved specification version. See [Coverage and Limitations](12-other-resources.md#121-coverage-and-limitations) for the maturity of individual capabilities and publication gaps.

## 4.2 Inherited cross-functional requirements

This specification extends `govstack-cfr-2.1.0`. Every parent requirement applies with its original classifier and applicability conditions unless a Digital Registries requirement explicitly identifies a permitted extension or replacement under the GovStack Requirements Model.

This release defines no Registry-specific cross-functional extension or replacement. It does not impose a jurisdiction-specific security framework, a universal legal basis for data processing, or one deletion policy on every type of Registry.

## 4.3 Conformance model

Minimum conformance consists of **Registry Core plus at least one declared Registry capability**. All API families and operations, including Consultation Retrieve, are optional.

An implementation claiming conformance:

1. satisfies the applicable [Registry Core requirements](05-api-families/registry-core.md#registry-core-functional-requirements), including publication of machine-readable Registry and service metadata;
2. implements at least one declared Registry capability with approved requirements, contracts, and tests;
3. identifies the Digital Registries specification version and capabilities covered by its claim;
4. publishes the API-family classifications, endpoints, and linked machine-readable operational contracts for the services it exposes through the Registry BB interface; and
5. satisfies the applicable `govstack-cfr-2.1.0` requirements.

Core requirements concerning returned Records apply when a selected capability returns Records. The Consultation Retrieve, Lookup, List, and Search requirements and shared HTTP binding apply only to the selected capabilities. Retrieve resolves a stable Record Identifier; Lookup resolves a declared exact selector; List and Search return bounded Pages. An authorised API consumer receives the current permitted representation or a policy-appropriate unsuccessful outcome. The permitted representation is governed by access policy. Consumer guidance in the capability pages is informative; conformance applies to implementations only.

Registry metadata can describe a Registry for directory participation without establishing functional Registry BB conformance. A specification reference or family classification in metadata is not, by itself, a conformance claim.

## 4.4 Capability claims

A capability claim names the selected families and capabilities; every applicable REQUIRED requirement, operation, contract, and test for a claimed capability forms part of the claim. Publishing a family label and an operational contract describes a service. A conformance claim additionally requires approved capability requirements, contracts, and tests, subject to [Requirement Maturity](#41-requirement-maturity).

## 4.5 Adaptors

An existing registry does not need to replace its internal software to conform. An adaptor may translate an existing interface into the operations, metadata, outcomes, and bindings required by its conformance claim. Conformance applies to the resulting external behaviour. The adapter documents source currency, identifier mapping where needed, supported selectors and searches, and representation mappings. It does not fabricate source revisions, recording times, or lifecycle facts to fill an envelope. A service offering current reads does not need to implement Revision History or a general query engine.
