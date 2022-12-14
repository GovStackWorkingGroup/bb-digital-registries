Feature: API endpoint allowing users to search multiple records in the Digital Registries database.
  Request endpoint: GET /data/{registryname}/{versionnumber}/

  Scenario: The user receives a list with all records including "John Helmut" in the Digital Registries database
    Given The user wants to search for "John Helmut" in the database
    And The records including "John Helmut" exists in the database
    When The user triggers an action to search "John Helmut" in the database
    And The request with a valid payload is sent
    And The searched value exists in several records in the database
    Then The user receives a list with all records including "John Helmut"

  Scenario: The user receives an empty list from the Digital Registries database
    Given The user wants to search for "Adrien" in the database
    And The records including "Adrien" do not exist in the database
    When The user triggers an action to search "Adrien" in the database
    And The request with a valid payload is sent
    And The searched value does not exist in any record in the database
    Then The user receives an empty list because there is no record including "Adrien" in the database

  Scenario: The user is not able to search for the records in the Digital Registries database
    Given The user wants to search for "John Helmut" in the database
    And The records including "John Helmut" exists in the database
    When The user triggers an action to search "John Helmut" in the database
    And The request with an invalid payload is sent
    Then The user receives an error message
