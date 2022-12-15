@data
Feature: API endpoint allowing users to create a new record in the Digital Registries database.
  Request endpoint: POST /data/{registryname}/{versionnumber}/create

  Background:
    Given The user wants to create a new record in the Digital Registries database

  Scenario: The user successfully creates the record in the Digital Registries database
    Given The record does not exist in the database 
    When The user triggers an action to create a new record in the database
    And The request with a valid payload is sent
    Then Operation finishes successfully

  Scenario: The user is not able to create a record that already exists in the Digital Registries database
    Given The record already exists in the database 
    When The user triggers an action to create a new record in the database
    And The request with a valid payload is sent
    Then Operation results in an error

  Scenario: The user is not able to create a record in the database which not exist
    Given The database does not exist
    When The user triggers an action to create a new record in the database
    And The request with a valid payload is sent
    Then Operation results in an error

  Scenario: The user is not able to create a record in the Digital Registries database
    When The user triggers an action to create a new record in the database
    And The request with an invalid payload is sent
    Then Operation results in an error
