Feature: API endopoint allowing users to search multiple records in the Digital Registries database.
  Request endpoint: GET /data/{registryname}/{versionnumber}/

  Background:
    Given The user wants to search for "John Helmut" in the Digital Registries database

  Scenario: The user receives a list with all records including "John Helmut" in the Digital Registries database
    When The user triggers an action to search "John Helmut" in the database
    And The request with a valid payload is sent
    Then The user receives a list with all records which including "John Helmut"

  Scenario: The user receives an empty list from the Digital Registries database
    When The user triggers an action to search "John Helmut" in the database
    And The request with a valid payload is sent
    Then The user receives an empty list because there is no record including "John Helmut" in the database

  Scenario: The user is not able to search for the records in the Digital Registries database
    When The user triggers an action to search "John Helmut" in the database
    And The request with an invalid payload is sent
    Then The user receives an error message
