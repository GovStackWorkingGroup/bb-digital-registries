#!/usr/bin/env python3
"""Regression tests for the repository-level specification validator."""

from __future__ import annotations

from contextlib import contextmanager
import hashlib
import importlib.util
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "tools/validate_specification.py"
ARCHIVE = ROOT / "resources/history/requirements.md"
ARCHIVE_BLOCK = re.compile(r"(?ms)^(### #\d+ .*?)(?=^### #\d+ |^## |\Z)")
ARCHIVE_IDENTIFIER = re.compile(
    r"`(govstack-bb-digital-registries-fr-(?:core|consultation)#req-\d+)`"
)
BASELINE_REQUIREMENT_HASHES = {
    "govstack-bb-digital-registries-fr-consultation#req-1": "327b9b5aa871f36fcca8780f73e392f50748cb547a3364e963c70c094fd4fd09",
    "govstack-bb-digital-registries-fr-consultation#req-2": "866e9cce33f67fe71ba02e348a51794465f3ada2aa297566f218e767e09a03bc",
    "govstack-bb-digital-registries-fr-consultation#req-3": "ef97daee9e0be07b5d6c8ee911b8ce60e43442b4937b065cac951aeff54b807d",
    "govstack-bb-digital-registries-fr-consultation#req-4": "65932bc0e3f080b84fd468fba8671b94a916d9c9729057415b66243ab682cee4",
    "govstack-bb-digital-registries-fr-consultation#req-5": "4c5fcc75fd0521c3fd7df2011cc66b8f14f978f32711b978d68a178a336beafb",
    "govstack-bb-digital-registries-fr-consultation#req-6": "af673c80f49b1ef4cbc3b059bb9de2dc2416d0cc951e28d8cb853bdfa07b4c36",
    "govstack-bb-digital-registries-fr-consultation#req-7": "758ede2eb4d59c41662a7873a7e82ae9fb07379ec4e7cd40ae9586f5e93dff84",
    "govstack-bb-digital-registries-fr-core#req-1": "811f7446db24027554a0e374a67c20e798de8942a32370f8a7d362f4a41b132e",
    "govstack-bb-digital-registries-fr-core#req-2": "cc9c638bf28801e28d296d61d88caa666b8348a1b2ebca7d3260de4b903aad7d",
    "govstack-bb-digital-registries-fr-core#req-3": "0be5e1ea4ccf3ab8d19276e9876dafc9ee8e0a99e5a3f8c41b5c194c4ffc2789",
    "govstack-bb-digital-registries-fr-core#req-4": "938eb7317cb28c1d1c3df4d2d75d85bfe65127e48faa5531a28fc09375f4ccab",
    "govstack-bb-digital-registries-fr-core#req-5": "7358fb74d0792845501de4ceaf198aae30b00017b135d20f0c73257fc8667953",
    "govstack-bb-digital-registries-fr-core#req-6": "806fc1e869593d0cb100af6169bfc70d9f4cfa368dedf09d4339f070111a3635",
    "govstack-bb-digital-registries-fr-core#req-7": "0e015cc88f5c35f15492a9c632c0bbdc44d02a29dc3f93d92b67c43bd19c6ed1",
    "govstack-bb-digital-registries-fr-core#req-8": "f0e7757adae059bd94fe660e4aac26177b12a9a4d3a1b8b8b733daeb3f055e6e",
}


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_specification", VALIDATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot import {VALIDATOR}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def front_matter(data: dict, body: str = "") -> str:
    return "---\n" + yaml.safe_dump(data, sort_keys=False) + "---\n" + body


def archive_source_errors(text: str) -> list[str]:
    errors: list[str] = []
    blocks: dict[str, list[str]] = {}
    for block in ARCHIVE_BLOCK.findall(text):
        match = ARCHIVE_IDENTIFIER.search(block)
        if match:
            blocks.setdefault(match.group(1), []).append(block)
    expected = set(BASELINE_REQUIREMENT_HASHES)
    actual = set(blocks)
    for identifier in sorted(expected - actual):
        errors.append(f"missing archived source block {identifier}")
    for identifier in sorted(actual - expected):
        errors.append(f"unexpected archived source block {identifier}")
    for identifier in sorted(expected & actual):
        if len(blocks[identifier]) != 1:
            errors.append(f"duplicate archived source block {identifier}")
            continue
        normalized = re.sub(r"\s+", " ", blocks[identifier][0]).strip()
        digest = hashlib.sha256(normalized.encode()).hexdigest()
        if digest != BASELINE_REQUIREMENT_HASHES[identifier]:
            errors.append(f"changed archived source block {identifier}")
    return errors


class RepositoryFixture:
    """A minimal, valid specification repository used by focused tests."""

    legacy_uri = "govstack-bb-digital-registries-fr-core#req-1"
    statement = "The solution shall publish Registry metadata."

    def __init__(self, root: Path):
        self.root = root
        self.write(
            "metadata.yml",
            yaml.safe_dump(
                {
                    "name": "Digital Registries",
                    "abstract": "A registry interoperability specification.",
                    "url": "https://specs.govstack.global/digital-registries/",
                    "repository": "https://github.com/GovStackWorkingGroup/bb-digital-registries",
                    "urn": "govstack:spec:bb:digital-registries",
                    "owner_group": "govstack:team:technical-committee",
                    "capabilities": [
                        {
                            "id": "registry-information",
                            "title": "Registry information",
                            "description": "Authorized users obtain Registry information.",
                        }
                    ],
                    "extensions": [],
                    "versions": [
                        {
                            "version": "3.0.0",
                            "url_suffix": "/digital-registries/3.0.0",
                            "latest": True,
                            "release_date": None,
                            "short_description": "Draft specification format migration.",
                        }
                    ],
                },
                sort_keys=False,
            ),
        )
        self.write(
            "authors.yml",
            yaml.safe_dump(
                {
                    "authors": [
                        {
                            "name": "Digital Registries Working Group",
                            "roles": ["Author"],
                            "urn": "govstack:person:digital-registries-working-group",
                            "url": "https://govstack.global/",
                        }
                    ]
                },
                sort_keys=False,
            ),
        )
        self.write(
            "toc.yml",
            yaml.safe_dump(
                {
                    "toc": {
                        "introduction": ["overview.md"],
                        "requirements": ["core.md"],
                        "resources": ["api.yml", "testing.md"],
                    }
                },
                sort_keys=False,
            ),
        )
        self.write("introduction/overview.md", "# Overview\n\nSee [testing](../resources/testing.md#consultation-1).\n")
        self.write("resources/contract.md", "# File contract\n")
        self.write("resources/testing.md", "# Testing\n\n<a id=\"consultation-1\"></a>\n\n## Consultation 1\n")
        self.write(
            "resources/api.yml",
            yaml.safe_dump(
                {
                    "openapi": "3.1.0",
                    "info": {"title": "Fixture API", "version": "1.0.0"},
                    "paths": {
                        "/v1/records/{recordId}": {
                            "get": {
                                "operationId": "retrieveRecord",
                                "responses": {"200": {"description": "Found"}},
                            }
                        }
                    },
                },
                sort_keys=False,
            ),
        )
        self.write("resources/diagram.svg", '<svg xmlns="http://www.w3.org/2000/svg"><title>Valid</title></svg>\n')
        self.write("resources/history/requirements.md", f"# Legacy requirements\n\n`{self.legacy_uri}`\n")
        self.write(
            "resources/requirement-migration.yml",
            yaml.safe_dump(
                {
                    "version": 1,
                    "mappings": [
                        {
                            "legacy": self.legacy_uri,
                            "targets": [{"file": "requirements/core.md", "statement": self.statement}],
                        }
                    ],
                },
                sort_keys=False,
            ),
        )
        self.requirements = {
            "title": "Registry service",
            "description": "Publish metadata and provide at least one Registry service operation.",
            "realises": ["registry-information"],
            "conformance": "CORE",
            "requirements": [
                {
                    "key": "registry-service",
                    "select": {"min": 1},
                    "id": None,
                    "status": "DRAFT",
                    "level": "REQUIRED",
                    "observability": "AUDITABLE",
                    "mutability": "EXTENSIBLE",
                    "statement": "The solution shall implement at least one Registry service option.",
                    "documentation": "The supplier identifies every implemented option.",
                },
                {
                    "key": "consultation-retrieve",
                    "option_of": "registry-service",
                    "id": None,
                    "status": "DRAFT",
                    "observability": "OBSERVABLE",
                    "mutability": "EXTENSIBLE",
                    "interaction": "SERVICE_API",
                    "contract": "resources/api.yml",
                    "api_operation_id": "retrieveRecord",
                    "statement": "The solution shall retrieve an authorized Record by identifier.",
                    "test": "resources/testing.md#consultation-1",
                },
                {
                    "id": None,
                    "status": "DRAFT",
                    "level": "REQUIRED",
                    "observability": "AUDITABLE",
                    "mutability": "EXTENSIBLE",
                    "interaction": "FILE",
                    "contract": "resources/contract.md",
                    "statement": self.statement,
                    "documentation": "The supplier provides the published metadata document.",
                    "applies_when": ["consultation-retrieve"],
                },
                {
                    "key": "registry-file",
                    "option_of": "registry-service",
                    "id": None,
                    "status": "DRAFT",
                    "observability": "OBSERVABLE",
                    "mutability": "EXTENSIBLE",
                    "interaction": "FILE",
                    "contract": "resources/contract.md",
                    "statement": "The solution shall publish authorized Registry information as a file.",
                    "test": "resources/testing.md#consultation-1",
                },
            ],
        }
        self.save_requirements()

    def path(self, relative: str) -> Path:
        return self.root / relative

    def write(self, relative: str, content: str) -> None:
        path = self.path(relative)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)

    def save_requirements(self, name: str = "core.md", data: dict | None = None, body: str = "# Workflow\n") -> None:
        self.write(f"requirements/{name}", front_matter(data or self.requirements, body))

    def load_yaml(self, relative: str) -> dict:
        return yaml.safe_load(self.path(relative).read_text())

    def save_yaml(self, relative: str, data: dict) -> None:
        self.write(relative, yaml.safe_dump(data, sort_keys=False))


class SpecificationValidatorTests(unittest.TestCase):
    @contextmanager
    def fixture(self):
        with tempfile.TemporaryDirectory() as directory:
            yield RepositoryFixture(Path(directory))

    def errors(self, fixture: RepositoryFixture) -> list[str]:
        return load_validator().validate_repository(fixture.root)

    def assert_error(self, errors: list[str], *terms: str) -> None:
        rendered = "\n".join(errors).lower()
        for term in terms:
            self.assertIn(term.lower(), rendered, rendered)

    def test_minimal_draft_repository_is_valid_without_claiming_conformance(self):
        with self.fixture() as fixture:
            self.assertEqual(self.errors(fixture), [])

    def test_requires_root_metadata_authors_and_toc(self):
        for relative in ("metadata.yml", "authors.yml", "toc.yml"):
            with self.subTest(relative=relative), self.fixture() as fixture:
                fixture.path(relative).unlink()
                self.assert_error(self.errors(fixture), relative)

    def test_rejects_malformed_metadata(self):
        with self.fixture() as fixture:
            fixture.write("metadata.yml", "capabilities: [\n")
            self.assert_error(self.errors(fixture), "metadata.yml", "yaml")

    def test_authors_require_name_roles_and_person_urn(self):
        invalid_authors = (
            ({"roles": ["Author"], "urn": "govstack:person:missing-name"}, "name"),
            ({"name": "No roles", "roles": [], "urn": "govstack:person:no-roles"}, "roles"),
            ({"name": "Team urn", "roles": ["Author"], "urn": "govstack:team:authors"}, "govstack:person"),
        )
        for author, message in invalid_authors:
            with self.subTest(author=author), self.fixture() as fixture:
                fixture.save_yaml("authors.yml", {"authors": [author]})
                self.assert_error(self.errors(fixture), "authors.yml", message)

    def test_versions_require_semver_and_exactly_one_latest(self):
        with self.fixture() as fixture:
            metadata = fixture.load_yaml("metadata.yml")
            metadata["versions"][0]["version"] = "3.0"
            fixture.save_yaml("metadata.yml", metadata)
            self.assert_error(self.errors(fixture), "version", "semver")
        with self.fixture() as fixture:
            metadata = fixture.load_yaml("metadata.yml")
            metadata["versions"].append(
                {
                    "version": "3.0.1",
                    "url_suffix": "/digital-registries/3.0.1",
                    "latest": True,
                    "release_date": None,
                    "short_description": "Another latest version.",
                }
            )
            fixture.save_yaml("metadata.yml", metadata)
            self.assert_error(self.errors(fixture), "exactly one", "latest")

    def test_toc_entries_must_resolve_in_their_sections(self):
        with self.fixture() as fixture:
            toc = fixture.load_yaml("toc.yml")
            toc["toc"]["resources"].append("missing.md")
            fixture.save_yaml("toc.yml", toc)
            self.assert_error(self.errors(fixture), "toc.yml", "resources/missing.md")

    def test_malformed_types_produce_diagnostics_instead_of_exceptions(self):
        with self.fixture() as fixture:
            metadata = fixture.load_yaml("metadata.yml")
            metadata["capabilities"] = {"registry-information": "not-a-list"}
            fixture.save_yaml("metadata.yml", metadata)
            fixture.requirements["requirements"] = {"not": "a-list"}
            fixture.save_requirements()
            errors = self.errors(fixture)
            self.assert_error(errors, "capabilities", "list")
            self.assert_error(errors, "requirements", "list")

    def test_functionality_requires_exact_root_fields_and_known_capability(self):
        for field in ("title", "description", "realises", "conformance", "requirements"):
            with self.subTest(field=field), self.fixture() as fixture:
                del fixture.requirements[field]
                fixture.save_requirements()
                self.assert_error(self.errors(fixture), "core.md", field)
        with self.fixture() as fixture:
            fixture.requirements["realises"] = ["missing-capability"]
            fixture.save_requirements()
            self.assert_error(self.errors(fixture), "missing-capability")

    def test_functionality_level_conditions_use_declared_option_or_extension_keys(self):
        with self.fixture() as fixture:
            fixture.requirements["applies_when"] = ["consultation-retrieve"]
            fixture.requirements["applies_when_all"] = ["registry-file"]
            fixture.save_requirements()
            self.assertEqual(self.errors(fixture), [])
        with self.fixture() as fixture:
            fixture.requirements["applies_when"] = ["unknown-condition"]
            fixture.save_requirements()
            self.assert_error(self.errors(fixture), "applies_when", "unknown-condition")

    def test_every_capability_and_extension_is_realised(self):
        with self.fixture() as fixture:
            metadata = fixture.load_yaml("metadata.yml")
            metadata["capabilities"].append(
                {"id": "registry-discovery", "title": "Discovery", "description": "Users discover Registry services."}
            )
            fixture.save_yaml("metadata.yml", metadata)
            self.assert_error(self.errors(fixture), "registry-discovery", "realised")
        with self.fixture() as fixture:
            metadata = fixture.load_yaml("metadata.yml")
            metadata["extensions"] = [
                {"id": "bulk-read", "title": "Bulk read", "description": "Read records in bulk.", "requires": []}
            ]
            fixture.save_yaml("metadata.yml", metadata)
            self.assert_error(self.errors(fixture), "bulk-read", "functionality")

    def test_extension_functionality_requires_declared_extension_and_core_forbids_it(self):
        with self.fixture() as fixture:
            fixture.requirements["conformance"] = "EXTENSION"
            fixture.requirements["extension"] = "missing-extension"
            fixture.save_requirements()
            self.assert_error(self.errors(fixture), "missing-extension")
        with self.fixture() as fixture:
            fixture.requirements["extension"] = "anything"
            fixture.save_requirements()
            self.assert_error(self.errors(fixture), "core", "extension")

    def test_extension_dependency_must_exist_and_cycles_are_rejected(self):
        with self.fixture() as fixture:
            metadata = fixture.load_yaml("metadata.yml")
            metadata["extensions"] = [
                {"id": "one", "title": "One", "description": "One.", "requires": ["missing"]}
            ]
            fixture.save_yaml("metadata.yml", metadata)
            self.assert_error(self.errors(fixture), "missing", "requires")
        with self.fixture() as fixture:
            metadata = fixture.load_yaml("metadata.yml")
            metadata["extensions"] = [
                {"id": "one", "title": "One", "description": "One.", "requires": ["two"]},
                {"id": "two", "title": "Two", "description": "Two.", "requires": ["one"]},
            ]
            fixture.save_yaml("metadata.yml", metadata)
            for extension in ("one", "two"):
                data = {
                    "title": extension.title(),
                    "description": f"The {extension} extension.",
                    "realises": ["registry-information"],
                    "conformance": "EXTENSION",
                    "extension": extension,
                    "requirements": [],
                }
                fixture.save_requirements(f"{extension}.md", data)
            self.assert_error(self.errors(fixture), "cycle", "one", "two")

    def test_requirements_need_explicit_classifiers_and_singular_statement(self):
        for field in ("id", "status", "level", "observability", "mutability", "interaction", "statement"):
            with self.subTest(field=field), self.fixture() as fixture:
                del fixture.requirements["requirements"][2][field]
                fixture.save_requirements()
                self.assert_error(self.errors(fixture), field)

    def test_rejects_nested_classifiers_and_legacy_field_aliases(self):
        with self.fixture() as fixture:
            item = fixture.requirements["requirements"][2]
            item["classifiers"] = {"status": item["status"]}
            item["lifecycle"] = item["status"]
            item["title"] = "Legacy title"
            item["core"] = True
            item["extends"] = []
            fixture.save_requirements()
            errors = self.errors(fixture)
            for field in ("classifiers", "lifecycle", "title", "core", "extends"):
                self.assert_error(errors, "unsupported", field)

    def test_draft_and_candidate_ids_are_empty(self):
        for status in ("DRAFT", "CANDIDATE"):
            with self.subTest(status=status), self.fixture() as fixture:
                requirement = fixture.requirements["requirements"][2]
                requirement["status"] = status
                requirement["id"] = "govstack:spec:bb:digital-registries#req-7"
                fixture.save_requirements()
                self.assert_error(self.errors(fixture), status, "id")

    def test_accepted_lifecycle_ids_are_numbered_and_globally_unique(self):
        for status in ("ACCEPTED", "PUBLISHED", "DEPRECATED"):
            with self.subTest(status=status), self.fixture() as fixture:
                fixture.requirements["requirements"][2]["status"] = status
                fixture.save_requirements()
                self.assert_error(self.errors(fixture), status, "id")
        with self.fixture() as fixture:
            item = fixture.requirements["requirements"][2]
            item.update(status="ACCEPTED", id="1")
            fixture.save_requirements()
            self.assertEqual(self.errors(fixture), [])
        with self.fixture() as fixture:
            item = fixture.requirements["requirements"][2]
            item.update(status="ACCEPTED", id="1")
            duplicate = dict(item)
            fixture.requirements["requirements"].append(duplicate)
            fixture.save_requirements()
            self.assert_error(self.errors(fixture), "duplicate", "id 1")

    def test_non_string_enum_values_produce_diagnostics(self):
        with self.fixture() as fixture:
            fixture.requirements["conformance"] = []
            fixture.requirements["requirements"][2]["status"] = []
            fixture.requirements["requirements"][2]["interaction"] = []
            fixture.save_requirements()
            errors = self.errors(fixture)
            self.assert_error(errors, "conformance")
            self.assert_error(errors, "status")
            self.assert_error(errors, "interaction")

    def test_variation_point_shape_is_enforced(self):
        forbidden = {
            "interaction": "INTERNAL",
            "api_operation_id": "retrieveRecord",
            "test": "resources/testing.md#consultation-1",
        }
        for field, value in forbidden.items():
            with self.subTest(field=field), self.fixture() as fixture:
                fixture.requirements["requirements"][0][field] = value
                fixture.save_requirements()
                self.assert_error(self.errors(fixture), "variation", field)
        with self.fixture() as fixture:
            del fixture.requirements["requirements"][0]["key"]
            fixture.save_requirements()
            self.assert_error(self.errors(fixture), "variation", "key")

    def test_variation_point_cardinality_is_valid(self):
        invalid = (
            ({"min": 0}, "positive integer"),
            ({"min": -1}, "positive integer"),
            ({"min": 3}, "exceeds"),
            ({"min": 2, "max": 1}, "max"),
        )
        for select, message in invalid:
            with self.subTest(select=select), self.fixture() as fixture:
                fixture.requirements["requirements"][0]["select"] = select
                fixture.save_requirements()
                self.assert_error(self.errors(fixture), "select", message)
        with self.fixture() as fixture:
            fixture.requirements["requirements"].pop()
            fixture.save_requirements()
            self.assert_error(self.errors(fixture), "variation", "at least two options")

    def test_option_shape_and_prerequisite_are_enforced(self):
        with self.fixture() as fixture:
            fixture.requirements["requirements"][1]["level"] = "REQUIRED"
            fixture.save_requirements()
            self.assert_error(self.errors(fixture), "option", "level")
        with self.fixture() as fixture:
            fixture.requirements["requirements"][1]["option_of"] = "missing-prerequisite"
            fixture.save_requirements()
            self.assert_error(self.errors(fixture), "missing-prerequisite", "variation")
        with self.fixture() as fixture:
            del fixture.requirements["requirements"][1]["test"]
            fixture.save_requirements()
            self.assert_error(self.errors(fixture), "option", "test")

    def test_option_keys_are_unique_and_do_not_collide_with_extension_ids(self):
        with self.fixture() as fixture:
            duplicate = dict(fixture.requirements["requirements"][1])
            fixture.requirements["requirements"].append(duplicate)
            fixture.save_requirements()
            self.assert_error(self.errors(fixture), "consultation-retrieve", "duplicate")
        with self.fixture() as fixture:
            metadata = fixture.load_yaml("metadata.yml")
            metadata["extensions"] = [
                {
                    "id": "consultation-retrieve",
                    "title": "Conflicting extension",
                    "description": "Conflicts with an option key.",
                    "requires": [],
                }
            ]
            fixture.save_yaml("metadata.yml", metadata)
            self.assert_error(self.errors(fixture), "consultation-retrieve", "extension", "option")

    def test_conditions_reference_only_declared_options_or_extensions(self):
        for field in ("applies_when", "applies_when_all"):
            with self.subTest(field=field), self.fixture() as fixture:
                fixture.requirements["requirements"][2].pop("applies_when", None)
                fixture.requirements["requirements"][2][field] = ["unknown-condition"]
                fixture.save_requirements()
                self.assert_error(self.errors(fixture), field, "unknown-condition")

    def test_service_api_operation_must_exist_in_declared_contract(self):
        with self.fixture() as fixture:
            fixture.requirements["requirements"][1]["api_operation_id"] = "missingOperation"
            fixture.save_requirements()
            self.assert_error(self.errors(fixture), "missingOperation", "resources/api.yml")

    def test_service_api_accepts_operation_from_separate_declared_contract(self):
        with self.fixture() as fixture:
            fixture.write(
                "api/write.openapi.yaml",
                yaml.safe_dump(
                    {
                        "openapi": "3.1.0",
                        "info": {"title": "Write fixture", "version": "1.0.0"},
                        "paths": {
                            "/v1/records": {
                                "post": {
                                    "operationId": "createRecord",
                                    "responses": {"201": {"description": "Created"}},
                                }
                            }
                        },
                    },
                    sort_keys=False,
                ),
            )
            fixture.path("resources/write-api.yml").symlink_to(
                "../api/write.openapi.yaml"
            )
            requirement = fixture.requirements["requirements"][1]
            requirement["contract"] = "resources/write-api.yml"
            requirement["api_operation_id"] = "createRecord"
            fixture.save_requirements()
            self.assertEqual(self.errors(fixture), [])

    def test_service_api_does_not_accept_operation_from_the_wrong_contract(self):
        with self.fixture() as fixture:
            fixture.write(
                "resources/write-api.yml",
                yaml.safe_dump(
                    {
                        "openapi": "3.1.0",
                        "info": {"title": "Write fixture", "version": "1.0.0"},
                        "paths": {
                            "/v1/records": {
                                "post": {
                                    "operationId": "createRecord",
                                    "responses": {"201": {"description": "Created"}},
                                }
                            }
                        },
                    },
                    sort_keys=False,
                ),
            )
            requirement = fixture.requirements["requirements"][1]
            requirement["contract"] = "resources/write-api.yml"
            requirement["api_operation_id"] = "retrieveRecord"
            fixture.save_requirements()
            self.assert_error(
                self.errors(fixture), "retrieveRecord", "resources/write-api.yml"
            )

    def test_service_api_contract_is_explicit_and_repository_local(self):
        mutations = (
            None,
            "https://example.test/write.openapi.yaml",
            "../write.openapi.yaml",
        )
        for contract in mutations:
            with self.subTest(contract=contract), self.fixture() as fixture:
                requirement = fixture.requirements["requirements"][1]
                if contract is None:
                    requirement.pop("contract")
                else:
                    requirement["contract"] = contract
                fixture.save_requirements()
                self.assert_error(self.errors(fixture), "contract", "repository-local")

    def test_resources_api_symlink_to_canonical_api_is_supported(self):
        with self.fixture() as fixture:
            canonical = fixture.path("api/openapi.yaml")
            canonical.parent.mkdir(parents=True, exist_ok=True)
            fixture.path("resources/api.yml").replace(canonical)
            fixture.path("resources/api.yml").symlink_to("../api/openapi.yaml")
            self.assertEqual(self.errors(fixture), [])

    def test_canonical_api_requires_exact_resources_symlink_alias(self):
        with self.fixture() as fixture:
            canonical = fixture.path("api/openapi.yaml")
            canonical.parent.mkdir(parents=True, exist_ok=True)
            canonical.write_text(fixture.path("resources/api.yml").read_text())
            self.assert_error(self.errors(fixture), "resources/api.yml", "symlink")
        with self.fixture() as fixture:
            canonical = fixture.path("api/openapi.yaml")
            canonical.parent.mkdir(parents=True, exist_ok=True)
            canonical.write_text(fixture.path("resources/api.yml").read_text())
            other = fixture.path("api/other.yaml")
            other.write_text(canonical.read_text())
            fixture.path("resources/api.yml").unlink()
            fixture.path("resources/api.yml").symlink_to("../api/other.yaml")
            errors = self.errors(fixture)
            self.assert_error(errors, "resources/api.yml", "../api/openapi.yaml")

    def test_api_inventory_paths_are_repository_relative_and_include_canonical(self):
        with self.fixture() as fixture:
            canonical = fixture.path("api/openapi.yaml")
            canonical.parent.mkdir(parents=True, exist_ok=True)
            fixture.path("resources/api.yml").replace(canonical)
            fixture.path("resources/api.yml").symlink_to("../api/openapi.yaml")
            fixture.save_yaml(
                "api/index.yaml",
                {
                    "version": 1,
                    "apis": [{"type": "openapi", "path": "api/openapi.yaml"}],
                },
            )
            self.assertEqual(self.errors(fixture), [])

        with self.fixture() as fixture:
            canonical = fixture.path("api/openapi.yaml")
            canonical.parent.mkdir(parents=True, exist_ok=True)
            fixture.path("resources/api.yml").replace(canonical)
            fixture.path("resources/api.yml").symlink_to("../api/openapi.yaml")
            fixture.save_yaml(
                "api/index.yaml",
                {"version": 1, "apis": [{"type": "openapi", "path": "openapi.yaml"}]},
            )
            self.assert_error(
                self.errors(fixture), "api/index.yaml", "api/openapi.yaml"
            )

        with self.fixture() as fixture:
            canonical = fixture.path("api/openapi.yaml")
            canonical.parent.mkdir(parents=True, exist_ok=True)
            fixture.path("resources/api.yml").replace(canonical)
            fixture.path("resources/api.yml").symlink_to("../api/openapi.yaml")
            fixture.write("api/other.yaml", canonical.read_text())
            fixture.save_yaml(
                "api/index.yaml",
                {"version": 1, "apis": [{"type": "openapi", "path": "api/other.yaml"}]},
            )
            self.assert_error(
                self.errors(fixture), "api/index.yaml", "api/openapi.yaml"
            )

    def test_archive_preserves_all_immutable_baseline_requirement_blocks(self):
        self.assertEqual(archive_source_errors(ARCHIVE.read_text()), [])

    def test_archive_guard_rejects_removed_or_reworded_source_blocks(self):
        archive = ARCHIVE.read_text()
        blocks = {
            match.group(1): block
            for block in ARCHIVE_BLOCK.findall(archive)
            if (match := ARCHIVE_IDENTIFIER.search(block))
        }
        removed = archive.replace(
            blocks["govstack-bb-digital-registries-fr-core#req-1"],
            "",
            1,
        )
        self.assert_error(
            archive_source_errors(removed),
            "missing",
            "govstack-bb-digital-registries-fr-core#req-1",
        )
        reworded = archive.replace(
            "An implementation publishes machine-readable Registry metadata",
            "A solution publishes machine-readable Registry metadata",
            1,
        )
        self.assert_error(
            archive_source_errors(reworded),
            "changed",
            "govstack-bb-digital-registries-fr-core#req-1",
        )

    def test_contract_and_test_targets_must_exist_with_valid_anchors(self):
        with self.fixture() as fixture:
            fixture.requirements["requirements"][2]["contract"] = "resources/missing.md"
            fixture.save_requirements()
            self.assert_error(self.errors(fixture), "resources/missing.md")
        with self.fixture() as fixture:
            fixture.requirements["requirements"][1]["test"] = "resources/testing.md#missing-anchor"
            fixture.save_requirements()
            self.assert_error(self.errors(fixture), "missing-anchor")

    def test_contract_and_test_references_cannot_leave_repository(self):
        for index, field in ((2, "contract"), (1, "test")):
            with self.subTest(field=field), self.fixture() as fixture:
                fixture.requirements["requirements"][index][field] = "../outside.md"
                fixture.save_requirements()
                self.assert_error(self.errors(fixture), field, "leaves repository")

    def test_active_markdown_links_and_anchors_are_checked_but_history_is_excluded(self):
        with self.fixture() as fixture:
            fixture.save_requirements(body="# Workflow\n\nSee [missing](../resources/missing.md).\n")
            self.assert_error(self.errors(fixture), "resources/missing.md")
        with self.fixture() as fixture:
            fixture.write(
                "resources/history/requirements.md",
                f"# Legacy\n\n`{fixture.legacy_uri}`\n\n[Historical broken link](missing.md)\n",
            )
            self.assertEqual(self.errors(fixture), [])

    def test_svg_assets_must_be_well_formed_xml(self):
        with self.fixture() as fixture:
            fixture.write("resources/diagram.svg", "<svg><g></svg>\n")
            self.assert_error(self.errors(fixture), "diagram.svg", "xml")

    def test_migration_targets_resolve_to_exact_unique_requirement_statements(self):
        with self.fixture() as fixture:
            migration = fixture.load_yaml("resources/requirement-migration.yml")
            migration["mappings"][0]["targets"][0]["statement"] = "Not the exact statement."
            fixture.save_yaml("resources/requirement-migration.yml", migration)
            self.assert_error(self.errors(fixture), "exact", "statement")
        with self.fixture() as fixture:
            migration = fixture.load_yaml("resources/requirement-migration.yml")
            migration["mappings"].append(migration["mappings"][0])
            fixture.save_yaml("resources/requirement-migration.yml", migration)
            self.assert_error(self.errors(fixture), "duplicate", "legacy")

    def test_every_archived_legacy_identifier_is_mapped(self):
        with self.fixture() as fixture:
            fixture.write(
                "resources/history/requirements.md",
                f"# Legacy\n\n`{fixture.legacy_uri}`\n\n`govstack-bb-digital-registries-fr-core#req-2`\n",
            )
            self.assert_error(self.errors(fixture), "unmapped", "req-2")

    def test_migration_uses_exact_baseline_legacy_identifiers(self):
        with self.fixture() as fixture:
            migration = fixture.load_yaml("resources/requirement-migration.yml")
            migration["mappings"][0]["legacy"] = "https://govstack.global/spec/digital-registries/fr-core#req-1"
            fixture.save_yaml("resources/requirement-migration.yml", migration)
            self.assert_error(self.errors(fixture), "exact baseline", "legacy")

    def test_migration_map_is_required(self):
        with self.fixture() as fixture:
            fixture.path("resources/requirement-migration.yml").unlink()
            self.assert_error(self.errors(fixture), "requirement-migration.yml", "missing")

    def test_cli_exits_zero_for_valid_repository_and_nonzero_with_sorted_errors(self):
        with self.fixture() as fixture:
            valid = subprocess.run(
                [sys.executable, str(VALIDATOR), "--root", str(fixture.root)],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(valid.returncode, 0, valid.stdout + valid.stderr)
            fixture.path("authors.yml").unlink()
            fixture.path("toc.yml").unlink()
            invalid = subprocess.run(
                [sys.executable, str(VALIDATOR), "--root", str(fixture.root)],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(invalid.returncode, 0)
            lines = [line.removeprefix("ERROR: ") for line in invalid.stdout.splitlines() if line.startswith("ERROR: ")]
            self.assertEqual(lines, sorted(lines))

    def test_reader_reachable_legacy_and_history_pages_have_checked_links(self):
        for relative in (
            "api/legacy/generated-crud/README.md",
            "resources/history/release-notes.md",
        ):
            with self.subTest(relative=relative), self.fixture() as fixture:
                fixture.write(relative, "See [missing](missing.md).\n")
                self.assert_error(self.errors(fixture), relative, "missing.md")

    def test_publication_identity_preserves_the_govstack_transition_identifier(self):
        # GovStackWorkingGroup/transition-specs, bb-digital-registries/metadata.yml.
        metadata = yaml.safe_load((ROOT / "metadata.yml").read_text())
        expected = {
            "urn": "govstack:spec:bb:registries",
            "url": "https://specs.govstack.global/registries/",
            "repository": "https://github.com/GovStackWorkingGroup/bb-digital-registries",
            "owner_group": "govstack:wg:registries-registration",
        }
        for field, value in expected.items():
            with self.subTest(field=field):
                self.assertEqual(metadata[field], value)

    def test_openapi_publication_requirements_name_the_digital_registry_as_subject(
        self,
    ):
        source = (ROOT / "requirements/registry-services.md").read_text()
        functionality = yaml.safe_load(source.split("---", 2)[1])
        requirements = [
            requirement
            for requirement in functionality["requirements"]
            if requirement.get("interaction") == "FILE"
            and requirement.get("contract")
            == "api/extensions/x-govstack-digital-registries.schema.json"
        ]
        self.assertEqual(len(requirements), 6)
        prefix = "The Digital Registry publishes an OpenAPI contract that declares the "
        for requirement in requirements:
            with self.subTest(applies_when=requirement["applies_when"]):
                self.assertTrue(
                    requirement["statement"].startswith(prefix),
                    requirement["statement"],
                )

    def test_readme_home_page_leaves_contributor_material_to_contributing(self):
        # The publication renderer uses README.md as the site home page.
        readme = (ROOT / "README.md").read_text()
        contributing = (ROOT / "CONTRIBUTING.md").read_text()
        repository = yaml.safe_load((ROOT / "metadata.yml").read_text())["repository"]
        self.assertIn(f"]({repository}/blob/main/CONTRIBUTING.md)", readme)
        for heading in ("## Repository layout", "## Validation"):
            with self.subTest(heading=heading):
                self.assertNotIn(heading, readme)
                self.assertIn(heading, contributing)

    def test_checked_in_repository_is_valid(self):
        self.assertEqual(load_validator().validate_repository(ROOT), [])


if __name__ == "__main__":
    unittest.main()
