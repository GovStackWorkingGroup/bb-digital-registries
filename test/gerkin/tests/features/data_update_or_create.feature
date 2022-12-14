Feature: API endpoint allowing users to create a new record if it not exists in the Digital Registries database or update records if already exists.
  Request endpoint: POST /data/{registryname}/{versionnumber}/update-or-create

  Background:
    Given The user wants to create a new record or update an existing one if already exists in the Digital Registries database

  Scenario: The user successfully create new record in the Digital Registries database
    When The user triggers an action to creates a new record in the database
    And The request with a valid payload is sent
    Then The record does not exist in the database
    And The user receives a success message

  Scenario: The user successfully updates the already existing record in the Digital Registries database
    When The user triggers an action to create a new record in the database
    And The request with a valid payload is sent
    Then The record already exists in the database
    And The user receives a success message

  Scenario: The user is not able to create/update a record in the Digital Registries database
    When The user triggers an action to create a new record in the database
    And The request with an invalid payload is sent
    Then The user receives an error message
