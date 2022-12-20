Feature: API endpoint allowing users to delete Digital registries schema.
  Request endpoint: DELETE /database/{id}/

  Background:
    Given User wants to delete the Digital Registries schema

  Scenario: The user successfully deletes the Digital Registries schema
    Given The requested database schema exists
    When The user triggers an action to delete the database schema
    And The request with a valid payload is sent
    Then Operation finishes successfully

  Scenario: The user is not able to delete the Digital Registries schema
    Given The requested database schema does not exists
    When The user triggers an action to delete the database schema
    And The request with a valid payload is sent
    Then Operation finishes successfully

  Scenario: The user is not able to delete Digital Registries schema
    When The user triggers an action to delete the database schema
    And The request with an invalid payload is sent
    Then Operation results in an error'
