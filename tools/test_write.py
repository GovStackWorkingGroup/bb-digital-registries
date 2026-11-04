#!/usr/bin/env python3
"""Mutation-based regression tests for Write artifacts, not a runtime."""

from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import re
import unittest
from urllib.parse import urldefrag, urlparse

from jsonschema import Draft202012Validator, FormatChecker, ValidationError
from referencing.exceptions import Unresolvable
import yaml

try:
    from . import validate_write as write
except ImportError:
    import validate_write as write


ROOT = Path(__file__).resolve().parents[1]
API = ROOT / "api"


def operation(document, operation_id):
    matches = [
        value
        for _route, _method, value in write.operations(document)
        if value.get("operationId") == operation_id
    ]
    if len(matches) != 1:
        raise AssertionError(f"Expected one {operation_id}, found {len(matches)}")
    return matches[0]


def without_parameter(operation_value, suffix):
    operation_value["parameters"] = [
        parameter
        for parameter in operation_value.get("parameters", [])
        if not str(parameter.get("$ref", "")).endswith(suffix)
    ]


def values_for_keys(value, keys):
    found = []
    if isinstance(value, dict):
        for key, child in value.items():
            if key in keys:
                found.append((key, child))
            found.extend(values_for_keys(child, keys))
    elif isinstance(value, list):
        for child in value:
            found.extend(values_for_keys(child, keys))
    return found


class WriteArtifactTests(unittest.TestCase):
    def test_required_write_artifacts_exist(self):
        expected = (
            write.WRITE,
            write.WRITE_EXTENSION_SCHEMA,
            write.EXAMPLE_API,
            write.EXAMPLE_SCHEMA,
            write.EXCHANGES,
            write.CONTRACT_FIXTURES,
            write.VENDOR,
        )
        missing = [
            str(path.relative_to(ROOT)) for path in expected if not path.exists()
        ]
        self.assertEqual(
            missing, [], "Write validation requires every current contract artifact"
        )

    def test_current_artifacts_pass_the_offline_write_gate(self):
        write.validate_all()

    def test_canonical_contract_fixtures_are_schema_validated(self):
        fixtures = write.contract_fixture_items()
        for fixture in fixtures:
            with self.subTest(fixture=fixture["name"]):
                write.validate_contract_fixture(fixture)

        blocked = deepcopy(
            next(
                fixture
                for fixture in fixtures
                if fixture["name"] == "application-blocked-by-source-change"
            )
        )
        blocked["value"].pop("error")
        with self.assertRaises(ValidationError):
            write.validate_contract_fixture(blocked)

    def test_background_execution_fixtures_are_distinct_from_review(self):
        fixtures = {item["name"]: item for item in write.contract_fixture_items()}
        names = (
            "background-create-accepted",
            "background-create-running",
            "background-create-succeeded",
            "background-create-failed",
        )
        self.assertTrue(
            set(names) <= fixtures.keys(),
            "Canonical fixtures must show actual background execution",
        )
        for name in names:
            write.validate_contract_fixture(fixtures[name])
        accepted = fixtures[names[0]]["response"]
        self.assertEqual(accepted["status"], 202)
        self.assertEqual(accepted["body"]["status"], "pending")
        proposal = fixtures["governed-update-submission"]["response"]
        self.assertEqual(proposal["status"], 201)
        self.assertEqual(proposal["body"]["reviewState"], "pending")
        self.assertEqual(proposal["body"]["applicationState"], "not-started")
        with self.assertRaises(ValidationError):
            write.validate_schema_value(
                write.WRITE,
                {"$ref": "#/components/schemas/Operation"},
                proposal["body"],
            )
        wrong = deepcopy(accepted["body"])
        wrong["status"] = "awaiting-approval"
        with self.assertRaises(ValidationError):
            write.validate_schema_value(
                write.WRITE, {"$ref": "#/components/schemas/Operation"}, wrong
            )
        for name, outcome in ((names[2], "result"), (names[3], "error")):
            wrong = deepcopy(fixtures[name])
            wrong["response"]["body"].pop(outcome)
            with self.assertRaises(ValidationError):
                write.validate_contract_fixture(wrong)

    def test_write_capabilities_are_separate_and_normative(self):
        contract = yaml.safe_load(write.WRITE.read_text())
        selected = {
            value[write.EXTENSION]["capability"]
            for _route, _method, value in write.operations(contract)
            if write.EXTENSION in value
        }
        self.assertEqual(
            selected, {"create", "update", "transition", "change-requests"}
        )
        extension = json.loads(write.WRITE_EXTENSION_SCHEMA.read_text())
        self.assertFalse(extension["additionalProperties"])
        self.assertEqual(
            set(extension["properties"]["capability"]["enum"]),
            {"create", "update", "transition", "change-requests"},
        )

    def test_optional_purpose_metadata_has_only_trusted_bindings(self):
        schema = json.loads(write.WRITE_EXTENSION_SCHEMA.read_text())
        check = Draft202012Validator(schema, format_checker=FormatChecker())
        baseline = {
            "registry": "https://registry.example/registries/people",
            "collection": "individuals",
            "capability": "create",
            "inputSchema": "#/components/schemas/CreatePerson",
        }
        check.validate(baseline)
        check.validate(
            {
                **baseline,
                "purpose": {
                    "required": True,
                    "binding": "access-token-claim",
                    "claim": "purpose",
                    "allowedPurposes": [
                        "benefit-enrolment",
                        "https://policy.example/purposes/audit",
                    ],
                },
            }
        )
        check.validate(
            {
                **baseline,
                "purpose": {
                    "required": True,
                    "binding": "trusted-authorization-context",
                    "allowedPurposes": ["civil-registration"],
                },
            }
        )
        invalid_purposes = (
            {
                "required": False,
                "binding": "trusted-authorization-context",
                "allowedPurposes": ["audit"],
            },
            {
                "required": True,
                "binding": "access-token-claim",
                "allowedPurposes": ["audit"],
            },
            {
                "required": True,
                "binding": "trusted-authorization-context",
                "claim": "purpose",
                "allowedPurposes": ["audit"],
            },
            {
                "required": True,
                "binding": "trusted-authorization-context",
                "allowedPurposes": [],
            },
            {
                "required": True,
                "binding": "trusted-authorization-context",
                "allowedPurposes": ["bad purpose"],
            },
        )
        for purpose in invalid_purposes:
            with self.subTest(purpose=purpose):
                self.assertFalse(check.is_valid({**baseline, "purpose": purpose}))
        self.assertFalse(check.is_valid({**baseline, "requestPurpose": True}))

    def test_openapi_and_example_schema_are_complete_offline_documents(self):
        for path in (write.WRITE, write.EXAMPLE_API):
            with self.subTest(path=path.name):
                document = yaml.safe_load(path.read_text())
                self.assertTrue(document.get("paths"))
                self.assertTrue(document.get("components", {}).get("schemas"))
                write.validate_openapi(document, base_uri=path.as_uri())
        schema = json.loads(write.EXAMPLE_SCHEMA.read_text())
        self.assertTrue(schema.get("$defs"))
        Draft202012Validator.check_schema(schema)

    def test_normative_write_contract_is_independent_of_example_models(self):
        def dependency_closure(document):
            dependencies = set()
            pending = [(write.WRITE, document)]
            while pending:
                source, current = pending.pop()
                source = source.resolve()
                if source in dependencies:
                    continue
                dependencies.add(source)
                for _pointer, node in write.nodes(current):
                    if not isinstance(node, dict) or "$ref" not in node:
                        continue
                    target, _value = write.resolve_ref(source, node["$ref"])
                    if target.is_relative_to(API / "examples"):
                        dependencies.add(target)
                    elif target not in dependencies:
                        pending.append((target, write.load_document(target)))
            return dependencies

        canonical = write.load_document(write.WRITE)
        dependencies = dependency_closure(canonical)
        self.assertTrue(dependencies)
        self.assertFalse(
            any(path.is_relative_to(API / "examples") for path in dependencies),
            "The canonical Write contract must not depend on an example model",
        )
        mutated = deepcopy(canonical)
        mutated["components"]["schemas"]["DomainExampleDependency"] = {
            "$ref": "./examples/write-examples.schema.json"
        }
        self.assertTrue(
            any(
                path.is_relative_to(API / "examples")
                for path in dependency_closure(mutated)
            )
        )

        normative_documents = (
            ROOT / "requirements/registry-services.md",
            ROOT / "resources/write-binding.md",
        )
        for document in normative_documents:
            for target in re.findall(r"\]\(([^)]+)\)", document.read_text()):
                target, _fragment = urldefrag(target)
                if not target or urlparse(target).scheme:
                    continue
                resolved = (document.parent / target).resolve()
                if resolved.is_relative_to(API / "examples"):
                    self.assertEqual(
                        resolved,
                        API / "examples/README.md",
                        f"{document.name} must not require a domain-specific example",
                    )
                self.assertNotEqual(resolved.name, "publicschema-write-examples.md")

        toc = yaml.safe_load((ROOT / "toc.yml").read_text())
        self.assertNotIn("publicschema-write-examples.md", toc["toc"]["resources"])

    def test_unvendored_remote_schema_reference_is_rejected_offline(self):
        with self.assertRaises((ValueError, Unresolvable)):
            write.validate_schema_value(
                write.EXAMPLE_SCHEMA,
                {"$ref": "https://example.invalid/unvendored.schema.json"},
                {},
            )

    def test_offline_mirror_matches_raw_vendor_except_identifier_rewrites(self):
        write.validate_vendor_provenance()
        mirror = write.VENDOR / "offline/Person.schema.json"
        uri = mirror.resolve().as_uri()
        original = write.DOCUMENTS[uri]
        mutated = deepcopy(original)
        mutated["description"] = "Permissive handwritten replacement"
        write.DOCUMENTS[uri] = mutated
        try:
            with self.assertRaises(ValueError):
                write.validate_vendor_provenance()
        finally:
            write.DOCUMENTS[uri] = original

    def test_examples_use_fixed_named_transition_endpoints(self):
        example_api = yaml.safe_load(write.EXAMPLE_API.read_text())
        expected = {
            "correctBirth": (
                "/v1/collections/birth-registrations/records/{recordId}/correct-birth",
                "correct-birth",
            ),
            "addHouseholdMember": (
                "/v1/collections/households/records/{recordId}/add-member",
                "add-member",
            ),
        }
        actual = {
            value["operationId"]: (route, value[write.EXTENSION]["action"])
            for route, _method, value in write.operations(example_api)
            if value.get("operationId") in expected
        }
        self.assertEqual(actual, expected)

    def test_write_coverage_is_exact_and_cross_referenced(self):
        coverage = yaml.safe_load(write.WRITE_COVERAGE.read_text())
        contract = yaml.safe_load(write.WRITE.read_text())
        write.validate_write_coverage(coverage, contract)

        mutations = []
        duplicate = deepcopy(coverage)
        duplicate["draftRequirements"][1]["key"] = "write-1"
        mutations.append(duplicate)
        wrong_test = deepcopy(coverage)
        wrong_test["draftRequirements"][0]["test"] = (
            "resources/write-testing.md#write-2"
        )
        mutations.append(wrong_test)
        wrong_operation = deepcopy(coverage)
        wrong_operation["draftRequirements"][0]["operations"] = ["missingOperation"]
        mutations.append(wrong_operation)
        wrong_capability = deepcopy(coverage)
        wrong_capability["capabilities"][0]["metadataCapability"] = "update"
        mutations.append(wrong_capability)
        for mutation in mutations:
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                write.validate_write_coverage(mutation, contract)


class WriteContractMutationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.canonical = yaml.safe_load(write.WRITE.read_text())

    def validate_document(self, document, *, require_reference_surface=False):
        uri = write.WRITE.resolve().as_uri()
        missing = object()
        previous = write.DOCUMENTS.get(uri, missing)
        write.DOCUMENTS[uri] = document
        try:
            write.validate_write_document(
                document,
                write.WRITE,
                require_reference_surface=require_reference_surface,
            )
        finally:
            if previous is missing:
                write.DOCUMENTS.pop(uri, None)
            else:
                write.DOCUMENTS[uri] = previous

    def assert_rejected(self, document):
        with self.assertRaises((ValueError, ValidationError)):
            self.validate_document(document, require_reference_surface=True)

    def test_synchronous_only_profiles_need_no_operation_endpoint(self):
        synchronous = deepcopy(self.canonical)
        synchronous["paths"].pop("/v1/operations/{operationId}")
        for _route, _method, item in write.operations(synchronous):
            item.get("responses", {}).pop("202", None)
        self.validate_document(synchronous, require_reference_surface=True)
        write.validate_openapi(synchronous, base_uri=write.WRITE.as_uri())

    def test_direct_only_and_governed_only_profiles_are_valid_selections(self):
        direct = deepcopy(self.canonical)
        direct["paths"] = {
            route: item
            for route, item in direct["paths"].items()
            if route.startswith("/v1/collections/")
        }
        write.validate_write_document(
            direct, write.WRITE, require_reference_surface=False
        )

        governed = deepcopy(self.canonical)
        governed["paths"] = {
            route: item
            for route, item in governed["paths"].items()
            if route.startswith("/v1/change-requests")
            or route.startswith("/v1/operations/")
        }
        write.validate_write_document(
            governed, write.WRITE, require_reference_surface=False
        )

        renamed = deepcopy(self.canonical)
        counter = 0
        for _route, _method, operation_value in write.operations(renamed):
            if write.EXTENSION in operation_value:
                counter += 1
                operation_value["operationId"] = f"profileWriteOperation{counter}"
        write.validate_write_document(
            renamed, write.WRITE, require_reference_surface=False
        )

    def test_governed_profiles_can_select_one_or_more_typed_branches_independently(
        self,
    ):
        governed = deepcopy(self.canonical)
        governed["paths"] = {
            "/v1/change-requests": deepcopy(governed["paths"]["/v1/change-requests"])
        }
        submission = governed["paths"]["/v1/change-requests"]["post"]

        def proposal(kind, input_name):
            return {
                "type": "object",
                "properties": {
                    "kind": {"const": kind},
                    "input": {"$ref": f"#/components/schemas/{input_name}"},
                },
            }

        governed["components"]["schemas"]["CreateOnlyChangeRequest"] = {
            "oneOf": [proposal("create", "CreateInput")]
        }
        submission["requestBody"]["content"]["application/json"]["schema"] = {
            "$ref": "#/components/schemas/CreateOnlyChangeRequest"
        }
        submission[write.EXTENSION]["inputSchema"] = (
            "#/components/schemas/CreateOnlyChangeRequest"
        )
        self.validate_document(governed)

        multi = deepcopy(governed)
        multi["components"]["schemas"]["CreateOnlyChangeRequest"]["oneOf"] = [
            proposal("create", "CreateInput"),
            proposal("update", "UpdateInput"),
            proposal("transition", "TransitionInput"),
            proposal("create", "TransitionInput"),
        ]
        self.validate_document(multi)

        partial = deepcopy(governed)
        partial["paths"]["/v1/collections/{collectionId}/records"] = deepcopy(
            self.canonical["paths"]["/v1/collections/{collectionId}/records"]
        )
        partial["components"]["schemas"]["CreateOnlyChangeRequest"] = {
            "oneOf": [proposal("update", "UpdateInput")]
        }
        self.validate_document(partial)

    def test_withdraw_is_optional_in_a_change_request_profile(self):
        governed = deepcopy(self.canonical)
        governed["paths"] = {
            route: item
            for route, item in governed["paths"].items()
            if route.startswith("/v1/change-requests")
            or route.startswith("/v1/operations/")
        }
        governed["paths"].pop("/v1/change-requests/{changeRequestId}/withdraw")
        write.validate_write_document(
            governed, write.WRITE, require_reference_surface=False
        )

    def test_capability_and_input_schema_must_match_the_operation(self):
        broken = deepcopy(self.canonical)
        operation(broken, "updateRecord")[write.EXTENSION]["capability"] = "create"
        self.assert_rejected(broken)

        broken = deepcopy(self.canonical)
        operation(broken, "updateRecord")[write.EXTENSION]["inputSchema"] = (
            "#/components/schemas/TransitionInput"
        )
        self.assert_rejected(broken)

        broken = deepcopy(self.canonical)
        operation(broken, "updateRecord")["requestBody"]["content"][
            "application/merge-patch+json"
        ]["schema"] = {"$ref": "#/components/schemas/TransitionInput"}
        self.assert_rejected(broken)

    def test_preconditions_and_idempotency_are_required_and_typed(self):
        broken = deepcopy(self.canonical)
        without_parameter(
            operation(broken, "updateRecord"), "#/components/parameters/IfMatch"
        )
        self.assert_rejected(broken)

        broken = deepcopy(self.canonical)
        without_parameter(
            operation(broken, "approveChangeRequest"), "#/components/parameters/IfMatch"
        )
        self.assert_rejected(broken)

        broken = deepcopy(self.canonical)
        without_parameter(
            operation(broken, "createRecord"), "#/components/parameters/IdempotencyKey"
        )
        self.assert_rejected(broken)

        strong_etag = self.canonical["components"]["schemas"]["StrongETag"]
        for invalid in (
            'W/"weak"',
            "*",
            '"one", "two"',
            '"v1"\n',
            '"v\x001"',
            '"has space"',
            '"café"',
        ):
            with self.subTest(invalid=invalid), self.assertRaises(ValidationError):
                write.validate_schema_value(write.WRITE, strong_etag, invalid)

        broken = deepcopy(self.canonical)
        without_parameter(
            operation(broken, "withdrawChangeRequest"),
            "#/components/parameters/IfMatch",
        )
        self.assert_rejected(broken)

    def test_selected_operations_keep_distinct_oauth_scopes(self):
        broken = deepcopy(self.canonical)
        operation(broken, "createRecord").pop("security")
        self.assert_rejected(broken)

        broken = deepcopy(self.canonical)
        operation(broken, "submitChangeRequest")["security"] = [
            {"serviceOAuth": ["bb:digital-registries:record:write"]}
        ]
        self.assert_rejected(broken)

    def test_update_input_is_a_data_only_merge_patch_envelope(self):
        schema = self.canonical["components"]["schemas"]["UpdateInput"]
        write.validate_schema_value(
            write.WRITE, schema, {"data": {"optionalMember": None}}
        )
        for invalid in (
            {},
            {"data": {}},
            {
                "data": {"legalName": "Changed"},
                "source": {"system": "https://source.example", "revision": "7"},
            },
        ):
            with self.subTest(invalid=invalid), self.assertRaises(ValidationError):
                write.validate_schema_value(write.WRITE, schema, invalid)

    def test_idempotency_key_is_an_exact_structured_field_string(self):
        schema = self.canonical["components"]["parameters"]["IdempotencyKey"]["schema"]
        for valid in ('"opaque-123"', '"escaped\\\\backslash"', '"escaped\\"quote"'):
            with self.subTest(valid=valid):
                write.validate_schema_value(write.WRITE, schema, valid)
        for invalid in (
            "unquoted",
            '"line\nbreak"',
            '"control\x01"',
            '"café"',
            '"bad\\q"',
            '"trailing\\"',
        ):
            with self.subTest(invalid=invalid), self.assertRaises(ValidationError):
                write.validate_schema_value(write.WRITE, schema, invalid)

    def test_success_response_headers_and_bodylessness_are_enforced(self):
        broken = deepcopy(self.canonical)
        operation(broken, "createRecord")["responses"]["201"] = {
            "description": "Created without its resource location",
            "headers": {
                "Cache-Control": {"$ref": "#/components/headers/CacheControl"},
                "ETag": {"$ref": "#/components/headers/StrongETag"},
            },
            "content": {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/WriteResult"}
                }
            },
        }
        self.assert_rejected(broken)

    def test_problem_responses_fix_their_status_and_type(self):
        broken = deepcopy(self.canonical)
        operation(broken, "createRecord")["responses"]["409"] = {
            "description": "Generic error with no response-specific status or type",
            "headers": {"Cache-Control": {"$ref": "#/components/headers/CacheControl"}},
            "content": {
                "application/problem+json": {
                    "schema": {"$ref": "#/components/schemas/Problem"}
                }
            },
        }
        self.assert_rejected(broken)

        broken = deepcopy(self.canonical)
        operation(broken, "createRecord")["responses"]["422"] = {
            "description": "Wrong status contract",
            "headers": {"Cache-Control": {"$ref": "#/components/headers/CacheControl"}},
            "content": {
                "application/problem+json": {
                    "schema": {"$ref": "#/components/schemas/ConflictProblem"}
                }
            },
        }
        self.assert_rejected(broken)

        broken = deepcopy(self.canonical)
        operation(broken, "updateRecord")["responses"]["204"] = {
            "description": "Incorrectly includes a body",
            "headers": {
                "ETag": {"$ref": "#/components/headers/StrongETag"},
                "Cache-Control": {"$ref": "#/components/headers/CacheControl"},
            },
            "content": {"application/json": {"schema": {"type": "object"}}},
        }
        self.assert_rejected(broken)

        broken = deepcopy(self.canonical)
        operation(broken, "createRecord")["responses"]["202"] = {
            "description": "Accepted without an operation location",
            "headers": {"Cache-Control": {"$ref": "#/components/headers/CacheControl"}},
        }
        self.assert_rejected(broken)

    def test_references_and_operation_ids_resolve_uniquely(self):
        broken = deepcopy(self.canonical)
        operation(broken, "createRecord")["requestBody"]["content"]["application/json"][
            "schema"
        ] = {"$ref": "#/components/schemas/MissingInput"}
        self.assert_rejected(broken)

        broken = deepcopy(self.canonical)
        operation(broken, "updateRecord")["operationId"] = "createRecord"
        self.assert_rejected(broken)

    def test_clients_cannot_supply_authority_owned_control_fields(self):
        forbidden = ("actor", "purpose", "reviewState", "approval", "decision")
        for field in forbidden:
            with self.subTest(field=field):
                broken = deepcopy(self.canonical)
                operation(broken, "submitChangeRequest")["requestBody"] = {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {field: {"type": "string"}},
                            }
                        }
                    },
                }
                self.assert_rejected(broken)

    def test_review_comment_is_optional_and_cannot_carry_authority_fields(self):
        for operation_id in (
            "approveChangeRequest",
            "rejectChangeRequest",
            "withdrawChangeRequest",
        ):
            with self.subTest(operation=operation_id):
                self.assertFalse(
                    operation(self.canonical, operation_id)["requestBody"].get(
                        "required", False
                    )
                )
        schema = self.canonical["components"]["schemas"]["ReviewDecisionInput"]
        write.validate_schema_value(
            write.WRITE,
            schema,
            {"comment": "Reviewed against the submitted evidence."},
        )
        for invalid in (
            {},
            {"comment": ""},
            {"comment": "Valid", "actor": "client-selected"},
            {"comment": "Valid", "purpose": "client-selected"},
            {"comment": "Valid", "decision": "approved"},
            {"comment": "Valid", "reviewState": "approved"},
            {"comment": "Valid", "unknown": True},
        ):
            with self.subTest(invalid=invalid), self.assertRaises(ValidationError):
                write.validate_schema_value(write.WRITE, schema, invalid)


class WriteExchangeMutationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.exchanges = write.exchange_items()

    def exchange_for(self, operation_id, *, status=None):
        return deepcopy(
            next(
                exchange
                for exchange in self.exchanges
                if exchange["operationId"] == operation_id
                and (status is None or exchange["response"]["status"] == status)
            )
        )

    def exchange_named(self, fragment):
        return deepcopy(
            next(
                exchange for exchange in self.exchanges if fragment in exchange["name"]
            )
        )

    def exchange_status(self, status):
        return deepcopy(
            next(
                exchange
                for exchange in self.exchanges
                if exchange["response"]["status"] == status
            )
        )

    def test_every_published_exchange_matches_its_operation(self):
        for exchange in self.exchanges:
            with self.subTest(exchange=exchange["name"]):
                write.validate_exchange(write.EXAMPLE_API, exchange)

    def test_error_fixtures_distinguish_transport_and_body_validation(self):
        missing_key = self.exchange_named("individualCreateMissingIdempotencyKey")
        fingerprint = self.exchange_named(
            "individualCreateIdempotencyFingerprintMismatch"
        )
        semantic = self.exchange_named("individualCreateSemanticValidationFailure")
        protected = self.exchange_named("birthCorrectionProtectedTargetNotAvailable")
        stale_review = self.exchange_named(
            "birthCorrectionApprovalStaleProposalVersion"
        )

        self.assertEqual(
            missing_key["expectedRequestFailure"], "missing-required-header"
        )
        self.assertNotIn("errors", missing_key["response"]["body"])
        self.assertEqual(fingerprint["response"]["status"], 422)
        self.assertNotIn("errors", fingerprint["response"]["body"])
        self.assertEqual(semantic["expectedRequestFailure"], "schema-validation")
        self.assertTrue(semantic["response"]["body"]["errors"])
        self.assertEqual(protected["response"]["status"], 404)
        self.assertEqual(
            protected["response"]["body"]["type"],
            "https://govstack.global/problems/digital-registries/not-available",
        )
        self.assertEqual(stale_review["response"]["status"], 412)
        self.assertIn(
            "if-match", {name.casefold() for name in stale_review["request"]["headers"]}
        )

        wrong_status = deepcopy(fingerprint)
        wrong_status["response"]["body"]["status"] = 409
        with self.assertRaises((ValueError, ValidationError)):
            write.validate_exchange(write.EXAMPLE_API, wrong_status)

        wrong_type = deepcopy(semantic)
        wrong_type["response"]["body"]["type"] = fingerprint["response"]["body"]["type"]
        with self.assertRaises((ValueError, ValidationError)):
            write.validate_exchange(write.EXAMPLE_API, wrong_type)

        invalid_success = deepcopy(semantic)
        invalid_success["response"] = self.exchange_named("individualDirectApplied")[
            "response"
        ]
        with self.assertRaises(ValueError):
            write.validate_exchange(write.EXAMPLE_API, invalid_success)

    def test_headers_are_case_insensitive_but_required(self):
        exchange = self.exchange_status(204)
        exchange["request"]["headers"] = {
            name.upper(): value
            for name, value in exchange["request"]["headers"].items()
        }
        exchange["response"]["headers"] = {
            name.lower(): value
            for name, value in exchange["response"]["headers"].items()
        }
        write.validate_exchange(write.EXAMPLE_API, exchange)

        missing = self.exchange_status(204)
        header = next(
            name
            for name in missing["request"]["headers"]
            if name.casefold() == "if-match"
        )
        del missing["request"]["headers"][header]
        with self.assertRaises((ValueError, ValidationError)):
            write.validate_exchange(write.EXAMPLE_API, missing)

    def test_weak_preconditions_and_unquoted_idempotency_are_rejected(self):
        weak = self.exchange_status(204)
        header = next(
            name for name in weak["request"]["headers"] if name.casefold() == "if-match"
        )
        weak["request"]["headers"][header] = 'W/"weak"'
        with self.assertRaises((ValueError, ValidationError)):
            write.validate_exchange(write.EXAMPLE_API, weak)

        unquoted = self.exchange_named("birthDeclarationDirectApplied")
        header = next(
            name
            for name in unquoted["request"]["headers"]
            if name.casefold() == "idempotency-key"
        )
        unquoted["request"]["headers"][header] = "not-quoted"
        with self.assertRaises((ValueError, ValidationError)):
            write.validate_exchange(write.EXAMPLE_API, unquoted)

    def test_bodyless_204_rejects_a_body(self):
        exchange = self.exchange_status(204)
        exchange["response"]["body"] = {}
        with self.assertRaises(ValueError):
            write.validate_exchange(write.EXAMPLE_API, exchange)

    def test_change_request_state_negative_cases(self):
        applied = next(
            deepcopy(exchange)
            for exchange in self.exchanges
            if isinstance(exchange.get("response", {}).get("body"), dict)
            and exchange["response"]["body"].get("applicationState") == "applied"
        )
        del applied["response"]["body"]["result"]
        with self.assertRaises((ValueError, ValidationError)):
            write.validate_exchange(write.EXAMPLE_API, applied)

        pending = next(
            deepcopy(exchange)
            for exchange in self.exchanges
            if isinstance(exchange.get("response", {}).get("body"), dict)
            and exchange["response"]["body"].get("reviewState") == "pending"
        )
        pending["response"]["body"]["applicationState"] = "applied"
        with self.assertRaises((ValueError, ValidationError)):
            write.validate_exchange(write.EXAMPLE_API, pending)

        failed = next(
            deepcopy(exchange)
            for exchange in self.exchanges
            if isinstance(exchange.get("response", {}).get("body"), dict)
            and exchange["response"]["body"].get("applicationState")
            in {"blocked", "failed"}
        )
        failed["response"]["body"].pop("error", None)
        with self.assertRaises((ValueError, ValidationError)):
            write.validate_exchange(write.EXAMPLE_API, failed)

        wrong_target = self.exchange_named("individualApprovalPending")
        wrong_target["response"]["body"]["target"]["collectionId"] = "households"
        with self.assertRaises((ValueError, ValidationError)):
            write.validate_exchange(write.EXAMPLE_API, wrong_target)

        approval = self.exchange_named("birthCorrectionApprovalDecision")
        approval["response"]["body"]["applicationState"] = "applied"
        approval["response"]["body"]["result"] = {
            "collectionId": "birth-registrations",
            "recordId": "birth_19",
            "etag": '"birth-v9"',
        }
        with self.assertRaises((ValueError, ValidationError)):
            write.validate_exchange(write.EXAMPLE_API, approval)

        rejection = self.exchange_named("birthCorrectionApprovalRejected")
        rejection["response"]["body"]["reviewState"] = "approved"
        with self.assertRaises((ValueError, ValidationError)):
            write.validate_exchange(write.EXAMPLE_API, rejection)

    def test_change_request_target_etag_is_not_the_review_etag(self):
        approval = self.exchange_named("birthCorrectionApprovalDecision")
        request_headers = {
            name.casefold(): value
            for name, value in approval["request"]["headers"].items()
        }
        review_etag = request_headers["if-match"]
        body = approval["response"].get("body", {})
        self.assertIn("baseETag", body)
        self.assertNotEqual(review_etag, body["baseETag"])

    def test_request_local_references_and_results_resolve_exactly_once(self):
        baseline = self.exchange_named("householdCompoundDirectApplied")
        write.validate_request_local_mappings(baseline, {"collectionId": "households"})

        duplicate_declaration = deepcopy(baseline)
        data = duplicate_declaration["request"]["body"]["data"]
        data["memberships"][0]["person"]["@id"] = data["@id"]

        unresolved_reference = deepcopy(baseline)
        unresolved_reference["request"]["body"]["data"]["memberships"][0]["group"] = (
            "urn:request-local:missing-household"
        )

        duplicate_mapping = deepcopy(baseline)
        repeated = deepcopy(
            duplicate_mapping["response"]["body"]["requestLocalReferences"][0]
        )
        repeated["recordId"] = "household_other"
        duplicate_mapping["response"]["body"]["requestLocalReferences"].append(repeated)

        undeclared_mapping = deepcopy(baseline)
        undeclared_mapping["response"]["body"]["requestLocalReferences"][1][
            "requestLocalId"
        ] = "urn:request-local:invented-person"

        missing_mapping = deepcopy(baseline)
        missing_mapping["response"]["body"]["requestLocalReferences"].pop()

        wrong_collection = deepcopy(baseline)
        wrong_collection["response"]["body"]["requestLocalReferences"][1][
            "collectionId"
        ] = "households"

        cross_bound = deepcopy(baseline)
        cross_bound["response"]["body"]["requestLocalReferences"][0]["recordId"] = (
            "person_102"
        )

        for mutation in (
            duplicate_declaration,
            unresolved_reference,
            duplicate_mapping,
            undeclared_mapping,
            missing_mapping,
            wrong_collection,
            cross_bound,
        ):
            with self.subTest(mutation=mutation["name"]), self.assertRaises(ValueError):
                write.validate_request_local_mappings(
                    mutation, {"collectionId": "households"}
                )

        governed = deepcopy(
            next(
                exchange
                for exchange in self.exchanges
                if "householdCompound" in exchange["name"]
                and exchange.get("response", {}).get("body", {}).get("applicationState")
                == "applied"
            )
        )
        write.validate_request_local_mappings(governed, {})
        governed["response"]["body"]["result"]["requestLocalReferences"].pop()
        with self.assertRaises(ValueError):
            write.validate_request_local_mappings(governed, {})

    def test_transition_result_must_match_the_target_record(self):
        exchange = self.exchange_named("birthCorrectionDirectApplied")
        write.validate_request_local_mappings(
            exchange,
            {"collectionId": "birth-registrations", "recordId": "birth_19"},
        )
        exchange["response"]["body"]["recordId"] = "birth_other"
        with self.assertRaises(ValueError):
            write.validate_request_local_mappings(
                exchange,
                {"collectionId": "birth-registrations", "recordId": "birth_19"},
            )

    def test_domain_dates_and_source_timestamps_use_distinct_lexical_forms(self):
        domain_date_keys = {
            "event_date",
            "date_of_birth",
            "formation_date",
            "start_date",
        }
        timestamp_keys = {
            "issued_at",
            "issuedAt",
            "recordedAt",
            "submittedAt",
            "updatedAt",
            "completedAt",
        }
        dates = [
            pair
            for exchange in self.exchanges
            for pair in values_for_keys(exchange, domain_date_keys)
        ]
        timestamps = [
            pair
            for exchange in self.exchanges
            for pair in values_for_keys(exchange, timestamp_keys)
        ]
        self.assertTrue(dates)
        self.assertTrue(timestamps)
        for key, value in dates:
            with self.subTest(key=key, value=value):
                self.assertRegex(value, r"^\d{4}-\d{2}-\d{2}$")
        for key, value in timestamps:
            with self.subTest(key=key, value=value):
                self.assertRegex(
                    value, r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$"
                )

    def test_birth_declaration_rejects_authority_owned_and_unknown_fields(self):
        for field, value in (
            ("registration_status", "registered"),
            ("registration_date", "2026-10-30"),
            ("registrar", "https://authority.example/registrars/7"),
            ("identifiers", []),
            ("invented_field", "not in the declared command"),
        ):
            with self.subTest(field=field):
                exchange = self.exchange_named("birthDeclarationDirectApplied")
                exchange["request"]["body"]["data"]["birth"][field] = value
                with self.assertRaises((ValueError, ValidationError)):
                    write.validate_exchange(write.EXAMPLE_API, exchange)

        exchange = self.exchange_named("birthDeclarationDirectApplied")
        exchange["request"]["body"]["data"]["birth"]["child"]["person"]["@id"] = (
            "https://registry.example/v1/collections/individuals/records/person_999"
        )
        with self.assertRaises((ValueError, ValidationError)):
            write.validate_exchange(write.EXAMPLE_API, exchange)

    def test_example_create_and_correction_inputs_reject_identity_scope_bypass(self):
        individual = self.exchange_named("individualDirectApplied")
        individual["request"]["body"]["data"]["@id"] = (
            "https://registry.example/v1/collections/individuals/records/person_999"
        )
        with self.assertRaises((ValueError, ValidationError)):
            write.validate_exchange(write.EXAMPLE_API, individual)

        individual = self.exchange_named("individualDirectApplied")
        individual["request"]["body"]["data"]["group_memberships"] = [
            "arbitrary-group-ref"
        ]
        with self.assertRaises((ValueError, ValidationError)):
            write.validate_exchange(write.EXAMPLE_API, individual)

        household = self.exchange_named("householdExistingPersonsDirectApplied")
        household["request"]["body"]["data"]["identifiers"] = []
        with self.assertRaises((ValueError, ValidationError)):
            write.validate_exchange(write.EXAMPLE_API, household)

        for field in ("child", "parents", "informant"):
            with self.subTest(field=field):
                correction = self.exchange_named("birthCorrectionDirectApplied")
                correction["request"]["body"]["parameters"]["birthPatch"][field] = (
                    "arbitrary-record-reference"
                )
                with self.assertRaises((ValueError, ValidationError)):
                    write.validate_exchange(write.EXAMPLE_API, correction)


if __name__ == "__main__":
    unittest.main(verbosity=2)
