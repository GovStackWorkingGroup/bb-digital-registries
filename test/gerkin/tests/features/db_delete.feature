Feature: API endpoint allowing users to delete Digital registries schema.
  Request endpoint: DELETE /database/{id}/

  Background:
    Given User wants to delete the Digital Registries schema

  Scenario: The user successfully deletes the Digital Registries schema
    And The database schema exists
    When The user triggers an action to delete the database schema
    And The request with a valid payload is sent
    And The requested database schema exists in the database
    Then The user received a success message

  Scenario: The user is not able to delete the Digital Registries schema
    And The database schema does not exist
    When The user triggers an action to delete the database schema
    And The request with a valid payload is sent
    And The requested database schema does not exist in the database
    Then The user received a success message

  Scenario: The user is not able to delete Digital Registries schema
    When The user triggers an action to delete the database schema
    And The request with an invalid payload is sent
    Then The user received an error message
