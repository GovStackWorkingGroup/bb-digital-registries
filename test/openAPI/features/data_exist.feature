Feature: API endpoint that allows users to check if an entry exists in the Digital Registries database.
  Request endpoint: POST /data/{registryname}/{versionnumber}/exists

  Scenario: The user receives a message that the record exists in the Digital Registries database
    Given The user wants to check if a record exists in the Digital Registries database
    When The user sends a valid request to check if a record exists in the database
    Then The process of receiving a message that a record exists in the database completes successfully
    And The user receives the information that a record exists in the database

  Scenario: The user receives the message that the record does not exist in the Digital Registries database
    Given The user wants to check if the record exists in the Digital Registries database
    When The user sends a valid request to check if a record exists in the database
    Then The process of receiving a message that a record exists in the database completes successfully
    And The user receives the information that the record does not exist in the database

  Scenario: The user is unable to verify that the record exists in the Digital Registries database due to an invalid request
    Given The user wants to check if a record exists in the Digital Registries database
    When The user sends an invalid request to check if the record exists in the database
    Then The operation returns an error due to an invalid request
