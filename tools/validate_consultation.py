#!/usr/bin/env python3
"""Validate the current Consultation contracts and their concrete examples.

Run from the repository root:
  uv run --with-requirements tools/requirements-api.txt python tools/validate_consultation.py

This checks artifacts and schema acceptance/rejection, not deployed authorization,
source matching, cursor integrity/expiry, resource limits or selected traversal
guarantees, or disclosure behavior.
It reads only explicitly named current artifacts and their local dependencies.
"""

from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import re
import unittest
from urllib.parse import unquote, urldefrag, urljoin, urlparse

from jsonschema import Draft202012Validator, FormatChecker
from openapi_spec_validator import validate
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012
import yaml


ROOT = Path(__file__).resolve().parents[1]
API = ROOT / "api"
CANONICAL = API / "openapi.yaml"
BUSINESS = API / "examples/business-registry.openapi.yaml"
BINDING = API / "examples/business-registry.schema.json"
HOUSEHOLD = API / "examples/household-registry.openapi.yaml"
BIRTH = API / "examples/birth-registration.openapi.yaml"
RELATIONSHIPS = API / "examples/relationship-examples.schema.json"
OPENAPI_DOCUMENTS = (CANONICAL, BUSINESS, HOUSEHOLD, BIRTH)
EXTENSION = "x-govstack-digital-registries"
WRITE_EXTENSION = "x-govstack-digital-registries-write"
EXTENSION_SCHEMA = API / "extensions/x-govstack-digital-registries.schema.json"
METADATA_SCHEMA = API / "extensions/registry-metadata.schema.json"
METADATA_EXAMPLE = API / "examples/registry-metadata.jsonld"
LINKSET_EXAMPLE = API / "examples/api-catalog.linkset.json"
CONTEXT = ROOT / "assets/registry-core-context.jsonld"
DISCOVERY_PAGE = ROOT / "requirements/registry-discovery.md"
SERVICES_PAGE = ROOT / "requirements/registry-services.md"
ADOPTION_GUIDE = ROOT / "guides/adopting-digital-registries.md"
CONTEXT_URI = "https://vocab.govstack.global/digital-registries/context/v1"
API_FAMILY_PREFIX = "apif:"
CAPABILITY_BY_ROUTE = {
    ("get", "item"): "retrieve",
    ("get", "collection"): "list",
    ("post", "lookup"): "lookup",
    ("post", "search"): "search",
    ("get", "revision-list"): "revision-list",
    ("get", "revision-retrieve"): "revision-retrieve",
}
KNOWN_CAPABILITIES = set(CAPABILITY_BY_ROUTE.values())
WRITE_CAPABILITY_BY_OPERATION = {
    "createRecord": "create",
    "updateRecord": "update",
    "applyRecordTransition": "transition",
    "submitChangeRequest": "change-requests",
    "listChangeRequests": "change-request-list",
    "getChangeRequest": "change-request-retrieve",
    "approveChangeRequest": "change-request-approve",
    "rejectChangeRequest": "change-request-reject",
    "withdrawChangeRequest": "change-request-withdraw",
    "getOperation": "operation-retrieve",
}
KNOWN_WRITE_CAPABILITIES = set(WRITE_CAPABILITY_BY_OPERATION.values())
KNOWN_FEATURES = {
    "conditional-read", "field-selection", "complete-traversal", "snapshot-traversal",
    "recorded-time", "effective-time", "purpose-bound",
}
PUBLISHED_CONTRACTS = {
    "https://registry.example/contracts/1.0.0-draft/openapi.yaml": CANONICAL,
    "https://registry.example/contracts/1.0.0-draft/examples/business-registry.openapi.yaml": BUSINESS,
    "https://registry.example/contracts/1.0.0-draft/examples/household-registry.openapi.yaml": HOUSEHOLD,
    "https://registry.example/contracts/1.0.0-draft/examples/birth-registration.openapi.yaml": BIRTH,
}
SCHEMA_DOCUMENTS = (BINDING, RELATIONSHIPS, EXTENSION_SCHEMA, METADATA_SCHEMA)
DOCUMENTS: dict[str, dict] = {}


def load_local(uri: str) -> Resource:
    """Resolve shipped references without network access or legacy inspection."""
    parsed = urlparse(uri)
    if parsed.scheme != "file" or parsed.netloc:
        raise ValueError(f"Only local contract references are permitted: {uri}")
    source = Path(unquote(parsed.path)).resolve()
    if not source.is_relative_to(API) or source.is_relative_to(API / "legacy"):
        raise ValueError("Contract reference leaves current API artifacts")
    if uri not in DOCUMENTS:
        DOCUMENTS[uri] = yaml.safe_load(source.read_text())
    return Resource.from_contents(DOCUMENTS[uri], default_specification=DRAFT202012)


REGISTRY = Registry(retrieve=load_local)


def document(path: Path) -> dict:
    return load_local(path.as_uri()).contents


def validator(path: Path, pointer: str) -> Draft202012Validator:
    return Draft202012Validator(
        {"$ref": path.as_uri() + "#" + pointer},
        registry=REGISTRY,
        format_checker=FormatChecker(),
    )


def pointer_key(key: str) -> str:
    return str(key).replace("~", "~0").replace("/", "~1")


def nodes(value, pointer=""):
    if isinstance(value, dict):
        yield pointer, value
        for key, child in value.items():
            yield from nodes(child, pointer + "/" + pointer_key(key))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from nodes(child, pointer + "/" + str(index))


def resolve_object(path: Path, value: dict) -> tuple[Path, dict]:
    """Resolve OpenAPI Reference Objects while preserving the correct file base."""
    while "$ref" in value:
        reference, fragment = urldefrag(value["$ref"])
        path = (path.parent / reference).resolve() if reference else path
        value = document(path)
        for token in fragment.lstrip("/").split("/") if fragment else []:
            value = value[token.replace("~1", "/").replace("~0", "~")]
    return path, value


def route_kind(path: str, method: str) -> tuple[str, str] | None:
    """Classify only declared Record reads, independently from API resources."""
    if method not in {"get", "post"} or not path.startswith("/v1/collections/"):
        return None
    declared = (
        ("get", "/revisions/{revisionId}", "revision-retrieve"),
        ("get", "/revisions", "revision-list"),
        ("post", "/lookup", "lookup"),
        ("post", "/search", "search"),
        ("get", "/{recordId}", "item"),
        ("get", "/records", "collection"),
    )
    for expected_method, suffix, kind in declared:
        if method == expected_method and path.endswith(suffix):
            return method, kind
    return None


def collection_segment(path: str) -> str:
    return path.removeprefix("/v1/collections/").split("/")[0]


def success_record_schema_with_path(path: Path, operation: dict) -> tuple[Path, dict]:
    """Return the resolved Record schema and source, unwrapping a Page's items."""
    response_path, response = resolve_object(path, operation["responses"]["200"])
    schema_path, schema = resolve_object(response_path, response["content"]["application/json"]["schema"])
    for member in [schema, *schema.get("allOf", [])]:
        if "items" in member.get("properties", {}):
            schema_path, items = resolve_object(schema_path, member["properties"]["items"])
            schema_path, schema = resolve_object(schema_path, items["items"])
            break
    return schema_path, schema


def success_record_schema(path: Path, operation: dict) -> dict:
    """Return the resolved Record schema of a 200 response, unwrapping a Page's items."""
    return success_record_schema_with_path(path, operation)[1]


def operation_parameters(path: Path, operation: dict) -> list[tuple[Path, dict]]:
    return [resolve_object(path, parameter) for parameter in operation.get("parameters", [])]


def operation_features(operation: dict) -> set[str]:
    return set(operation[EXTENSION].get("features", []))


def response_headers(path: Path, operation: dict, status: str) -> dict[str, tuple[Path, dict]]:
    response_path, response = resolve_object(path, operation["responses"][status])
    return {name: resolve_object(response_path, header)
            for name, header in response.get("headers", {}).items()}


def response_records(response: dict) -> list[dict]:
    if "items" in response:
        return response["items"]
    return [response]


def as_list(value) -> list:
    return value if isinstance(value, list) else [value]


def validate_capability_identities(value: dict) -> None:
    """Check keyed discovery uniqueness that JSON Schema uniqueItems cannot express."""
    collections, operations = set(), set()
    for collection in value["collections"]:
        identity = collection["collectionId"]
        if identity in collections:
            raise ValueError("Caller capabilities repeat a collection identity")
        collections.add(identity)
        for operation in collection["operations"]:
            identity = (operation["contract"], operation["operationId"])
            if identity in operations:
                raise ValueError("Caller capabilities repeat a contract operation identity")
            operations.add(identity)
    for entry in value.get("operations", []):
        operation = entry["operation"]
        identity = (operation["contract"], operation["operationId"])
        if identity in operations:
            raise ValueError("Caller capabilities repeat a contract operation identity")
        operations.add(identity)


def _absolute_schema_refs(path: Path, value):
    """Copy a schema while making every reference absolute to its owning document."""
    if isinstance(value, dict):
        return {key: (urljoin(path.as_uri(), child) if key == "$ref" else
                      _absolute_schema_refs(path, child))
                for key, child in value.items()}
    if isinstance(value, list):
        return [_absolute_schema_refs(path, child) for child in value]
    return value


def _validate_schema_value(path: Path, schema: dict, value) -> None:
    Draft202012Validator(
        _absolute_schema_refs(path, schema),
        registry=REGISTRY,
        format_checker=FormatChecker(),
    ).validate(value)


def _casefold_headers(headers) -> dict[str, tuple[str, object]]:
    if headers is None:
        return {}
    if not isinstance(headers, dict):
        raise ValueError("HTTP headers must be an object")
    folded = {}
    for name, value in headers.items():
        if not isinstance(name, str):
            raise ValueError("HTTP header names must be strings")
        key = name.casefold()
        if key in folded:
            raise ValueError(f"HTTP header is repeated with different casing: {name}")
        folded[key] = (name, value)
    return folded


def _operation_by_id(contract: Path, operation_id: str) -> tuple[str, str, dict]:
    matches = [(path, method, operation)
               for path, item in document(contract)["paths"].items()
               for method, operation in item.items()
               if method in {"get", "post", "head", "put", "patch", "delete"}
               and operation.get("operationId") == operation_id]
    if len(matches) != 1:
        raise ValueError(f"Expected one operationId {operation_id!r} in {contract.name}")
    return matches[0]


def validate_exchange(contract: Path, exchange: dict) -> None:
    """Validate one illustrative exchange against its published operation contract."""
    route, method, operation = _operation_by_id(contract, exchange["operationId"])
    request = exchange.get("request", {})
    declared_parameters = {}
    for source, parameter in operation_parameters(contract, operation):
        location = parameter["in"]
        name = parameter["name"].casefold() if location == "header" else parameter["name"]
        declared_parameters[(location, name)] = (source, parameter)

    supplied = {
        "path": request.get("path", {}),
        "query": request.get("query", {}),
        "header": _casefold_headers(request.get("headers")),
    }
    for location, values in supplied.items():
        for supplied_name, supplied_value in values.items():
            lookup_name = supplied_name.casefold() if location == "header" else supplied_name
            if (location, lookup_name) not in declared_parameters:
                raise ValueError(f"Undeclared {location} parameter: {supplied_name}")
            source, parameter = declared_parameters[(location, lookup_name)]
            value = supplied_value[1] if location == "header" else supplied_value
            _validate_schema_value(source, parameter["schema"], value)
    for (location, name), (_, parameter) in declared_parameters.items():
        if parameter.get("required") and name not in supplied.get(location, {}):
            raise ValueError(f"Required {location} parameter is absent: {parameter['name']}")

    if "requestBody" in operation:
        body_path, request_body = resolve_object(contract, operation["requestBody"])
        if request_body.get("required") and "body" not in request:
            raise ValueError("Required request body is absent")
        if "body" in request:
            _validate_schema_value(
                body_path, request_body["content"]["application/json"]["schema"], request["body"])
    elif "body" in request:
        raise ValueError("Operation does not declare a request body")

    response_fixture = exchange["response"]
    status = str(response_fixture["status"])
    if status not in operation["responses"]:
        raise ValueError(f"Undeclared response status: {status}")
    response_path, response = resolve_object(contract, operation["responses"][status])
    declared_headers = {name.casefold(): (source, header)
                        for name, (source, header) in response_headers(contract, operation, status).items()}
    supplied_headers = _casefold_headers(response_fixture.get("headers"))
    for name, (_, value) in supplied_headers.items():
        if name not in declared_headers:
            raise ValueError(f"Undeclared response header: {name}")
        source, header = declared_headers[name]
        _validate_schema_value(source, header["schema"], value)
    for name, (_, header) in declared_headers.items():
        if header.get("required") and name not in supplied_headers:
            raise ValueError(f"Required response header is absent: {name}")

    content = response.get("content", {})
    if not content:
        if "body" in response_fixture:
            raise ValueError(f"Response {status} is bodyless")
    else:
        if "body" not in response_fixture:
            raise ValueError(f"Response {status} requires a body fixture")
        media = "application/problem+json" if int(status) >= 400 else "application/json"
        if media not in content:
            raise ValueError(f"Response {status} does not declare {media}")
        _validate_schema_value(response_path, content[media]["schema"], response_fixture["body"])

    body = response_fixture.get("body")
    request_path = request.get("path", {})
    successful = 200 <= int(status) < 300
    if successful and isinstance(body, dict) and "recordId" in request_path:
        records = body.get("items", [body])
        for record in records:
            if record.get("recordId") != request_path["recordId"]:
                raise ValueError("Response Record Identifier does not match the path recordId")
    if successful and isinstance(body, dict) and "revisionId" in request_path:
        if body.get("revision", {}).get("revisionId") != request_path["revisionId"]:
            raise ValueError("Response Revision Identifier does not match the path revisionId")
    if exchange["operationId"] == "getCallerCapabilities" and status == "200":
        validate_caller_capabilities(body)


def validate_conditional_exchange_pair(success: dict, not_modified: dict) -> None:
    """Check the ETag relationship between paired conditional 200 and 304 fixtures."""
    if success["operationId"] != not_modified["operationId"]:
        raise ValueError("Conditional exchanges use different operations")
    for key in ("path", "query"):
        if success.get("request", {}).get(key, {}) != not_modified.get("request", {}).get(key, {}):
            raise ValueError(f"Conditional exchanges use different request {key}")
    if success["response"]["status"] != 200 or not_modified["response"]["status"] != 304:
        raise ValueError("Conditional exchange pair must contain 200 then 304")
    success_headers = _casefold_headers(success["response"].get("headers"))
    request_headers = _casefold_headers(not_modified.get("request", {}).get("headers"))
    response_headers_value = _casefold_headers(not_modified["response"].get("headers"))
    try:
        tags = (success_headers["etag"][1], request_headers["if-none-match"][1],
                response_headers_value["etag"][1])
    except KeyError as error:
        raise ValueError(f"Conditional exchange pair lacks {error.args[0]}") from error
    if len(set(tags)) != 1:
        raise ValueError("Conditional 304 request and response must use the 200 response ETag")
    if "body" in not_modified["response"]:
        raise ValueError("Conditional 304 response must omit body")


def _schema_nodes(path: Path, schema: dict, seen=None):
    """Yield one schema and its composed or referenced descendants."""
    seen = set() if seen is None else seen
    if "$ref" in schema:
        reference = urljoin(path.as_uri(), schema["$ref"])
        if reference in seen:
            return
        seen.add(reference)
        path, schema = resolve_object(path, schema)
    yield path, schema
    for key in ("allOf", "anyOf", "oneOf"):
        for child in schema.get(key, []):
            yield from _schema_nodes(path, child, seen)


def _declared_property_names(path: Path, schema: dict) -> set[str]:
    names = set()
    for _, node in _schema_nodes(path, schema):
        names.update(node.get("properties", {}))
    return names


def _record_data_fields(contract: Path, operation: dict) -> set[str]:
    schema_path, record_schema = success_record_schema_with_path(contract, operation)
    fields = set()
    for source, node in _schema_nodes(schema_path, record_schema):
        data = node.get("properties", {}).get("data")
        if isinstance(data, dict):
            fields.update(_declared_property_names(source, data))
    return fields


def _request_discriminator_values(contract: Path, operation: dict, name: str) -> set[str]:
    if "requestBody" not in operation:
        return set()
    body_path, body = resolve_object(contract, operation["requestBody"])
    values = set()
    for _, node in _schema_nodes(body_path, body["content"]["application/json"]["schema"]):
        discriminator = node.get("properties", {}).get(name, {})
        if "const" in discriminator:
            values.add(discriminator["const"])
        values.update(discriminator.get("enum", []))
    return values


def validate_caller_capabilities(value: dict) -> None:
    """Validate discovery shape and agreement with explicitly mapped current contracts."""
    validator(CANONICAL, "/components/schemas/CallerCapabilities").validate(value)
    validate_capability_identities(value)
    entries = [
        (collection, advertised)
        for collection in value["collections"]
        for advertised in collection["operations"]
    ]
    entries.extend(
        (
            {"registry": entry["registry"], "collectionId": None},
            entry["operation"],
        )
        for entry in value.get("operations", [])
    )
    for collection, advertised in entries:
        family = advertised.get("family")
        capability = advertised["capability"]
        if family is None and capability in KNOWN_CAPABILITIES:
            family = "consultation"
        if (
            capability not in KNOWN_CAPABILITIES
            and capability not in KNOWN_WRITE_CAPABILITIES
        ):
            continue
        contract = PUBLISHED_CONTRACTS.get(advertised["contract"])
        if contract is None:
            raise ValueError("Caller capability references an unmapped contract URI")
        _, _, operation = _operation_by_id(contract, advertised["operationId"])
        if family == "write":
            read_only_fields = {
                "view",
                "features",
                "purpose",
                "readableFields",
                "selectors",
                "searches",
            }
            if read_only_fields & advertised.keys():
                raise ValueError(
                    "Caller Write capability contains Consultation-only metadata"
                )
            expected_capability = WRITE_CAPABILITY_BY_OPERATION.get(
                advertised["operationId"]
            )
            if expected_capability != capability:
                raise ValueError(
                    "Caller Write capability disagrees with linked operation"
                )
            declared_write = operation.get(WRITE_EXTENSION, {})
            if declared_write.get("registry") not in {
                None,
                collection["registry"],
            }:
                raise ValueError(
                    "Caller Write capability registry disagrees with linked operation"
                )
            if collection["collectionId"] is not None and declared_write.get(
                "collection"
            ) != collection["collectionId"]:
                raise ValueError(
                    "Caller Write capability collection disagrees with linked operation"
                )
            if capability in {"update", "transition"} and advertised.get(
                "write", {}
            ).get("companionRead") != declared_write.get("companionRead"):
                raise ValueError(
                    "Caller Write companion read disagrees with linked operation"
                )
            continue
        if family != "consultation" or collection["collectionId"] is None:
            raise ValueError(
                "Caller Consultation capability needs a Collection context"
            )
        declared = operation.get(EXTENSION)
        if declared is None:
            raise ValueError(
                "Caller capability references a non-Consultation operation"
            )
        expected = {
            "registry": collection["registry"],
            "collection": collection["collectionId"],
            "capability": capability,
            "view": advertised["view"],
        }
        for key, expected_value in expected.items():
            if declared.get(key) != expected_value:
                raise ValueError(
                    f"Caller capability {key} disagrees with linked operation"
                )
        advertised_features = set(advertised.get("features", [])) & KNOWN_FEATURES
        if advertised_features != set(declared.get("features", [])):
            raise ValueError(
                "Caller capability features disagree with linked operation"
            )
        advertised_purpose = deepcopy(advertised.get("purpose"))
        declared_purpose = deepcopy(declared.get("purpose"))
        for purpose in (advertised_purpose, declared_purpose):
            if isinstance(purpose, dict) and "allowedPurposes" in purpose:
                purpose["allowedPurposes"] = sorted(purpose["allowedPurposes"])
        if advertised_purpose != declared_purpose:
            raise ValueError("Caller capability purpose disagrees with linked operation")
        readable = set(advertised.get("readableFields", []))
        if not readable.issubset(_record_data_fields(contract, operation)):
            raise ValueError("Caller capability names an undeclared readable field")
        selectors = set(advertised.get("selectors", []))
        if selectors and capability != "lookup":
            raise ValueError("Caller capability selectors belong only to Lookup")
        if not selectors.issubset(
            _request_discriminator_values(contract, operation, "selector")
        ):
            raise ValueError("Caller capability names an undeclared selector")
        searches = set(advertised.get("searches", []))
        if searches and capability != "search":
            raise ValueError("Caller capability searches belong only to Search")
        if not searches.issubset(
            _request_discriminator_values(contract, operation, "search")
        ):
            raise ValueError("Caller capability names an undeclared search")


def fenced_json_blocks(markdown: str, anchor: str) -> list[dict]:
    """Parse JSON fences in the section identified by a stable explicit anchor."""
    lines = markdown.splitlines()
    anchor_marker = re.compile(rf'\bid=["\']{re.escape(anchor)}["\']')
    headings = [
        (index, match)
        for index, line in enumerate(lines)
        if (match := re.match(r"^(#{1,6})\s+", line))
        and anchor_marker.search(line)
    ]
    if len(headings) != 1:
        raise ValueError(
            f"Expected one heading with anchor {anchor}, found {len(headings)}"
        )
    start, heading_match = headings[0]
    level = len(heading_match.group(1))
    blocks, current = [], None
    for line in lines[start + 1:]:
        next_heading = re.match(r"^(#{1,6})\s+", line)
        if next_heading and len(next_heading.group(1)) <= level:
            break
        if line.strip() == "```json":
            if current is not None:
                raise ValueError(f"Nested JSON fence under {anchor}")
            current = []
        elif line.strip() == "```" and current is not None:
            try:
                blocks.append(json.loads("\n".join(current)))
            except json.JSONDecodeError as error:
                raise ValueError(f"Invalid JSON fence under {anchor}: {error}") from error
            current = None
        elif current is not None:
            current.append(line)
    if current is not None:
        raise ValueError(f"Unclosed JSON fence under {anchor}")
    return blocks


def exact_fenced_json_example(markdown: str, anchor: str, expected: dict) -> dict:
    """Require one authoritative JSON example with the shipped artifact value."""
    blocks = fenced_json_blocks(markdown, anchor)
    if blocks != [expected]:
        raise ValueError(
            f"{anchor} must contain exactly the authoritative JSON example"
        )
    return blocks[0]


PUBLICATION_GUIDANCE_MARKERS = (
    "api.yml",
    "registry-metadata.jsonld",
    "registry-metadata.schema.json",
    "api-catalog.linkset.json",
    "/.well-known/api-catalog",
    "/health",
    "validate_consultation.py",
)
PUBLICATION_GUIDANCE_LINKS = (
    "../resources/api.yml",
    "../api/examples/registry-metadata.jsonld",
    "../api/extensions/registry-metadata.schema.json",
    "../api/examples/api-catalog.linkset.json",
)


def validate_publication_guidance(markdown: str) -> None:
    """Reject adoption guidance that omits a required publication artifact."""
    missing = [marker for marker in PUBLICATION_GUIDANCE_MARKERS if marker not in markdown]
    if missing:
        raise ValueError(f"Adoption guide omits publication guidance: {missing}")
    links = {
        urldefrag(target)[0]
        for target in re.findall(r"\]\(([^)]+)\)", markdown)
    }
    wrong_links = [target for target in PUBLICATION_GUIDANCE_LINKS if target not in links]
    if wrong_links:
        raise ValueError(
            f"Adoption guide does not link the published artifacts: {wrong_links}"
        )


class ConsultationContractTests(unittest.TestCase):
    def test_required_format_checkers_are_available(self):
        self.assertIn("iri", FormatChecker().checkers,
                      "Install tools/requirements-api.txt so Registry IRI formats are asserted")

    def test_openapi_and_local_schema_documents(self):
        for path in OPENAPI_DOCUMENTS:
            with self.subTest(path=path.name):
                validate(document(path), base_uri=path.as_uri())
        for path in SCHEMA_DOCUMENTS:
            Draft202012Validator.check_schema(document(path))
        for schema in document(CANONICAL)["components"]["schemas"].values():
            Draft202012Validator.check_schema(schema)

    def test_framework_api_entrypoint_resolves_shared_components(self):
        entrypoint = ROOT / "resources/api.yml"
        shared = ROOT / "resources/common"
        self.assertTrue(shared.is_symlink(), "Shared components have one source")
        self.assertEqual(shared.readlink(), Path("../api/common"))
        self.assertTrue(shared.samefile(API / "common"))
        # Keep the requested URI as the base, as ordinary OpenAPI tooling does.
        validate(yaml.safe_load(entrypoint.read_text()), base_uri=entrypoint.as_uri())

    def test_all_inline_schema_and_media_examples(self):
        count = 0
        for path in (*OPENAPI_DOCUMENTS, *SCHEMA_DOCUMENTS):
            for pointer, node in nodes(document(path)):
                if isinstance(node.get("examples"), list):
                    for example in node["examples"]:
                        with self.subTest(file=path.name, pointer=pointer):
                            validator(path, pointer).validate(example)
                        count += 1
                if "schema" in node:
                    examples = []
                    if "example" in node:
                        examples.append(node["example"])
                    if isinstance(node.get("examples"), dict):
                        examples.extend(e["value"] for e in node["examples"].values() if "value" in e)
                    for example in examples:
                        with self.subTest(file=path.name, pointer=pointer):
                            validator(path, pointer + "/schema").validate(example)
                        count += 1
        self.assertGreater(count, 30, "The current request, response and domain examples must be exercised")

    def test_published_exchanges_use_actual_operation_schemas(self):
        spec = document(BUSINESS)
        operations = {
            operation["operationId"]: (path, method, operation)
            for path, item in spec["paths"].items()
            for method, operation in item.items()
            if method in ("get", "post")
        }
        exchanges = json.loads((API / "examples/consultation-exchanges.json").read_text())["exchanges"]
        for exchange in exchanges:
            path, method, operation = operations[exchange["operationId"]]
            base = "/paths/" + pointer_key(path) + "/" + method
            with self.subTest(exchange=exchange["name"]):
                for name, value in exchange.get("query", {}).items():
                    matches = [(parameter_path, parameter) for parameter_path, parameter
                               in operation_parameters(BUSINESS, operation)
                               if parameter["in"] == "query" and parameter["name"] == name]
                    self.assertEqual(len(matches), 1, f"{name} must be a declared query parameter")
                    parameter_path, parameter = matches[0]
                    schema = parameter["schema"]
                    if "$ref" in schema:
                        schema = {"$ref": urljoin(parameter_path.as_uri(), schema["$ref"])}
                    else:
                        schema = {"$id": parameter_path.as_uri(), **schema}
                    Draft202012Validator(
                        schema,
                        registry=REGISTRY,
                        format_checker=FormatChecker(),
                    ).validate(value)
                if "request" in exchange:
                    validator(BUSINESS, base + "/requestBody/content/application~1json/schema").validate(exchange["request"])
                response_path, response = resolve_object(BUSINESS, operation["responses"][str(exchange["status"])])
                media = "application/json" if exchange["status"] < 400 else "application/problem+json"
                schema = response["content"][media]["schema"]
                Draft202012Validator(
                    {**schema, "$ref": urljoin(response_path.as_uri(), schema["$ref"])},
                    registry=REGISTRY,
                    format_checker=FormatChecker(),
                ).validate(exchange["response"])
                if exchange["status"] >= 400:
                    self.assertEqual(exchange["response"]["status"], exchange["status"])

    def test_exact_selectors_reject_incomplete_or_undeclared_keys(self):
        check = validator(BINDING, "/$defs/BusinessLookupRequest")
        valid = {"selector": "byJurisdictionNumber", "values": {"jurisdictionCode": "AA", "localNumber": "00000042"}}
        check.validate(valid)
        invalid = [
            {"selector": "byJurisdictionNumber", "values": {"localNumber": "00000042"}},
            {"selector": "byJurisdictionNumber", "values": {"jurisdictionCode": "AA", "localNumber": 42}},
            {"selector": "byRegistrationNumber", "values": {"registrationNumber": "br-000042"}},
            {"selector": "byRegistrationNumber", "values": {"registrationNumber": "BR-000042\n"}},
            {"selector": "byJurisdictionNumber", "values": {"jurisdictionCode": "AA\n", "localNumber": "00000042"}},
            {"selector": "byJurisdictionNumber", "values": {"jurisdictionCode": "AA", "localNumber": "00000042\n"}},
            {"selector": "byRegistrationNumber", "values": valid["values"]},
            {"selector": "byRegistrationNumber", "values": {"registrationNumber": "BR-000042", "legalName": "Example Ltd"}},
            {"selector": "byUnknownKey", "values": {"key": "42"}},
            {"selector": "byRegistrationNumber", "values": {}},
            {**valid, "fields": []},
            {**valid, "fields": ["legalName", "legalName"]},
            {**valid, "fields": ["unknown"]},
            {**valid, "fields": "legalName"},
            {**valid, "pageSize": 1},
        ]
        for value in invalid:
            with self.subTest(value=value):
                self.assertFalse(check.is_valid(value))
        # A different deployment can bind a context-only selector with values:{}.
        validator(CANONICAL, "/components/schemas/LookupRequest").validate({"selector": "byVerifiedCaller", "values": {}})

    def test_declared_search_rejects_unbounded_and_undeclared_inputs(self):
        check = validator(BINDING, "/$defs/BusinessSearchRequest")
        valid = {"search": "byRegistrationStatus", "criteria": {"registrationStatus": "DISSOLVED"}}
        check.validate(valid)
        invalid = [
            {**valid, "filter": "registrationStatus eq 'DISSOLVED'"},
            {**valid, "sort": "recordId"},
            {**valid, "search": "anyExpression"},
            {**valid, "criteria": {"registrationStatus": "DISSOLVED", "legalName": "Example Ltd"}},
            {**valid, "criteria": {"registrationStatus": None}},
            {**valid, "pageSize": 0},
            {**valid, "pageSize": 101},
            {**valid, "cursor": ""},
            {**valid, "cursor": "opaqueCursor\n"},
            {**valid, "cursor": None},
            {**valid, "fields": []},
            {**valid, "fields": ["legalName", "legalName"]},
            {**valid, "fields": ["unknown"]},
            {**valid, "fields": 42},
        ]
        for value in invalid:
            with self.subTest(value=value):
                self.assertFalse(check.is_valid(value))

        self.assertFalse(validator(CANONICAL, "/components/schemas/Sort").is_valid("recordId\n"))

    def test_field_equality_search_accepts_declared_field_combinations(self):
        check = validator(BINDING, "/$defs/BusinessSearchRequest")
        for criteria in ({"legalName": "Example Ltd"}, {"registrationStatus": "DISSOLVED"},
                         {"legalName": "Example Ltd", "registrationStatus": "DISSOLVED"}):
            with self.subTest(criteria=criteria):
                check.validate({"search": "byFields", "criteria": criteria, "pageSize": 20})
        for criteria in ({}, {"recordId": "r_42"}, {"legalName": ""}, {"registrationStatus": None},
                         {"legalName": "Example Ltd", "undeclaredField": "value"}):
            with self.subTest(criteria=criteria):
                self.assertFalse(check.is_valid({"search": "byFields", "criteria": criteria}))

    def test_sort_accepts_adopted_and_nested_field_names(self):
        check = validator(CANONICAL, "/components/schemas/Sort")
        for value in ("recordId", "-legalName,recordId", "legal_name", "-address.city,registration_date.year"):
            with self.subTest(value=value):
                check.validate(value)
        for value in ("", "-", "--legalName", "_legalName", "legalName,", ",legalName", "address..city",
                      "address.", ".city", "legal name", "legal-name", "recordId\n"):
            with self.subTest(value=value):
                self.assertFalse(check.is_valid(value))

    def test_fixed_view_and_additive_envelope(self):
        check = validator(BINDING, "/$defs/BusinessRecord")
        record = {"recordId": "r_42", "data": {"legalName": "Example Ltd", "registrationStatus": "DISSOLVED"}}
        check.validate(record)
        check.validate({"recordId": "r_42", "data": {"legalName": "Example Ltd"}})
        check.validate({"recordId": "r_42", "data": {"registrationStatus": "DISSOLVED"}})
        check.validate({**record, "additionalEnvelopeMetadata": "future declared field"})
        self.assertFalse(check.is_valid({**record, "recordId": "r_42\n"}))
        self.assertFalse(check.is_valid({"data": {"legalName": "Example Ltd"}}))
        self.assertFalse(check.is_valid({"recordId": "r_42"}))
        for data in ({**record["data"], "undeclaredPrivateField": "value"}, {**record["data"], "legalName": 42}):
            self.assertFalse(check.is_valid({**record, "data": data}))

    def test_field_selection_schemas_and_projected_exchanges(self):
        generic = validator(CANONICAL, "/components/schemas/FieldSelection")
        business = validator(BINDING, "/$defs/BusinessFields")
        self.assertEqual(document(BINDING)["$defs"]["BusinessFields"]["maxItems"], 2)
        fields_parameter = document(CANONICAL)["components"]["parameters"]["Fields"]
        self.assertEqual((fields_parameter["name"], fields_parameter["in"]), ("fields", "query"))
        self.assertEqual((fields_parameter["style"], fields_parameter["explode"]), ("form", False))
        self.assertFalse(fields_parameter["required"])
        for value in (["legalName"], ["registrationStatus"], ["legalName", "registrationStatus"]):
            with self.subTest(valid=value):
                generic.validate(value)
                business.validate(value)
        for value in ([], ["legalName", "legalName"], ["unknown"], "legalName", [42]):
            with self.subTest(invalid=value):
                self.assertFalse(business.is_valid(value))

        self.assertFalse(validator(CANONICAL, "/components/schemas/LookupRequest").is_valid(
            {"selector": "byRegistrationNumber", "values": {"registrationNumber": "BR-000042"},
             "fields": ["legalName"]}))
        self.assertFalse(validator(CANONICAL, "/components/schemas/SearchRequest").is_valid(
            {"search": "byRegistrationStatus", "criteria": {"registrationStatus": "DISSOLVED"},
             "fields": ["legalName"]}))

        exchanges = json.loads((API / "examples/consultation-exchanges.json").read_text())["exchanges"]
        projected = [exchange for exchange in exchanges
                     if exchange.get("query", {}).get("fields") or exchange.get("request", {}).get("fields")]
        self.assertGreaterEqual(len(projected), 4)
        empty_data = 0
        for exchange in projected:
            fields = exchange.get("query", {}).get("fields", exchange.get("request", {}).get("fields"))
            for record in response_records(exchange["response"]):
                with self.subTest(exchange=exchange["name"], record=record):
                    self.assertIn("recordId", record)
                    self.assertIn("data", record)
                    self.assertTrue(set(record["data"]).issubset(fields))
                    empty_data += not record["data"]
        self.assertGreater(empty_data, 0, "A projected response retains identity when disclosure withholds every selected field")

    def test_registration_status_is_an_open_vocabulary(self):
        status = document(BINDING)["$defs"]["RegistrationStatus"]
        self.assertNotIn("enum", status)
        self.assertEqual(status["x-extensible-enum"], ["ACTIVE", "DISSOLVED"])
        record = validator(BINDING, "/$defs/BusinessRecord")
        criteria = validator(BINDING, "/$defs/RegistrationStatusCriteria")
        for value in ("ACTIVE", "DISSOLVED", "SUSPENDED"):
            with self.subTest(value=value):
                record.validate({"recordId": "r_42", "data": {"legalName": "Example Ltd", "registrationStatus": value}})
                criteria.validate({"registrationStatus": value})
        for value in ("", "dissolved", "DISSOLVED\n", 42, None):
            with self.subTest(value=value):
                self.assertFalse(criteria.is_valid({"registrationStatus": value}))

    def test_conditional_retrieve_follows_feature_declaration(self):
        saw_conditional = saw_baseline = False
        for path in OPENAPI_DOCUMENTS:
            spec = document(path)
            for route, item in spec["paths"].items():
                if route_kind(route, "get") != ("get", "item") or "get" not in item:
                    continue
                operation = item["get"]
                with self.subTest(file=path.name, operation=operation["operationId"]):
                    names = [(parameter["name"], parameter["in"])
                             for _, parameter in operation_parameters(path, operation)]
                    if "conditional-read" in operation_features(operation):
                        saw_conditional = True
                        self.assertIn(("If-None-Match", "header"), names)
                        self.assertIn("304", operation["responses"])
                        for status in ("200", "304"):
                            headers = response_headers(path, operation, status)
                            self.assertIn("ETag", headers, f"{status} carries the representation ETag")
                            self.assertTrue(headers["ETag"][1]["required"])
                        _, not_modified = resolve_object(path, operation["responses"]["304"])
                        self.assertNotIn("content", not_modified)
                    else:
                        saw_baseline = True
                        self.assertNotIn(("If-None-Match", "header"), names)
                        self.assertNotIn("304", operation["responses"])
        self.assertTrue(saw_conditional, "At least one example exercises conditional-read")
        self.assertTrue(saw_baseline, "The canonical and simple examples exercise baseline Retrieve")
        headers = document(CANONICAL)["components"]["headers"]
        self.assertFalse(headers["ETag"].get("required", False))
        self.assertTrue(headers["ConditionalETag"]["required"])

    def test_record_namespace_keeps_collection_actions_addressable(self):
        record_id = validator(CANONICAL, "/components/schemas/RecordId")
        ordinary_ids = ("r_42", "lookup", "search", "revisions", "capabilities", "lookups", "search-1")
        for source_id in ordinary_ids:
            with self.subTest(recordId=source_id):
                record_id.validate(source_id)
        bindings = ((CANONICAL, "{collectionId}"), (BUSINESS, "businesses"),
                    (HOUSEHOLD, "households"), (BIRTH, "birth-registrations"))
        write_methods = {"post", "put", "patch", "delete"}
        for contract, collection in bindings:
            spec = document(contract)
            collection_path = "/v1/collections/" + collection
            retrieve_path = collection_path + "/records/{recordId}"
            retrieve = spec["paths"][retrieve_path]
            self.assertIn("get", retrieve)
            expected_write_methods = {"patch"} if contract == CANONICAL else set()
            self.assertEqual(set(retrieve) & write_methods, expected_write_methods)
            parameters = [resolve_object(contract, parameter) for parameter in retrieve["get"]["parameters"]]
            id_parameter = [(path, value) for path, value in parameters if value["in"] == "path" and value["name"] == "recordId"]
            self.assertEqual(id_parameter, [(CANONICAL, document(CANONICAL)["components"]["parameters"]["RecordId"])])
            for source_id in ordinary_ids:
                with self.subTest(contract=contract.name, recordId=source_id):
                    requested_path = collection_path.replace("{collectionId}", "records") + "/records/" + source_id
                    matches = []
                    for path in spec["paths"]:
                        pattern = "".join("[^/]+" if part.startswith("{") else re.escape(part)
                                          for part in re.split(r"(\{[^{}]+\})", path))
                        if re.fullmatch(pattern, requested_path):
                            matches.append(path)
                    self.assertEqual(matches, [retrieve_path])
            if contract in (CANONICAL, BUSINESS):
                for suffix in ("lookup", "search"):
                    action = spec["paths"][collection_path + "/" + suffix]
                    self.assertEqual(set(action) & ({"get"} | write_methods), {"post"})
        concrete_operations = [operation["operationId"]
                               for contract in (BUSINESS, HOUSEHOLD, BIRTH)
                               for path, item in document(contract)["paths"].items()
                               if path.startswith("/v1/")
                               for method, operation in item.items()
                               if method in ("get", "post")]
        self.assertEqual(len(concrete_operations), len(set(concrete_operations)),
                         "Collection operations must remain unique when composing these examples into one API")

    def test_page_completion_and_bounds(self):
        check = validator(BINDING, "/$defs/BusinessPage")
        check.validate({"items": [], "pageInfo": {"nextCursor": "opaqueContinuation"}})
        check.validate({"items": [], "pageInfo": {"nextCursor": None, "total": 0}})
        for page_info in ({}, {"nextCursor": ""}, {"nextCursor": "invalid+cursor"},
                          {"nextCursor": "opaqueCursor\n"},
                          {"nextCursor": "a" * 4097}, {"hasMore": False},
                          {"nextCursor": None, "total": 1.5}):
            self.assertFalse(check.is_valid({"items": [], "pageInfo": page_info}))
        item = {"recordId": "r_42", "data": {"legalName": "Example Ltd", "registrationStatus": "DISSOLVED"}}
        self.assertFalse(check.is_valid({"items": [item] * 101, "pageInfo": {"nextCursor": None}}))
        exchanges = json.loads((API / "examples/consultation-exchanges.json").read_text())["exchanges"]
        empty_list = next(exchange for exchange in exchanges if exchange["name"] == "emptyList")
        self.assertEqual(empty_list["response"], {"items": [], "pageInfo": {"nextCursor": None, "total": 0}})
        search_id = document(BUSINESS)["paths"]["/v1/collections/businesses/search"]["post"]["operationId"]
        pages = [e for e in exchanges if e["operationId"] == search_id]
        first, final = pages
        self.assertEqual(first["response"]["items"], [])
        self.assertEqual(first["response"]["pageInfo"]["nextCursor"], final["request"]["cursor"])
        self.assertEqual(first["request"]["search"], final["request"]["search"])
        self.assertEqual(first["request"]["criteria"], final["request"]["criteria"])
        self.assertEqual(first["request"]["fields"], final["request"]["fields"])
        self.assertNotIn("pageSize", final["request"], "Example must exercise omission reusing the bound size")
        self.assertLessEqual(len(final["response"]["items"]), first["request"]["pageSize"])
        self.assertIsNone(final["response"]["pageInfo"]["nextCursor"])

    def test_error_examples_match_http_status_and_namespace(self):
        for name, response in document(CANONICAL)["components"]["responses"].items():
            media = response.get("content", {}).get("application/problem+json")
            if not media:
                continue
            examples = [media["example"]] if "example" in media else [e["value"] for e in media["examples"].values()]
            for example in examples:
                with self.subTest(response=name):
                    self.assertTrue(example["type"].startswith("https://govstack.global/problems/digital-registries/"))
                    self.assertNotIn("code", example)
                    self.assertNotIn("timestamp", example)
                    for item in document(CANONICAL)["paths"].values():
                        for method, operation in item.items():
                            if method not in ("get", "post"):
                                continue
                            for status, declared in operation["responses"].items():
                                if declared.get("$ref") == "#/components/responses/" + name:
                                    self.assertEqual(example["status"], int(status))

    def test_relationship_fixtures_use_concrete_schemas(self):
        fixtures = json.loads((API / "examples/relationship-exchanges.json").read_text())["examples"]
        for fixture in fixtures:
            with self.subTest(fixture=fixture["name"]):
                validator(RELATIONSHIPS, "/$defs/" + fixture["schema"]).validate(fixture["value"])
                if "contract" in fixture:
                    contract = API / "examples" / fixture["contract"]
                    self.assertIn(contract, OPENAPI_DOCUMENTS)
                    matches = [(path, method, operation)
                               for path, item in document(contract)["paths"].items()
                               for method, operation in item.items()
                               if method in ("get", "post") and operation["operationId"] == fixture["operationId"]]
                    self.assertEqual(len(matches), 1)
                    path, method, operation = matches[0]
                    status = str(fixture["status"])
                    media = operation["responses"][status]["content"]["application/json"]
                    pointer = "/paths/" + pointer_key(path) + "/" + method + "/responses/" + status + "/content/application~1json/schema"
                    validator(contract, pointer).validate(fixture["value"])
                    examples = ([media["example"]] if "example" in media else
                                [example["value"] for example in media.get("examples", {}).values()
                                 if "value" in example])
                    self.assertIn(fixture["value"], examples,
                                  "The operation publishes the same concrete relationship fixture")
        for contract, collection in ((HOUSEHOLD, "households"), (BIRTH, "birth-registrations")):
            operation = document(contract)["paths"]["/v1/collections/" + collection + "/records/{recordId}"]["get"]
            parameters = [resolve_object(contract, p)[1] for p in operation["parameters"]]
            self.assertFalse(any(p["in"] == "query" and p["name"] == "fields" for p in parameters), "These Retrieve contracts do not offer consumer-selected fields")

    def test_reference_context_rejects_ambiguous_or_conflicting_targets(self):
        fixed = validator(RELATIONSHIPS, "/$defs/IndividualReference")
        explicit = validator(RELATIONSHIPS, "/$defs/UnscopedRecordReference")
        target = "https://registry.example/registries/individuals"
        fixed.validate({"recordId": "person_42"})
        fixed.validate({"recordId": "person_42", "registryId": target})
        explicit.validate({"recordId": "person_42", "registryId": target})
        explicit.validate({"recordId": "r_7", "registryId": "urn:example:registry:external"})
        explicit.validate({"recordId": "r_7", "registryId": "urn:example:registre:état-civil"})
        for value in ({"recordId": "person_42", "registryId": "https://registry.example/registries/other"},
                      {"registryId": target}, {"recordId": ""},
                      {"recordId": "person_42", "href": "https://registry.example/person_42"}):
            with self.subTest(fixed_target=value):
                self.assertFalse(fixed.is_valid(value))
        for value in ({"recordId": "person_42"}, {"registryId": target},
                      {"recordId": "person_42", "registryId": "/registries/individuals"},
                      {"recordId": "person_42", "registryId": "urn:example:invalid registry"},
                      {"recordId": "person_42", "registryId": "https://registry.example/%invalid"},
                      {"recordId": "person_42", "registryId": 42}):
            with self.subTest(unscoped_target=value):
                self.assertFalse(explicit.is_valid(value))

    def test_household_nested_types_and_profile_bounds(self):
        check = validator(RELATIONSHIPS, "/$defs/HouseholdRecord")
        record = deepcopy(document(RELATIONSHIPS)["$defs"]["HouseholdRecord"]["examples"][0])
        check.validate(record)
        check.validate({**record, "additionalEnvelopeMetadata": "future declared field"})
        invalid_data = [
            {**record["data"], "address": "12 Example Street"},
            {**record["data"], "address": {"addressLines": [12], "locality": "Example Town"}},
            {**record["data"], "address": {"addressLines": ["Line"] * 4, "locality": "Example Town"}},
            {**record["data"], "address": {"addressLines": ["Line"], "locality": "Example Town", "postalCode": 120}},
            {**record["data"], "memberships": {}},
            {**record["data"], "memberships": [{"membershipId": "m_1", "role": "MEMBER", "individualRef": "person_42"}]},
            {**record["data"], "memberships": [{"role": "MEMBER", "individualRef": {"recordId": "person_42"}}]},
            {**record["data"], "memberships": [{"membershipId": "m_1", "role": 1, "individualRef": {"recordId": "person_42"}}]},
            {**record["data"], "memberships": [{"membershipId": "m_" + str(i), "role": "MEMBER", "individualRef": {"recordId": "person_" + str(i)}} for i in range(21)]},
            {**record["data"], "include": "individuals"},
        ]
        for data in invalid_data:
            with self.subTest(data=data):
                self.assertFalse(check.is_valid({**record, "data": data}))

    def test_registration_snapshots_do_not_require_parent_references(self):
        parent_check = validator(RELATIONSHIPS, "/$defs/ParentAtRegistration")
        parent_check.validate({"nameAtRegistration": "Alex Example"})
        parent_check.validate({"nameAtRegistration": "Robin Example", "individualRef": {"recordId": "person_57"}})
        for value in ({"individualRef": {"recordId": "person_57"}},
                      {"nameAtRegistration": "Robin Example", "individualRef": None},
                      {"nameAtRegistration": "Robin Example", "individualRef": {"recordId": "person_57", "registryId": "urn:example:wrong-registry"}},
                      {"nameAtRegistration": 57}):
            self.assertFalse(parent_check.is_valid(value))
        record_check = validator(RELATIONSHIPS, "/$defs/BirthRegistrationRecord")
        record = deepcopy(document(RELATIONSHIPS)["$defs"]["BirthRegistrationRecord"]["examples"][0])
        record_check.validate(record)
        self.assertEqual(set(record), {"recordId", "data"}, "The example must not require source metadata enrichment")
        self.assertFalse(record_check.is_valid({**record, "data": {**record["data"], "parents": [{"nameAtRegistration": "Example"}] * 5}}))
        self.assertFalse(record_check.is_valid({**record, "data": {**record["data"], "dateOfBirth": "2020-02-30"}}))

    def test_consultation_operations_declare_registry_context(self):
        extension_check = validator(EXTENSION_SCHEMA, "")
        for path in OPENAPI_DOCUMENTS:
            spec = document(path)
            views: dict[tuple[str, str, str], tuple[str, dict]] = {}
            for route, item in spec["paths"].items():
                for method, operation in item.items():
                    kind = route_kind(route, method)
                    if kind is None:
                        continue
                    with self.subTest(file=path.name, operation=operation.get("operationId")):
                        self.assertIn(EXTENSION, operation, "Every Consultation operation declares its Registry context")
                        declared = operation[EXTENSION]
                        extension_check.validate(declared)
                        self.assertEqual(declared["capability"], CAPABILITY_BY_ROUTE[kind])
                        if collection_segment(route) == "{collectionId}":
                            collection_params = [p for _, p in operation_parameters(path, operation)
                                                 if p["name"] == "collectionId" and p["in"] == "path"]
                            self.assertEqual(len(collection_params), 1)
                            _, collection_schema = resolve_object(path, collection_params[0]["schema"])
                            self.assertEqual(collection_schema["enum"], [declared["collection"]])
                        else:
                            self.assertEqual(declared["collection"], collection_segment(route))
                        key = (declared["registry"], declared["collection"], declared["view"])
                        schema = success_record_schema(path, operation)
                        if key in views:
                            self.assertEqual(views[key][1], schema,
                                             f"{operation['operationId']} and {views[key][0]} share a view but not a Record schema")
                        views[key] = (operation["operationId"], schema)
        for path, invalid in (
            (EXTENSION_SCHEMA, {"registry": "https://registry.example/registries/business", "collection": "businesses", "capability": "retrieve"}),
            (EXTENSION_SCHEMA, {"registry": "not an iri", "collection": "businesses", "capability": "retrieve", "view": "public"}),
            (EXTENSION_SCHEMA, {"registry": "https://registry.example/registries/business", "collection": "Businesses", "capability": "retrieve", "view": "public"}),
            (EXTENSION_SCHEMA, {"registry": "https://registry.example/registries/business", "collection": "businesses", "capability": "delete", "view": "public"}),
            (EXTENSION_SCHEMA, {"registry": "https://registry.example/registries/business", "collection": "businesses", "capability": "retrieve", "view": "public", "family": "consultation"}),
        ):
            self.assertFalse(validator(path, "").is_valid(invalid), invalid)

    def test_optional_feature_schema_and_operation_surfaces(self):
        extension = validator(EXTENSION_SCHEMA, "")
        base = {"registry": "https://registry.example/registries/business",
                "collection": "businesses", "capability": "retrieve", "view": "public"}
        for value in (
            base,
            {**base, "features": []},
            {**base, "features": ["conditional-read", "field-selection"]},
            {**base, "capability": "lookup", "features": ["field-selection"]},
            {**base, "capability": "list", "features": ["complete-traversal"]},
            {**base, "capability": "search", "features": ["complete-traversal", "snapshot-traversal"]},
        ):
            with self.subTest(valid=value):
                extension.validate(value)
        for value in (
            {**base, "capability": "lookup", "features": ["conditional-read"]},
            {**base, "features": ["complete-traversal"]},
            {**base, "capability": "list", "features": ["snapshot-traversal"]},
            {**base, "features": ["field-selection", "field-selection"]},
            {**base, "features": ["unknown-feature"]},
        ):
            with self.subTest(invalid=value):
                self.assertFalse(extension.is_valid(value))

        expected_business = {
            "retrieveBusiness": {"conditional-read", "field-selection"},
            "lookupBusiness": {"field-selection"},
            "listBusinesses": {"field-selection", "complete-traversal"},
            "searchBusinesses": {"field-selection", "complete-traversal"},
        }
        for path in OPENAPI_DOCUMENTS:
            for route, item in document(path)["paths"].items():
                for method, operation in item.items():
                    if route_kind(route, method) is None:
                        continue
                    features = operation_features(operation)
                    expected = expected_business.get(operation["operationId"], set())
                    if path == CANONICAL and operation["operationId"] == "retrieveRecord":
                        expected = {"conditional-read"}
                    with self.subTest(file=path.name, operation=operation["operationId"]):
                        if path == BUSINESS or (path == CANONICAL and operation[EXTENSION]["capability"] in {"retrieve", "lookup", "list", "search"}):
                            self.assertEqual(features, expected)
                        if method == "get":
                            query_names = {parameter["name"] for _, parameter
                                           in operation_parameters(path, operation)
                                           if parameter["in"] == "query"}
                            self.assertEqual("fields" in query_names, "field-selection" in features)
                            if "field-selection" in features:
                                self.assertIn("400", operation["responses"])
                        else:
                            body_path, body = resolve_object(path, operation["requestBody"])
                            _, schema = resolve_object(
                                body_path, body["content"]["application/json"]["schema"])
                            self.assertEqual("fields" in schema.get("properties", {}),
                                             "field-selection" in features)
                            if "field-selection" in features:
                                self.assertTrue({"400", "422"}.issubset(operation["responses"]))

    def test_registry_metadata_example_is_well_formed(self):
        metadata = json.loads(METADATA_EXAMPLE.read_text())
        validator(METADATA_SCHEMA, "").validate(metadata)
        self.assertEqual(metadata["@context"], CONTEXT_URI)
        from pyld import jsonld
        local_context = json.loads(CONTEXT.read_text())
        def loader(url, options=None):
            self.assertEqual(url, CONTEXT_URI, "The example must only depend on the shipped context")
            return {"contextUrl": None, "documentUrl": url, "document": local_context}
        expanded = jsonld.expand(metadata, {"documentLoader": loader})
        by_id = {node["@id"]: node for node in expanded}
        registries = [n for n in expanded if "https://vocab.govstack.global/digital-registries#Registry" in n.get("@type", [])]
        self.assertTrue(registries, "The example describes at least one Registry")
        for registry in registries:
            for property_iri in ("http://purl.org/dc/terms/title", "http://purl.org/dc/terms/description",
                                 "http://purl.org/dc/terms/references",
                                 "https://vocab.govstack.global/digital-registries#authority",
                                 "https://vocab.govstack.global/digital-registries#dataService"):
                self.assertIn(property_iri, registry, f"{registry['@id']} lacks {property_iri}")
            for service_ref in registry["https://vocab.govstack.global/digital-registries#dataService"]:
                service = by_id[service_ref["@id"]]
                self.assertIn("http://www.w3.org/ns/dcat#DataService", service["@type"])
                families = [t["@id"] for t in service["http://purl.org/dc/terms/type"]]
                self.assertTrue(all(f.startswith("https://vocab.govstack.global/digital-registries/api-families#") for f in families))
                self.assertIn("http://www.w3.org/ns/dcat#endpointURL", service)
                self.assertIn("http://www.w3.org/ns/dcat#endpointDescription", service)
        metadata_check = validator(METADATA_SCHEMA, "")
        registry_node = next(n for n in metadata["@graph"] if "govreg:Registry" in as_list(n["@type"]))
        for missing in ("title", "authority", "specification", "description", "dataService"):
            broken = deepcopy(metadata)
            node = next(n for n in broken["@graph"] if n["@id"] == registry_node["@id"])
            del node[missing]
            self.assertFalse(metadata_check.is_valid(broken), f"Registry without {missing} must be rejected")
        broken = deepcopy(metadata)
        broken["@context"] = "https://vocab.govstack.global/digital-registries/context/v2"
        self.assertFalse(metadata_check.is_valid(broken), "Only the pinned context version is accepted")

    def test_registry_and_authority_identifiers_need_not_be_https(self):
        metadata = json.loads(METADATA_EXAMPLE.read_text())
        registry_node = next(n for n in metadata["@graph"] if "govreg:Registry" in as_list(n["@type"]))
        registry_node["@id"] = "urn:example:registries:business"
        registry_node["authority"] = "urn:example:organisations:business-authority"
        validator(METADATA_SCHEMA, "").validate(metadata)
        validator(EXTENSION_SCHEMA, "").validate({"registry": "urn:example:registries:business",
                                                  "collection": "businesses", "capability": "retrieve",
                                                  "view": "business-public"})

    def test_api_catalog_links_contracts_and_metadata(self):
        linkset = json.loads(LINKSET_EXAMPLE.read_text())
        metadata = json.loads(METADATA_EXAMPLE.read_text())
        self.assertEqual(list(linkset), ["linkset"])
        descriptions, metadata_links = set(), set()
        for context in linkset["linkset"]:
            self.assertTrue(context["anchor"].startswith("https://"))
            for link in context.get("service-desc", []):
                self.assertTrue(link["href"].startswith("https://"))
                self.assertIn(link["type"], ("application/vnd.oai.openapi", "application/vnd.oai.openapi+json"))
                descriptions.add(link["href"])
            for link in context.get("service-meta", []):
                self.assertEqual(link["type"], "application/ld+json")
                metadata_links.add(link["href"])
        services = [n for n in metadata["@graph"] if "dcat:DataService" in as_list(n["@type"])]
        self.assertTrue(services)
        self.assertEqual({s["endpointDescription"] for s in services}, descriptions,
                         "The linkset advertises exactly the contracts the metadata declares")
        catalog = next(n for n in metadata["@graph"] if "dcat:Catalog" in as_list(n["@type"]))
        self.assertEqual(metadata_links, {catalog["@id"]}, "service-meta points at the metadata document")
        self.assert_registry_associations(document(BUSINESS), metadata)

    def test_api_catalog_endpoint_is_described_at_the_origin_root(self):
        route = "/.well-known/api-catalog"
        catalog = document(CANONICAL)["paths"][route]
        self.assertEqual({key for key in catalog if key not in ("summary", "description", "servers")}, {"get", "head"},
                         "Well-known endpoints are read-only")
        self.assertEqual([server["url"] for server in catalog["servers"]], ["https://{gatewayHost}"],
                         "RFC 8615 roots the catalog at the origin, outside any routing prefix")
        for method in ("get", "head"):
            operation = catalog[method]
            with self.subTest(method=method):
                self.assertEqual(operation["security"], [])
                self.assertNotIn(EXTENSION, operation, "The catalog is not a Consultation operation")
                response_path, response = resolve_object(CANONICAL, operation["responses"]["200"])
                _, link = resolve_object(response_path, response["headers"]["Link"])
                self.assertTrue(link["required"], "RFC 9727 requires the api-catalog Link header on HEAD")
                _, etag = resolve_object(response_path, response["headers"]["ETag"])
                self.assertTrue(etag["required"], "Catalog GET and HEAD responses require ETag")
                header = Draft202012Validator(link["schema"], format_checker=FormatChecker())
                header.validate('</.well-known/api-catalog>; rel="api-catalog"')
                header.validate('<https://registry.example/catalogs/apis.json>; rel=api-catalog')
                self.assertFalse(header.is_valid('</catalog>; rel="service-meta"'))
        _, head = resolve_object(CANONICAL, catalog["head"]["responses"]["200"])
        self.assertNotIn("content", head)
        _, get = resolve_object(CANONICAL, catalog["get"]["responses"]["200"])
        self.assertEqual(list(get["content"]), ["application/linkset+json"])
        self.assertIn("ETag", get["headers"])
        parameters = [resolve_object(CANONICAL, parameter)[1] for parameter in catalog["get"]["parameters"]]
        self.assertIn(("If-None-Match", "header"), [(p["name"], p["in"]) for p in parameters])
        not_modified_path, not_modified = resolve_object(CANONICAL, catalog["get"]["responses"]["304"])
        self.assertIn("ETag", not_modified["headers"])
        _, not_modified_etag = resolve_object(not_modified_path, not_modified["headers"]["ETag"])
        self.assertTrue(not_modified_etag["required"], "Catalog 304 requires the matching ETag")
        self.assertNotIn("content", not_modified)
        check = validator(CANONICAL, "/components/schemas/ApiCatalog")
        check.validate(json.loads(LINKSET_EXAMPLE.read_text()))
        for invalid in ({}, {"linkset": {}}, {"linkset": []},
                        {"linkset": [{"service-desc": [{"type": "application/vnd.oai.openapi"}]}]},
                        {"linkset": [{"service-desc": {"href": "https://registry.example/openapi.yaml"}}]},
                        {"linkset": [{"anchor": 42}]}):
            with self.subTest(invalid=invalid):
                self.assertFalse(check.is_valid(invalid))
        for example in (BUSINESS, HOUSEHOLD, BIRTH):
            with self.subTest(file=example.name):
                self.assertEqual(document(example)["paths"][route],
                                 {"$ref": "../openapi.yaml#/paths/" + pointer_key(route)})

    def assert_registry_associations(self, contract, metadata):
        registry_ids = {n["@id"] for n in metadata["@graph"]
                        if "govreg:Registry" in as_list(n["@type"])}
        for route, item in contract["paths"].items():
            for method, operation in item.items():
                if route_kind(route, method) and EXTENSION in operation:
                    self.assertIn(operation[EXTENSION]["registry"], registry_ids)

    def test_registry_association_rejects_undeclared_registry(self):
        metadata = json.loads(METADATA_EXAMPLE.read_text())
        business = document(BUSINESS)
        for route, item in business["paths"].items():
            for method, operation in item.items():
                if EXTENSION not in operation:
                    continue
                with self.subTest(operation=operation["operationId"]):
                    broken = deepcopy(business)
                    broken["paths"][route][method][EXTENSION]["registry"] = "https://registry.example/registries/absent"
                    with self.assertRaises(AssertionError):
                        self.assert_registry_associations(broken, metadata)

    def test_requirement_pages_match_discovery_and_schema_examples(self):
        discovery = DISCOVERY_PAGE.read_text()
        metadata = exact_fenced_json_example(
            discovery,
            "core-informative-json-ld-example",
            json.loads(METADATA_EXAMPLE.read_text()),
        )
        validator(METADATA_SCHEMA, "").validate(metadata)
        linkset = exact_fenced_json_example(
            discovery,
            "core-discovery-publication",
            json.loads(LINKSET_EXAMPLE.read_text()),
        )
        validator(CANONICAL, "/components/schemas/ApiCatalog").validate(linkset)

        services = SERVICES_PAGE.read_text()
        business_example = document(BINDING)["$defs"]["BusinessRecord"]["examples"][0]
        business = exact_fenced_json_example(
            services, "core-common-record-context", business_example)
        validator(BINDING, "/$defs/BusinessRecord").validate(business)

        reference_example = document(RELATIONSHIPS)["$defs"]["UnscopedRecordReference"]["examples"][0]
        reference = exact_fenced_json_example(
            services,
            "core-structured-values-and-references",
            reference_example,
        )
        validator(RELATIONSHIPS, "/$defs/UnscopedRecordReference").validate(
            reference)

    def test_relocated_example_checks_reject_mutated_json(self):
        discovery = DISCOVERY_PAGE.read_text()
        expected_metadata = json.loads(METADATA_EXAMPLE.read_text())
        mutated_discovery = discovery.replace(
            '"@context": "https://vocab.govstack.global/digital-registries/context/v1"',
            '"@context": "https://vocab.govstack.global/digital-registries/context/v2"',
            1,
        )
        self.assertNotEqual(mutated_discovery, discovery)
        with self.assertRaisesRegex(ValueError, "authoritative JSON example"):
            exact_fenced_json_example(
                mutated_discovery,
                "core-informative-json-ld-example",
                expected_metadata,
            )

        services = SERVICES_PAGE.read_text()
        expected_record = document(BINDING)["$defs"]["BusinessRecord"]["examples"][0]
        mutated_services = services.replace('"recordId": "r_42"', '"recordId": "r_43"', 1)
        self.assertNotEqual(mutated_services, services)
        with self.assertRaisesRegex(ValueError, "authoritative JSON example"):
            exact_fenced_json_example(
                mutated_services,
                "core-common-record-context",
                expected_record,
            )

    def test_adoption_guide_names_the_published_artifacts_and_links_resolve(self):
        page = ADOPTION_GUIDE.read_text()
        validate_publication_guidance(page)
        for target in re.findall(r"\]\(([^)#\s]+)(?:#[^)]*)?\)", page):
            if target.startswith("http"):
                continue
            self.assertTrue(
                (ADOPTION_GUIDE.parent / target).exists(),
                f"{ADOPTION_GUIDE.name} links to missing {target}",
            )

    def test_publication_guidance_check_rejects_an_omitted_artifact(self):
        guidance = "\n".join(
            (*PUBLICATION_GUIDANCE_MARKERS,
             *(f"[artifact]({target})" for target in PUBLICATION_GUIDANCE_LINKS))
        )
        validate_publication_guidance(guidance)
        with self.assertRaisesRegex(ValueError, "api-catalog.linkset.json"):
            validate_publication_guidance(
                guidance.replace("api-catalog.linkset.json", "catalog.json")
            )
        with self.assertRaisesRegex(ValueError, "does not link"):
            validate_publication_guidance(
                guidance.replace(
                    "../api/examples/registry-metadata.jsonld",
                    "../resources/registry-metadata.jsonld",
                )
            )

    def test_discovery_page_contains_the_metadata_vocabulary_guidance(self):
        discovery = DISCOVERY_PAGE.read_text()
        for anchor in (
            "vocabulary-key-to-term-mapping",
            "vocabulary-govstack-vocabulary-terms",
            "vocabulary-dcat-composition",
            "vocabulary-processing-as-rdf",
        ):
            with self.subTest(anchor=anchor):
                self.assertIn(f'id="{anchor}"', discovery)
        self.assertIn(
            "| Concept | JSON key | Status | Meaning |",
            discovery,
            "Discovery describes metadata by JSON key",
        )


if __name__ == "__main__":
    from test_consultation_extensions import ConsultationExtensionTests

    unittest.main(defaultTest=(ConsultationContractTests.__name__, ConsultationExtensionTests.__name__),
                  verbosity=2)
