Feature: API endpoint that allows users to retrieve Digital Registries database information with schema versions.
  Request endpoint: GET /database/{id}/

  Background:
    Given User wants to get the database information of Digital Registries with schema version

  Scenario: User successfully obtains Digital Registries database information with schema version
    When The user sends a valid request to view a database schema version
    Then The user has received a database information with schema version

  Scenario: The user cannot get database information from Digital Registries with the schema version because he did not specify a route parameter
    When The user sends an invalid request without routing parameters to view a database schema version
    Then The result of an operation to receive database information from Digital Registries with schema version returns an invalid route param error

  Scenario: The user is unable to receive database information from Digital Registries with schema version because no header is included
    When The user sends an invalid request to view a database schema version
    Then The result of an operation to receive database information from Digital Registries with the schema version returns an error

  Scenario: The user cannot receive Digital Registries database information with the schema version because there is no header included
    When The user sends an invalid request with no payload to view a database schema version
    Then The result of receiving Digital Registries database information with the schema version is an error
