---
description: Illustrative API for reading birth-registration Records with recorded parent details.
---

# Birth-registration API example

Use this example to read a birth-registration Record with parent details preserved as recorded at registration, rather than replaced by a person's current details. The current Retrieve example below returns that recorded view without temporal metadata; the contract also illustrates typed Search and retained revision operations over the same Collection.

The [birth-registration OpenAPI](../../api/examples/birth-registration.openapi.yaml) is an illustrative profile of the [canonical DRAFT Consultation contract](../api-reference.md), not a normative or ratified CRVS profile. `effectiveAt` selects the date when the Registry Record applies and is distinct from `dateOfBirth`; purpose comes from the declared trusted access-token claim, not user input. Its fields, legal scope, access rules, and temporal choices do not prescribe universal CRVS requirements.
