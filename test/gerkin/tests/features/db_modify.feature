Feature: API endpoint allowing users to create or modify the Digital Registries database schema.
  Request endpoint: POST /database/modify/

  Background:
    Given The user wants to create or modify Digital Registries database schema

  Scenario: The user successfully create the Digital Registries database schema
    When The user triggers an action to create a database schema
    And The request with a valid payload is sent
    Then The user receives a successs message

  Scenario: The user successfully modify the Digital Registries database schema
    When The user triggers an action to modify already exists database schema
    And The request with a valid payload is sent
    Then The user receives a successs message

  Scenario: The user is not able to create the Digital Registries database schema
    When The user triggers an action to create a database schema
    And The request with an invalid payload is sent
    Then The user receives an error message

  Scenario: The user is not able to modify the Digital Registries database schema
    When The user triggers an action to modify already existing database schema
    And The request with an invalid payload is sent
    Then The user receives an error message
