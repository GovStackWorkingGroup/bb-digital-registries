Feature: API endpoint allowing users to update a new record in the Digital Registries database.
  Request endpoint: PUT /data/{registryname}/{versionnumber}/update

  Background:
    Given The user wants to update a record in the Digital Registries database

  Scenario: The user successfully updates the record in the Digital Registries database
    And The record exists in the database 
    When The user triggers an action to update a record in the database
    And The request with a valid payload is sent
    And The requested record exist in the database
    Then The record has been updated
    And The user receives a success message

  Scenario: The user is not able to udpade the record, because the record does not exist in the Digital Registries database
    And The record does not exist in the database 
    When The user triggers an action to update a record in the database
    And The request with a valid payload is sent
    And The requested record does not exist in the database
    Then The user receives an error message

  Scenario: The user is not able to update a record in the Digital Registries database
    And The record exists in the database 
    When The user triggers an action to update a new record in the database
    And The request with an invalid payload is sent
    Then The user receives an error message
