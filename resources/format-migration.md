---
title: Specification format migration
---

# Specification format migration

This record describes the authoring transformation of the existing
`3.0.0-alpha.2` draft. It does not publish a version, approve a Registry
requirement, or establish implementation conformance.

## Governing format

The target combines the Specification Framework's
[functionalities, extensions, and requirements model](https://github.com/GovStackWorkingGroup/specification-framework/pull/1)
with its [options and conditional requirements model](https://github.com/GovStackWorkingGroup/specification-framework/pull/2),
and the corresponding [BB template](https://github.com/GovStackWorkingGroup/bb-template/pull/21).
The migration applies their substance as the authoring contract.

Draft requirements remain unnumbered. Their intended obligation is explicit in
`level`; options inherit obligation from their variation point. The migrated
`registry-service` choice initially had six independently selectable Consultation
options. The subsequent [Write draft](write-binding.md) adds four Write options
as a content change after migration. All remain DRAFT, so none counts toward a
published conformance claim.

The `capability` property in the existing OpenAPI extension is retained as binding
vocabulary. Its values map to the `consultation-retrieve`,
`consultation-lookup`, `consultation-list`, `consultation-search`,
`consultation-revision-list`, and `consultation-revision-retrieve` option keys.
It is distinct from informative business capabilities declared in `metadata.yml`.

## Content locations

| Previous source | Migrated source |
|---|---|
| Specification README | [Publication entrypoint](../README.md) |
| Description and scope | [Overview](../introduction/overview.md) and [scope](../introduction/scope.md) |
| Terminology and references | [Terminology](../introduction/terminology.md) and [references](../introduction/references.md) |
| Core and Consultation requirement blocks | [Discover Registry Services](../requirements/registry-discovery.md) and [Provide Registry Services](../requirements/registry-services.md) |
| Core model and Consultation binding prose | [Registry Core model](registry-core-model.md) and [Consultation binding](consultation-binding.md) |
| Conformance | [Conformance](conformance.md) |
| API-family catalogue and seven roadmap pages | [Family catalogue](family-catalogue.md) and its linked roadmap pages |
| Service interfaces, workflows, and testing | [Interfaces](service-interfaces.md), [workflows](workflows.md), and [testing](testing.md) |
| Adopter and supporting resources | [Resources](README.md) and its linked pages |
| Version history and release notes | [Version history](version-history.md) and [release notes](history/release-notes.md) |
| GitBook assets, metadata context, and vocabulary | Root `assets/` |
| Original repository README, navigation, and numbered API coverage | Preserved under `resources/history/` |
| Original requirement wording and identifiers | [Historical requirement text](history/requirements.md) and [migration mapping](requirement-migration.yml) |

The original fifteen requirement blocks and the eleven Consultation requirements
added after the baseline (#8 through #18) are mapped to the migrated statements.
A block may map to several statements when it applies to several API operations
or contains distinct obligations. Splitting a statement does not grant a new
permission, impose another operation, or change the behaviour of the source API.

Historical identifiers remain available as migration references. They are not
reissued as current numbered DRAFT requirements. The earlier
[DRS-1 through DRS-37 disposition ledger](migration-from-3.0.md) is preserved.

## API and verification preservation

The canonical `api/openapi.yaml`, examples, schemas, fixtures, and vendored
components retain their existing contents. `resources/api.yml` is a Git symlink
to the canonical file, satisfying the framework's authoring location without
duplicating the contract. The adjacent `resources/common` symlink points to
`api/common` so the contract's relative shared-component references resolve even
when a tool retains the authoring entrypoint URI as its base. The artifact suite
validates that entrypoint directly as well as the canonical API path.

The metadata JSON-LD context and vocabulary move with their existing contents;
their public vocabulary IRIs do not change. Manual verification procedures are
retained in [Testing](testing.md), including stable links for the historical
Core and Consultation verification items.

The [publication validator](../tools/validate_specification.py) checks the migrated
model, mapping consistency, and local links. The repository tests separately guard
the complete original fifteen-block requirement archive against deletion or
alteration; the later revised blocks are archived beside it. That archive check does not freeze the evolving active draft.
The [Consultation artifact checks](../tools/validate_consultation.py)
continue to validate schemas and examples. Neither is a deployed implementation
conformance suite.

The older API Guide coverage scanner understands the numbered Markdown format.
It does not validate the migrated requirement front matter. Consequently
`api/coverage.yaml` has no active or numbered draft claims; the previous mappings
are preserved in [historical coverage](history/api-coverage.yaml). The publication
validator and requirement front matter supply the current draft traceability.
A successful API lint run alone does not establish that traceability.

## Publication limits

The [local workflow](../.github/workflows/validate.yml) runs executable repository
checks. A central compiler workflow is not installed here because its inspected
default branch contains requirements rather than an executable reusable workflow.
The GitBook configuration retains source navigation and redirects; it is not
evidence that a hosted site has been rebuilt.

The publication URN, `govstack:spec:bb:registries`, is retained from
[GovStack's existing transition metadata](https://github.com/GovStackWorkingGroup/transition-specs/blob/4e34c78857d550dbe274c2c566f6c4e22c0ae2cc/bb-digital-registries/metadata.yml).
The owning group,
`govstack:wg:registries-registration`, matches the GovStack Working Group record.
This migration does not create a publication proposal record, a release record,
or person records, or change branch protection or tag rules. Those remain
publication-administration steps before a registered release.

The metadata describes the current migrated draft and does not assign it a
version-specific publication URL. Historical versions and their
attribution remain in the historical sources; this migration does not republish
them or invent their publication URLs.

This authoring metadata does not replace the existing publication catalogue or
change which released version a hosted site serves. The historical transition
entries remain at their existing identity and locations.

## Subsequent content changes

The committed authoring baseline contained Retrieve, Lookup, List, and Search.
The later old-layout revisions, covering explicit Collection addressing, selectable
read features, Revision List and Revision Retrieve, recorded-time and
effective-time selection, Search semantics, caller capability discovery, and
purpose binding, are migrated into the same requirement, contract, and
verification model. Further changes follow the same rule.

Use the content-location and requirement mappings when replaying changes from the
previous layout. Reapply content deliberately rather than copying the old
`spec/` tree back over the migrated publication. Verify the requirement mappings,
local links, artifact checks, and unchanged draft maturity after each coherent
addition.
