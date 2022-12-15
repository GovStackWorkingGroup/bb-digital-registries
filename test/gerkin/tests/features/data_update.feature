Feature: API endpoint allowing users to update a new record in the Digital Registries database.
  Request endpoint: PUT /data/{registryname}/{versionnumber}/update

  Background:
    Given The user wants to update a record in the Digital Registries database

  Scenario: The user successfully updates the record in the Digital Registries database
    Given The record exists in the database 
    When The user triggers an action to update a record in the database
    And The request with a valid payload is sent
    Then Operation finishes successfully

  Scenario: The user is not able to udpate the record, because the record does not exist in the Digital Registries database
    Given The record does not exist in the database 
    When The user triggers an action to update a record in the database
    And The request with a valid payload is sent
    Then Operation results in an error

  Scenario: The user is not able to update a record in the Digital Registries database
    When The user triggers an action to update a new record in the database
    And The request with an invalid payload is sent
    Then Operation results in an error
