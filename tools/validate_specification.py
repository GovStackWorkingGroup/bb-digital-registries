#!/usr/bin/env python3
"""Validate the GovStack specification repository structure and traceability.

This validator checks the concrete repository format used by Digital Registries.
It is deliberately not a general specification compiler or a conformance test.
In particular, structurally valid DRAFT requirements do not establish solution
conformance.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from pathlib import Path
import re
import sys
from typing import Any, Iterable
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET

import yaml


LIFECYCLE = {"DRAFT", "WITHDRAWN", "CANDIDATE", "ACCEPTED", "PUBLISHED", "DEPRECATED"}
UNNUMBERED = {"DRAFT", "CANDIDATE"}
NUMBERED = {"ACCEPTED", "PUBLISHED", "DEPRECATED"}
LEVELS = {"REQUIRED", "RECOMMENDED"}
OBSERVABILITY = {"OBSERVABLE", "AUDITABLE"}
MUTABILITY = {"IMMUTABLE", "EXTENSIBLE", "REPLACEABLE", "INAPPLICABLE"}
INTERACTIONS = {
    "SERVICE_API",
    "CONSUMED_API",
    "PROTOCOL",
    "EVENT",
    "USER_INTERFACE",
    "DEVICE",
    "FILE",
    "INTERNAL",
}
FUNCTIONALITY_FIELDS = {"title", "description", "realises", "conformance", "requirements"}
FUNCTIONALITY_OPTIONAL_FIELDS = {"extension", "applies_when", "applies_when_all"}
REQUIREMENT_FIELDS = {"id", "status", "level", "observability", "mutability", "interaction", "statement"}
VARIATION_FIELDS = {"id", "status", "level", "observability", "mutability", "key", "select", "statement"}
OPTION_FIELDS = {"id", "status", "observability", "mutability", "interaction", "key", "option_of", "statement", "test"}
COMMON_OPTIONAL_FIELDS = {"documentation", "api_operation_id", "contract", "test", "applies_when", "applies_when_all"}
FORBIDDEN_VARIATION_FIELDS = {"interaction", "api_operation_id", "contract", "test", "option_of"}
ACTIVE_MARKDOWN_EXCLUSIONS = {".git", ".venv", "node_modules"}
RAW_MARKDOWN_SNAPSHOTS = {
    "resources/history/navigation.md",
    "resources/history/repository-readme.md",
    "resources/history/requirements.md",
}
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\((?P<target>[^)\s]+)(?:\s+['\"][^)]*['\"])?\)")
EXPLICIT_ANCHOR = re.compile(r"<(?:a\s+[^>]*?(?:id|name)|[^>]+\s+id)=[\"']([^\"']+)[\"']", re.IGNORECASE)
HEADING = re.compile(r"^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$", re.MULTILINE)
LEGACY_ID = re.compile(r"govstack-bb-digital-registries-fr-(?:core|consultation)#req-\d+")
LOCAL_REQUIREMENT_ID = re.compile(r"[1-9]\d*")
SEMVER = re.compile(
    r"(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
)


def describe(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return str(path)


def load_yaml(path: Path, root: Path, errors: list[str]) -> Any | None:
    if not path.is_file():
        errors.append(f"{describe(path, root)}: required file is missing")
        return None
    try:
        return yaml.safe_load(path.read_text())
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        errors.append(f"{describe(path, root)}: invalid YAML: {exc}")
        return None


def load_functionality(path: Path, root: Path, errors: list[str]) -> tuple[dict[str, Any] | None, str]:
    try:
        text = path.read_text()
    except (OSError, UnicodeError) as exc:
        errors.append(f"{describe(path, root)}: cannot be read: {exc}")
        return None, ""
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        errors.append(f"{describe(path, root)}: YAML front matter must start with ---")
        return None, text
    end = next((index for index, line in enumerate(lines[1:], 1) if line.strip() == "---"), None)
    if end is None:
        errors.append(f"{describe(path, root)}: YAML front matter has no closing ---")
        return None, text
    try:
        data = yaml.safe_load("".join(lines[1:end]))
    except yaml.YAMLError as exc:
        errors.append(f"{describe(path, root)}: invalid YAML front matter: {exc}")
        return None, "".join(lines[end + 1 :])
    if not isinstance(data, dict):
        errors.append(f"{describe(path, root)}: YAML front matter must be a mapping")
        return None, "".join(lines[end + 1 :])
    return data, "".join(lines[end + 1 :])


def require_nonempty_string(mapping: dict[str, Any], field: str, location: str, errors: list[str]) -> bool:
    if field not in mapping:
        errors.append(f"{location}: missing required field {field}")
        return False
    value = mapping[field]
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{location}: {field} must be a non-empty string")
        return False
    return True


def require_list(mapping: dict[str, Any], field: str, location: str, errors: list[str], *, nonempty: bool = False) -> list[Any]:
    if field not in mapping:
        errors.append(f"{location}: missing required field {field}")
        return []
    value = mapping[field]
    if not isinstance(value, list):
        errors.append(f"{location}: {field} must be a list")
        return []
    if nonempty and not value:
        errors.append(f"{location}: {field} must contain at least one value")
    return value


def scalar_ids(items: Any, kind: str, location: str, errors: list[str]) -> tuple[dict[str, dict[str, Any]], set[str]]:
    result: dict[str, dict[str, Any]] = {}
    duplicates: set[str] = set()
    if not isinstance(items, list):
        errors.append(f"{location}: {kind} must be a list")
        return result, duplicates
    for index, item in enumerate(items):
        item_location = f"{location}:{kind}[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{item_location}: entry must be a mapping")
            continue
        for field in ("id", "title", "description"):
            require_nonempty_string(item, field, item_location, errors)
        identifier = item.get("id")
        if not isinstance(identifier, str) or not identifier:
            continue
        if identifier in result:
            duplicates.add(identifier)
        result[identifier] = item
    for identifier in sorted(duplicates):
        errors.append(f"{location}: duplicate {kind[:-1]} id {identifier}")
    return result, duplicates


def validate_root_documents(root: Path, errors: list[str]) -> tuple[dict[str, Any], dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    metadata_raw = load_yaml(root / "metadata.yml", root, errors)
    authors_raw = load_yaml(root / "authors.yml", root, errors)
    toc_raw = load_yaml(root / "toc.yml", root, errors)
    metadata = metadata_raw if isinstance(metadata_raw, dict) else {}
    if metadata_raw is not None and not isinstance(metadata_raw, dict):
        errors.append("metadata.yml: root must be a mapping")
    for field in ("name", "abstract", "url", "repository", "urn", "owner_group"):
        require_nonempty_string(metadata, field, "metadata.yml", errors)
    capabilities, _ = scalar_ids(metadata.get("capabilities"), "capabilities", "metadata.yml", errors)
    extensions_raw = metadata.get("extensions", [])
    extensions, _ = scalar_ids(extensions_raw, "extensions", "metadata.yml", errors)
    versions = metadata.get("versions")
    if not isinstance(versions, list) or not versions:
        errors.append("metadata.yml: versions must be a non-empty list")
    else:
        latest_count = 0
        for index, version in enumerate(versions):
            location = f"metadata.yml:versions[{index}]"
            if not isinstance(version, dict):
                errors.append(f"{location}: version entry must be a mapping")
                continue
            value = version.get("version")
            if not isinstance(value, str) or SEMVER.fullmatch(value) is None:
                errors.append(f"{location}: version must be a three-part SemVer string")
            if version.get("latest") is True:
                latest_count += 1
            elif version.get("latest") not in (False, None):
                errors.append(f"{location}: latest must be a boolean")
        if latest_count != 1:
            errors.append("metadata.yml: versions must declare exactly one latest version")
    if authors_raw is not None:
        if not isinstance(authors_raw, dict) or not isinstance(authors_raw.get("authors"), list) or not authors_raw["authors"]:
            errors.append("authors.yml: authors must be a non-empty list")
        else:
            for index, author in enumerate(authors_raw["authors"]):
                location = f"authors.yml:authors[{index}]"
                if not isinstance(author, dict):
                    errors.append(f"{location}: author must be a mapping")
                    continue
                require_nonempty_string(author, "name", location, errors)
                roles = author.get("roles")
                if (
                    not isinstance(roles, list)
                    or not roles
                    or any(not isinstance(role, str) or not role for role in roles)
                ):
                    errors.append(f"{location}: roles must be a non-empty list of strings")
                urn = author.get("urn")
                if not isinstance(urn, str) or not urn.startswith("govstack:person:") or urn == "govstack:person:":
                    errors.append(f"{location}: urn must be a govstack:person identifier")
    if toc_raw is not None:
        if not isinstance(toc_raw, dict) or not isinstance(toc_raw.get("toc"), dict):
            errors.append("toc.yml: toc must be a mapping")
        else:
            for section, directory in (
                ("introduction", root / "introduction"),
                ("requirements", root / "requirements"),
                ("resources", root / "resources"),
            ):
                entries = toc_raw["toc"].get(section)
                if not isinstance(entries, list) or not entries:
                    errors.append(f"toc.yml: {section} must be a non-empty list")
                    continue
                for index, entry in enumerate(entries):
                    if not isinstance(entry, str) or not entry:
                        errors.append(f"toc.yml:{section}[{index}]: entry must be a non-empty path")
                        continue
                    target = directory / entry
                    try:
                        target.relative_to(directory)
                    except ValueError:
                        errors.append(f"toc.yml:{section}[{index}]: path leaves {section}/: {entry}")
                        continue
                    if Path(entry).is_absolute() or ".." in Path(entry).parts:
                        errors.append(f"toc.yml:{section}[{index}]: path leaves {section}/: {entry}")
                        continue
                    if not target.exists():
                        errors.append(f"toc.yml:{section}[{index}]: referenced path does not exist: {section}/{entry}")
    return metadata, capabilities, extensions


def validate_extension_dependencies(extensions: dict[str, dict[str, Any]], errors: list[str]) -> None:
    graph: dict[str, list[str]] = {}
    for identifier, extension in extensions.items():
        requires = extension.get("requires", [])
        if not isinstance(requires, list) or any(not isinstance(value, str) for value in requires):
            errors.append(f"metadata.yml: extension {identifier} requires must be a list of extension ids")
            requires = []
        graph[identifier] = requires
        for dependency in requires:
            if dependency not in extensions:
                errors.append(f"metadata.yml: extension {identifier} requires undeclared extension {dependency}")

    visiting: list[str] = []
    visited: set[str] = set()

    def visit(identifier: str) -> None:
        if identifier in visiting:
            cycle = visiting[visiting.index(identifier) :] + [identifier]
            errors.append(f"metadata.yml: extension dependency cycle: {' -> '.join(cycle)}")
            return
        if identifier in visited:
            return
        visiting.append(identifier)
        for dependency in graph.get(identifier, []):
            if dependency in graph:
                visit(dependency)
        visiting.pop()
        visited.add(identifier)

    for identifier in sorted(graph):
        visit(identifier)


def operation_ids(root: Path, errors: list[str]) -> set[str]:
    api_path = root / "resources/api.yml"
    canonical_path = root / "api/openapi.yaml"
    if canonical_path.exists():
        expected_target = Path("../api/openapi.yaml")
        if not api_path.is_symlink():
            errors.append(
                "resources/api.yml: must be a symlink to ../api/openapi.yaml when api/openapi.yaml exists"
            )
        else:
            try:
                target = api_path.readlink()
            except OSError as exc:
                errors.append(f"resources/api.yml: cannot read symlink target: {exc}")
            else:
                if target != expected_target:
                    errors.append(
                        f"resources/api.yml: symlink target must be {expected_target}, found {target}"
                    )
                try:
                    same_file = api_path.samefile(canonical_path)
                except OSError:
                    same_file = False
                if not same_file:
                    errors.append("resources/api.yml: symlink must resolve to the canonical api/openapi.yaml file")
    document = load_yaml(api_path, root, errors)
    if not isinstance(document, dict):
        if document is not None:
            errors.append("resources/api.yml: OpenAPI document must be a mapping")
        return set()
    if not isinstance(document.get("paths"), dict):
        errors.append("resources/api.yml: OpenAPI document must contain a paths mapping")
        return set()
    operations: list[str] = []
    for path_name, path_item in document["paths"].items():
        if not isinstance(path_item, dict):
            continue
        for method, operation in path_item.items():
            if method.lower() not in {"get", "put", "post", "delete", "options", "head", "patch", "trace"}:
                continue
            if isinstance(operation, dict) and isinstance(operation.get("operationId"), str):
                operations.append(operation["operationId"])
    for duplicate, count in sorted(Counter(operations).items()):
        if count > 1:
            errors.append(f"resources/api.yml: duplicate operationId {duplicate}")

    index_path = root / "api/index.yaml"
    if index_path.is_file():
        index = load_yaml(index_path, root, errors)
        scalars: list[str] = []

        def collect(value: Any) -> None:
            if isinstance(value, dict):
                for child in value.values():
                    collect(child)
            elif isinstance(value, list):
                for child in value:
                    collect(child)
            elif isinstance(value, str):
                scalars.append(value)

        collect(index)
        canonical = canonical_path.resolve()
        references_canonical = False
        for value in scalars:
            if urlsplit(value).scheme:
                continue
            candidate = (root / value.split("#", 1)[0]).resolve()
            if candidate == canonical:
                references_canonical = True
                break
        if not references_canonical:
            errors.append("api/index.yaml: inventory must reference api/openapi.yaml")
    return set(operations)


def requirement_label(path: Path, root: Path, index: int) -> str:
    return f"{describe(path, root)}:requirements[{index}]"


def validate_enum(item: dict[str, Any], field: str, allowed: set[str], location: str, errors: list[str]) -> None:
    if field not in item:
        errors.append(f"{location}: missing required field {field}")
    elif not isinstance(item[field], str) or item[field] not in allowed:
        errors.append(f"{location}: {field} must be one of {', '.join(sorted(allowed))}")


def validate_lifecycle(item: dict[str, Any], location: str, errors: list[str]) -> None:
    if "id" not in item:
        errors.append(f"{location}: missing required field id")
    validate_enum(item, "status", LIFECYCLE, location, errors)
    status = item.get("status")
    identifier = item.get("id")
    if isinstance(status, str) and status in UNNUMBERED and identifier not in (None, ""):
        errors.append(f"{location}: {status} requirement id must be empty")
    if isinstance(status, str) and status in NUMBERED:
        if not isinstance(identifier, str) or LOCAL_REQUIREMENT_ID.fullmatch(identifier) is None:
            errors.append(f"{location}: {status} requirement id must be a positive local number")
    if status == "WITHDRAWN" and identifier not in (None, ""):
        if not isinstance(identifier, str) or LOCAL_REQUIREMENT_ID.fullmatch(identifier) is None:
            errors.append(f"{location}: numbered WITHDRAWN requirement id must be a positive local number")


def split_local_reference(reference: str) -> tuple[str, str]:
    path, separator, fragment = reference.partition("#")
    return unquote(path), unquote(fragment) if separator else ""


def github_slug(heading: str) -> str:
    heading = re.sub(r"<[^>]+>", "", heading)
    heading = heading.strip().lower()
    heading = re.sub(r"[^\w\- ]", "", heading, flags=re.UNICODE)
    return re.sub(r"[\s-]+", "-", heading).strip("-")


def markdown_anchors(path: Path) -> set[str]:
    try:
        text = path.read_text()
    except (OSError, UnicodeError):
        return set()
    anchors = set(EXPLICIT_ANCHOR.findall(text))
    counts: defaultdict[str, int] = defaultdict(int)
    for heading in HEADING.findall(text):
        base = github_slug(heading)
        if not base:
            continue
        suffix = counts[base]
        counts[base] += 1
        anchors.add(base if suffix == 0 else f"{base}-{suffix}")
    return anchors


def validate_local_reference(root: Path, reference: Any, location: str, errors: list[str]) -> None:
    if not isinstance(reference, str) or not reference.strip():
        errors.append(f"{location}: reference must be a non-empty string")
        return
    parsed = urlsplit(reference)
    if parsed.scheme or parsed.netloc:
        return
    relative, anchor = split_local_reference(reference)
    if not relative:
        errors.append(f"{location}: repository reference must include a file path")
        return
    target = (root / relative).resolve()
    try:
        target.relative_to(root.resolve())
    except ValueError:
        errors.append(f"{location}: reference leaves repository: {reference}")
        return
    if not target.is_file():
        errors.append(f"{location}: referenced file does not exist: {reference}")
        return
    if anchor and target.suffix.lower() == ".md" and anchor not in markdown_anchors(target):
        errors.append(f"{location}: referenced Markdown anchor does not exist: {reference}")


def validate_functionalities(
    root: Path,
    metadata: dict[str, Any],
    capabilities: dict[str, dict[str, Any]],
    extensions: dict[str, dict[str, Any]],
    errors: list[str],
) -> tuple[dict[str, list[dict[str, Any]]], set[str]]:
    requirement_dir = root / "requirements"
    files = sorted(requirement_dir.glob("*.md")) if requirement_dir.is_dir() else []
    if not files:
        errors.append("requirements/: at least one functionality Markdown file is required")
        return {}, set()
    realised_capabilities: set[str] = set()
    realised_extensions: set[str] = set()
    core_count = 0
    all_requirements: dict[str, list[dict[str, Any]]] = {}
    all_keys: list[tuple[str, str, str]] = []
    variation_keys: set[str] = set()
    option_keys: set[str] = set()
    variation_selects: dict[str, tuple[dict[str, Any], str]] = {}
    option_parents: Counter[str] = Counter()
    numbered_ids: list[tuple[str, str]] = []
    functionality_conditions: list[tuple[str, str, list[Any]]] = []
    contract_operations: dict[Path, set[str] | None] = {}

    def operations_for_contract(
        reference: Any, location: str
    ) -> tuple[set[str] | None, str]:
        if not isinstance(reference, str) or not reference.strip():
            errors.append(
                f"{location}: SERVICE_API requirement needs an explicit repository-local contract"
            )
            return None, "declared contract"
        parsed = urlsplit(reference)
        relative, anchor = split_local_reference(reference)
        if parsed.scheme or parsed.netloc or not relative or anchor:
            errors.append(
                f"{location}: SERVICE_API contract must be an explicit repository-local OpenAPI path"
            )
            return None, reference
        target = (root / relative).resolve()
        try:
            target.relative_to(root.resolve())
        except ValueError:
            errors.append(
                f"{location}: SERVICE_API contract must be an explicit repository-local OpenAPI path"
            )
            return None, reference
        if target in contract_operations:
            return contract_operations[target], reference
        document = load_yaml(target, root, errors)
        if not isinstance(document, dict):
            if document is not None:
                errors.append(
                    f"{location}: declared contract must be an OpenAPI mapping: {reference}"
                )
            contract_operations[target] = None
            return None, reference
        paths = document.get("paths")
        if not isinstance(paths, dict):
            errors.append(
                f"{location}: declared contract must contain an OpenAPI paths mapping: {reference}"
            )
            contract_operations[target] = None
            return None, reference
        found = [
            operation["operationId"]
            for path_item in paths.values()
            if isinstance(path_item, dict)
            for method, operation in path_item.items()
            if method.lower()
            in {"get", "put", "post", "delete", "options", "head", "patch", "trace"}
            and isinstance(operation, dict)
            and isinstance(operation.get("operationId"), str)
        ]
        for duplicate, count in sorted(Counter(found).items()):
            if count > 1:
                errors.append(f"{reference}: duplicate operationId {duplicate}")
        contract_operations[target] = set(found)
        return contract_operations[target], reference


    for path in files:
        data, _body = load_functionality(path, root, errors)
        if data is None:
            continue
        relative = describe(path, root)
        all_requirements[relative] = []
        for field in FUNCTIONALITY_FIELDS:
            if field not in data:
                errors.append(f"{relative}: missing required functionality field {field}")
        for field in sorted(set(data) - FUNCTIONALITY_FIELDS - FUNCTIONALITY_OPTIONAL_FIELDS):
            errors.append(f"{relative}: unsupported functionality field {field}")
        require_nonempty_string(data, "title", relative, errors)
        require_nonempty_string(data, "description", relative, errors)
        realises = require_list(data, "realises", relative, errors, nonempty=True)
        for capability in realises:
            if not isinstance(capability, str):
                errors.append(f"{relative}: realises entries must be capability ids")
            elif capability not in capabilities:
                errors.append(f"{relative}: realises undeclared capability {capability}")
            else:
                realised_capabilities.add(capability)
        conformance = data.get("conformance")
        if not isinstance(conformance, str) or conformance not in {"CORE", "EXTENSION"}:
            errors.append(f"{relative}: conformance must be CORE or EXTENSION")
        elif conformance == "CORE":
            core_count += 1
            if "extension" in data:
                errors.append(f"{relative}: CORE functionality must not declare extension")
        else:
            extension = data.get("extension")
            if not isinstance(extension, str) or not extension:
                errors.append(f"{relative}: EXTENSION functionality must declare extension")
            elif extension not in extensions:
                errors.append(f"{relative}: functionality names undeclared extension {extension}")
            else:
                realised_extensions.add(extension)

        for field in ("applies_when", "applies_when_all"):
            if field in data:
                conditions = data[field]
                if not isinstance(conditions, list) or not conditions or any(not isinstance(value, str) for value in conditions):
                    errors.append(f"{relative}: {field} must be a non-empty list of keys")
                else:
                    functionality_conditions.append((relative, field, conditions))

        requirements = data.get("requirements")
        if not isinstance(requirements, list):
            errors.append(f"{relative}: requirements must be a list")
            continue
        for index, item in enumerate(requirements):
            location = requirement_label(path, root, index)
            if not isinstance(item, dict):
                errors.append(f"{location}: requirement must be a mapping")
                continue
            all_requirements[relative].append(item)
            validate_lifecycle(item, location, errors)
            validate_enum(item, "observability", OBSERVABILITY, location, errors)
            validate_enum(item, "mutability", MUTABILITY, location, errors)
            require_nonempty_string(item, "statement", location, errors)
            identifier = item.get("id")
            if isinstance(identifier, str) and LOCAL_REQUIREMENT_ID.fullmatch(identifier):
                numbered_ids.append((identifier, location))

            is_variation = "select" in item
            is_option = "option_of" in item
            if is_variation and is_option:
                errors.append(f"{location}: a requirement cannot be both variation point and option")
            if is_variation:
                for field in sorted(set(item) - VARIATION_FIELDS - {"documentation", "applies_when", "applies_when_all"}):
                    errors.append(f"{location}: unsupported variation point field {field}")
                missing = VARIATION_FIELDS - item.keys()
                for field in sorted(missing):
                    errors.append(f"{location}: variation point missing required field {field}")
                validate_enum(item, "level", LEVELS, location, errors)
                key = item.get("key")
                if not isinstance(key, str) or not key:
                    errors.append(f"{location}: variation point key must be a non-empty string")
                else:
                    variation_keys.add(key)
                    all_keys.append((key, "variation point", location))
                select = item.get("select")
                if not isinstance(select, dict):
                    errors.append(f"{location}: variation point select must be a mapping")
                elif not isinstance(select.get("min"), int) or isinstance(select.get("min"), bool) or select["min"] < 1:
                    errors.append(f"{location}: variation point select.min must be a positive integer")
                else:
                    if isinstance(key, str) and key:
                        variation_selects[key] = (select, location)
                    unexpected_select = set(select) - {"min", "max"}
                    for field in sorted(unexpected_select):
                        errors.append(f"{location}: variation point select has unsupported field {field}")
                    maximum = select.get("max")
                    if maximum is not None and (
                        not isinstance(maximum, int)
                        or isinstance(maximum, bool)
                        or maximum < select["min"]
                    ):
                        errors.append(f"{location}: variation point select.max must be an integer not less than select.min")
                for field in sorted(FORBIDDEN_VARIATION_FIELDS & item.keys()):
                    errors.append(f"{location}: variation point must not declare {field}")
            elif is_option:
                for field in sorted(set(item) - OPTION_FIELDS - COMMON_OPTIONAL_FIELDS):
                    errors.append(f"{location}: unsupported option field {field}")
                missing = OPTION_FIELDS - item.keys()
                for field in sorted(missing):
                    errors.append(f"{location}: option missing required field {field}")
                if "level" in item:
                    errors.append(f"{location}: option must not declare level")
                key = item.get("key")
                if not isinstance(key, str) or not key:
                    errors.append(f"{location}: option key must be a non-empty string")
                else:
                    option_keys.add(key)
                    all_keys.append((key, "option", location))
                require_nonempty_string(item, "option_of", location, errors)
                if isinstance(item.get("option_of"), str):
                    option_parents[item["option_of"]] += 1
                validate_enum(item, "interaction", INTERACTIONS, location, errors)
                validate_local_reference(root, item.get("test"), f"{location}:test", errors)
            else:
                for field in sorted(set(item) - REQUIREMENT_FIELDS - COMMON_OPTIONAL_FIELDS):
                    errors.append(f"{location}: unsupported requirement field {field}")
                missing = REQUIREMENT_FIELDS - item.keys()
                for field in sorted(missing):
                    errors.append(f"{location}: requirement missing required field {field}")
                validate_enum(item, "level", LEVELS, location, errors)
                validate_enum(item, "interaction", INTERACTIONS, location, errors)

            if item.get("observability") == "AUDITABLE":
                require_nonempty_string(item, "documentation", location, errors)
            interaction = item.get("interaction")
            if interaction == "SERVICE_API":
                operation = item.get("api_operation_id")
                if not isinstance(operation, str) or not operation:
                    errors.append(
                        f"{location}: SERVICE_API requirement needs api_operation_id"
                    )
                declared_operations, contract = operations_for_contract(
                    item.get("contract"), location
                )
                if (
                    isinstance(operation, str)
                    and operation
                    and declared_operations is not None
                    and operation not in declared_operations
                ):
                    errors.append(
                        f"{location}: api_operation_id {operation} is missing from {contract}"
                    )
            elif "api_operation_id" in item:
                errors.append(
                    f"{location}: api_operation_id is only valid for SERVICE_API requirements"
                )
            for field in ("contract", "test"):
                if field in item and not is_variation:
                    validate_local_reference(root, item[field], f"{location}:{field}", errors)
            for field in ("applies_when", "applies_when_all"):
                if field in item:
                    conditions = item[field]
                    if not isinstance(conditions, list) or not conditions or any(not isinstance(value, str) for value in conditions):
                        errors.append(f"{location}: {field} must be a non-empty list of keys")

    if core_count == 0:
        errors.append("requirements/: at least one CORE functionality is required")
    for capability in sorted(set(capabilities) - realised_capabilities):
        errors.append(f"metadata.yml: capability {capability} is not realised by any functionality")
    for extension in sorted(set(extensions) - realised_extensions):
        errors.append(f"metadata.yml: extension {extension} has no functionality")

    by_key: defaultdict[str, list[tuple[str, str]]] = defaultdict(list)
    for key, kind, location in all_keys:
        by_key[key].append((kind, location))
    for key, locations in sorted(by_key.items()):
        if len(locations) > 1:
            errors.append(f"requirements/: duplicate requirement key {key}: {', '.join(location for _kind, location in locations)}")
    for key in sorted(option_keys & set(extensions)):
        errors.append(f"metadata.yml: extension id {key} conflicts with option key {key}")
    for key, (select, location) in sorted(variation_selects.items()):
        minimum = select["min"]
        if option_parents[key] < 2:
            errors.append(f"{location}: variation point must have at least two options")
        if option_parents[key] < minimum:
            errors.append(
                f"{location}: variation point select.min {minimum} exceeds its {option_parents[key]} declared option(s)"
            )

    known_conditions = option_keys | set(extensions)
    for relative, field, conditions in functionality_conditions:
        for condition in conditions:
            if condition not in known_conditions:
                errors.append(f"{relative}: {field} references unknown option or extension {condition}")
    for relative, requirements in all_requirements.items():
        for index, item in enumerate(requirements):
            location = f"{relative}:requirements[{index}]"
            option_of = item.get("option_of")
            if isinstance(option_of, str) and option_of not in variation_keys:
                errors.append(f"{location}: option_of {option_of} does not identify a variation point")
            for field in ("applies_when", "applies_when_all"):
                conditions = item.get(field)
                if isinstance(conditions, list):
                    for condition in conditions:
                        if isinstance(condition, str) and condition not in known_conditions:
                            errors.append(f"{location}: {field} references unknown option or extension {condition}")

    by_identifier: defaultdict[str, list[str]] = defaultdict(list)
    for identifier, location in numbered_ids:
        by_identifier[identifier].append(location)
    for identifier, locations in sorted(by_identifier.items()):
        if len(locations) > 1:
            errors.append(f"requirements/: duplicate requirement id {identifier}: {', '.join(locations)}")
    return all_requirements, option_keys | variation_keys


def active_markdown_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*.md"):
        try:
            relative_parts = path.relative_to(root).parts
        except ValueError:
            continue
        if any(part in ACTIVE_MARKDOWN_EXCLUSIONS for part in relative_parts):
            continue
        if path.relative_to(root).as_posix() in RAW_MARKDOWN_SNAPSHOTS:
            continue
        yield path


def validate_markdown_links(root: Path, errors: list[str]) -> None:
    for path in sorted(active_markdown_files(root)):
        try:
            text = path.read_text()
        except (OSError, UnicodeError) as exc:
            errors.append(f"{describe(path, root)}: cannot be read: {exc}")
            continue
        for match in MARKDOWN_LINK.finditer(text):
            target_reference = match.group("target").strip("<>")
            parsed = urlsplit(target_reference)
            if parsed.scheme or parsed.netloc:
                continue
            relative, anchor = split_local_reference(target_reference)
            target = path if not relative else (path.parent / relative).resolve()
            try:
                target.relative_to(root.resolve())
            except ValueError:
                errors.append(f"{describe(path, root)}: Markdown link leaves repository: {target_reference}")
                continue
            if not target.is_file() and not target.is_dir():
                errors.append(f"{describe(path, root)}: broken Markdown link: {target_reference}")
                continue
            if anchor and target.is_file() and target.suffix.lower() == ".md" and anchor not in markdown_anchors(target):
                errors.append(f"{describe(path, root)}: missing Markdown anchor: {target_reference}")


def validate_svgs(root: Path, errors: list[str]) -> None:
    for path in sorted(root.rglob("*.svg")):
        if any(part in {".git", ".venv", "node_modules"} for part in path.relative_to(root).parts):
            continue
        try:
            ET.parse(path)
        except (ET.ParseError, OSError) as exc:
            errors.append(f"{describe(path, root)}: malformed SVG XML: {exc}")


def validate_migration(
    root: Path,
    requirements: dict[str, list[dict[str, Any]]],
    errors: list[str],
) -> None:
    migration_path = root / "resources/requirement-migration.yml"
    migration = load_yaml(migration_path, root, errors)
    if not isinstance(migration, dict):
        if migration is not None:
            errors.append("resources/requirement-migration.yml: root must be a mapping")
        return
    if migration.get("version") != 1:
        errors.append("resources/requirement-migration.yml: version must be 1")
    mappings = migration.get("mappings")
    if not isinstance(mappings, list):
        errors.append("resources/requirement-migration.yml: mappings must be a list")
        return
    seen_legacy: set[str] = set()
    seen_targets: set[tuple[str, str]] = set()
    mapped_legacy: set[str] = set()
    for index, mapping in enumerate(mappings):
        location = f"resources/requirement-migration.yml:mappings[{index}]"
        if not isinstance(mapping, dict):
            errors.append(f"{location}: mapping must be a mapping")
            continue
        legacy = mapping.get("legacy")
        if not isinstance(legacy, str) or LEGACY_ID.fullmatch(legacy) is None:
            errors.append(f"{location}: legacy must be an exact baseline Digital Registries requirement identifier")
        else:
            if legacy in seen_legacy:
                errors.append(f"{location}: duplicate legacy mapping {legacy}")
            seen_legacy.add(legacy)
            mapped_legacy.add(legacy)
        targets = mapping.get("targets")
        if not isinstance(targets, list) or not targets:
            errors.append(f"{location}: targets must be a non-empty list")
            continue
        for target_index, target in enumerate(targets):
            target_location = f"{location}:targets[{target_index}]"
            if not isinstance(target, dict):
                errors.append(f"{target_location}: target must be a mapping")
                continue
            file = target.get("file")
            statement = target.get("statement")
            if not isinstance(file, str) or not file:
                errors.append(f"{target_location}: file must be a non-empty repository path")
                continue
            if not isinstance(statement, str) or not statement:
                errors.append(f"{target_location}: statement must be a non-empty exact statement")
                continue
            identity = (file, statement)
            if identity in seen_targets:
                errors.append(f"{target_location}: duplicate migration target {file} with exact statement {statement!r}")
            seen_targets.add(identity)
            statements = [item.get("statement") for item in requirements.get(file, [])]
            if file not in requirements:
                errors.append(f"{target_location}: target requirement file does not exist: {file}")
            elif statement not in statements:
                errors.append(f"{target_location}: exact statement does not resolve in {file}: {statement!r}")

    history_path = root / "resources/history/requirements.md"
    if not history_path.is_file():
        errors.append("resources/history/requirements.md: required nonnormative legacy archive is missing")
        return
    try:
        history = history_path.read_text()
    except (OSError, UnicodeError) as exc:
        errors.append(f"resources/history/requirements.md: cannot be read: {exc}")
        return
    archived = set(LEGACY_ID.findall(history))
    for identifier in sorted(archived - mapped_legacy):
        errors.append(f"resources/requirement-migration.yml: unmapped archived legacy id {identifier}")
    for identifier in sorted(mapped_legacy - archived):
        errors.append(f"resources/requirement-migration.yml: mapped legacy id is absent from archive {identifier}")


def validate_repository(root: Path) -> list[str]:
    """Return deterministic repository validation errors, or an empty list."""
    root = Path(root).resolve()
    errors: list[str] = []
    if not root.is_dir():
        return [f"{root}: repository root is not a directory"]
    metadata, capabilities, extensions = validate_root_documents(root, errors)
    validate_extension_dependencies(extensions, errors)
    operation_ids(root, errors)
    requirements, _keys = validate_functionalities(root, metadata, capabilities, extensions, errors)
    validate_migration(root, requirements, errors)
    validate_markdown_links(root, errors)
    validate_svgs(root, errors)
    return sorted(set(errors))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="repository root (default: parent of tools/)",
    )
    arguments = parser.parse_args(argv)
    errors = validate_repository(arguments.root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        print(f"Validation failed with {len(errors)} error(s).")
        return 1
    print("Repository structure is valid. DRAFT requirements do not establish conformance.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
