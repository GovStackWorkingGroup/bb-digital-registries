Feature: API endpoint allowing users to create or modify the Digital Registries database schema.
  Request endpoint: POST /database/modify/

  Background:
    Given The user wants to create or modify the Digital Registries database schema

  Scenario: The user successfully creates the Digital Registries database schema
    Given The requested database schema does not exist in the database
    When The user triggers an action to create a database schema
    Then Operation to create new database schema finishes successfully

  Scenario: The user successfully modifies the Digital Registries database schema
    Given The requested database schema exists in the database
    When The user triggers an action to modify a database schema
    Then Operation to modify a database schema finishes successfully

  Scenario: The user is not able to modify the Digital Registries database schema because of an invalid request
    When The user triggers an action to modify the already existing database schema
    Then Operation results to modify a database schema is an error
