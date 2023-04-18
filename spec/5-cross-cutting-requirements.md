---
description: >-
  This section will highlight important requirements or describe any additional
  cross-cutting requirements that apply to this Building Block.
---

# 5 Cross-Cutting Requirements

The Cross-cutting requirements described in this section are an extension of the cross-cutting requirements defined in the [Architecture specification](https://govstack.gitbook.io/specification/v/1-0/architecture-and-nonfunctional-requirements) and [Security requirements](https://govstack.gitbook.io/specification/v/1-0/security-requirements). This section highlights cross-functional requirements for the Digital Registries Building Block and in addition, describes any deviation to the Architecture Building Block cross-cutting requirements.

## 5.1  Citizen-Centric (RECOMMENDED)

Right to be forgotten: everything must be deletable (not a good practice for government registries).

## 5.2  Open (RECOMMENDED)

Cloud-native, i.e. Docker and Kubernetes (must have also an on-site installation option).

## 5.3  Robust (RECOMMENDED)

Operates in low-resource environments

* Occasional power: not possible, should be optional. This can be solved with backup power resources (UPS) and a generator that keeps the systems running without interruptions.
* Low-reliability connectivity: Client-server systems are not reliable in this situation.

## 5.3  Databases must not include business logic (REQUIRED)

This means no triggers/stored procedures shall be used (some stored procedures may be needed FOR database record ID generation).

## 5.4  Privacy and protection of user data (REQUIRED)

This requirement should be added to other Building Blocks' cross-cutting requirements. Each owner of the personal data (e.g. citizen) must be able to see who has looked at their personal data in the registry. All captured personal user data must be marked as “personal data”. Users can make requests to see the information/logs of accessing personal information. API must be available for authenticated users to see their own personal data audit logs.
