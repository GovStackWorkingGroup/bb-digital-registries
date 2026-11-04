#!/usr/bin/env python3
"""Keep historical integration samples free of literal credentials."""

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EREGISTRATION_EXAMPLES = (
    ROOT / "examples/eRegistrations/api1_read_example.md",
    ROOT / "examples/eRegistrations/api2_create_example.md",
    ROOT / "examples/eRegistrations/api3_create_example.md",
)
OPENIMIS = ROOT / "examples/openIMIS"


class HistoricalExampleConfigurationTests(unittest.TestCase):
    def test_eregistration_examples_use_an_explicit_token_placeholder(self) -> None:
        jwt = re.compile(r"eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+")

        for path in EREGISTRATION_EXAMPLES:
            with self.subTest(path=path.relative_to(ROOT)):
                text = path.read_text()
                self.assertEqual(text.count("Authorization: Bearer <ACCESS_TOKEN>"), 1)
                self.assertIsNone(jwt.search(text))

    def test_openimis_compose_requires_injected_credentials(self) -> None:
        compose = (OPENIMIS / "docker-compose.yml").read_text()

        expected_bindings = (
            ("POSTGRES_PASSWORD", "${DB_PASSWORD:?"),
            ("DB_PASSWORD", "${DB_PASSWORD:?"),
            ("login_openIMIS", "${OPENIMIS_ADMIN_USERNAME:?"),
            ("password_openIMIS", "${OPENIMIS_ADMIN_PASSWORD:?"),
        )
        for key, prefix in expected_bindings:
            with self.subTest(key=key):
                values = re.findall(rf"^\s*-\s*{key}=(.*)$", compose, re.MULTILINE)
                valid = len(values) == 1 and values[0].startswith(prefix)
                self.assertTrue(valid, f"{key} must have one required variable binding")

    def test_openimis_example_environment_is_safe_to_copy(self) -> None:
        example = (OPENIMIS / ".env.example").read_text()

        self.assertIn("DB_PASSWORD=\n", example)
        self.assertIn("OPENIMIS_ADMIN_PASSWORD=\n", example)
        self.assertIn("OPENIMIS_ADMIN_USERNAME=Admin\n", example)

    def test_openimis_readme_labels_history_and_documents_local_setup(self) -> None:
        readme = (OPENIMIS / "README.md").read_text()

        self.assertIn("historical", readme.lower())
        self.assertIn("not evidence of conformance", readme.lower())
        self.assertIn(".env.example", readme)
        self.assertIn("OPENIMIS_ADMIN_PASSWORD", readme)


if __name__ == "__main__":
    unittest.main()
