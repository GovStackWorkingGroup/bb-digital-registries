# 7 Data Structures

## 7.1 Standards/Protocols <a href="#docs-internal-guid-1e590c21-7fff-9d6f-674a-fa9e678943e1" id="docs-internal-guid-1e590c21-7fff-9d6f-674a-fa9e678943e1"></a>

The following standards are applicable to data structures in the registration building block:

1. All dates should follow [ISO 8601](http://en.wikipedia.org/wiki/ISO\_8601).
2. RFC 7159 - The JavaScript Object Notation (JSON)
3. Open -API Version 3.1.0

## 7.2 Resource Model

The resource model shows the relationship between data objects that are used by this Building Block.

**Resource Model**:

![Illustration 3- Resource model. See editable image here.](<.gitbook/assets/GDB datamodel(1) (1).JPG>)

## 7.3 Data Elements <a href="#docs-internal-guid-f4ace18b-7fff-ada5-ebbb-3aaf5e08cb17" id="docs-internal-guid-f4ace18b-7fff-ada5-ebbb-3aaf5e08cb17"></a>

_The Data Elements provide detail for the Resource Model defined above. This section will list the core/required fields for each resource. Note that the Data Elements can be extended for a particular use case, but they must always contain, at the minimum, the fields defined here._

**Minimum Required Data:**

| Name                | Description                                                                                             | Type                                  | Required |   |
| ------------------- | ------------------------------------------------------------------------------------------------------- | ------------------------------------- | -------- | - |
| Database ID         | Unique identifier of a database                                                                         | integer                               | yes      |   |
| Database name       | Name that will define the database content. Name is public.                                             | varchar                               | yes      |   |
| Database schema     | Database schema. See example in Appendix 1, Appendix 2.                                                 | json                                  | yes      |   |
| Database logo       | Visual image for the database                                                                           | bytea                                 | no       |   |
| Version             | Database version. Each change in schema will produce the next version of the database and API services. | numeric                               | yes      |   |
| Catalogue name      | Database name in the list                                                                               | varchar                               | yes      |   |
| Data ID             | Data element unique identifier                                                                          | integer                               | yes      |   |
| Registry number     | Additional registry identifier. Unique identifier in the registry.                                      | varchar                               | yes      |   |
| Field type          | Field type: datetime, date, boolean, text, number, file                                                 | varchar                               | yes      |   |
| Field value         | Field value, data stored in the field.                                                                  | datetime, date, boolean, text, number | yes      |   |
| Audit log old value | Field value before change                                                                               | datetime, date, boolean, text, number | yes      |   |
| Audit log new value | Field value after the change                                                                            | datetime, date, boolean, text, number | yes      |   |
