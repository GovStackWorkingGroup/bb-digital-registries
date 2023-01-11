Feature: API endpoint allowing users to search for one record's field value in the Digital Registries database.
  Request endpoint: GET /data/{registryname}/{versionnumber}/{uuid}/read-value/{field}.{ext}

  Scenario: The user receives the first name of searched user from the Digital Registries database
    Given The user wants to search for the first name of the user with UUID 2dcad39a-9abb-4552-954d-c62958d44ec5 in the Digital Registries database
    Given The record's first name is fullfill
    When The user triggers an action to receive the first name of searched user with UUID 2dcad39a-9abb-4552-954d-c62958d44ec5 from the database
    Then The user receives the first name of the searched user

  Scenario: The user does not receive the first name of searched user from the Digital Registries database
    Given The user wants to search for the first name of the user with UUID 3dcad39a-9abb-4552-954d-c62958d44ec9 in the Digital Registries database
    And The record's first name is empty
    When The user triggers an action to receive the first name of searched user with UUID 3dcad39a-9abb-222-954d-c62958d44ec9 from the database
    Then The user receives a message that the first name of the searched user is empty

  Scenario: The user is not able to receive the first name of the user from the Digital Registries database because of an invalid request
    When The user triggers an action to receive the first name of searched user from the database
    Then Operation results for /data/registryname/versionnumber/uuid/read-value/field.ext is an error
