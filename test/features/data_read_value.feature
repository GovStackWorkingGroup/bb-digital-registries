Feature: API endpoint allowing users to search for one record's field value in the Digital Registries database.
  Request endpoint: GET /data/{registryname}/{versionnumber}/{uuid}/read-value/{field}.{ext}

  Scenario: The user receives the first name of searched user from the Digital Registries database
    Given The user wants to search for the first name of the user in the Digital Registries database and the record's first name is fulfilled
    When The user triggers an action to receive the first name of searched user from the database
    Then The user receives the first name of the searched user

  Scenario: The user does not receive the first name of searched user from the Digital Registries database
    Given The user wants to search for the first name of the user in the Digital Registries database and the record's first name is empty
    When The user triggers an action to receive the first name of searched user from the database
    Then The user receives a message that the first name of the searched user is empty

  Scenario: The user is not able to receive the first name of the user from the Digital Registries database because of an invalid request
    Given The user wants to search for the first name of the user in the Digital Registries database
    When The user triggers an action to receive the first name of searched user from the database with an invalid request
    Then Operation results for receive the first name of the user is an error
