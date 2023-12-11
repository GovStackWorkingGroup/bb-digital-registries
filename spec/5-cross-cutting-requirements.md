---
description: >-
  This section will highlight important requirements or describe any additional
  cross-cutting requirements that apply to this Building Block.
---

# 5 Cross-Cutting Requirements

## 5.1 Requirements

The Cross-cutting requirements described in this section are an extension of the cross-cutting requirements defined in the [Architecture specification](https://govstack.gitbook.io/specification/v/1-0/architecture-and-nonfunctional-requirements) and [Security requirements](https://govstack.gitbook.io/specification/v/1-0/security-requirements). This section highlights cross-functional requirements for the Digital Registries Building Block and in addition, describes any deviation to the Architecture Building Block cross-cutting requirements.

### 5.1.1 Privacy and protection of user data (REQUIRED)

Add mandatory requirement. The following requirement should be added to other Building Blocks' cross-cutting requirements: Each owner of the personal data (e.g. citizen) must be able to see who has looked at their personal data in the registry. All captured personal user data must be marked as “personal data”. Users can make requests to see the information/logs of accessing personal information. API must be available for authenticated users to see their own personal data audit logs.

## 5.2 Exceptions to Architectural Cross-Cutting Specifications

### 5.2.1 Citizen-Centric (RECOMMENDED)

Cancel mandatory requirement: "Right to be forgotten: everything must be deletable". This is not a good practice for government registries.

### 5.2.2 Open (RECOMMENDED)

Cancel mandatory requirement: "Cloud-native, i.e. Docker and Kubernetes". Digital Registries must have also an on-site installation option.

### 5.2.3 Robust (RECOMMENDED)

Operates in low-resource environments

Cancel mandatory requirement: "Occasional power". In Digital Registries not possible, thus should be optional. This can be solved with backup power resources (UPS) and a generator that keeps the systems running without interruptions.

Cancel mandatory requirement: "Low-reliability connectivity". Client-server systems are not reliable in this situation, instead additional hand held connection-less data capturing devices should be used and data reentered/uploaded to the servers when connection is restored (not covered in this version scope).

### 5.2.4 Databases must not include business logic (RECOMMENDED)

Cancel mandatory requirement. "no triggers/stored procedures shall be used". Some stored procedures may be needed for database record ID generation.

## 5.3 Standards

The following standards are applicable to data structures in the Digital Registries Building Block:

### 5.3.1 OpenAPI

OpenAPI Version [3.0.0](https://spec.openapis.org/oas/v3.0.0), [3.0.1](https://spec.openapis.org/oas/v3.0.1), [3.1.0](https://spec.openapis.org/oas/v3.1.0).
