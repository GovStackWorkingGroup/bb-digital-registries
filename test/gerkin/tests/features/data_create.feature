@data
Feature: API endpoint allowing users to create a new record in the Digital Registries database.
  Request endpoint: POST /data/{registryname}/{versionnumber}/create

  Background:
    Given The user wants to create a new record in the Digital Registries database

  Scenario: The user successfully creates the record in the Digital Registries database
    And The record does not exist in the database 
    When The user triggers an action to create a new record in the database
    And The request with a valid payload is sent
    And The requested record does not exist in the database
    Then The record has been created
    And The user receives a success message

  Scenario: The user is not able to create a record that already exists in the Digital Registries database
    And The record already exists in the database 
    When The user triggers an action to create a new record in the database
    And The request with a valid payload is sent
    And The requested record does exist in the database
    Then The record has not been created
    And The user receives an error message

  Scenario: The user is not able to create a record in the database which not exist
    And The database does not exists
    When The user triggers an action to create a new record in the database
    And The request with a valid payload is sent
    And The database does not exists
    Then The record has not been created
    And The user receives an error message

  Scenario: The user is not able to create a record in the Digital Registries database
    And The record exists in the database 
    When The user triggers an action to update a new record in the database
    And The request with an invalid payload is sent
    Then The user receives an error message
