# Contributing to the Digital Registries specification

This page is for contributors working in the repository. Readers of the
specification start at the [README](README.md).

## Repository layout

| Path | Contents |
|---|---|
| `metadata.yml`, `authors.yml`, `toc.yml` | Publication identity, current-version credits, and ordered content |
| `introduction/` | Overview, scope, terminology, and references |
| `requirements/` | Machine-readable DRAFT requirements, options, and applicability |
| `resources/` | Binding definitions, workflows, verification, adopter guidance, and history |
| `assets/` | Diagrams, metadata context, vocabulary, and preserved historical images |
| `ADR/` | Working Group decision-record location |
| `api/` | Canonical OpenAPI contract, schemas, examples, and legacy API archives |
| `tools/` | Publication and API artifact validation, separate from implementation assessment |
| `test/`, `examples/` | Historical generated-CRUD tests and product examples, not current conformance evidence |

The canonical API source remains [api/openapi.yaml](api/openapi.yaml).
[resources/api.yml](resources/api.yml) is a Git symlink to that file for the
Specification Framework's authoring entrypoint; it is not a second contract.
The adjacent `resources/common` symlink points to `api/common` so ordinary
OpenAPI tools resolve the shared components from either entrypoint.

## Validation

From the repository root:

```sh
uv sync --frozen
uv run python -m unittest discover -s tools -p 'test_*.py'
uv run python tools/validate_specification.py
uv run python tools/validate_consultation.py
uv run python tools/validate_write.py
```

These commands check the publication structure, links, requirement model and
option applicability, plus the canonical contract and examples. They do not
exercise a deployed Registry. [Testing](resources/testing.md) describes the
separate runtime evidence needed for implementation assessment.

## Publication boundary

`toc.yml` lists the specification pages; the root README is the home page.
Keep contributor build instructions in this file or the
[site wrapper README](specification-site/README.md). Repository files do not become
site pages or downloads merely because they exist in the tree.

Select public examples and downloads deliberately. A published page links only to
other pages in `toc.yml`, external sources, or selected downloadable artifacts.
Original OpenAPI contracts and their local dependencies remain downloadable with
their relative paths intact. Required attribution and licence notices accompany
the examples that use them.

## Local working material

Keep brainstorming, review notes, migration records, and temporary snapshots under
`.local/working-documents/`. Git ignores `.local/`; source validation and site
publication exclude it. Do not link published content to that folder or commit it.
Git history preserves earlier requirement text without duplicate archive pages.
