Feature: API endpoint allowing users to search for one record's field value in the Digital Registries database.
  Request endpoint: GET /data/{registryname}/{versionnumber}/{uuid}/read-value/{field}.{ext}

  Background:
    Given The user wants to search for the first name of the user with UUID "DB-1" in the Digital Registries database

  Scenario: The user receives the first name of searches user from the Digital Registries database
    When The user triggers an action to receive the first name of searched user from the database
    And The request is sent
    And The searched record's first name is fullfill
    Then The user receives the first name of the searched user

  Scenario: The user does not receives the first name of searches user from the Digital Registries database
    When The user triggers an action to receive the first name of searched user from the database
    And The request is sent
    And The searched record's first name is empty
    Then The user receives a message that the first name of the searched user is empty

  Scenario: The user is not able to receive the first name of the user from the Digital Registries database
    When The user triggers an action to receive the first name of searched user from the database
    And The invalid request is sent
    Then The user receives an error message
