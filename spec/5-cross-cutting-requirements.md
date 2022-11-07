# 5 Cross-Cutting Requirements

The Cross-cutting requirements described in this section are an extension of the cross-cutting requirements defined in the Architecture [specification ](https://govstack.gitbook.io/specification/building-blocks/architecture-and-nonfunctional-requirements)and Security [requirements](https://govstack.gitbook.io/specification/building-blocks/security-requirements). This section highlights cross-functional requirements for Digital Registries BB and in addition describes any deviation to the Architecture BB cross-cutting requirements.

The following requirements should be optional:

**Citizen-Centric (2.1 in Architecture Blueprint)**

* Right to be forgotten: everything must be deletable. - not a good practice for gov. registries.

**Open (2.2 in Architecture Blueprint )**

* Cloud native (Docker and Kubernetes). - **must have also on-site installation option**.

**Robust ( 2.7 in Architecture Blueprint)**

* Operates in low-resource environments:
  * Occasional power - **not possible, should be optional. This can be solved with UPS and generator that keeps the systems running without interruptions**.
  * Low-reliability connectivity - **Client-server systems are not reliable in this situation**.

**Databases MUST not include business logic (3.21 in Architecture Blueprint)**

* This means no triggers/stored procedures shall be used. - some stored procedures may be needed FOR database record ID generation.

The following requirement should be added to other BB cross cutting requirements:

**Privacy and protection of user data**

Each owner of the personal data (e.g. citizen) must be able to see who has looked at their personal data in the registry. All captured personal user data must be marked as “personal data”. Users can make requests to see the information/logs of accessing personal information. API must be available for authenticated users to see their own personal data audit logs.
