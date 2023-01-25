Feature: API endpoint allowing users to search for one record in the Digital Registries database.
  Request endpoint: POST /data/{registryname}/{versionnumber}/read

  Scenario: The user receives one searched record from the Digital Registries database
    Given The user wants to search for one record in the Digital Registries database and the searched record exists in the database
    When The user triggers an action to search for a record in the database
    Then The user receives a searched record

  Scenario: The user does not receive searched record from the Digital Registries database
   Given The user wants to search for one record in the Digital Registries database and the searched record does not exist in the database
    When The user triggers an action to search for a record in the database
    Then The user receives a message that there is no searched record in the database

  Scenario: The user is not able to receive one searched record from the Digital Registries database because of an invalid request
    Given The user wants to search for one record in the Digital Registries database
    When The user triggers an action with an invalid request to search for a record in the Digital Registries database
    Then Operation results for receiving one searched record is an error
