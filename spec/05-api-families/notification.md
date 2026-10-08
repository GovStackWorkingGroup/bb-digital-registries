---
description: Authorised delivery of Registry change events.
---

# Notification

> **Status:** Informative. See [Conformance](../04-conformance.md#44-capability-claims).

## Purpose and applicability

Notification informs authorised subscribers that Registry state changed. It applies when downstream systems need timely cache invalidation, propagation, or processing and cannot rely on polling Consultation.

## Capability areas

| Area | Outcome |
|---|---|
| Subscription | Establishes and manages an authorised interest in declared event types or Records. |
| Filtering | Limits delivery according to an approved scope. |
| Delivery | Sends a change event through the selected binding. |
| Recovery | Supports acknowledgement, retry, deduplication, or replay according to a declared delivery profile. |

A change event is not necessarily the authoritative Record. A consumer that needs the current permitted representation uses [Consultation](consultation.md). Notification is also distinct from internal security and audit logging.

## Adoption considerations

Deployment rules cover event identifiers, Registry and Record context, revision references, event types, occurrence and publication time, subscription authorisation, minimisation, ordering, duplicate handling, delivery guarantees, and replay.

## Implementation options

Illustrative, non-normative options include OpenAPI webhooks for HTTP push and AsyncAPI descriptions for event-driven transports such as AMQP, MQTT, Kafka, or WebSockets. A Messaging or Information Mediator component can carry events without owning their Registry meaning.

## Example

A benefits service subscribes to permitted civil-status changes. After receiving an event, it retrieves the current permitted Record representation before updating its own decision state.
