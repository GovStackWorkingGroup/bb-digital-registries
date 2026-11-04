#!/usr/bin/env python3
"""Validate the current Write contracts and concrete examples offline.

Run from the repository root:
  uv run python tools/validate_write.py

This validates published artifacts, schema relationships, and illustrative HTTP
exchanges. It does not claim that a deployed implementation enforces authority,
preconditions, idempotency, atomicity, review policy, or audit requirements.
"""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
from pathlib import Path
from pathlib import PurePosixPath
import posixpath
import re
import sys
from typing import Any, Iterable
from urllib.parse import unquote, urldefrag, urljoin, urlparse

from jsonschema import Draft202012Validator, FormatChecker, ValidationError
from openapi_spec_validator.validation.validators import OpenAPIV31SpecValidator
from jsonschema_path import SchemaPath
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012
import yaml


ROOT = Path(__file__).resolve().parents[1]
API = ROOT / "api"
WRITE = API / "write.openapi.yaml"
WRITE_EXTENSION_SCHEMA = (
    API / "extensions/x-govstack-digital-registries-write.schema.json"
)
WRITE_COVERAGE = API / "write-coverage.yaml"
EXAMPLE_API = API / "examples/write-examples.openapi.yaml"
EXAMPLE_SCHEMA = API / "examples/write-examples.schema.json"
EXCHANGES = API / "examples/write-exchanges.json"
CONTRACT_FIXTURES = API / "examples/write-contract-fixtures.json"
VENDOR = API / "examples/publicschema"
VENDOR_PROVENANCE = VENDOR / "PROVENANCE.md"
EXTENSION = "x-govstack-digital-registries-write"
HTTP_METHODS = {"get", "put", "post", "delete", "options", "head", "patch", "trace"}

WRITE_OPERATIONS = {
    "createRecord": "create",
    "updateRecord": "update",
    "applyRecordTransition": "transition",
    "submitChangeRequest": "change-requests",
    "approveChangeRequest": "change-requests",
    "rejectChangeRequest": "change-requests",
    "withdrawChangeRequest": "change-requests",
}
REFERENCE_REQUIRED_OPERATIONS = set(WRITE_OPERATIONS) - {"withdrawChangeRequest"}
DIRECT_INPUTS = {
    "createRecord": "CreateInput",
    "updateRecord": "UpdateInput",
    "applyRecordTransition": "TransitionInput",
}
STRONG_PRECONDITION_OPERATIONS = {
    "updateRecord",
    "applyRecordTransition",
    "approveChangeRequest",
    "rejectChangeRequest",
    "withdrawChangeRequest",
}
FORBIDDEN_CLIENT_FIELDS = {
    "actor",
    "actorId",
    "approval",
    "approvedBy",
    "appliedBy",
    "applicationState",
    "decision",
    "error",
    "purpose",
    "result",
    "reviewState",
    "reviewStatus",
    "reviewer",
    "reviewerId",
}
DOCUMENTS: dict[str, Any] = {}


def load_document(path: Path) -> Any:
    """Load JSON or YAML by content and retain the document for local resolution."""
    path = path.resolve()
    uri = path.as_uri()
    if uri not in DOCUMENTS:
        DOCUMENTS[uri] = yaml.safe_load(path.read_text())
    return DOCUMENTS[uri]


def _load_local(uri: str) -> Resource:
    parsed = urlparse(uri)
    if parsed.scheme != "file" or parsed.netloc:
        raise ValueError(f"Only local Write contract references are permitted: {uri}")
    source = Path(unquote(parsed.path)).resolve()
    if not source.is_relative_to(API) or source.is_relative_to(API / "legacy"):
        raise ValueError(
            f"Write contract reference leaves current API artifacts: {uri}"
        )
    value = load_document(source)
    return Resource.from_contents(value, default_specification=DRAFT202012)


def _schema_registry() -> Registry:
    registry = Registry(retrieve=_load_local)
    if not VENDOR.is_dir():
        return registry
    for path in sorted(VENDOR.rglob("*.json")):
        value = load_document(path)
        canonical_id = value.get("$id") if isinstance(value, dict) else None
        if isinstance(canonical_id, str):
            registry = registry.with_resource(
                canonical_id,
                Resource.from_contents(value, default_specification=DRAFT202012),
            )
    return registry


REGISTRY = _schema_registry()


class _OfflineOpenAPIHandler:
    def __call__(self, uri: str) -> Any:
        base_uri, _fragment = urldefrag(uri)
        parsed = urlparse(base_uri)
        if parsed.scheme == "file" and not parsed.netloc:
            path = Path(unquote(parsed.path)).resolve()
            if not path.is_relative_to(API) or path.is_relative_to(API / "legacy"):
                raise ValueError(
                    f"OpenAPI reference leaves current API artifacts: {uri}"
                )
            return load_document(path)
        if parsed.scheme in {"http", "https"}:
            for path in VENDOR.rglob("*.json"):
                value = load_document(path)
                if isinstance(value, dict) and value.get("$id") == base_uri:
                    return value
        raise ValueError(f"OpenAPI validation refuses unvendored reference: {uri}")


class _OfflineOpenAPIV31Validator(OpenAPIV31SpecValidator):
    _handler = _OfflineOpenAPIHandler()
    resolver_handlers = {
        "<all_urls>": _handler,
        "file": _handler,
        "http": _handler,
        "https": _handler,
    }


def validate_openapi(spec: dict[str, Any], base_uri: str = "") -> None:
    """Validate OpenAPI 3.1 while resolving only current local or vendored artifacts."""
    handlers = _OfflineOpenAPIV31Validator.resolver_handlers
    schema_path = SchemaPath.from_dict(
        spec,
        base_uri=base_uri,
        handlers=handlers,
    )
    _OfflineOpenAPIV31Validator(schema_path).validate()


def nodes(value: Any, pointer: str = "") -> Iterable[tuple[str, Any]]:
    if isinstance(value, dict):
        yield pointer, value
        for key, child in value.items():
            escaped = str(key).replace("~", "~0").replace("/", "~1")
            yield from nodes(child, pointer + "/" + escaped)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from nodes(child, pointer + "/" + str(index))


def resolve_ref(source: Path, reference: str) -> tuple[Path, Any]:
    """Resolve exactly one local JSON Reference and return its owning file."""
    uri, fragment = urldefrag(urljoin(source.resolve().as_uri(), reference))
    parsed = urlparse(uri)
    if parsed.scheme != "file" or parsed.netloc:
        raise ValueError(f"Reference is not local: {reference}")
    target = Path(unquote(parsed.path)).resolve()
    if not target.is_relative_to(API) or target.is_relative_to(API / "legacy"):
        raise ValueError(f"Reference leaves current API artifacts: {reference}")
    if not target.is_file():
        raise ValueError(f"Reference target does not exist: {reference}")
    value = load_document(target)
    if fragment:
        if not fragment.startswith("/"):
            raise ValueError(f"Reference fragment is not a JSON Pointer: {reference}")
        for token in fragment.lstrip("/").split("/"):
            key = token.replace("~1", "/").replace("~0", "~")
            try:
                value = value[int(key)] if isinstance(value, list) else value[key]
            except (KeyError, IndexError, TypeError, ValueError) as exc:
                raise ValueError(
                    f"Reference fragment does not resolve: {reference}"
                ) from exc
    return target, value


def resolve_object(source: Path, value: dict[str, Any]) -> tuple[Path, dict[str, Any]]:
    seen: set[tuple[Path, str]] = set()
    while isinstance(value, dict) and "$ref" in value:
        reference = value["$ref"]
        if not isinstance(reference, str):
            raise ValueError("JSON Reference must be a string")
        identity = (source.resolve(), reference)
        if identity in seen:
            raise ValueError(
                f"Cyclic reference does not resolve exactly once: {reference}"
            )
        seen.add(identity)
        source, value = resolve_ref(source, reference)
    if not isinstance(value, dict):
        raise ValueError("Reference must resolve to an object")
    return source, value


def operations(document: dict[str, Any]) -> Iterable[tuple[str, str, dict[str, Any]]]:
    for route, item in document.get("paths", {}).items():
        if not isinstance(item, dict):
            continue
        for method, operation in item.items():
            if method.lower() in HTTP_METHODS and isinstance(operation, dict):
                yield route, method.lower(), operation


def operation_by_id(source: Path, operation_id: str) -> tuple[str, str, dict[str, Any]]:
    matches = [
        entry
        for entry in operations(load_document(source))
        if entry[2].get("operationId") == operation_id
    ]
    if len(matches) != 1:
        raise ValueError(
            f"Expected exactly one operationId {operation_id!r} in {source.name}"
        )
    return matches[0]


def _absolute_refs(source: Path, value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: urljoin(source.resolve().as_uri(), child)
            if key == "$ref"
            else _absolute_refs(source, child)
            for key, child in value.items()
        }
    if isinstance(value, list):
        return [_absolute_refs(source, child) for child in value]
    return value


def validate_schema_value(source: Path, schema: dict[str, Any], value: Any) -> None:
    Draft202012Validator(
        _absolute_refs(source, schema),
        registry=REGISTRY,
        format_checker=FormatChecker(),
    ).validate(value)


def _parameter_entries(
    source: Path, operation: dict[str, Any]
) -> list[tuple[Path, dict[str, Any]]]:
    return [resolve_object(source, value) for value in operation.get("parameters", [])]


def _casefold_headers(headers: Any) -> dict[str, tuple[str, Any]]:
    if headers is None:
        return {}
    if not isinstance(headers, dict):
        raise ValueError("HTTP headers must be an object")
    folded: dict[str, tuple[str, Any]] = {}
    for name, value in headers.items():
        if not isinstance(name, str):
            raise ValueError("HTTP header names must be strings")
        key = name.casefold()
        if key in folded:
            raise ValueError(f"HTTP header is repeated with different casing: {name}")
        folded[key] = (name, value)
    return folded


def _select_media(
    content: dict[str, Any], requested: str | None, context: str
) -> tuple[str, dict[str, Any]]:
    if requested is not None:
        if requested not in content:
            raise ValueError(f"{context} uses undeclared media type {requested}")
        return requested, content[requested]
    if len(content) != 1:
        raise ValueError(
            f"{context} must name mediaType when the contract declares multiple representations"
        )
    return next(iter(content.items()))


def _path_parameters(route: str, supplied: Any) -> dict[str, str]:
    if isinstance(supplied, dict):
        return supplied
    if not isinstance(supplied, str):
        raise ValueError(
            "Request path must be a URI path string or path-parameter object"
        )
    names = re.findall(r"\{([^{}]+)\}", route)
    pattern = "^" + re.sub(r"\{[^{}]+\}", r"([^/]+)", route) + "$"
    match = re.fullmatch(pattern, urlparse(supplied).path)
    if match is None:
        raise ValueError(
            f"Request path {supplied} does not match operation route {route}"
        )
    return {
        name: unquote(value) for name, value in zip(names, match.groups(), strict=True)
    }


def validate_exchange(source: Path, exchange: dict[str, Any]) -> None:
    """Validate one illustrative exchange against its declared OpenAPI operation."""
    if not isinstance(exchange, dict):
        raise ValueError("Exchange must be an object")
    operation_id = exchange.get("operationId")
    if not isinstance(operation_id, str):
        raise ValueError("Exchange needs operationId")
    route, _method, operation = operation_by_id(source, operation_id)
    request = exchange.get("request", {})
    response = exchange.get("response")
    if not isinstance(request, dict) or not isinstance(response, dict):
        raise ValueError("Exchange request and response must be objects")
    status = response.get("status")
    if not isinstance(status, int):
        raise ValueError("Response status must be an integer")
    expected_request_failure = exchange.get("expectedRequestFailure")
    if expected_request_failure not in (
        None,
        "missing-required-header",
        "schema-validation",
    ):
        raise ValueError("Exchange names an unknown expectedRequestFailure")
    request_failures: list[str] = []

    declared: dict[tuple[str, str], tuple[Path, dict[str, Any]]] = {}
    for parameter_source, parameter in _parameter_entries(source, operation):
        location = parameter["in"]
        name = (
            parameter["name"].casefold() if location == "header" else parameter["name"]
        )
        declared[(location, name)] = (parameter_source, parameter)
    supplied_headers = _casefold_headers(request.get("headers"))
    content_type = supplied_headers.pop("content-type", (None, None))[1]
    supplied_headers.pop("accept", None)
    supplied = {
        "path": _path_parameters(route, request.get("path", {})),
        "query": request.get("query", {}),
        "header": {key: value for key, (_name, value) in supplied_headers.items()},
    }
    for location, values in supplied.items():
        if not isinstance(values, dict):
            raise ValueError(f"Request {location} parameters must be an object")
        for name, value in values.items():
            key = name.casefold() if location == "header" else name
            if (location, key) not in declared:
                raise ValueError(
                    f"Request supplies undeclared {location} parameter {name}"
                )
            parameter_source, parameter = declared[(location, key)]
            try:
                validate_schema_value(parameter_source, parameter["schema"], value)
            except ValidationError:
                request_failures.append(
                    f"parameter-validation:{location}:{parameter['name']}"
                )
    for (location, name), (_parameter_source, parameter) in declared.items():
        if parameter.get("required") and name not in supplied[location]:
            request_failures.append(f"missing-required:{location}:{parameter['name']}")

    request_body = operation.get("requestBody")
    if request_body is not None:
        body_source, request_body = resolve_object(source, request_body)
        if request_body.get("required") and "body" not in request:
            request_failures.append("missing-required-body")
        if "body" in request:
            requested_media = request.get("mediaType", content_type)
            _media_type, media = _select_media(
                request_body.get("content", {}), requested_media, "Request"
            )
            try:
                validate_schema_value(body_source, media["schema"], request["body"])
            except ValidationError:
                request_failures.append("schema-validation")
    elif "body" in request:
        raise ValueError("Request body is not declared by the operation")

    expected_failures = {
        None: [],
        "missing-required-header": ["missing-required:header:Idempotency-Key"],
        "schema-validation": ["schema-validation"],
    }[expected_request_failure]
    if request_failures != expected_failures:
        raise ValueError(
            f"Exchange request failures differ from expectation: {request_failures!r}"
        )
    expected_failure_status = {
        "missing-required-header": 400,
        "schema-validation": 422,
    }.get(expected_request_failure)
    if expected_failure_status is not None and status != expected_failure_status:
        raise ValueError(
            f"{expected_request_failure} exchange must use {expected_failure_status} response"
        )
    status_key = str(status)
    declared_response = operation.get("responses", {}).get(status_key)
    if declared_response is None:
        raise ValueError(f"Response status {status} is not declared by {operation_id}")
    response_source, declared_response = resolve_object(source, declared_response)
    declared_headers = {
        name.casefold(): (name, *resolve_object(response_source, header))
        for name, header in declared_response.get("headers", {}).items()
    }
    supplied_response_headers = _casefold_headers(response.get("headers"))
    for key, (name, value) in supplied_response_headers.items():
        if key not in declared_headers:
            raise ValueError(f"Response supplies undeclared header {name}")
        _declared_name, header_source, header = declared_headers[key]
        validate_schema_value(header_source, header["schema"], value)
    for key, (name, _header_source, header) in declared_headers.items():
        if header.get("required") and key not in supplied_response_headers:
            raise ValueError(f"Response omits required header {name}")
    content = declared_response.get("content", {})
    if "body" in response:
        if not content:
            raise ValueError(f"Bodyless {status} response contains a body")
        _media_type, media = _select_media(
            content, response.get("mediaType"), "Response"
        )
        validate_schema_value(response_source, media["schema"], response["body"])
    elif content and 200 <= status < 300:
        raise ValueError(f"Successful {status} response omits its declared body")

    review_state = {
        "approve": "approved",
        "reject": "rejected",
        "withdraw": "withdrawn",
    }.get(route.rsplit("/", 1)[-1])
    if review_state and 200 <= status < 300:
        body = response.get("body")
        if not isinstance(body, dict):
            raise ValueError("Review action success must return its decision state")
        if (
            body.get("reviewState") != review_state
            or body.get("applicationState") != "not-started"
        ):
            raise ValueError(
                "Review action response must remain a pure decision outcome"
            )
        if "result" in body or "error" in body:
            raise ValueError(
                "Review action response must not imply application success or failure"
            )

    for key in ("if-match", "idempotency-key"):
        if key not in supplied_headers:
            continue
        value = supplied_headers[key][1]
        if not isinstance(value, str) or not re.fullmatch(r'"[^"\r\n]+"', value):
            raise ValueError(f"{supplied_headers[key][0]} must be a quoted field value")
        if key == "if-match" and value.startswith('W/"'):
            raise ValueError("If-Match must carry a strong entity-tag")

    _validate_exchange_identity(exchange, supplied["path"])
    if 200 <= status < 300:
        validate_request_local_mappings(exchange, supplied["path"])


def _validate_exchange_identity(exchange: dict[str, Any], path: dict[str, Any]) -> None:
    request = exchange.get("request", {})
    body = request.get("body")
    if not isinstance(path, dict) or not isinstance(body, dict):
        return
    candidates = [body]
    target = body.get("target")
    if isinstance(target, dict):
        candidates.append(target)
    for key in ("registryId", "collectionId", "recordId"):
        if key not in path:
            continue
        for candidate in candidates:
            if key in candidate and candidate[key] != path[key]:
                raise ValueError(f"Exchange {key} does not match the request path")


def _request_local_values(
    value: Any,
) -> tuple[list[tuple[str, dict[str, Any]]], list[str]]:
    declarations: list[tuple[str, dict[str, Any]]] = []
    references: list[str] = []

    def visit(child: Any, key: str | None = None) -> None:
        if isinstance(child, dict):
            for child_key, grandchild in child.items():
                visit(grandchild, child_key)
        elif isinstance(child, list):
            for grandchild in child:
                visit(grandchild, key)
        elif isinstance(child, str) and child.startswith("urn:request-local:"):
            if key == "@id":
                return
            references.append(child)

    for _pointer, node in nodes(value):
        if not isinstance(node, dict):
            continue
        identifier = node.get("@id")
        if isinstance(identifier, str) and identifier.startswith("urn:request-local:"):
            declarations.append((identifier, node))
    visit(value)
    return declarations, references


def _declared_collection(value: dict[str, Any]) -> str | None:
    types = value.get("@type", [])
    if isinstance(types, str):
        types = [types]
    suffixes = {
        "https://publicschema.org/Household": "households",
        "https://publicschema.org/Person": "individuals",
        "https://publicschema.org/crvs/Birth": "birth-registrations",
    }
    matches = {
        collection
        for schema_type, collection in suffixes.items()
        if schema_type in types
    }
    if len(matches) > 1:
        raise ValueError(
            "A request-local object maps to conflicting Registry collections"
        )
    return next(iter(matches), None)


def validate_request_local_mappings(
    exchange: dict[str, Any], path: dict[str, Any]
) -> None:
    """Validate compound-create identities and their authoritative result mapping."""
    request_body = exchange.get("request", {}).get("body")
    response_body = exchange.get("response", {}).get("body")
    proposal = request_body if isinstance(request_body, dict) else response_body
    if not isinstance(proposal, dict):
        return
    request_input = proposal.get("input", proposal)
    declarations, references = _request_local_values(request_input)
    declared_ids = [identifier for identifier, _value in declarations]
    if len(declared_ids) != len(set(declared_ids)):
        raise ValueError(
            "A request-local identifier is declared by more than one creating object"
        )
    undeclared_references = set(references) - set(declared_ids)
    if undeclared_references:
        raise ValueError(
            "Request-local reference has no creating object: "
            + ", ".join(sorted(undeclared_references))
        )

    if not isinstance(response_body, dict):
        return
    result = response_body.get("result", response_body)
    if not isinstance(result, dict):
        return
    mappings = result.get("requestLocalReferences", [])
    if not isinstance(mappings, list):
        raise ValueError("requestLocalReferences must be a list")
    mapped_ids = [
        mapping.get("requestLocalId")
        for mapping in mappings
        if isinstance(mapping, dict)
    ]
    if len(mapped_ids) != len(mappings) or any(
        not isinstance(identifier, str) for identifier in mapped_ids
    ):
        raise ValueError("Every request-local result mapping needs requestLocalId")
    if len(mapped_ids) != len(set(mapped_ids)):
        raise ValueError("A request-local identifier is mapped more than once")
    if set(mapped_ids) - set(declared_ids):
        raise ValueError(
            "A result mapping names an undeclared request-local identifier"
        )

    applied = (
        response_body.get("applicationState") == "applied"
        if "applicationState" in response_body
        else True
    )
    if applied and set(mapped_ids) != set(declared_ids):
        raise ValueError(
            "Every created request-local object must resolve exactly once when applied"
        )
    if not applied:
        if mappings:
            raise ValueError(
                "Pending or non-applied requests must not publish result mappings"
            )
        return
    declaration_by_id = dict(declarations)
    for mapping in mappings:
        expected_collection = _declared_collection(
            declaration_by_id[mapping["requestLocalId"]]
        )
        if expected_collection and mapping.get("collectionId") != expected_collection:
            raise ValueError(
                "Request-local result collection does not match the created object type"
            )

    target = proposal.get("target", {})
    target_collection = path.get("collectionId", target.get("collectionId"))
    target_record = path.get("recordId", target.get("recordId"))
    if target_collection and result.get("collectionId") != target_collection:
        raise ValueError(
            "Primary Write result collection does not match the request target"
        )
    if target_record and result.get("recordId") != target_record:
        raise ValueError(
            "Primary transition result Record does not match the request target"
        )
    if proposal.get("kind") == "create" or (
        "recordId" not in path and "data" in proposal
    ):
        primary = [
            mapping
            for mapping in mappings
            if mapping.get("collectionId") == target_collection
        ]
        if primary and not any(
            mapping.get("recordId") == result.get("recordId") for mapping in primary
        ):
            raise ValueError(
                "Primary create result is cross-bound to another request-local object"
            )


def _schema_ref_name(value: Any) -> str | None:
    if isinstance(value, dict) and isinstance(value.get("$ref"), str):
        return urldefrag(value["$ref"])[1].rsplit("/", 1)[-1]
    return None


def _ref_identity(source: Path, value: Any) -> str | None:
    if not isinstance(value, dict) or not isinstance(value.get("$ref"), str):
        return None
    return urljoin(source.resolve().as_uri(), value["$ref"])


def _collect_property_schemas(
    source: Path, schema: dict[str, Any], name: str
) -> list[tuple[Path, dict[str, Any]]]:
    source, schema = resolve_object(source, schema)
    found: list[tuple[Path, dict[str, Any]]] = []
    if name in schema.get("properties", {}):
        found.append((source, schema["properties"][name]))
    for composition in ("allOf", "oneOf", "anyOf"):
        for branch in schema.get(composition, []):
            found.extend(_collect_property_schemas(source, branch, name))
    return found


def _referenced_property_identities(source: Path, schema: Any, name: str) -> list[str]:
    found: list[str] = []
    visited: set[str] = set()

    def visit(current_source: Path, value: Any) -> None:
        if isinstance(value, dict):
            if "$ref" in value:
                identity = _ref_identity(current_source, value)
                if identity in visited:
                    return
                visited.add(identity)
                target_source, target = resolve_ref(current_source, value["$ref"])
                visit(target_source, target)
                return
            properties = value.get("properties")
            if isinstance(properties, dict) and isinstance(properties.get(name), dict):
                identity = _ref_identity(current_source, properties[name])
                if identity is not None:
                    found.append(identity)
            for key, child in value.items():
                if key == "properties" and isinstance(child, dict):
                    for property_name, property_schema in child.items():
                        if property_name != name:
                            visit(current_source, property_schema)
                else:
                    visit(current_source, child)
        elif isinstance(value, list):
            for child in value:
                visit(current_source, child)

    visit(source, schema)
    return found


def _request_schema(
    source: Path, operation: dict[str, Any]
) -> tuple[Path, dict[str, Any], str]:
    body_source, body = resolve_object(source, operation["requestBody"])
    content = body.get("content", {})
    if len(content) != 1:
        raise ValueError(
            f"{operation['operationId']} must declare exactly one request media type"
        )
    media_type, media = next(iter(content.items()))
    return body_source, media["schema"], media_type


def _header_parameter(
    source: Path, operation: dict[str, Any], name: str
) -> tuple[Path, dict[str, Any]] | None:
    matches = [
        (parameter_source, parameter)
        for parameter_source, parameter in _parameter_entries(source, operation)
        if parameter.get("in") == "header"
        and str(parameter.get("name", "")).casefold() == name.casefold()
    ]
    if len(matches) > 1:
        raise ValueError(
            f"{operation['operationId']} repeats header {name} with different casing"
        )
    return matches[0] if matches else None


def validate_write_document(
    document: dict[str, Any],
    source: Path = WRITE,
    *,
    require_reference_surface: bool | None = None,
) -> None:
    """Validate cross-field Write invariants on one canonical-shaped document."""
    if require_reference_surface is None:
        require_reference_surface = source.resolve() == WRITE.resolve()
    operation_entries = list(operations(document))
    operation_ids = [
        operation.get("operationId") for _route, _method, operation in operation_entries
    ]
    missing_ids = (
        sorted(REFERENCE_REQUIRED_OPERATIONS - set(operation_ids))
        if require_reference_surface
        else []
    )
    if missing_ids:
        raise ValueError(f"Write contract omits operations: {', '.join(missing_ids)}")
    duplicates = [
        key for key, count in Counter(operation_ids).items() if key and count > 1
    ]
    if duplicates:
        raise ValueError(
            f"Write contract repeats operationId: {', '.join(sorted(duplicates))}"
        )

    extension_schema = load_document(WRITE_EXTENSION_SCHEMA)
    extension_validator = Draft202012Validator(
        extension_schema, format_checker=FormatChecker()
    )
    by_id = {
        operation["operationId"]: (route, method, operation)
        for route, method, operation in operation_entries
    }
    write_entries = [
        (operation["operationId"], route, method, operation)
        for route, method, operation in operation_entries
        if EXTENSION in operation
    ]
    for operation_id, _route, _method, operation in write_entries:
        if EXTENSION not in operation:
            raise ValueError(f"{operation_id} omits {EXTENSION}")
        extension_validator.validate(operation[EXTENSION])
        expected_capability = WRITE_OPERATIONS.get(operation_id)
        if (
            expected_capability
            and operation[EXTENSION].get("capability") != expected_capability
        ):
            raise ValueError(f"{operation_id} selects the wrong Write capability")

    for operation_id, route, _method, operation in write_entries:
        capability = operation[EXTENSION]["capability"]
        if capability not in {"create", "update", "transition"}:
            continue
        body_source, schema, media_type = _request_schema(source, operation)
        input_identity = _ref_identity(body_source, schema)
        if input_identity is None:
            raise ValueError(
                f"{operation_id} request body must use a referenced typed input schema"
            )
        canonical_input_name = DIRECT_INPUTS.get(operation_id)
        if (
            canonical_input_name
            and source.resolve() == WRITE.resolve()
            and _schema_ref_name(schema) != canonical_input_name
        ):
            raise ValueError(
                f"{operation_id} request body must reference {canonical_input_name}"
            )
        extension_input = operation[EXTENSION].get("inputSchema")
        if _ref_identity(source, {"$ref": extension_input}) != input_identity:
            raise ValueError(
                f"{operation_id} inputSchema must match its request body schema"
            )
        expected_media = (
            "application/merge-patch+json"
            if capability == "update"
            else "application/json"
        )
        if media_type != expected_media:
            raise ValueError(f"{operation_id} must use {expected_media}")
        if capability == "transition":
            action = operation[EXTENSION].get("action")
            if route.rsplit("/", 1)[-1] != action:
                raise ValueError(f"{operation_id} action must match its fixed path")
            if source.resolve() != WRITE.resolve():
                input_source, input_schema = resolve_object(body_source, schema)
                if _property_consts(input_source, input_schema, "name") != {action}:
                    raise ValueError(
                        f"{operation_id} input name must match its fixed action"
                    )

    submissions = [
        (operation_id, operation)
        for operation_id, route, method, operation in write_entries
        if operation[EXTENSION]["capability"] == "change-requests"
        and method == "post"
        and route.rstrip("/").endswith("/change-requests")
        and "requestBody" in operation
    ]
    if len(submissions) > 1:
        raise ValueError(
            "A Write profile must not declare multiple change-request submission operations"
        )
    if submissions:
        submission_operation_id, submission_operation = submissions[0]
        submission_source, submission_schema, submission_media = _request_schema(
            source, submission_operation
        )
        if submission_media != "application/json":
            raise ValueError(f"{submission_operation_id} must use application/json")
        submission_identity = _ref_identity(submission_source, submission_schema)
        if submission_identity is None:
            raise ValueError(
                "submitChangeRequest request body must use a referenced typed proposal schema"
            )
        submission_source, submission_schema = resolve_object(
            submission_source, submission_schema
        )
        governed_inputs = _referenced_property_identities(
            submission_source, submission_schema, "input"
        )
        if not governed_inputs:
            raise ValueError(
                "Change-request submission needs at least one typed input branch"
            )
        if require_reference_surface and len(set(governed_inputs)) != 3:
            raise ValueError(
                "Reference change requests need create, update, and transition inputs"
            )
        submission_extension_ref = submission_operation[EXTENSION].get("inputSchema")
        if (
            _ref_identity(source, {"$ref": submission_extension_ref})
            != submission_identity
        ):
            raise ValueError(
                "submitChangeRequest inputSchema must match its request body schema"
            )

    strong_preconditions = {
        operation_id
        for operation_id, route, _method, operation in write_entries
        if operation[EXTENSION]["capability"] in {"update", "transition"}
        or (
            operation[EXTENSION]["capability"] == "change-requests"
            and route.rsplit("/", 1)[-1] in {"approve", "reject", "withdraw"}
        )
    } | (STRONG_PRECONDITION_OPERATIONS & set(by_id))
    for operation_id in strong_preconditions:
        operation = by_id[operation_id][2]
        header = _header_parameter(source, operation, "If-Match")
        if header is None or not header[1].get("required"):
            raise ValueError(f"{operation_id} requires If-Match")
        header_source, header_value = header
        schema = header_value.get("schema", {})
        validator = Draft202012Validator(
            _absolute_refs(header_source, schema), registry=REGISTRY
        )
        for weak in (
            'W/"v1"',
            "*",
            '"unterminated',
            '"v1"\n',
            '"v\x001"',
            '"has space"',
            '"café"',
        ):
            if validator.is_valid(weak):
                raise ValueError(
                    f"{operation_id} If-Match schema accepts a weak or non-specific validator"
                )
        if not validator.is_valid('"v1"'):
            raise ValueError(
                f"{operation_id} If-Match schema rejects a strong entity-tag"
            )

    for operation_id, (_route, method, operation) in by_id.items():
        if method not in {"post", "put", "patch", "delete"}:
            continue
        idempotency = _header_parameter(source, operation, "Idempotency-Key")
        if idempotency is None or not idempotency[1].get("required"):
            raise ValueError(f"{operation_id} requires Idempotency-Key")
        header_source, header_value = idempotency
        idempotency_validator = Draft202012Validator(
            _absolute_refs(header_source, header_value.get("schema", {})),
            registry=REGISTRY,
        )
        if idempotency_validator.is_valid("unquoted-key"):
            raise ValueError(
                f"{operation_id} Idempotency-Key schema accepts an unquoted key"
            )
        if not idempotency_validator.is_valid('"quoted-key"'):
            raise ValueError(
                f"{operation_id} Idempotency-Key schema rejects a quoted key"
            )

    _validate_response_shapes(source, by_id)
    _validate_error_response_schemas(source, by_id)
    _validate_operation_scopes(document)
    _validate_client_fields(source, by_id)
    _validate_refs(source, document)


def _validate_response_shapes(
    source: Path, by_id: dict[str, tuple[str, str, dict[str, Any]]]
) -> None:
    for operation_id, (_route, _method, create) in by_id.items():
        extension = create.get(EXTENSION, {})
        if extension.get("capability") != "create":
            continue
        response_source, created = resolve_object(source, create["responses"]["201"])
        location = created.get("headers", {}).get("Location")
        if location is None or not resolve_object(response_source, location)[1].get(
            "required"
        ):
            raise ValueError(f"{operation_id} 201 requires Location")
    for operation_id, (_route, _method, operation) in by_id.items():
        for status, response in operation.get("responses", {}).items():
            response_source, response = resolve_object(source, response)
            if status == "204" and "content" in response:
                raise ValueError(f"{operation_id} 204 must be bodyless")
            if status == "202":
                operation_header = response.get("headers", {}).get("Location")
                if operation_header is None or not resolve_object(
                    response_source, operation_header
                )[1].get("required"):
                    raise ValueError(f"{operation_id} 202 requires Location")
            headers = {
                name.casefold(): resolve_object(response_source, value)[1]
                for name, value in response.get("headers", {}).items()
            }
            cache = headers.get("cache-control")
            if cache is None or not cache.get("required"):
                raise ValueError(f"{operation_id} {status} requires Cache-Control")
            cache_schema = cache.get("schema", {})
            if cache_schema.get("const") != "no-store" and cache_schema.get("enum") != [
                "no-store"
            ]:
                raise ValueError(
                    f"{operation_id} {status} Cache-Control must be no-store"
                )


def _property_consts(source: Path, schema: Any, property_name: str) -> set[Any]:
    found: set[Any] = set()
    visited: set[str] = set()

    def visit(current_source: Path, value: Any) -> None:
        if not isinstance(value, dict):
            return
        if "$ref" in value:
            identity = _ref_identity(current_source, value)
            if identity in visited:
                return
            visited.add(identity)
            target_source, target = resolve_ref(current_source, value["$ref"])
            visit(target_source, target)
            return
        properties = value.get("properties", {})
        if isinstance(properties, dict) and isinstance(
            properties.get(property_name), dict
        ):
            property_schema = properties[property_name]
            if "const" in property_schema:
                found.add(property_schema["const"])
        for composition in ("allOf", "oneOf", "anyOf"):
            for branch in value.get(composition, []):
                visit(current_source, branch)

    visit(source, schema)
    return found


def _validate_error_response_schemas(
    source: Path, by_id: dict[str, tuple[str, str, dict[str, Any]]]
) -> None:
    for operation_id, (_route, _method, operation) in by_id.items():
        for status, response in operation.get("responses", {}).items():
            if not status.startswith(("4", "5")):
                continue
            response_source, response = resolve_object(source, response)
            media = response.get("content", {}).get("application/problem+json")
            if not isinstance(media, dict) or not isinstance(media.get("schema"), dict):
                raise ValueError(
                    f"{operation_id} {status} must declare application/problem+json"
                )
            statuses = _property_consts(response_source, media["schema"], "status")
            if statuses != {int(status)}:
                raise ValueError(
                    f"{operation_id} {status} Problem must fix status to {status}"
                )
            problem_types = _property_consts(response_source, media["schema"], "type")
            if not problem_types or any(
                not isinstance(problem_type, str)
                or not problem_type.startswith("https://")
                for problem_type in problem_types
            ):
                raise ValueError(
                    f"{operation_id} {status} Problem must declare stable HTTPS type identifiers"
                )


def _validate_operation_scopes(document: dict[str, Any]) -> None:
    supporting_scopes = {
        "getWritableRecord": "bb:digital-registries:record:read",
        "listChangeRequests": "bb:digital-registries:change-request:read",
        "getChangeRequest": "bb:digital-registries:change-request:read",
        "approveChangeRequest": "bb:digital-registries:change-request:review",
        "rejectChangeRequest": "bb:digital-registries:change-request:review",
        "withdrawChangeRequest": "bb:digital-registries:change-request:withdraw",
        "getOperation": "bb:digital-registries:operation:read",
    }
    capability_scopes = {
        "create": "bb:digital-registries:record:create",
        "update": "bb:digital-registries:record:update",
        "transition": "bb:digital-registries:record:transition",
    }
    for route, method, operation in operations(document):
        operation_id = operation.get("operationId")
        expected = supporting_scopes.get(operation_id)
        extension = operation.get(EXTENSION, {})
        capability = extension.get("capability")
        if capability in capability_scopes:
            expected = capability_scopes[capability]
        elif capability == "change-requests":
            final_segment = route.rsplit("/", 1)[-1]
            if final_segment in {"approve", "reject"}:
                expected = "bb:digital-registries:change-request:review"
            elif final_segment == "withdraw":
                expected = "bb:digital-registries:change-request:withdraw"
            elif method == "post" and final_segment == "change-requests":
                expected = "bb:digital-registries:change-request:submit"
        elif method == "get" and route.startswith("/v1/change-requests"):
            expected = "bb:digital-registries:change-request:read"
        elif method == "get" and route.startswith("/v1/operations/"):
            expected = "bb:digital-registries:operation:read"
        if expected is None:
            continue
        security = operation.get("security")
        if not isinstance(security, list) or not security:
            raise ValueError(
                f"{operation_id} must declare its operation-specific OAuth scope"
            )
        alternatives = [
            scopes
            for requirement in security
            if isinstance(requirement, dict)
            for scopes in requirement.values()
        ]
        if not alternatives or any(scopes != [expected] for scopes in alternatives):
            raise ValueError(
                f"{operation_id} must require only its operation-specific scope {expected}"
            )


def _validate_client_fields(
    source: Path, by_id: dict[str, tuple[str, str, dict[str, Any]]]
) -> None:
    for operation_id, (_route, method, operation) in by_id.items():
        if (
            method not in {"post", "put", "patch", "delete"}
            or "requestBody" not in operation
        ):
            continue
        body_source, schema, _media = _request_schema(source, operation)
        _resolved_source, schema = resolve_object(body_source, schema)
        forbidden = {
            key
            for _pointer, node in nodes(schema)
            if isinstance(node, dict)
            for key in node.get("properties", {})
            if key in FORBIDDEN_CLIENT_FIELDS
        }
        if forbidden:
            raise ValueError(
                f"{operation_id} lets clients set authority-owned fields: {', '.join(sorted(forbidden))}"
            )


def _validate_refs(source: Path, document: Any) -> None:
    for pointer, node in nodes(document):
        if not isinstance(node, dict):
            continue
        if "$ref" in node:
            resolve_ref(source, node["$ref"])
        for composition in ("oneOf", "anyOf", "allOf"):
            references = [
                branch.get("$ref")
                for branch in node.get(composition, [])
                if isinstance(branch, dict) and "$ref" in branch
            ]
            if len(references) != len(set(references)):
                raise ValueError(
                    f"{pointer}/{composition} repeats a local schema reference"
                )


def validate_example_schema(path: Path = EXAMPLE_SCHEMA) -> None:
    schema = load_document(path)
    Draft202012Validator.check_schema(schema)
    _validate_refs(path, schema)


def validate_vendor_provenance() -> None:
    provenance = VENDOR_PROVENANCE.read_text()
    rows = re.findall(
        r"^\| `([^`]+\.schema\.json)` \| `([^`]+)` \| `([0-9a-f]{64})` \|$",
        provenance,
        flags=re.MULTILINE,
    )
    geometry_file = re.search(
        r"^- Local file: `([^`]+\.schema\.json)`$", provenance, re.MULTILINE
    )
    geometry_uri = re.search(r"^- Canonical URL: `([^`]+)`$", provenance, re.MULTILINE)
    geometry_hash = re.search(
        r"^- SHA-256: `([0-9a-f]{64})`$", provenance, re.MULTILINE
    )
    if not rows or not geometry_file or not geometry_uri or not geometry_hash:
        raise ValueError("Vendored schema provenance is incomplete")
    expected = {
        relative: (canonical_id, digest) for relative, canonical_id, digest in rows
    }
    expected[geometry_file.group(1)] = (geometry_uri.group(1), geometry_hash.group(1))
    actual_files = {
        path.relative_to(VENDOR).as_posix()
        for path in VENDOR.rglob("*.schema.json")
        if not path.is_relative_to(VENDOR / "offline")
    }
    if set(expected) != actual_files:
        raise ValueError(
            "Vendored schema provenance does not cover the exact schema closure"
        )
    for relative, (canonical_id, digest) in expected.items():
        path = VENDOR / relative
        actual_digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual_digest != digest:
            raise ValueError(
                f"Vendored schema hash differs from provenance: {relative}"
            )
        schema = load_document(path)
        if schema.get("$id") != canonical_id:
            raise ValueError(
                f"Vendored schema canonical $id differs from provenance: {relative}"
            )

    mirror_root = VENDOR / "offline"
    mirror_files = {
        path.relative_to(mirror_root).as_posix()
        for path in mirror_root.rglob("*.schema.json")
    }
    if mirror_files != set(expected):
        raise ValueError(
            "Generated offline mirror does not cover the exact raw schema closure"
        )
    canonical_targets = {
        canonical_id: PurePosixPath(relative)
        for relative, (canonical_id, _digest) in expected.items()
    }

    def mirrored(value: Any, current: PurePosixPath) -> Any:
        if isinstance(value, dict):
            result = {}
            for key, child in value.items():
                if key == "$id":
                    continue
                if key == "$ref" and isinstance(child, str):
                    base, separator, fragment = child.partition("#")
                    if base in canonical_targets:
                        relative = posixpath.relpath(
                            str(canonical_targets[base]), str(current.parent)
                        )
                        if not relative.startswith("."):
                            relative = "./" + relative
                        result[key] = relative + ("#" + fragment if separator else "")
                        continue
                result[key] = mirrored(child, current)
            return result
        if isinstance(value, list):
            return [mirrored(child, current) for child in value]
        return value

    for relative in sorted(expected):
        raw = load_document(VENDOR / relative)
        mirror = load_document(mirror_root / relative)
        if mirror != mirrored(raw, PurePosixPath(relative)):
            raise ValueError(
                f"Generated offline mirror differs beyond $id/$ref transport rewriting: {relative}"
            )


def validate_write_coverage(
    coverage: dict[str, Any] | None = None,
    contract: dict[str, Any] | None = None,
) -> None:
    coverage = load_document(WRITE_COVERAGE) if coverage is None else coverage
    contract = load_document(WRITE) if contract is None else contract
    if coverage.get("contract") != WRITE.name:
        raise ValueError("Write coverage must name the canonical Write contract")
    contract_operations = {
        operation["operationId"]: (route, method, operation)
        for route, method, operation in operations(contract)
    }
    capability_entries = coverage.get("capabilities")
    if not isinstance(capability_entries, list):
        raise ValueError("Write coverage capabilities must be a list")
    expected_capability_keys = {
        "write-create",
        "write-update",
        "write-transition",
        "write-change-requests",
    }
    if {entry.get("key") for entry in capability_entries} != expected_capability_keys:
        raise ValueError(
            "Write coverage must map each independently selectable capability once"
        )
    for entry in capability_entries:
        operation_id = entry.get("operationId")
        if operation_id not in contract_operations:
            raise ValueError(f"Write coverage names unknown operation {operation_id}")
        route, method, operation = contract_operations[operation_id]
        if (entry.get("path"), entry.get("method")) != (route, method):
            raise ValueError(f"Write coverage route differs for {operation_id}")
        if entry.get("metadataCapability") != operation[EXTENSION]["capability"]:
            raise ValueError(f"Write coverage capability differs for {operation_id}")

    requirements = coverage.get("draftRequirements")
    if not isinstance(requirements, list):
        raise ValueError("Write coverage draftRequirements must be a list")
    expected_keys = {f"write-{index}" for index in range(1, 20)}
    keys = [entry.get("key") for entry in requirements]
    if len(keys) != len(set(keys)) or set(keys) != expected_keys:
        raise ValueError(
            "Write coverage must contain each write-1 through write-19 key exactly once"
        )
    testing_page = (ROOT / "resources/write-testing.md").read_text()
    dispositions = set(coverage.get("dispositions", {}))
    for entry in requirements:
        key = entry["key"]
        if entry.get("test") != f"resources/write-testing.md#{key}":
            raise ValueError(f"Write coverage test target differs for {key}")
        if f'id="{key}"' not in testing_page:
            raise ValueError(f"Write testing page omits anchor {key}")
        disposition = entry.get("disposition")
        if disposition not in dispositions:
            raise ValueError(f"Write coverage uses unknown disposition for {key}")
        declared_operations = entry.get("operations", [])
        if disposition == "operation" and not declared_operations:
            raise ValueError(f"Operation disposition needs operations for {key}")
        if any(
            operation_id not in contract_operations
            for operation_id in declared_operations
        ):
            raise ValueError(f"Write coverage names an unknown operation for {key}")
        if disposition == "review" and not entry.get("rationale"):
            raise ValueError(f"Review disposition needs a rationale for {key}")


def exchange_items() -> list[dict[str, Any]]:
    value = load_document(EXCHANGES)
    if isinstance(value, dict):
        value = value.get("exchanges")
    if not isinstance(value, list) or not value:
        raise ValueError("write-exchanges.json must contain a non-empty exchanges list")
    if any(not isinstance(item, dict) for item in value):
        raise ValueError("Every Write exchange must be an object")
    names = [item.get("name") for item in value]
    if any(not isinstance(name, str) or not name for name in names):
        raise ValueError("Every Write exchange needs a name")
    if len(names) != len(set(names)):
        raise ValueError("Write exchange names must be unique")
    return value


def contract_fixture_items() -> list[dict[str, Any]]:
    value = load_document(CONTRACT_FIXTURES)
    if not isinstance(value, dict):
        raise ValueError("write-contract-fixtures.json must be an object")
    fixtures = value.get("fixtures")
    if not isinstance(fixtures, list) or not fixtures:
        raise ValueError(
            "write-contract-fixtures.json must contain a non-empty fixtures list"
        )
    if any(not isinstance(item, dict) for item in fixtures):
        raise ValueError("Every canonical Write fixture must be an object")
    names = [item.get("name") for item in fixtures]
    if any(not isinstance(name, str) or not name for name in names):
        raise ValueError("Every canonical Write fixture needs a name")
    if len(names) != len(set(names)):
        raise ValueError("Canonical Write fixture names must be unique")
    return fixtures


def validate_contract_fixture(fixture: dict[str, Any]) -> None:
    has_operation = "operationId" in fixture
    has_schema_value = "schema" in fixture or "value" in fixture
    if has_operation == has_schema_value:
        raise ValueError(
            "Canonical Write fixture must declare either an operation or schema/value"
        )
    if has_operation:
        validate_exchange(WRITE, fixture)
        return
    schema = fixture.get("schema")
    if not isinstance(schema, str) or not schema.startswith("#/"):
        raise ValueError("Canonical schema/value fixture needs a local schema pointer")
    if "value" not in fixture:
        raise ValueError("Canonical schema/value fixture needs a value")
    validate_schema_value(WRITE, {"$ref": schema}, fixture["value"])


def validate_example_coverage(exchanges: list[dict[str, Any]]) -> None:
    names = {exchange["name"].lower() for exchange in exchanges}
    required_scenarios = {
        "birth declaration direct": ("birth", "declaration", "direct"),
        "birth declaration governed": ("birth", "declaration", "approval"),
        "birth correction direct": ("birth", "correction", "direct"),
        "birth correction governed": ("birth", "correction", "approval"),
        "household existing-person create direct": ("household", "existing", "direct"),
        "household existing-person create governed": (
            "household",
            "existing",
            "approval",
        ),
        "household compound create direct": ("household", "compound", "direct"),
        "household compound create governed": ("household", "compound", "approval"),
        "household add-existing direct": ("household", "addexisting", "direct"),
        "household add-existing governed": ("household", "addexisting", "approval"),
        "household add-new direct": ("household", "addnew", "direct"),
        "household add-new governed": ("household", "addnew", "approval"),
    }
    for label, fragments in required_scenarios.items():
        if not any(all(fragment in name for fragment in fragments) for name in names):
            raise ValueError(f"Write exchanges omit {label}")
    if not any(
        exchange.get("response", {}).get("status") == 204 for exchange in exchanges
    ):
        raise ValueError("Write exchanges omit a direct update 204 case")
    outcomes = {
        outcome
        for name in names
        for outcome in ("pending", "applied", "rejected", "blocked")
        if outcome in name
    }
    if not {"pending", "applied"} <= outcomes:
        raise ValueError(
            "Write exchanges must distinguish pending and applied outcomes"
        )


def validate_all() -> None:
    required = (
        WRITE,
        WRITE_EXTENSION_SCHEMA,
        WRITE_COVERAGE,
        EXAMPLE_API,
        EXAMPLE_SCHEMA,
        EXCHANGES,
        CONTRACT_FIXTURES,
        VENDOR,
    )
    missing = [str(path.relative_to(ROOT)) for path in required if not path.exists()]
    if missing:
        raise ValueError(f"Required Write artifact is missing: {', '.join(missing)}")
    canonical = load_document(WRITE)
    example_api = load_document(EXAMPLE_API)
    validate_openapi(canonical, base_uri=WRITE.as_uri())
    validate_openapi(example_api, base_uri=EXAMPLE_API.as_uri())
    validate_write_document(canonical, WRITE)
    validate_write_document(example_api, EXAMPLE_API)
    validate_example_schema()
    validate_vendor_provenance()
    validate_write_coverage()
    exchanges = exchange_items()
    for exchange in exchanges:
        validate_exchange(EXAMPLE_API, exchange)
    validate_example_coverage(exchanges)
    for fixture in contract_fixture_items():
        validate_contract_fixture(fixture)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args(argv)
    try:
        validate_all()
    except Exception as exc:  # The CLI reports the precise validation failure.
        print(f"ERROR: {exc}")
        return 1
    print(
        "Write contract artifacts are valid; deployed Write behavior was not exercised."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
