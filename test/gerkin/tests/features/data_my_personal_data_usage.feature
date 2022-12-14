Feature: API endopoint allowing users to check who had read their personal data in the Digital Registries database.
  Request endpoint: GET /data/MyPersonalDataUsage/1.0/

  Background:
    Given The user wants to check who had read his personal data in the Digital Registries database

  Scenario: The user receives a list with all records that had read his personal data in the Digital Registries database
    When The user triggers an action to receive records from the database
    And The request with a valid payload is sent
    Then The user receives a list with all records

  Scenario: The user receives an empty list of records that had read his personal data from the Digital Registries database
    When The user triggers an action to receive records from the database
    And The request with a valid payload is sent
    Then The user receives an empty list because there is no record because no one read his personal data in the database

  Scenario: The user is not able to receive data from the Digital Registries database
    When The user triggers an action to receive records from the database
    And The request with an invalid payload is sent
    Then The user received an error message
    