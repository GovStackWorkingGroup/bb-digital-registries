# Historical implementation examples

The examples in this directory demonstrate products and test environments developed against earlier Digital Registries requirements and generated CRUD APIs.

They are retained for migration and implementation research. They do not demonstrate conformance with the 3.0.0-alpha.2 Base Registry Profile.

## Preserved implementation context

### UNCTAD Generic Database Builder (eRegistrations)

Earlier Digital Registries releases identified the UNCTAD Generic Database Builder, also known as eRegistrations, as an implementation of the generated CRUD and no-code Registry model. The original repository description characterised it as proprietary software available with a one-time UNCTAD support fee.

The files under [eRegistrations](eRegistrations/README.md) preserve example requests and documentation from that integration. Previously listed GovStack sandbox and authorisation endpoints are no longer presented as active services.

### Mockoon API mock

The [Mockoon example](mockoon/README.md) preserves a local mock of the previous OpenAPI surface for development and migration analysis.

Any future example intended as conformance evidence needs to identify the specification and capability profile it implements and be verified by the corresponding conformance tests.
