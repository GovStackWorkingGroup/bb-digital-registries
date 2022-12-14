Feature: API endpoint allowing users to get the Digital Registries database information with schema versions.
  Request endpoint: GET /database/{id}/

  Background:
    Given The user wants to retrieve the Digital Registries database information with schema versions

  Scenario: The user successfully receives one Digital Registries database information with schema versions
    When The user triggers an action to display one database schema versions
    And The request with a valid payload is sent
    Then The user received one database information with schema versions

  Scenario: The user is not able to receive any Digital Registries database information with schema versions
    When The user triggers an action to display one database schema versions
    And The request with an invalid payload is sent
    Then The user received an error message
