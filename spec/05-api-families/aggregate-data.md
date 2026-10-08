---
description: Approved statistics derived from Registry Records.
---

# Aggregate Data

> **Status:** Informative. See [Conformance](../04-conformance.md#44-capability-claims).

## Purpose and applicability

Aggregate Data provides approved statistics derived from Registry Records, such as counts, distributions, or time series. It applies when the Registry itself publishes statistical outputs. In other deployments, a national statistics service or open-data platform can own that responsibility instead.

## Capability areas

| Area | Outcome |
|---|---|
| Aggregate query | Returns an approved result for declared dimensions, measures, population, and time scope. |
| Dataset metadata | Describes definitions, units, provenance, release policy, and applicable disclosure controls. |
| Published release | Returns an identified statistical release or revision. |

## Capability boundary

Aggregate Data returns statistical outputs rather than the individual Records provided by [Consultation](consultation.md). Analytics engines and dashboards are deployment choices. Access depends on the release policy, and aggregation alone does not ensure anonymity. Deployment rules cover disclosure thresholds, suppression, legal controls, revisions, and indicators of applied protection.

## Implementation options

Illustrative, non-normative options include synchronous HTTP described by OpenAPI, or SDMX for outputs that participate in national or international statistical ecosystems.

## Example

A vehicle Registry publishes quarterly counts by vehicle class and region under a statistical release policy that suppresses disclosive small cells.
