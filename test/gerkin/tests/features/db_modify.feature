Feature: API endpoint allowing users to create or modify the Digital Registries database schema.
  Request endpoint: POST /database/modify/

  Background:
    Given The user wants to create or modify the Digital Registries database schema

  Scenario: The user successfully creates the Digital Registries database schema
    Given The requested database schema does not exist in the database
    When The user triggers an action to create a database schema
    And The request with a valid payload is sent
    Then Operation finishes successfully

  Scenario: The user successfully modifies the Digital Registries database schema
    Given The requested database schema exists in the database
    When The user triggers an action to create a database schema
    And The request with a valid payload is sent
    Then Operation finishes successfully

  Scenario: The user is not able to modify the Digital Registries database schema because it doesn't exist
    Given The requested database schema does not exist in the database
    When The user triggers an action to create a database schema
    And The request with a valid payload is sent
    Then Operation results in an error

  Scenario: The user is not able to modify the Digital Registries database schema
    When The user triggers an action to modify the already existing database schema
    And The request with an invalid payload is sent
    Then Operation results in an error
