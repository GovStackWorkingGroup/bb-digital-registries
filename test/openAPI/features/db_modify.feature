Feature: API endpoint that allows users to create or modify the Digital Registries database schema.
  Request endpoint: POST /database/modify/

  Background:
    Given User wants to create or modify the Digital Registries database schema

  Scenario: The user successfully creates the Digital Registries database schema
    Given The requested database schema does not exist in the database
    When The user sends a valid request to create a database schema
    Then The operation to create a new database schema completes successfully

  Scenario: The user successfully modifies the Digital Registries database schema
    Given The requested database schema exists in the database
    When The user sends a valid request to modify a database schema
    Then The operation to change a database schema completes successfully

  Scenario: The user is unable to modify the Digital Registries database schema because of an invalid request
    When The user sends a valid request to modify the already existing database schema
    Then The result of the operation to change a database schema is an error
