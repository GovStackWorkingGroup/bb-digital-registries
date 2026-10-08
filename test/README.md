# Test artifacts

The [Consultation validator](../tools/validate_consultation.py) checks the canonical transport and the Business, Household and Birth Registration contracts. It also checks domain schemas, inline examples and exchange fixtures, including rejection cases for invalid inputs and references.

Run the [documented validation commands](../api/README.md#validation). Deployment behavior and audit evidence are covered by [the Testing chapter](../spec/11-testing.md).

The `openAPI/` directory retains the earlier generated CRUD harness as migration evidence.
