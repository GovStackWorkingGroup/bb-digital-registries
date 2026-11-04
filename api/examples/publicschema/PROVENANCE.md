# Vendored schema provenance

This directory contains unmodified published JSON Schema files used to validate the non-normative GovStack Write examples without network access.

## PublicSchema

- Project: [PublicSchema](https://publicschema.org/)
- Source repository: <https://github.com/PublicSchema/publicschema.org>
- Source revision: `7352b360706c4002033e6db2919d9d3b6d13e7a8`
- Published deployment: GitHub deployment `6855518368`, successfully deployed to <https://publicschema.org/> at `2026-10-05T09:23:18Z`
- Downloaded: `2026-11-04`
- License: Creative Commons Attribution 4.0 International, reproduced in `LICENSE-CC-BY-4.0.txt`
- Changes: none. Each file preserves the bytes downloaded from its canonical `$id` URL.

| Local file | Canonical `$id` | SHA-256 |
| --- | --- | --- |
| `Address.schema.json` | `https://publicschema.org/Address.schema.json` | `11ddaa388cef3c5c92475177de5353d45901155f225e2f00aa63837e961a34f8` |
| `BiometricSample.schema.json` | `https://publicschema.org/BiometricSample.schema.json` | `8e539e5b1bf48f303473791687be25c1ef608faee9c223cd2d8f401b9841584b` |
| `Group.schema.json` | `https://publicschema.org/Group.schema.json` | `1c92a1d86187b189f872c3e1bbac1177cac13e61ceef3f5163306e44aa55dfe4` |
| `GroupMembership.schema.json` | `https://publicschema.org/GroupMembership.schema.json` | `59eb156cc663780ed36d5a3ba6a7320397edc13afaaed3d109c698cbe2de256c` |
| `Household.schema.json` | `https://publicschema.org/Household.schema.json` | `d2f810998cef0bbb5ac4fa4f5bd50526b889d7904567547215bb8a2c0f7b5003` |
| `Identifier.schema.json` | `https://publicschema.org/Identifier.schema.json` | `0ebac26f626df640f684ea361cbd46419f1f67302f35ae00743957817f6974ad` |
| `IdentityDocument.schema.json` | `https://publicschema.org/IdentityDocument.schema.json` | `61d40c95bbe7aa22c61187a34da38a354c8ec03adf4cbb9fe33b45e44234f264` |
| `Location.schema.json` | `https://publicschema.org/Location.schema.json` | `5149194be1690eb918cae72d3a91c348f1e532d58967e5929a53cb4820f10ce3` |
| `Party.schema.json` | `https://publicschema.org/Party.schema.json` | `7232cf38518848f530eaed17db5d9489894700f04bbd0c9341f9eac4f7422b10` |
| `Person.schema.json` | `https://publicschema.org/Person.schema.json` | `8a0795cd0c9c16fb591a41c326a15d83302760f3633f977e7a91d644242eb1bf` |
| `crvs/Birth.schema.json` | `https://publicschema.org/crvs/Birth.schema.json` | `41442486a8c83ed9a055b9dba3de0fb748b9fbd516f10cd42eaba75f68a7d700` |
| `crvs/Parent.schema.json` | `https://publicschema.org/crvs/Parent.schema.json` | `6652fa2f7e12b88a7d74cb6a2374dce13a3ec06a4ce24ecc0e137fc12b7556e5` |
| `crvs/Person.schema.json` | `https://publicschema.org/crvs/Person.schema.json` | `98b3aff8f90ca251c4ea62ff3c53e8795476100d43716b97eafd3341dc770afd` |
| `ctx/draft.jsonld` | `https://publicschema.org/ctx/draft.jsonld` | `231382b4daee6fbb1b48f7a3789a03eba2a213240e31429044db5e8a512b96ac` |

The closure is intentionally limited to the requested `Household`, `GroupMembership`, `Person`, `crvs/Birth`, `crvs/Person`, and `crvs/Parent` schemas, the schemas reachable through their `$ref` values, and the published JSON-LD context explicitly used by the example instances. Validation in this repository establishes JSON Schema conformance. It does not run JSON-LD expansion or claim general JSON-LD conformance.

## GeoJSON Geometry

`Location.schema.json` references the published GeoJSON Geometry schema.

- Project: <https://github.com/geojson/schema>
- Published branch revision: `f2bc6e8f1e8e1ba376d901914ecf8d0fed947d6e`
- Source branch revision at verification: `268ba0af5f8f2c455dd0032caca10403b8bf74cc`
- Canonical URL: `https://geojson.org/schema/Geometry.json`
- Local file: `geojson/Geometry.schema.json`
- SHA-256: `152369d7eb6b3314ffc7deca1d66f9d498ed5b614ca38ed4e2c813fed01024fd`
- License: MIT, reproduced in `geojson/LICENSE-MIT.md`
- Changes: none. The canonical download and the file at the pinned published branch revision were byte-identical when verified.

Validators map the canonical `$id` and `$ref` URIs to these local files. The schemas themselves are not rewritten, so their upstream identifiers remain intact.

## Offline mirror

`offline/` is a generated transport mirror used by the example profile and ordinary offline OpenAPI tooling. For each schema listed above, `generate_offline_mirror.py` removes the canonical `$id` and rewrites only canonical PublicSchema and GeoJSON `$ref` values to relative files inside the mirror. All validation keywords, property definitions, descriptions, comments, and vocabulary values are otherwise retained. The immutable files outside `offline/` remain the published-byte evidence and the source of the hashes in this manifest.

The mirror is reproducible with:

```shell
uv run python api/examples/publicschema/generate_offline_mirror.py api/examples/publicschema api/examples/publicschema/offline
```

Repository tests compare the mirror with the raw source after applying those two identifier transformations and reject remote schema dependencies from the profile closure.

The native graph is intentionally recursive: `Person` and `Group` can reach `GroupMembership`, which references those types again. The current API-guide driver's reference-origin preprocessor overflows on this graph before executing guide rules. The repository therefore verifies the mirror and profile with its offline schema/OpenAPI gates and targeted guide-equivalent checks; the raw schemas and generated mirror are not weakened to accommodate that tool limitation.
