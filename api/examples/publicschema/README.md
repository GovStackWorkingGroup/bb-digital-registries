# Vendored PublicSchema dependencies

These unmodified files support offline validation of the non-normative PublicSchema Write examples. See [PROVENANCE.md](PROVENANCE.md) for the pinned deployments, canonical identifiers, SHA-256 hashes, dependency closure, and change statement.

PublicSchema reference-model files and the published context are licensed under CC BY 4.0; the attribution notice is reproduced in [LICENSE-CC-BY-4.0.txt](LICENSE-CC-BY-4.0.txt). The transitive GeoJSON Geometry schema is MIT-licensed; its notice is reproduced in [geojson/LICENSE-MIT.md](geojson/LICENSE-MIT.md).

The original schema bytes and identifiers are preserved outside `offline/`. The profile resolves through the generated `offline/` mirror so ordinary OpenAPI tools do not need custom canonical-URI aliases or network retrieval. The mirror removes `$id` and rewrites only schema `$ref` values to relative files; see `PROVENANCE.md` and `generate_offline_mirror.py`. The examples also pin `ctx/draft.jsonld` because their instances explicitly carry that `@context`.

The checks establish JSON Schema conformance and request-local reference invariants. They do not perform JSON-LD expansion or claim general JSON-LD conformance.
