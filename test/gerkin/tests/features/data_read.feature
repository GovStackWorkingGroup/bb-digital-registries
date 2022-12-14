Feature: API endpoint allowing users to search for one record in the Digital Registries database.
  Request endpoint: POST /data/{registryname}/{versionnumber}/read

  Background:
    Given The user wants to search for one record in the Digital Registries database

  Scenario: The user receives one searches record from the Digital Registries database
    When The user triggers an action to search record in the database
    And The request with a valid payload is sent
    And There is a searched record in the database
    Then The user receives a searches record

  Scenario: The user does not receive searches record from the Digital Registries database
    When The user triggers an action to search record in the database
    And The request with a valid payload is sent
    And There is no searched record in the database
    Then The user receives a message that there is no searched record in the database

  Scenario: The user is not able to receive one searches record from the Digital Registries database
    When The user triggers an action to search a record in the database
    And The request with an invalid payload is sent
    Then The user receives an error message
