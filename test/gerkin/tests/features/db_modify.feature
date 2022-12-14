Feature: API endpoint allowing users to create or modify the Digital Registries database schema.
  Request endpoint: POST /database/modify/

  Background:
    Given The user wants to create or modify the Digital Registries database schema

  Scenario: The user successfully creates the Digital Registries database schema
    And The database schema does not exist in the database
    When The user triggers an action to create a database schema
    And The request with a valid payload is sent
    And The record does not exist in the database
    Then The new record is successfully created in the database
    And The user receives a success message

  Scenario: The user successfully modifies the Digital Registries database schema
    And The database schema exists in the database
    When The user triggers an action to create a database schema
    And The request with a valid payload is sent
    And The record does exist in the database
    Then The record is successfully updated in the database
    And The user receives a success message

  Scenario: The user is not able to create the Digital Registries database schema
    And The database schema does not exist in the database
    When The user triggers an action to create a database schema
    And The request with an invalid payload is sent
    Then The user receives an error message

  Scenario: The user is not able to modify the Digital Registries database schema
    When The user triggers an action to modify the already existing database schema
    And The request with an invalid payload is sent
    Then The user receives an error message
