Feature: API endpoint that allows users to create a new record if it does not already exist in the Digital Registries database, or to update existing records.
  Request endpoint: POST /data/{registryname}/{versionnumber}/update-or-create

  Scenario: The user successfully creates a new record in the Digital Registries database
    Given The user wants to create a new record or update an existing record if it already exists in the Digital Registries database
    And The requested record does not exist in the database
    When The user sends a valid request to create or update a record in the database
    Then The process of creating the new record has been successfully completed

  Scenario: The user successfully updates an existing record in the Digital Registries database
    Given The user wants to update an existing record in the Digital Registries database
    And The requested record already exists in the database
    When The user sends a valid request to create or update a record in the database
    Then The process of updating the record has been successfully completed

  Scenario: The user is not able to create/update a record in the Digital Registries database because of an invalid request
    Given The user wants to create a new record or update an existing record if it already exists in the Digital Registries database
    When The user sends an invalid request to create or update a record in the database
    Then The result of an operation to create/update the record returns an error because the request is invalid
