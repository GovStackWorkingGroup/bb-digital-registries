Feature: API endpoint that allows users to search for a record in the Digital Registries database.
  Request endpoint: POST /data/{registryname}/{versionnumber}/read

  Scenario: User obtains a searched record from the Digital Registries database
    Given The user wants to search for a record in the Digital Registries database and the searched record exists in the database
    When The user sends a valid request to search for a record in the database
    Then The user receives a searched record

  Scenario: The user does not receive a searched record from the Digital Registries database
   Given The user wants to search for a record in the Digital Registries database and the searched record does not exist in the database
    When The user sends a valid request to search for a record in the database
    Then The user receives a message that there is no searched record in the database

  Scenario: The user is unable to obtain a searched record from the Digital Registries database because the request is invalid
    Given The user wants to search for one record in the Digital Registries database
    When The user sends an invalid request to search for a record in the Digital Registries database
    Then The result of the operation to obtain a searched record is an error
