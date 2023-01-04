Feature: API endpoint allowing users to get the Digital Registries database information with schema versions.
  Request endpoint: GET /database/{id}/

  Background:
    Given The user wants to retrieve the Digital Registries database information with schema versions

  Scenario: The user successfully receives one Digital Registries database information with schema versions
    When The user triggers an action with a valid payload to display one database schema versions
    Then The user received one database information with schema versions

  Scenario: The user is not able to receive any Digital Registries database information with schema versions bacause of not providing route param
    When The user triggers an action without a route param to display one database schema versions
    Then The operation of receiving any Digital Registries database information with schema versions results with an error of the invalid route param

  Scenario: The user is not able to receive any Digital Registries database information with schema versions because of empty value in the header
    When The user triggers an action with an invalid payload to display one database schema versions
    Then The operation of receiving any Digital Registries database information with schema versions results with an error of the invalid header

  Scenario: The user is not able to receive any Digital Registries database information with schema versions because of not including header
    When The user triggers an action without a payload to display one database schema versions
    Then The operation of receiving any Digital Registries database information with schema versions results with an error
