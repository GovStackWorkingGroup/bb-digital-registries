---
description: Informative background on the DCAT, RDF, and JSON-LD meaning of the Registry metadata document.
---

# Metadata vocabulary (informative)

The [Registry metadata document](../05-api-families/registry-core.md#registry-metadata) is plain JSON whose keys are fixed by the [metadata document schema](../../api/extensions/registry-metadata.schema.json). Because it is compacted with a published JSON-LD context, the same document is also an RDF graph aligned with the Data Catalog Vocabulary. This appendix records that alignment for catalogue integrators and vocabulary maintainers. Nothing here adds an obligation for an implementation.

## Key to term mapping

| JSON key | RDF term | Notes |
|---|---|---|
| `@id` of the Registry | Registry resource IRI | The Registry Identifier. |
| `title` | [`dct:title`](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/#title) | Language map allowed. |
| `description` | [`dct:description`](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/#description) | Language map allowed. |
| `authority` | `govreg:authority` with a [`prov:Agent`](https://www.w3.org/TR/prov-o/#Agent) value | |
| `specification` | [`dct:references`](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/#references) | Identifies the specification version used to describe the implementation. |
| `conformsTo` | [`dct:conformsTo`](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/#conformsTo) | A formal claim against an approved specification or profile. |
| `governedDataset` | `govreg:dataset` with a [`dcat:Dataset`](https://www.w3.org/TR/vocab-dcat-3/#Class:Dataset) value | |
| `dataService` | `govreg:dataService` with a [`dcat:DataService`](https://www.w3.org/TR/vocab-dcat-3/#Class:Data_Service) value | |
| `serviceType` | [`dct:type`](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/#type) | Values are concepts of the API-family scheme, prefix `apif:`. |
| `servesDataset` | [`dcat:servesDataset`](https://www.w3.org/TR/vocab-dcat-3/#Property:data_service_serves_dataset) | |
| `endpointURL` | [`dcat:endpointURL`](https://www.w3.org/TR/vocab-dcat-3/#Property:data_service_endpoint_url) | |
| `endpointDescription` | [`dcat:endpointDescription`](https://www.w3.org/TR/vocab-dcat-3/#Property:data_service_endpoint_description) | |
| `publisher`, `catalogResource`, `catalogDataset`, `catalogService` | [`dct:publisher`](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/#publisher), [`dcat:resource`](https://www.w3.org/TR/vocab-dcat-3/#Property:catalog_resource), [`dcat:dataset`](https://www.w3.org/TR/vocab-dcat-3/#Property:catalog_dataset), [`dcat:service`](https://www.w3.org/TR/vocab-dcat-3/#Property:catalog_service) | Catalogue membership. |

## GovStack vocabulary terms

| Term | Meaning |
|---|---|
| `govreg:Registry` | A specialisation of `dcat:Resource` for an institutionally governed system that maintains authoritative Records within a declared scope. |
| `govreg:authority` | Relates a Registry to the institution accountable for it and its authoritative scope. |
| `govreg:dataset` | Relates a Registry to a governed collection described as a DCAT Dataset. |
| `govreg:dataService` | Relates a Registry to a technical interface described as a DCAT Data Service. |

The [Turtle vocabulary](../05-api-families/registry-core-vocabulary.ttl) provides machine-readable definitions of these terms and the API-family concept scheme.

The vocabulary uses two namespace documents: `https://vocab.govstack.global/digital-registries` for Registry Core and `https://vocab.govstack.global/digital-registries/api-families` for the API-family concept scheme. Terms use stable, version-independent fragment IRIs. Namespace documents can provide HTML, Turtle, and JSON-LD representations through HTTP content negotiation. These vocabulary representations do not prescribe the format of an implementation's metadata.

The [JSON-LD context](../05-api-families/registry-core-context.jsonld) has the assigned publication URI `https://vocab.govstack.global/digital-registries/context/v1` and media type `application/ld+json`. Context versions are immutable and versioned independently of vocabulary terms, preserving the interpretation of existing JSON. See [publication coverage and limitations](../12-other-resources.md#121-coverage-and-limitations) for namespace availability and validation status.

## DCAT composition

The model composes Registry metadata with [Data Catalog Vocabulary 3](https://www.w3.org/TR/vocab-dcat-3/) resources:

- the institutionally governed Registry is a `govreg:Registry`;
- each governed collection can be a [`dcat:Dataset`](https://www.w3.org/TR/vocab-dcat-3/#Class:Dataset);
- each technical API or query interface can be a [`dcat:DataService`](https://www.w3.org/TR/vocab-dcat-3/#Class:Data_Service); and
- a directory that lists Registries can be a [`dcat:Catalog`](https://www.w3.org/TR/vocab-dcat-3/#Class:Catalog).

Catalogues can be operated by a Registry or by a national or sector directory serving multiple authorities.

In the [example document](../05-api-families/registry-core.md#informative-json-ld-example), the Registry has both `govreg:Registry` and [`dcat:Resource`](https://www.w3.org/TR/vocab-dcat-3/#Class:Resource) types. This explicitly expresses the vocabulary's subclass relationship and lets the catalogue list the Registry with [`dcat:resource`](https://www.w3.org/TR/vocab-dcat-3/#Property:catalog_resource), without relying on ontology inference.

The relationships have different scopes. `dcat:resource`, `dcat:dataset`, and `dcat:service` state what is listed in a catalogue. `govreg:dataset` and `govreg:dataService` state which datasets and services belong to a Registry. `dcat:servesDataset` states which dataset a technical service exposes, when applicable.

The same graph pattern covers common deployment arrangements:

- a single-Registry deployment publishes one Registry, its datasets, and its services in the catalogue;
- a multi-Registry implementation adds more Registry resources and their related datasets and services to the same catalogue; and
- an aggregating national catalogue can list resources from multiple Registry Authorities or use [`dcat:catalog`](https://www.w3.org/TR/vocab-dcat-3/#Property:catalog_catalog) to include catalogues published by those authorities.

## Processing as RDF

A consumer that needs RDF expands the document with the pinned context. `DigitalRegistriesApiFamilies` membership is then determined by the concept definitions in the Turtle vocabulary rather than by an IRI prefix. The `serviceType` values expand to concept IRIs under `https://vocab.govstack.global/digital-registries/api-families#`.

### External alignments

Adopting profiles can use external vocabularies to add jurisdictional or discovery semantics. These alignments are optional.

| Alignment | Intended use |
|---|---|
| Schema.org [`Service`](https://schema.org/Service) or [`GovernmentService`](https://schema.org/GovernmentService) | Web discovery when the Registry or its service facet meets the selected Schema.org type. |
| [Core Public Service Vocabulary Application Profile](https://github.com/SEMICeu/CPSV-AP) | Public-service description in implementations using CPSV or CPSV-AP. |
| [BRegDCAT-AP](https://github.com/SEMICeu/BRegDCAT-AP) | European base-registry catalogue interoperability. |
| National or sector profiles | Additional legal, organisational, service, or dataset metadata required by an adopter. |

An adopting profile adds types and properties where their semantics apply. Any equivalence between `govreg:Registry` and an external class is specific to that profile.
