Feature: API endpoint allowing users to search multiple records in the Digital Registries database.
  Request endpoint: GET /data/{registryname}/{versionnumber}/

  Scenario: The user receives a list with all records including "John" in the Digital Registries database
    Given The user wants to search for "John" in the database
    And The searched value exists in several records in the database
    When The user triggers an action to search "John" in the database
    Then The user receives a list with all records including "John"

  Scenario: The user receives an empty list from the Digital Registries database
    Given The user wants to search for "Adrien" in the database
    And The searched value does not exist in any record in the database
    When The user triggers an action to search "Adrien" in the database
    Then The user receives an empty list because there is no record including "Adrien" in the database

  Scenario: The user is not able to search for the records in the Digital Registries database because on an invalid request
    Given The user wants to search for "Anna" in the database
    When The user triggers an action to search "Anna" in the database and sent an invalid request
    Then Operation results in an error
