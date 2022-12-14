Feature: API endopont allowing users to check if a record exists in the Digital Registries database.
  Request endpoint: POST /data/{registryname}/{versionnumber}/exists

  Scenario: The user receives a message that the record exists in the Digital Registries database
    Given The user wants to check if a record with the first name "John Helmut" exists in the Digital Registries database
    And The record with the first name "John Helmut" is available in the database 
    When The user triggers an action to check if the record already exists in the database
    And The request with a valid payload is sent
    And The searched record exists in the database
    Then The user receives a success message with information that the record exists in the database

  Scenario: The user receives the message that the record does not exist in the Digital Registries database
    Given The user wants to check if a record with the first name "Adrien" exists in the Digital Registries database
    And The record with the first name "Adrien" is not available in the database 
    When The user triggers an action to check if the record exists in the database
    And The request with a valid payload is sent
    And The searched record doesn't exist in the database
    Then The user receives a success message with information that the record does not exist in the database

  Scenario: The user is not able to check if the record exists in the Digital Registries database
    When The user triggers an action to check if the record exists in the database
    And The request with an invalid payload is sent
    Then The user receives an error message
