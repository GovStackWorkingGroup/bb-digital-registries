@data
Feature: API endpoint allowing users to create a new record in the Digital Registries database.
  Request endpoint: POST /data/{registryname}/{versionnumber}/create

  Scenario: The user successfully creates a record in the Digital Registries database
    Given The user wants to create a new record in the Digital Registries database
    When The user triggers an action to create a new record in the database
    Then Operation to create a new record finishes successfully

  Scenario: The user is not able to create a record in the database which not exist
    Given The user wants to create a new record in the Digital Registries database which does not exist
    When The user triggers an action to create a new record in the database which not exist
    Then The operation result is an error because the database does not exist

  Scenario: The user is not able to create a record in the Digital Registries database because of an invalid request
    Given The user wants to create a new record in the Digital Registries database with an invalid request
    When The user triggers an action to create a new record in the database with an invalid request
    Then The operation result is an error for creating because of an invalid request
