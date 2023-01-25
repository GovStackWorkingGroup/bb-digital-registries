Feature: API endpoint allowing users to check if a record exists in the Digital Registries database.
  Request endpoint: POST /data/{registryname}/{versionnumber}/exists

  Scenario: The user receives a message that the record exists in the Digital Registries database
    Given The user wants to check if a record exists in the Digital Registries database
    When The user triggers an action to check if a record exists in the database
    Then Operation to receive a message that a record exists in the database finishes successfully
    And The user receives information that a record exists in the database

  Scenario: The user receives the message that the record does not exist in the Digital Registries database
    Given The user wants to check if the record exists in the Digital Registries database
    When The user triggers an action to check if a record exists in the database
    Then Operation to receive a message that a record exists in the database finishes successfully
    And The user receives information that the record does not exist in the database

  Scenario: The user is not able to check if the record exists in the Digital Registries database because of an invalid request
    Given The user wants to check if a record exists in the Digital Registries database
    When The user triggers an action with an invalid request to check if the record exists in the database
    Then Operation returns an error because of an invalid request
