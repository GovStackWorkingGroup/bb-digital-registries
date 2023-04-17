Feature: API endpoint that allows users to search multiple records in Digital Registries database.
  Request endpoint: GET /data/{registryname}/{versionnumber}/

  Scenario: The user gets a list of all searched records in the Digital Registries database
    Given The user wants to search for a specific value and the searched value exists in multiple records in the database
    When The user sends a valid request to search the database
    Then The operation results in an error due to an invalid query

  Scenario: The user receives an empty list from the Digital Registries database
    Given The user wants to search for a specific value and the searched value does not exist in any record in the database
    When The user sends a valid request to search the database
    Then The user receives an empty list because there is no record in the database that contains the searched value

  Scenario: The user cannot search for the records in the Digital Registries database due to an invalid query
    Given The user wants to search for a specific value and the searched value exists in multiple records in the database
    When The user sends an invalid request to search the database
    Then The operation results in an error due to an invalid query
