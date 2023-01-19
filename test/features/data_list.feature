Feature: API endpoint allowing users to search multiple records in the Digital Registries database.
  Request endpoint: GET /data/{registryname}/{versionnumber}/

  Scenario: The user receives a list with all searched records in the Digital Registries database
    Given The user wants to search for a specific value and the searched value exists in several records in the database
    When The user triggers an action to search in the database
    Then The user receives a list with all records including searched value

  Scenario: The user receives an empty list from the Digital Registries database
    Given The user wants to search for a specific value and the searched value does not exist in any record in the database
    When The user triggers an action to search in the database
    Then The user receives an empty list because there is no record including the searched value in the database

  Scenario: The user is not able to search for the records in the Digital Registries database because of an invalid request
    Given The user wants to search for a specific value and the searched value exists in several records in the database
    When The user triggers an action to search in the database and send an invalid request
    Then Operation results in an error because of an invalid request
