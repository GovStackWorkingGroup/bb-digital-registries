Feature: API endpoint allowing users to create a new record if it not exists in the Digital Registries database or update records if already exists.
  Request endpoint: POST /data/{registryname}/{versionnumber}/update-or-create

  Background:
    Given The user wants to create a new record or update an existing one if already exists in the Digital Registries database

  Scenario: The user successfully creates new record in the Digital Registries database
    Given The requested record does not exist in the database
    When The user triggers an action to create a new record in the database
    And The request with a valid payload is sent
    Then Operation finishes successfully

  Scenario: The user successfully updates the already existing record in the Digital Registries database
    Given The requested record already exist in the database
    When The user triggers an action to create a new record in the database
    And The request with a valid payload is sent
    Then Operation finishes successfully

  Scenario: The user is not able to create/update a record in the Digital Registries database
    When The user triggers an action to create a new record in the database
    And The request with an invalid payload is sent
    Then Operation results in an error
