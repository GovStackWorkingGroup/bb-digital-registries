Feature: API endpoint allowing users to get the Digital Registries database information with schema versions.
  Request endpoint: GET /database/{id}/

  Background:
    Given The user wants to receive the Digital Registries database information with schema version

  Scenario: The user successfully receives one Digital Registries database information with schema version
    When The user triggers an action with a valid payload to display one database schema version
    Then The user received one database information with the schema version

  Scenario: The user is not able to receive any Digital Registries database information with schema version because of not providing route param
    When The user triggers an action without a route param to display one database schema version
    Then The result of an operation to receive any Digital Registries database information with schema version returns an invalid route param error

  Scenario: The user is not able to receive any Digital Registries database information with the schema version because of an empty value in the header
    When The user triggers an action with an invalid payload to display one database schema version
    Then The result of an operation to receive any Digital Registries database information with schema version returns an error

  Scenario: The user is not able to receive any Digital Registries database information with the schema version because of not include a header
    When The user triggers an action without a payload to display one database schema version
    Then The operation result of receiving any Digital Registries database information with schema version is an error
