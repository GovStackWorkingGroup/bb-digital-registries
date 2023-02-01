@data
Feature: API endpoint that allows users to create a new record in the Digital Registries database.
  Request endpoint: POST /data/{registryname}/{versionnumber}/create

  Scenario: The user successfully creates a record in the Digital Registries database
    Given The user wants to create a new record in the Digital Registries database
    When The user sends a valid request to create a new record in the database
    Then The process to create a new record completes successfully

  Scenario: The user is unable to create a record in the database that does not exist
    Given The user wants to create a new record in the Digital Registries database that does not exist
    When The user sends a valid request to create a new record in the database that does not exist
    Then The result of the operation is an error because the database does not exist

  Scenario: The user is unable to create a record in the Digital Registries database because of an invalid request
    Given The user wants to create a new record in the Digital Registries database
    When The user sends an invalid request to create a new record in the database
    Then The result of the operation is an error due to an invalid request
