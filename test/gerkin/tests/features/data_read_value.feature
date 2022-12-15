Feature: API endpoint allowing users to search for one record's field value in the Digital Registries database.
  Request endpoint: GET /data/{registryname}/{versionnumber}/{uuid}/read-value/{field}.{ext}

  Background:
    Given The user wants to search for the first name of the user with UUID "DB-1" in the Digital Registries database

  Scenario: The user receives the first name of searched user from the Digital Registries database
    Given The record's first name is fullfill
    When The user triggers an action to receive the first name of searched user from the database
    And The request is sent
    Then The user receives the first name of the searched user

  Scenario: The user does not receive the first name of searched user from the Digital Registries database
    Given The record's first name is empty
    When The user triggers an action to receive the first name of searched user from the database
    And The request is sent
    Then The user receives a message that the first name of the searched user is empty

  Scenario: The user is not able to receive the first name of the user from the Digital Registries database
    When The user triggers an action to receive the first name of searched user from the database
    And The invalid request is sent
    Then Operation results in an error
