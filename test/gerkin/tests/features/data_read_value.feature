Feature: API endpoint allowing users to search for one record's field value in the Digital Registries database.
  Request endpoint: GET /data/{registryname}/{versionnumber}/{uuid}/read-value/{field}.{ext}

  Background:
    Given The user wants to search for the first name of the user with uuid "123" in the Digital Registries database


  Scenario: The user receives the first name of searches user from the Digital Registries database
    When The user triggers an action to receive the first name of searches user from the database
    And The request with a valid payload is sent
    Then The user receives a first name of the searches user

  Scenario: The user is not able to receive first name of the user from the Digital Registries database
    When The user triggers an action to receive a first name of searches user from the database
    And The request with an invalid payload is sent
    Then The user receives an error message
