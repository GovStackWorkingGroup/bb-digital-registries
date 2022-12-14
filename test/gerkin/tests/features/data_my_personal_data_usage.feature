Feature: API endopoint allowing users to check who had read their personal data in the Digital Registries database.
  Request endpoint: GET /data/MyPersonalDataUsage/1.0/

  Background:
    Given The user wants to check who had read his personal data in the Digital Registries database

  Scenario: The user receives a list with all records that had read his personal data in the Digital Registries database
    And Some users read his personal data
    When The user triggers an action to receive a list od users who read his personal data
    And The request is sent
    And In the database, there is a list of users who read his personal data
    Then The user receives a list with all records

  Scenario: The user receives an empty list of records that had read his personal data from the Digital Registries database
    And No one read his personal data
    When The user triggers an action to receive a list od users who read his personal data
    And The request is sent
    And In the database, a list of users who read his personal data is empty
    Then The user receives an empty list because there is no record because no one read his personal data in the database

  Scenario: The user is not able to receive data from the Digital Registries database
    And Some users read his personal data
    When The user triggers an action to receive a list od users who read his personal data
    And The invalid request is sent
    Then The user received an error message
