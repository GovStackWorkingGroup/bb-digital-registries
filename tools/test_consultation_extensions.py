#!/usr/bin/env python3
"""Regression checks for optional Consultation contract artifacts, not a runtime.

Run with the pinned dependencies in tools/requirements-api.txt. These tests
exercise published schemas, namespace routing, and concrete contract examples.
They do not establish source-history correctness or authorization enforcement.
"""

from copy import deepcopy
import json
import re
import unittest
from urllib.parse import urljoin

from jsonschema import Draft202012Validator, FormatChecker, ValidationError

import validate_consultation as consultation
from validate_specification import load_functionality
from validate_consultation import (
    API, CANONICAL, EXTENSION, EXTENSION_SCHEMA, OPENAPI_DOCUMENTS, REGISTRY,
    document, nodes, operation_parameters, resolve_object, route_kind,
    pointer_key, validate_capability_identities, validator,
)


REPOSITORY = API.parent
REQUIREMENTS = REPOSITORY / "requirements"
ROOT = "/v1/collections/{collectionId}"
ITEM = ROOT + "/records/{recordId}"


def schema(name):
    return validator(CANONICAL, "/components/schemas/" + name)


def operations():
    for contract in OPENAPI_DOCUMENTS:
        for route, item in document(contract)["paths"].items():
            for method, operation in item.items():
                if method in {"get", "post", "head"}:
                    yield contract, route, method, operation


def requirement_entries(name):
    errors = []
    data, _ = load_functionality(REQUIREMENTS / name, REPOSITORY, errors)
    if errors:
        raise AssertionError(errors)
    return data["requirements"]


def consultation_option_operations(entries):
    """Return the current Consultation option-to-operation declarations."""
    return {
        entry["key"]: entry["api_operation_id"]
        for entry in entries
        if entry.get("option_of") == "registry-service"
        and entry.get("key", "").startswith("consultation-")
        and entry.get("api_operation_id")
    }


def requirement_operations(entries, option_operations):
    """Return operations covered by matching option applicability in the front matter."""
    operations = set()
    for entry in entries:
        applicable = {
            option_operations[key]
            for key in entry.get("applies_when", ())
            if key in option_operations
        }
        if entry.get("api_operation_id"):
            if entry["api_operation_id"] in applicable:
                operations.add(entry["api_operation_id"])
        else:
            operations.update(applicable)
    return operations


def requirements_for_test(entries, test):
    return [entry for entry in entries if entry.get("test") == test]


def assert_requirement_coverage(entries, option_operations, test, expected):
    actual = requirement_operations(requirements_for_test(entries, test), option_operations)
    missing = sorted(expected - actual)
    unexpected = sorted(actual - expected)
    if missing or unexpected:
        raise AssertionError(
            f"{test} operation coverage differs: "
            f"missing={missing or 'none'}, unexpected={unexpected or 'none'}"
        )


def assert_source_verification(entries, test):
    matched = requirements_for_test(entries, test)
    if not matched:
        raise AssertionError(f"{test} has no current requirement entries")
    for entry in matched:
        evidence = verification(entry)
        if not re.search(r"\bsource (?:fixtures|evidence)\b", evidence):
            operation = entry.get("api_operation_id", "requirement without operationId")
            raise AssertionError(
                f"{test} {operation} verification must use source fixtures or source evidence"
            )


def verification(entry):
    for line in entry["documentation"].splitlines():
        if line.startswith("Verification:"):
            return line
    operation = entry.get("api_operation_id", "requirement without operationId")
    raise AssertionError(f"{operation} is missing a Verification section")


class ConsultationExtensionTests(unittest.TestCase):
    def test_consultation_classifier_excludes_mutations_on_shared_routes(self):
        self.assertEqual(
            consultation.route_kind(
                "/v1/collections/{collectionId}/records", "get"
            ),
            ("get", "collection"),
        )
        self.assertIsNone(
            consultation.route_kind(
                "/v1/collections/{collectionId}/records", "post"
            )
        )
        self.assertEqual(
            consultation.route_kind(
                "/v1/collections/{collectionId}/search", "post"
            ),
            ("post", "search"),
        )
        self.assertIsNone(
            consultation.route_kind(
                "/v1/collections/{collectionId}/records/{recordId}", "patch"
            )
        )

    def test_exchange_validator_covers_headers_bodyless_304_and_parent_identity(self):
        success = {
            "name": "businessConditionalRetrieve200",
            "operationId": "retrieveBusiness",
            "request": {
                "path": {"recordId": "r_42"},
                "headers": {"if-none-match": 'W/"business-public-r42-v6"'},
            },
            "response": {
                "status": 200,
                "headers": {"etag": 'W/"business-public-r42-v7"', "cache-control": "no-store"},
                "body": {"recordId": "r_42", "data": {"legalName": "Example Ltd"}},
            },
        }
        not_modified = {
            "name": "businessConditionalRetrieve304",
            "operationId": "retrieveBusiness",
            "request": {
                "path": {"recordId": "r_42"},
                "headers": {"IF-NONE-MATCH": 'W/"business-public-r42-v7"'},
            },
            "response": {
                "status": 304,
                "headers": {"ETag": 'W/"business-public-r42-v7"', "Cache-Control": "no-store"},
            },
        }
        consultation.validate_exchange(API / "examples/business-registry.openapi.yaml", success)
        consultation.validate_exchange(API / "examples/business-registry.openapi.yaml", not_modified)
        consultation.validate_conditional_exchange_pair(success, not_modified)

        not_found = {
            "name": "businessRecordNotAvailable",
            "operationId": "retrieveBusiness",
            "request": {"path": {"recordId": "r_missing"}},
            "response": {
                "status": 404,
                "body": {
                    "type": "https://govstack.global/problems/digital-registries/record-not-available",
                    "title": "Record not available",
                    "status": 404,
                    "traceId": "6f1c3f0e2a9b4c8d7e6f5a4b3c2d1e0f",
                },
            },
        }
        consultation.validate_exchange(API / "examples/business-registry.openapi.yaml", not_found)

        malformed_header = deepcopy(not_modified)
        malformed_header["request"]["headers"]["IF-NONE-MATCH"] = 42
        missing_etag = deepcopy(not_modified)
        del missing_etag["response"]["headers"]["ETag"]
        body_on_304 = deepcopy(not_modified)
        body_on_304["response"]["body"] = {"recordId": "r_42", "data": {}}
        for exchange in (malformed_header, missing_etag, body_on_304):
            with self.subTest(exchange=exchange["name"], mutation=exchange):
                with self.assertRaises((ValidationError, ValueError)):
                    consultation.validate_exchange(
                        API / "examples/business-registry.openapi.yaml", exchange)

        mismatched = deepcopy(not_modified)
        mismatched["response"]["headers"]["ETag"] = 'W/"business-public-r42-v8"'
        with self.assertRaises(ValueError):
            consultation.validate_conditional_exchange_pair(success, mismatched)
        changed_path = deepcopy(not_modified)
        changed_path["request"]["path"]["recordId"] = "r_other"
        with self.assertRaises(ValueError):
            consultation.validate_conditional_exchange_pair(success, changed_path)
        changed_query = deepcopy(not_modified)
        changed_query["request"]["query"] = {"fields": ["legalName"]}
        with self.assertRaises(ValueError):
            consultation.validate_conditional_exchange_pair(success, changed_query)

        exchanges = json.loads((API / "examples/consultation-extension-exchanges.json").read_text())["exchanges"]
        revision_list = deepcopy(next(
            exchange for exchange in exchanges
            if exchange["operationId"] == "listBirthRegistrationRevisions"))
        revision_list["response"]["body"]["items"][0]["recordId"] = "birth_wrong"
        with self.assertRaises(ValueError):
            consultation.validate_exchange(API / "examples/birth-registration.openapi.yaml", revision_list)

        revision = deepcopy(next(
            exchange for exchange in exchanges
            if exchange["operationId"] == "retrieveBirthRegistrationRevision"))
        wrong_revision_parent = deepcopy(revision)
        wrong_revision_parent["response"]["body"]["recordId"] = "birth_wrong"
        with self.assertRaises(ValueError):
            consultation.validate_exchange(
                API / "examples/birth-registration.openapi.yaml", wrong_revision_parent)
        revision["response"]["body"]["revision"]["revisionId"] = "rev-wrong"
        with self.assertRaises(ValueError):
            consultation.validate_exchange(API / "examples/birth-registration.openapi.yaml", revision)

    def test_published_optional_exchanges_use_their_actual_operation_contracts(self):
        declared = {operation["operationId"]: (contract, route, method, operation)
                    for contract, route, method, operation in operations()}
        exchanges = json.loads((API / "examples/consultation-extension-exchanges.json").read_text())["exchanges"]
        seen = set()
        for exchange in exchanges:
            with self.subTest(exchange=exchange["name"]):
                contract, route, method, operation = declared[exchange["operationId"]]
                seen.add(operation["operationId"])
                consultation.validate_exchange(contract, exchange)
                request = exchange["request"]
                response = exchange["response"]
                selected = {key: value for key, value in request.get("query", {}).items()
                            if key in {"recordedAsOf", "effectiveAt"}}
                selected.update(request.get("body", {}).get("temporal", {}))
                if response["status"] == 200 and selected:
                    self.assertEqual(response["body"].get("temporal"), selected)
                elif response["status"] == 200:
                    self.assertNotIn("temporal", response["body"])
        conditional = {exchange["name"]: exchange for exchange in exchanges
                       if exchange["name"].startswith("businessConditionalRetrieve")}
        self.assertEqual(set(conditional), {
            "businessConditionalRetrieve200", "businessConditionalRetrieve304"})
        consultation.validate_conditional_exchange_pair(
            conditional["businessConditionalRetrieve200"],
            conditional["businessConditionalRetrieve304"],
        )
        self.assertTrue({"retrieveBirthRegistration", "searchBirthRegistrations",
                         "listBirthRegistrationRevisions", "retrieveBirthRegistrationRevision",
                         "getCallerCapabilities"}.issubset(seen))

    def test_discovery_rejects_conflicting_duplicate_identities(self):
        operation = {"contract": "https://registry.example/contracts/1.0.0-draft/openapi.yaml",
                     "operationId": "retrieveRecord", "capability": "retrieve"}
        collection = {"registry": "https://registry.example/registries/records",
                      "collectionId": "records", "operations": [operation]}
        validate_capability_identities({"collections": [collection]})
        duplicate_collection = {"collections": [collection, {**collection, "operations": []}]}
        duplicate_operation = {"collections": [{**collection, "operations": [
            operation, {**operation, "capability": "search"}]}]}
        for invalid in (duplicate_collection, duplicate_operation):
            with self.assertRaises(ValueError):
                validate_capability_identities(invalid)

    def test_published_extension_fixtures_accept_and_refuse_declared_cases(self):
        fixtures = json.loads((API / "examples/consultation-extension-fixtures.json").read_text())
        tested = set()
        for group in fixtures["schemas"]:
            name = group["schema"]
            check = validator(CANONICAL, name) if name.startswith("/") else schema(name)
            self.assertTrue(group["valid"], name)
            self.assertTrue(group["invalid"], name)
            for value in group["valid"]:
                with self.subTest(schema=name, valid=value):
                    check.validate(value)
            for value in group["invalid"]:
                with self.subTest(schema=name, invalid=value):
                    self.assertFalse(check.is_valid(value))
            tested.add(name.rsplit("/", 1)[-1])
        self.assertTrue({"TemporalSelection", "RecordRevision", "CallerCapabilities",
                         "SearchRange", "SearchSet", "SearchPrefix"}.issubset(tested))
        check = validator(EXTENSION_SCHEMA, "")
        self.assertTrue(fixtures["extension"]["valid"])
        self.assertTrue(fixtures["extension"]["invalid"])
        for value in fixtures["extension"]["valid"]:
            check.validate(value)
        for value in fixtures["extension"]["invalid"]:
            self.assertFalse(check.is_valid(value), value)

    def test_route_classifier_separates_supporting_resources_from_record_reads(self):
        for route in ("/v1/capabilities", "/health", "/.well-known/api-catalog",
                      ROOT, ROOT + "/schemas"):
            self.assertIsNone(route_kind(route, "get"), route)
        for route, kind in ((ITEM, "item"), (ROOT + "/records", "collection"),
                            (ITEM + "/revisions", "revision-list"),
                            (ITEM + "/revisions/{revisionId}", "revision-retrieve")):
            self.assertEqual(route_kind(route, "get"), ("get", kind))
            self.assertIsNone(route_kind(route, "parameters"))

    def test_collection_record_namespace_has_no_action_identifier_collision(self):
        paths = document(CANONICAL)["paths"]
        for path in (ROOT + "/records", ITEM, ROOT + "/lookup", ROOT + "/search"):
            self.assertIn(path, paths)
        for identifier in ("lookup", "search", "revisions", "capabilities", "r_42"):
            schema("RecordId").validate(identifier)
            request = ITEM.replace("{collectionId}", "records").replace("{recordId}", identifier)
            matches = [route for route in paths if re.fullmatch(
                re.sub(r"\{[^{}]+\}", "[^/]+", route), request)]
            self.assertEqual(matches, [ITEM], request)
        for _, route, _, operation in operations():
            if EXTENSION in operation:
                self.assertTrue(route.startswith("/v1/collections/"), route)

    def test_reference_collection_is_constrained_not_an_untyped_dispatch(self):
        check = schema("CollectionId")
        check.validate("records")
        for value in ("", "other-registry", "../records", "records/people"):
            self.assertFalse(check.is_valid(value), value)
        for route, item in document(CANONICAL)["paths"].items():
            if "{collectionId}" not in route:
                continue
            for method in ("get", "post"):
                if method not in item:
                    continue
                parameters = [p for _, p in operation_parameters(CANONICAL, item[method])]
                self.assertTrue(any(p["name"] == "collectionId" and p["in"] == "path"
                                    and p["required"] for p in parameters), route)

    def test_history_operations_are_independently_declared(self):
        paths = document(CANONICAL)["paths"]
        for suffix, capability in (("/revisions", "revision-list"),
                                   ("/revisions/{revisionId}", "revision-retrieve")):
            operation = paths[ITEM + suffix]["get"]
            self.assertEqual(operation[EXTENSION]["capability"], capability)
            self.assertIn("404", operation["responses"])
            validator(EXTENSION_SCHEMA, "").validate(operation[EXTENSION])

    def test_current_requirement_front_matter_covers_consultation_operations(self):
        coverage = document(API / "coverage.yaml")
        self.assertEqual(coverage["draftRequirements"], [])

        entries = requirement_entries("registry-services.md")
        expected_options = {
            "consultation-retrieve": "retrieveRecord",
            "consultation-lookup": "lookupRecord",
            "consultation-list": "listRecords",
            "consultation-search": "searchRecords",
            "consultation-revision-list": "listRecordRevisions",
            "consultation-revision-retrieve": "retrieveRecordRevision",
        }
        options = consultation_option_operations(entries)
        self.assertEqual(options, expected_options)
        all_reads = set(expected_options.values())
        for test in ("resources/testing.md#core-2", "resources/testing.md#core-4",
                     "resources/testing.md#core-5", "resources/testing.md#core-6",
                     "resources/testing.md#core-8", "resources/testing.md#consultation-2"):
            with self.subTest(test=test):
                assert_requirement_coverage(entries, options, test, all_reads)

        protected = {"retrieveRecord", "lookupRecord", "listRecordRevisions",
                     "retrieveRecordRevision"}
        assert_requirement_coverage(
            entries, options, "resources/testing.md#consultation-3", protected)
        paged = {"listRecords", "searchRecords", "listRecordRevisions"}
        assert_requirement_coverage(
            entries, options, "resources/testing.md#consultation-7", paged)
        for test in ("resources/testing.md#core-5", "resources/testing.md#core-6"):
            with self.subTest(test=test):
                assert_source_verification(entries, test)

        revision_metadata = document(CANONICAL)["components"]["schemas"]["RevisionMetadata"]
        self.assertIn("revisionId", revision_metadata["required"])
        self.assertIn("recordedAt", revision_metadata["properties"])

    def test_current_requirement_checks_detect_missing_applicability_and_source_evidence(self):
        entries = requirement_entries("registry-services.md")
        options = consultation_option_operations(entries)
        all_reads = set(options.values())

        missing_applicability = deepcopy(entries)
        target = next(
            entry for entry in missing_applicability
            if entry.get("test") == "resources/testing.md#core-5"
            and entry.get("api_operation_id") == "retrieveRecord"
        )
        target["applies_when"] = []
        with self.assertRaisesRegex(AssertionError, r"missing=\['retrieveRecord'\]"):
            assert_requirement_coverage(
                missing_applicability, options, "resources/testing.md#core-5", all_reads)

        missing_source_evidence = deepcopy(entries)
        target = next(
            entry for entry in missing_source_evidence
            if entry.get("test") == "resources/testing.md#core-5"
            and entry.get("api_operation_id") == "retrieveRecord"
        )
        target["documentation"] = re.sub(
            r"\bsource (?:fixtures|evidence)\b", "published examples", target["documentation"])
        with self.assertRaisesRegex(
                AssertionError, r"core-5 retrieveRecord verification must use source"):
            assert_source_verification(missing_source_evidence, "resources/testing.md#core-5")

    def test_revision_schema_requires_source_revision_identity(self):
        record = {"recordId": "r_42", "data": {}, "revision": {"revisionId": "rev-2"}}
        check = schema("RecordRevision")
        check.validate(record)
        check.validate({**record, "revision": {"revisionId": "rev-2", "recordedAt": "2026-06-02T09:00:00Z"}})
        for invalid in ({"recordId": "r_42", "data": {}},
                        {**record, "revision": {}},
                        {**record, "revision": {"revisionId": ""}},
                        {**record, "revision": {"revisionId": "rev-2", "recordedAt": "yesterday"}}):
            self.assertFalse(check.is_valid(invalid), invalid)
        page = schema("RevisionPage")
        page.validate({"items": [record], "pageInfo": {"nextCursor": None}})
        self.assertFalse(page.is_valid({"items": [{"recordId": "r_42", "data": {}}],
                                       "pageInfo": {"nextCursor": None}}))

    def test_temporal_selection_is_typed_closed_and_nonempty(self):
        check = schema("TemporalSelection")
        for value in ({"recordedAsOf": "2026-04-20T00:00:00Z"},
                      {"effectiveAt": "2026-04-10"},
                      {"effectiveAt": "2026-04-10T12:00:00Z"},
                      {"recordedAsOf": "2026-06-03T00:00:00Z", "effectiveAt": "2026-04-10"}):
            check.validate(value)
        for value in ({}, {"recordedAsOf": "2026-04-20"},
                      {"recordedAsOf": "2026-04-20T00:00:00"},
                      {"effectiveAt": "2026-02-30"}, {"effectiveAt": None},
                      {"birthDate": "2026-04-10"},
                      {"recordedAsOf": "2026-06-03T00:00:00Z", "purpose": "anything"}):
            self.assertFalse(check.is_valid(value), value)

    def test_shared_timestamp_schemas_require_utc_z(self):
        valid = ("2026-04-20T12:34:56Z", "2026-04-20T12:34:56.123456Z")
        invalid = ("2026-04-20T12:34:56+07:00", "2026-04-20T12:34:56+00:00",
                   "2026-04-20T12:34:56-00:00", "2026-04-20T12:34:56z",
                   "2026-04-20T12:34:56", "2026-04-20T12:34:56Z\n")
        checks = {
            "RecordedAsOf": (schema("RecordedAsOf"), lambda value: value),
            "EffectiveAt": (schema("EffectiveAt"), lambda value: value),
            "RevisionMetadata.recordedAt": (
                schema("RevisionMetadata"),
                lambda value: {"revisionId": "rev-2", "recordedAt": value},
            ),
        }
        for name, (check, wrap) in checks.items():
            for value in valid:
                with self.subTest(schema=name, valid=value):
                    check.validate(wrap(value))
            for value in invalid:
                with self.subTest(schema=name, invalid=value):
                    self.assertFalse(check.is_valid(wrap(value)), value)
        schema("EffectiveAt").validate("2026-04-20")

    def test_temporal_input_locations_follow_declared_features(self):
        witnessed = set()
        for contract, route, method, operation in operations():
            if EXTENSION not in operation:
                continue
            features = set(operation[EXTENSION].get("features", []))
            temporal = features & {"recorded-time", "effective-time"}
            if not temporal:
                continue
            witnessed.update(temporal)
            if method == "get":
                names = {p["name"] for _, p in operation_parameters(contract, operation)
                         if p["in"] == "query"}
                self.assertEqual("recordedAsOf" in names, "recorded-time" in temporal, route)
                self.assertEqual("effectiveAt" in names, "effective-time" in temporal, route)
            elif method == "post":
                source, body = resolve_object(contract, operation["requestBody"])
                _, body_schema = resolve_object(source, body["content"]["application/json"]["schema"])
                self.assertIn("temporal", body_schema.get("properties", {}), route)
        self.assertEqual(witnessed, {"recorded-time", "effective-time"})

    def test_baseline_post_reads_do_not_accept_unselected_temporal_features(self):
        for name, request in (("LookupRequest", {"selector": "byCode", "values": {"code": "42"}}),
                              ("SearchRequest", {"search": "byStatus", "criteria": {"status": "ACTIVE"}})):
            check = schema(name)
            check.validate(request)
            self.assertFalse(check.is_valid({**request, "temporal": {"effectiveAt": "2026-04-10"}}))
            self.assertFalse(check.is_valid({**request, "purpose": "self-declared-authority"}))

    def test_purpose_requires_a_trusted_binding_and_controlled_values(self):
        base = {"registry": "https://registry.example/registries/business",
                "collection": "businesses", "capability": "retrieve", "view": "public",
                "features": ["purpose-bound"]}
        purpose = {"required": True, "binding": "access-token-claim", "claim": "purpose",
                   "allowedPurposes": ["benefit-eligibility"]}
        check = validator(EXTENSION_SCHEMA, "")
        check.validate({**base, "purpose": purpose})
        check.validate({**base, "purpose": {**purpose, "allowedPurposes": ["https://policy.example/purposes/benefit-eligibility"]}})
        check.validate({**base, "purpose": {"required": True, "binding": "trusted-authorization-context",
                                            "allowedPurposes": ["benefit-eligibility"]}})
        for invalid in (base, {**base, "purpose": {}},
                        {**base, "purpose": {**purpose, "binding": "request-query"}},
                        {**base, "purpose": {**purpose, "claim": ""}},
                        {**base, "purpose": {**purpose, "allowedPurposes": []}},
                        {**base, "purpose": {**purpose, "allowedPurposes": ["benefit-eligibility"] * 2}}):
            self.assertFalse(check.is_valid(invalid), invalid)
        self.assertFalse(check.is_valid({**base, "features": [], "purpose": purpose}))
        for capability in ("revision-list", "revision-retrieve"):
            self.assertFalse(check.is_valid({**base, "capability": capability,
                                            "features": ["recorded-time"]}))

    def test_discovery_operation_features_obey_the_same_selection_dependencies(self):
        check = schema("CapabilityOperation")
        operation = {"contract": "https://registry.example/contracts/1.0.0-draft/openapi.yaml",
                     "operationId": "listRecords", "capability": "list", "view": "public"}
        check.validate(operation)
        self.assertFalse(check.is_valid({key: value for key, value in operation.items() if key != "view"}))
        check.validate({**operation, "features": ["complete-traversal", "snapshot-traversal"]})
        for invalid in ({**operation, "features": ["snapshot-traversal"]},
                        {**operation, "features": ["conditional-read"]},
                        {**operation, "features": ["purpose-bound"]},
                        {**operation, "capability": "revision-list", "features": ["effective-time"]}):
            self.assertFalse(check.is_valid(invalid), invalid)

    def test_write_discovery_forbids_top_level_read_purpose(self):
        check = schema("CapabilityOperation")
        operation = {
            "operationId": "updateRecord",
            "contract": "https://registry.example/contracts/1.0.0-draft/openapi.yaml",
            "family": "write",
            "capability": "update",
            "write": {
                "companionRead": {
                    "operationId": "retrieveRecord",
                    "view": "record-public",
                }
            },
        }
        check.validate(operation)
        self.assertFalse(
            check.is_valid(
                {
                    **operation,
                    "purpose": {
                        "required": True,
                        "binding": "trusted-authorization-context",
                        "allowedPurposes": ["record-correction"],
                    },
                }
            )
        )

    def test_temporal_search_example_echoes_selection_on_empty_pages(self):
        witnessed = False
        for contract, _, method, operation in operations():
            if method != "post" or operation.get(EXTENSION, {}).get("capability") != "search":
                continue
            _, body = resolve_object(contract, operation["requestBody"])
            request = body["content"]["application/json"].get("example", {})
            if "temporal" not in request:
                continue
            _, response = resolve_object(contract, operation["responses"]["200"])
            example = response["content"]["application/json"].get("example")
            if example is not None:
                self.assertEqual(example.get("temporal"), request["temporal"])
                witnessed = witnessed or not example["items"]
        self.assertTrue(witnessed, "A temporal search must illustrate an empty Page with selection context")

    def test_crvs_named_search_keeps_occurrence_criteria_typed_and_separate(self):
        contract = API / "examples/birth-registration.openapi.yaml"
        route = "/v1/collections/birth-registrations/search"
        operation = document(contract)["paths"][route]["post"]
        _, body = resolve_object(contract, operation["requestBody"])
        sample = body["content"]["application/json"]["example"]
        check = validator(contract, "/paths/" + route.replace("/", "~1") +
                          "/post/requestBody/content/application~1json/schema")
        check.validate(sample)
        current = deepcopy(sample)
        current.pop("temporal", None)
        check.validate(current)
        for criteria in ({"occurrencePeriod": {"from": "2026-02-30"}},
                         {"occurrencePeriod": {"from": 42}},
                         {"occurrencePeriod": {}},
                         {"occurrencePeriod": {"from": "2026-01-01", "operator": "sql"}},
                         {"placePrefix": ""},
                         {"placePrefix": {"text": "Example", "fuzzy": True}},
                         {"filter": "dateOfBirth > anything"}):
            invalid = {**current, "criteria": criteria}
            self.assertFalse(check.is_valid(invalid), invalid)

    def test_concrete_temporal_responses_validate_metadata_when_present(self):
        contract = API / "examples/birth-registration.openapi.yaml"
        cases = (("/v1/collections/birth-registrations/records/{recordId}", "get"),
                 ("/v1/collections/birth-registrations/search", "post"))
        for route, method in cases:
            operation = document(contract)["paths"][route][method]
            _, response = resolve_object(contract, operation["responses"]["200"])
            media = response["content"]["application/json"]
            sample = deepcopy(media.get("example", next(iter(media.get("examples", {}).values()), {}).get("value")))
            check = validator(contract, "/paths/" + pointer_key(route) + "/" + method +
                              "/responses/200/content/application~1json/schema")
            sample.pop("temporal", None)
            check.validate(sample)
            for context in ({}, "yesterday", {"effectiveAt": "2026-02-30"},
                            {"recordedAsOf": "2026-04-10"}, {"birthDate": "2020-06-12"}):
                self.assertFalse(check.is_valid({**sample, "temporal": context}), (route, context))

    def test_birth_registration_effective_time_is_date_only_in_published_operations(self):
        contract = API / "examples/birth-registration.openapi.yaml"
        retrieve_route = "/v1/collections/birth-registrations/records/{recordId}"
        search_route = "/v1/collections/birth-registrations/search"
        retrieve = document(contract)["paths"][retrieve_route]["get"]
        search = document(contract)["paths"][search_route]["post"]
        date = "2020-07-15"
        instant = "2020-07-15T12:34:56Z"
        recorded = "2026-06-03T00:00:00.123Z"

        parameter_checks = {}
        for source, parameter in operation_parameters(contract, retrieve):
            if parameter["name"] not in {"recordedAsOf", "effectiveAt"}:
                continue
            parameter_schema = parameter["schema"]
            if "$ref" in parameter_schema:
                parameter_schema = {"$ref": urljoin(source.as_uri(), parameter_schema["$ref"])}
            parameter_checks[parameter["name"]] = Draft202012Validator(
                parameter_schema, registry=REGISTRY, format_checker=FormatChecker())
        self.assertEqual(set(parameter_checks), {"recordedAsOf", "effectiveAt"})
        parameter_checks["recordedAsOf"].validate(recorded)
        parameter_checks["effectiveAt"].validate(date)
        with self.subTest(surface="retrieve effectiveAt query parameter"):
            self.assertFalse(parameter_checks["effectiveAt"].is_valid(instant))

        request_check = validator(
            contract,
            "/paths/" + pointer_key(search_route) + "/post/requestBody/content/application~1json/schema",
        )
        _, request_body = resolve_object(contract, search["requestBody"])
        request = deepcopy(request_body["content"]["application/json"]["example"])
        request["temporal"] = {"recordedAsOf": recorded, "effectiveAt": date}
        request_check.validate(request)
        recorded_request = deepcopy(request)
        recorded_request["temporal"] = {"recordedAsOf": recorded}
        request_check.validate(recorded_request)
        instant_request = deepcopy(request)
        instant_request["temporal"]["effectiveAt"] = instant
        with self.subTest(surface="search request temporal effectiveAt"):
            self.assertFalse(request_check.is_valid(instant_request))

        _, retrieve_response = resolve_object(contract, retrieve["responses"]["200"])
        retrieve_media = retrieve_response["content"]["application/json"]
        record = deepcopy(retrieve_media["examples"]["selectedState"]["value"])
        retrieve_check = validator(
            contract,
            "/paths/" + pointer_key(retrieve_route) + "/get/responses/200/content/application~1json/schema",
        )
        record["temporal"] = {"recordedAsOf": recorded, "effectiveAt": date}
        retrieve_check.validate(record)
        recorded_record = deepcopy(record)
        recorded_record["temporal"] = {"recordedAsOf": recorded}
        retrieve_check.validate(recorded_record)
        instant_record = deepcopy(record)
        instant_record["temporal"]["effectiveAt"] = instant
        with self.subTest(surface="retrieve response temporal effectiveAt"):
            self.assertFalse(retrieve_check.is_valid(instant_record))

        _, search_response = resolve_object(contract, search["responses"]["200"])
        page = deepcopy(search_response["content"]["application/json"]["example"])
        page["temporal"] = {"recordedAsOf": recorded, "effectiveAt": date}
        page["items"] = [deepcopy(record)]
        page_check = validator(
            contract,
            "/paths/" + pointer_key(search_route) + "/post/responses/200/content/application~1json/schema",
        )
        page_check.validate(page)
        recorded_page = deepcopy(page)
        recorded_page["temporal"] = {"recordedAsOf": recorded}
        recorded_page["items"][0]["temporal"] = {"recordedAsOf": recorded}
        page_check.validate(recorded_page)
        instant_page = deepcopy(page)
        instant_page["temporal"]["effectiveAt"] = instant
        with self.subTest(surface="page response temporal effectiveAt"):
            self.assertFalse(page_check.is_valid(instant_page))
        instant_item = deepcopy(page)
        instant_item["items"][0]["temporal"]["effectiveAt"] = instant
        with self.subTest(surface="page item temporal effectiveAt"):
            self.assertFalse(page_check.is_valid(instant_item))

    def test_current_reference_bindings_use_the_collection_record_namespace(self):
        relationship = document(API / "examples/relationship-examples.schema.json")
        description = relationship["$defs"]["IndividualReference"]["description"]
        self.assertIn("/v1/collections/individuals/records/{recordId}", description)
        self.assertNotIn("/v1/individuals/", description)

    def test_discovery_is_authenticated_bounded_and_private(self):
        operation = document(CANONICAL)["paths"]["/v1/capabilities"]["get"]
        security = operation.get("security", document(CANONICAL)["security"])
        self.assertNotEqual(security, [])
        self.assertTrue(
            all(
                scopes == []
                for requirement in security
                for scopes in requirement.values()
            ),
            "Discovery authenticates without requiring a Record-read grant",
        )
        response_path, response = resolve_object(CANONICAL, operation["responses"]["200"])
        self.assertIn("Cache-Control", response["headers"])
        _, cache_control = resolve_object(response_path, response["headers"]["Cache-Control"])
        self.assertTrue(cache_control.get("required", False))
        self.assertEqual(cache_control["schema"].get("const"), "no-store")

        exchanges = json.loads((API / "examples/consultation-extension-exchanges.json").read_text())["exchanges"]
        missing_cache_control = deepcopy(next(
            exchange for exchange in exchanges
            if exchange["operationId"] == "getCallerCapabilities" and exchange["response"]["status"] == 200))
        missing_cache_control["response"].pop("headers", None)
        with self.assertRaises(ValueError):
            consultation.validate_exchange(CANONICAL, missing_cache_control)

        check = schema("CallerCapabilities")
        examples = document(CANONICAL)["components"]["schemas"]["CallerCapabilities"].get("examples", [])
        self.assertTrue(examples, "Discovery needs a consumable response example")
        for value in examples:
            check.validate(value)
            validate_capability_identities(value)
            for collection in value["collections"]:
                for operation_ref in collection["operations"]:
                    self.assertIn("contract", operation_ref)
                    self.assertIn("operationId", operation_ref)
                    broken = deepcopy(value)
                    del broken["collections"][0]["operations"][0]["operationId"]
                    self.assertFalse(check.is_valid(broken))
        for name in ("CallerCapabilities", "CapabilityCollection", "CapabilityOperation"):
            for _, node in nodes(document(CANONICAL)["components"]["schemas"][name]):
                if node.get("type") == "array":
                    self.assertIn("maxItems", node, name)

    def test_canonical_discovery_example_covers_read_write_and_workflow_operations(self):
        examples = document(CANONICAL)["components"]["schemas"]["CallerCapabilities"][
            "examples"
        ]
        self.assertTrue(examples)
        operation_refs = [
            operation_ref
            for example in examples
            for collection in example["collections"]
            for operation_ref in collection["operations"]
        ]
        operation_refs.extend(
            entry["operation"]
            for example in examples
            for entry in example["operations"]
        )
        advertised = {entry["operationId"] for entry in operation_refs}
        self.assertTrue(
            {
                "retrieveRecord",
                "listRecords",
                "lookupRecord",
                "searchRecords",
                "listRecordRevisions",
                "retrieveRecordRevision",
                "createRecord",
                "updateRecord",
                "applyRecordTransition",
                "submitChangeRequest",
                "listChangeRequests",
                "getChangeRequest",
                "approveChangeRequest",
                "rejectChangeRequest",
                "withdrawChangeRequest",
                "getOperation",
            }
            <= advertised
        )
        for entry in operation_refs:
            with self.subTest(operation=entry["operationId"]):
                self.assertIn(entry["family"], {"consultation", "write"})
                if entry["family"] == "consultation":
                    self.assertIn("view", entry)
                else:
                    self.assertNotIn("view", entry)
                    self.assertFalse(
                        {
                            "features",
                            "purpose",
                            "readableFields",
                            "selectors",
                            "searches",
                        }
                        & entry.keys()
                    )
                if entry["capability"] in {"update", "transition"}:
                    self.assertEqual(
                        set(entry["write"]["companionRead"]),
                        {"operationId", "view"},
                    )

        baseline = deepcopy(examples[0])
        update = next(
            entry
            for collection in baseline["collections"]
            for entry in collection["operations"]
            if entry["operationId"] == "updateRecord"
        )
        update["write"]["companionRead"]["view"] = "conflicting-view"
        with self.assertRaises(ValueError):
            consultation.validate_caller_capabilities(baseline)

        baseline = deepcopy(examples[0])
        operation_entry = next(
            entry["operation"]
            for entry in baseline["operations"]
            if entry["operation"]["operationId"] == "getOperation"
        )
        operation_entry["capability"] = "change-request-retrieve"
        with self.assertRaises(ValueError):
            consultation.validate_caller_capabilities(baseline)

    def test_registry_metadata_advertises_one_combined_read_write_service(self):
        metadata = json.loads(
            (API / "examples/registry-metadata.jsonld").read_text()
        )
        services = {
            node["@id"]: node
            for node in metadata["@graph"]
            if "dcat:DataService" in consultation.as_list(node["@type"])
        }
        combined = services["https://registry.example/services/business-registry"]
        self.assertEqual(
            set(consultation.as_list(combined["serviceType"])),
            {"apif:consultation", "apif:write"},
        )
        self.assertEqual(
            combined["endpointDescription"],
            "https://registry.example/contracts/1.0.0-draft/openapi.yaml",
        )
        self.assertNotIn(
            "https://registry.example/services/business-write", services
        )

        linkset = json.loads(
            (API / "examples/api-catalog.linkset.json").read_text()
        )
        descriptions = {
            link["href"]
            for context in linkset["linkset"]
            for link in context["service-desc"]
        }
        self.assertIn(combined["endpointDescription"], descriptions)
        self.assertNotIn(
            "https://registry.example/contracts/business-write.openapi.json",
            descriptions,
        )

    def test_caller_capability_examples_reference_published_operation_contexts(self):
        examples = document(CANONICAL)["components"]["schemas"]["CallerCapabilities"]["examples"]
        self.assertTrue(examples)
        for example in examples:
            consultation.validate_caller_capabilities(example)

    def test_caller_capability_semantics_match_linked_contracts(self):
        business_contract = "https://registry.example/contracts/1.0.0-draft/examples/business-registry.openapi.yaml"
        birth_contract = "https://registry.example/contracts/1.0.0-draft/examples/birth-registration.openapi.yaml"
        business = {
            "registry": "https://registry.example/registries/business",
            "collectionId": "businesses",
            "operations": [
                {
                    "operationId": "retrieveBusiness", "contract": business_contract,
                    "capability": "retrieve", "view": "business-public",
                    "features": ["conditional-read", "field-selection"],
                    "readableFields": ["legalName", "registrationStatus"],
                },
                {
                    "operationId": "lookupBusiness", "contract": business_contract,
                    "capability": "lookup", "view": "business-public",
                    "features": ["field-selection"],
                    "readableFields": ["legalName"],
                    "selectors": ["byRegistrationNumber", "byJurisdictionNumber"],
                },
                {
                    "operationId": "searchBusinesses", "contract": business_contract,
                    "capability": "search", "view": "business-public",
                    "features": ["field-selection", "complete-traversal"],
                    "readableFields": ["registrationStatus"],
                    "searches": ["byRegistrationStatus", "byFields"],
                },
            ],
        }
        birth = {
            "registry": "https://registry.example/registries/birth-registrations",
            "collectionId": "birth-registrations",
            "operations": [{
                "operationId": "retrieveBirthRegistration", "contract": birth_contract,
                "capability": "retrieve", "view": "birth-registration-with-recorded-parents",
                "features": ["recorded-time", "effective-time", "purpose-bound"],
                "purpose": {
                    "required": True, "binding": "access-token-claim", "claim": "purpose",
                    "allowedPurposes": ["benefit-eligibility"],
                },
                "readableFields": ["dateOfBirth", "placeOfBirth"],
            }],
        }
        value = {"collections": [business, birth]}
        consultation.validate_caller_capabilities(value)

        mutations = []
        unknown_selector = deepcopy(value)
        unknown_selector["collections"][0]["operations"][1]["selectors"] = ["byUnknown"]
        mutations.append(unknown_selector)
        unknown_search = deepcopy(value)
        unknown_search["collections"][0]["operations"][2]["searches"] = ["byUnknown"]
        mutations.append(unknown_search)
        unknown_field = deepcopy(value)
        unknown_field["collections"][0]["operations"][0]["readableFields"] = ["privateField"]
        mutations.append(unknown_field)
        wrong_purpose = deepcopy(value)
        wrong_purpose["collections"][1]["operations"][0]["purpose"]["allowedPurposes"] = ["other"]
        mutations.append(wrong_purpose)
        wrong_features = deepcopy(value)
        wrong_features["collections"][0]["operations"][0]["features"] = ["conditional-read"]
        mutations.append(wrong_features)
        basename_collision = deepcopy(value)
        basename_collision["collections"][0]["operations"][0]["contract"] = (
            "https://untrusted.example/business-registry.openapi.yaml")
        mutations.append(basename_collision)
        for invalid in mutations:
            with self.subTest(invalid=invalid):
                with self.assertRaises(ValueError):
                    consultation.validate_caller_capabilities(invalid)

    def test_caller_capability_semantics_tolerate_unknown_advisory_values(self):
        canonical_contract = "https://registry.example/contracts/1.0.0-draft/openapi.yaml"
        future = {
            "collections": [{
                "registry": "https://registry.example/registries/future",
                "collectionId": "future-records",
                "operations": [{
                    "operationId": "futureOperation", "contract": "https://future.example/openapi.yaml",
                    "capability": "future-capability", "view": "future-view",
                    "features": ["conditional-read"],
                }],
            }],
        }
        consultation.validate_caller_capabilities(future)
        known_with_future_feature = {
            "collections": [{
                "registry": "https://registry.example/registries/records",
                "collectionId": "records",
                "operations": [{
                    "operationId": "retrieveRecord", "contract": canonical_contract,
                    "capability": "retrieve", "view": "record-public",
                    "features": ["conditional-read", "future-feature"],
                }],
            }],
        }
        consultation.validate_caller_capabilities(known_with_future_feature)
        malformed_known_purpose = deepcopy(known_with_future_feature)
        malformed_known_purpose["collections"][0]["operations"][0]["purpose"] = {
            "required": False, "binding": "access-token-claim", "claim": "purpose",
            "allowedPurposes": ["benefit-eligibility"],
        }
        with self.assertRaises(ValidationError):
            consultation.validate_caller_capabilities(malformed_known_purpose)

        known_search_with_conditional = deepcopy(known_with_future_feature)
        operation = known_search_with_conditional["collections"][0]["operations"][0]
        operation.update({"operationId": "searchRecords", "capability": "search",
                          "features": ["conditional-read"]})
        with self.assertRaises(ValidationError):
            consultation.validate_caller_capabilities(known_search_with_conditional)


if __name__ == "__main__":
    unittest.main(verbosity=2)
