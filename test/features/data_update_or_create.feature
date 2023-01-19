Feature: API endpoint allowing users to create a new record if it not exists in the Digital Registries database or update records if already exists.
  Request endpoint: POST /data/{registryname}/{versionnumber}/update-or-create

  Scenario: The user successfully creates a new record in the Digital Registries database
    Given The user wants to create a new record or update an existing one if already exists in the Digital Registries database
    And The requested record does not exist in the database
    When The user triggers an action to create or update a record in the database
    Then Operation to create the new record finishes successfully

  Scenario: The user successfully updates the already existing record in the Digital Registries database
    Given The user wants to update an existing record in the Digital Registries database
    And The requested record already exists in the database
    When The user triggers an action to create or update a record in the database
    Then Operation to update the record finishes successfully

  Scenario: The user is not able to create/update a record in the Digital Registries database because of an invalid request
    Given The user wants to create a new record or update an existing one if already exists in the Digital Registries database
    When The user triggers an action to create or update a record in the database with an invalid request
    Then The result of an operation to create/update the record returns an error because of an invalid request
