Feature: API endpoint that allows users to update a new record in the Digital Registries database.
  Request endpoint: PUT /data/{registryname}/{versionnumber}/update

  Scenario: The user successfully updates the record in the Digital Registries database
    Given The user wants to update a record in the Digital Registries database and a record exists
    When The user sends a valid request to update the record in the database
    Then The operation to update a record is completed successfully

  Scenario: The user cannot update the record because the record does not exist in the Digital Registries database
    Given The user wants to update the record in the Digital Registries database and the record does not exist
    When The user sends a valid request to update the record in the database
    Then The result of the operation to update the record is an error because the record does not exist in the database

  Scenario: The user is not able to update a record in the Digital Registries database because of an invalid request
    Given The user wants to update a record in the Digital Registries database and a record exists
    When The user sends an invalid request to update a new record in the database
    Then The result of the operation to update a record returns an error due to an invalid request
