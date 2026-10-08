# Shared HTTP schemas

[govstack-openapi-common.yaml](govstack-openapi-common.yaml) is vendored unchanged
from `bb-template/api/common/govstack-openapi-common.yaml`, component version
**0.1.0-draft**. This component version is independent of the guide and ruleset
version **0.2.0-draft** used by the Consultation contracts.

SHA-256: `05d1bfc89c86a8d64005e343268326b3fb43cd044fe30f662fec0f9f573b0c73`.

The library contains no operations and is not a second API surface. Consultation
references its Problem, ValidationProblem and PageInfo schemas; local schemas
narrow pagination metadata to this binding's cursor constraints. Parameters,
headers, responses, error examples and security schemes remain local.

To update it, review the published version and changes, replace the file as a
unit, update this provenance record, and rerun [API validation](../README.md#validation).
