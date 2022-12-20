Feature: API endpoint allowing users to search for one record in the Digital Registries database.
  Request endpoint: POST /data/{registryname}/{versionnumber}/read

  Background:
    Given The user wants to search for one record in the Digital Registries database

  Scenario: The user receives one searched record from the Digital Registries database
    Given The searched record exists in the database
    When The user triggers an action to search record in the database
    And The request with a valid payload is sent
    Then The user receives a searched record

  Scenario: The user does not receive searched record from the Digital Registries database
    Given The searched does not exist in the database
    When The user triggers an action to search record in the database
    And The request with a valid payload is sent
    Then The user receives a message that there is no searched record in the database

  Scenario: The user is not able to receive one searched record from the Digital Registries database
    When The user triggers an action to search a record in the database
    And The request with an invalid payload is sent
    Then Operation results in an error
