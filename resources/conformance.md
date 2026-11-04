---
description: Draft requirement lifecycle, core variation point, and assessment boundaries for Digital Registries.
---

# Conformance

## Requirement maturity

All requirements and options in the `3.0.0-alpha.2` draft are `DRAFT`. Under the current GovStack Requirements Model, a DRAFT requirement has `id: null`, takes no part in compliance, and can change before acceptance. The previous `fr-core#req-*` and `fr-consultation#req-*` labels are retained only as historical aliases in the [migration ledger](migration-from-3.0.md#replacement-index); they are not current requirement identifiers.

Each requirement follows the [agreed GovStack Requirements Model](https://github.com/GovStackWorkingGroup/specification-framework/blob/7322f977a6a74127240cbab5ed9d5ad84b9d5c29/chapters/requirements.md). Requirement levels and other classifiers are interpreted according to that model. Lowercase modal verbs have their ordinary English meaning; this specification does not use BCP 14 keywords to assign requirement levels.

No implementation, operation, or functionality can claim conformance with this alpha. The requirements and Consultation and Write HTTP bindings are DRAFT, and no executable implementation conformance suite is published. The canonical Consultation and Write contracts, requirement-to-operation mappings, and example-validation checks support artifact review and prototyping only; they do not establish deployed runtime behaviour. Procurement and certification should reference an approved specification version. See [Coverage and limitations](README.md#coverage-and-limitations) for the maturity of the published material.

## Inherited cross-functional requirements

This specification extends `govstack-cfr-2.1.0`. Every parent requirement applies with its original classifier and applicability conditions unless a Digital Registries requirement explicitly identifies a permitted extension or replacement under the GovStack Requirements Model.

This draft defines no Registry-specific cross-functional extension or replacement. It does not impose a jurisdiction-specific security framework, a universal legal basis for data processing, or one deletion policy on every type of Registry.

## Draft conformance model

The intended core contains both [Discover Registry Services](../requirements/registry-discovery.md) and [Provide Registry Services](../requirements/registry-services.md). This preserves the parent model of Registry Core plus at least one approved Registry service, without making any API family permanently universal. The second functionality contains the REQUIRED `registry-service` variation point with `select.min: 1`. The options currently defined in this draft are:

| Option key | Operation | Binding `capability` value |
|---|---|---|
| `consultation-retrieve` | `retrieveRecord` | `retrieve` |
| `consultation-lookup` | `lookupRecord` | `lookup` |
| `consultation-list` | `listRecords` | `list` |
| `consultation-search` | `searchRecords` | `search` |
| `consultation-revision-list` | `listRecordRevisions` | `revision-list` |
| `consultation-revision-retrieve` | `retrieveRecordRevision` | `revision-retrieve` |
| `write-create` | `createRecord` | Write `create` |
| `write-update` | `updateRecord` | Write `update` |
| `write-transition` | `applyRecordTransition` | Write `transition` |
| `write-change-requests` | `submitChangeRequest` | Write `change-requests` |

A future claim against a published version will meet both core functionalities and at least one published option of the variation point. Only `PUBLISHED` options count toward `select.min`; because every option in this alpha is DRAFT, no solution can yet satisfy that published-option rule.

The current option set covers Consultation and Write. Direct creation, update, and named transition options are independently selectable from approval-based change requests. An implementation offering only the approval route need not expose the corresponding direct mutation endpoints. The other six families remain informative until a future version supplies their requirements, contracts, and tests. Informative family labels cannot satisfy the minimum. Publishing an additional option is a major change under the agreed framework; adding DRAFT options here does not publish a new release.

Conditions are machine-readable. Each operation-specific requirement names its option key in `applies_when`. Requirements that apply regardless of the selected option carry no selection condition. Conditions concerning source data or access policy are recorded in the requirement's `documentation`. This is the agreed variation-point model; it does not depend on the former provisional capability-namespace approach.

Core requirements concerning returned Records apply through each selected option. Retrieve resolves a stable Record Identifier; Lookup resolves a declared exact selector; List and Search return bounded Pages; revision capabilities return source-backed retained history. An authorised API consumer receives the permitted representation under the operation's declared currency, temporal, and traversal semantics or a policy-appropriate unsuccessful outcome. The permitted representation is governed by current access policy. Consumer guidance in the binding and workflow pages is informative; conformance applies to implementations only.

Caller capability discovery is supporting metadata and does not by itself satisfy the minimum Registry service choice.

An operation can also declare selectable Consultation features. `conditional-read` applies only to Retrieve, `field-selection` can apply to a declared read, and `complete-traversal` and `snapshot-traversal` apply only to List or Search. `snapshot-traversal` includes the `complete-traversal` guarantee. `recorded-time` and `effective-time` add explicit temporal selectors only to Retrieve, Lookup, List, or Search. `purpose-bound` adds a required trusted purpose binding to a Record or history operation's inherited security contract. An absent or empty `features` member declares none of these selectable guarantees. The normative operation extension remains closed to the capability and feature values of its contract version. Declaring a feature makes its applicable requirement, contract, and tests part of the operation's claim. Offering caller capability discovery applies its separate requirement and does not grant record-level authority or select `purpose-bound`; its capability and feature annotations are extensible advisory metadata under [`fr-consultation#req-17`](testing.md#consultation-17).

Features are not options of the variation point. Each feature requirement names the option of the operation it constrains in `applies_when` and records the feature declaration as a condition in its `documentation`. Caller capability discovery carries no selection condition and records its offer as a condition in the same way.

The following summary uses the historical aliases of the [traceability table](testing.md#requirement-traceability). The requirement front matter remains the authoritative statement of applicability.

| Option key | Consultation requirements that apply | Additional requirements under a declared condition |
|---|---|---|
| `consultation-retrieve` | [#1](testing.md#consultation-1), [#2](testing.md#consultation-2) | [#3](testing.md#consultation-3) when existence is protected; [#8](testing.md#consultation-8), [#9](testing.md#consultation-9), [#14](testing.md#consultation-14), [#15](testing.md#consultation-15), and [#18](testing.md#consultation-18) for declared features |
| `consultation-lookup` | [#2](testing.md#consultation-2), [#4](testing.md#consultation-4) | [#3](testing.md#consultation-3) when existence is protected; [#9](testing.md#consultation-9), [#14](testing.md#consultation-14), [#15](testing.md#consultation-15), and [#18](testing.md#consultation-18) for declared features |
| `consultation-list` | [#2](testing.md#consultation-2), [#5](testing.md#consultation-5), [#7](testing.md#consultation-7) | [#9](testing.md#consultation-9), [#10](testing.md#consultation-10), [#11](testing.md#consultation-11), [#14](testing.md#consultation-14), [#15](testing.md#consultation-15), and [#18](testing.md#consultation-18) for declared features |
| `consultation-search` | [#2](testing.md#consultation-2), [#6](testing.md#consultation-6), [#7](testing.md#consultation-7), [#16](testing.md#consultation-16) | [#9](testing.md#consultation-9), [#10](testing.md#consultation-10), [#11](testing.md#consultation-11), [#14](testing.md#consultation-14), [#15](testing.md#consultation-15), and [#18](testing.md#consultation-18) for declared features |
| `consultation-revision-list` | [#2](testing.md#consultation-2), [#7](testing.md#consultation-7), [#12](testing.md#consultation-12) | [#3](testing.md#consultation-3) when parent Record or history existence is protected; [#9](testing.md#consultation-9) and [#18](testing.md#consultation-18) for declared features |
| `consultation-revision-retrieve` | [#2](testing.md#consultation-2), [#13](testing.md#consultation-13) | [#3](testing.md#consultation-3) when parent Record or revision existence is protected; [#9](testing.md#consultation-9) and [#18](testing.md#consultation-18) for declared features |

Every selected Consultation option also applies the Registry Core requirements for returned Records ([`fr-core#req-2`](testing.md#core-2), [`fr-core#req-4`](testing.md#core-4), [`fr-core#req-5`](testing.md#core-5), [`fr-core#req-6`](testing.md#core-6)) and the operation contract requirement [`fr-core#req-8`](testing.md#core-8). Offering caller capability discovery applies [`fr-consultation#req-17`](testing.md#consultation-17). Capability conformance covers the shared contract and selected operations; additional feature claims establish their stronger guarantees. Applications needing complete exports, fixed snapshots, source history, temporal reads, or purpose binding check those declarations explicitly.

Registry metadata can describe a Registry for directory participation without establishing Digital Registries conformance. A specification reference, API-family classification, binding `capability` value, or linked operational contract is not by itself a conformance claim.

## Conformance declaration and binding vocabulary

The GovStack framework requires a future conformance declaration to list the options a solution claims. A claim also names any operation features its claimed operations declare; every applicable requirement, contract, and test for those features forms part of the claim. Its serialisation is not yet defined by the framework, so this specification does not invent one.

The Consultation OpenAPI extension retains `capability` as a wire-level field name. Its six values bind operations to the six Consultation option keys above. The separate Write extension binds its operations to the four Write options; it does not add Write values to the closed Consultation extension. Those values are not informative framework capabilities. The informative capabilities declared for this specification are Registry Service Discovery and Authoritative Registry Services.

## Adaptors

An existing Registry does not need to replace its internal software to implement the draft contract. An adaptor can translate an existing interface into the operations, metadata, outcomes, and bindings described here. Assessment concerns the resulting external behaviour and required evidence. The adaptor documents source currency, identifier mapping where needed, Collection membership, supported selectors and searches, and representation mappings. It does not fabricate source revisions, recording or effective times, history, or lifecycle facts to fill an envelope. A service offering latest reads does not need to implement revision capabilities, temporal features, caller capability discovery, purpose binding, or a general query engine.

## Write applicability

[Write requirements](../requirements/registry-services.md) and the [Write verification matrix](write-testing.md) apply to the selected Write options. Their canonical transport entry point is [write-api.yml](write-api.yml). A direct write selection does not require change requests or manual review; a change-request selection does not grant direct mutation authority. Compound changes are available only when the published operation declares its supported boundary and guarantees. Pending review and approval do not establish commitment.

Birth registration, Household, Person, and membership payloads in the [Write examples](../api/examples/README.md) are non-normative profiles. Their fields, vocabularies, local reference mappings, bounds, domain models, and policy rules are not requirements of the shared Write capabilities.
