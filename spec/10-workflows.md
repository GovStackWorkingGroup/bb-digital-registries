---
description: Registry service discovery, current Record reads, exact lookup, and bounded collection pagination.
---

# 10 Workflows

## 10.1 Discover Registry services and their contracts

This workflow applies to every Registry BB implementation. The publisher serves the Registry metadata document and locates it, with each contract, through the RFC 9727 `/.well-known/api-catalog` linkset at the API origin.

### Preconditions

1. The consumer knows the API origin or has a configured metadata document URI.
2. The consumer has any access needed to read the metadata and linked contracts.
3. The publisher provides the Registry metadata and service discovery required by Registry Core.

### Interaction

1. The consumer requests `/.well-known/api-catalog` at the API origin, follows its `service-meta` link to the Registry metadata document, and selects the Registry by its stable identifier.
2. The consumer inspects its authority, authoritative scope statement, and referenced Digital Registries specification version.
3. The consumer follows the Registry's service associations and reads each service's identifier, API-family labels, endpoint URL, and operational-contract reference for the services available to that consumer's audience.
4. The consumer follows the operational contract to determine the collections, the Registry context declared on each operation, exact operations, inputs, outputs, and access requirements. For HTTP APIs, this is an OpenAPI description unless the applicable binding defines an established protocol-native description.
5. The consumer selects a suitable operation, or determines that the required operation is unavailable.

### Outcomes

The linked contract, not the family label, tells the consumer which operations exist. Discovery is not satisfied when an exposed service is missing from the Registry description or lacks its identifier, valid family labels, endpoint, or machine-readable contract, or when the origin serves no `/.well-known/api-catalog` linkset with a `service-meta` link to the metadata document.

### Postconditions

- The consumer can distinguish the governed Registry, its authority, and its technical services.
- The consumer knows which operations are available from each service's operational contract.
- Family labels classify the service's operations. Capability claims follow the [conformance model](04-conformance.md#44-capability-claims).

## 10.2 Retrieve the current permitted Record representation

This workflow applies to implementations selecting Retrieve. The [HTTP binding](../api/openapi.yaml) defines request and response details.

### Preconditions

1. The published service contract exposes Retrieve and identifies its Registry, collection membership, and representation schema.
2. The consumer has the credentials and request context required by the deployment.

### Interaction

1. The consumer sends a request to the declared item path, such as `GET /v1/businesses/{recordId}`, with a Record Identifier within the Registry.
2. The Registry evaluates authentication, access, and disclosure policy.
3. The Registry resolves the current Record within the collection and constructs its permitted `{recordId, data}` representation. Current Records may include inactive Records.
4. The Registry returns that representation or the declared unsuccessful outcome.

### Outcomes

| Condition | Observable outcome |
|---|---|
| Current Record is accessible | The permitted representation is returned. |
| Consumer has narrower disclosure rights | The returned representation satisfies both disclosure policy and its schema. |
| Identifier is unknown, belongs to a Record outside the collection, or has protected existence | The same `record-not-available` outcome is returned. |

### Postconditions

- The source Record is unchanged.
- The returned identifier matches the requested identifier.
- Registry, schema, and authority context are unambiguous; any additional source metadata follows the published contract.

## 10.3 Look up a Record using an exact selector

This workflow applies to implementations selecting Lookup.

### Preconditions

1. The contract exposes a Lookup operation, such as `POST /v1/businesses:lookup`, and declares the collection and selector's typed components, comparison rules, and uniqueness scope.
2. The consumer has the required credentials and request context.

### Interaction

1. The consumer sends `{selector, values}` using the declared schema. A composite selector supplies every key component.
2. The Registry validates the input and evaluates access and disclosure policy.
3. The Registry resolves the selector within its declared scope, checks uniqueness, and applies collection membership.
4. One permitted match returns the common Record representation. Other outcomes follow the contract, including protected-existence handling and source uniqueness failures.

### Postconditions

- The source Record is unchanged.
- A successful Lookup returns the same Record schema and field meanings as other reads of that view.
- Multiple source matches fail without selecting an arbitrary Record.

## 10.4 Page through a declared collection or search result

This workflow applies independently to List and Search. For the business example, List uses `GET /v1/businesses`; Search uses `POST /v1/businesses:search`.

### Preconditions

1. The contract declares the collection or search, accepted inputs, deterministic ordering with a unique tie breaker, page limits, and cursor lifetime.
2. The consumer has the required credentials and request context.

### Interaction

1. The consumer sends the first request without a cursor, supplying the declared criteria and any supported ordering and page size.
2. The Registry validates the request, evaluates current access and disclosure policy, and returns `{items, pageInfo}`. Items use the Record schema for the selected view.
3. For a non-null `nextCursor`, the consumer repeats the criteria and ordering with that cursor. It may omit `pageSize` or repeat the effective size established by the first request.
4. The Registry reauthorizes the continuation and verifies its cursor binding, including the collection. An invalid, expired, or mismatched cursor produces the declared failure.
5. The consumer continues until `nextCursor` is `null`, including after short or empty Pages with a continuing cursor.

### Outcomes and limits

- Every Page respects the effective size bound; every continuation advances source processing.
- Live-data changes follow the published pagination and source-currency policy.
- An optional `pageInfo.total` is the exact count of the full permitted query at that Page's evaluation time.
- Revoked access applies to subsequent requests. A failed continuation allows the consumer to start a fresh request when permitted.

## 10.5 Read a household and interpret its relationships

This workflow uses the [household OpenAPI](../api/examples/household-registry.openapi.yaml).

1. The consumer sends `GET /v1/households/{recordId}` and receives a household containing its declared address and membership components.
2. The consumer interprets membership attributes as relationship facts. A `membershipId` identifies a component within that household.
3. The `individualRef` field schema fixes the target Individuals Registry, allowing the reference to omit `registryId`.
4. Where an individual read is offered, the consumer follows the field's declared target collection and operation binding through the target Registry's published service contract. The binding explains how to use the reference as input; the consumer follows the operation's access requirements.
5. The related read follows the target's authorization and source-currency contract. An unavailable target leaves the household's membership facts unchanged.

A predefined household view may instead include permitted individual summaries, with declared fields, bounds, and source currency.

The [birth-registration OpenAPI](../api/examples/birth-registration.openapi.yaml) illustrates recorded parent details. `nameAtRegistration` belongs to the birth-registration Record, with an optional reference to the individual. Changes to the individual's current Record leave this recorded value unchanged; accepted corrections to the birth-registration source may update it.
