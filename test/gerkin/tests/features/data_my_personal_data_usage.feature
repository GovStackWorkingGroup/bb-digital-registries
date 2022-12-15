Feature: API endopoint allowing users to check who had read their personal data in the Digital Registries database.
  Request endpoint: GET /data/MyPersonalDataUsage/1.0/

  Background:
    Given The user wants to check who had read his personal data in the Digital Registries database

  Scenario: The user receives a list with all records that had read his personal data in the Digital Registries database
    Given In the database, there is a list of users who read his personal data
    When The user triggers an action to receive a list od users who read his personal data
    And The request is sent
    Then The user receives a list with all records

  Scenario: The user receives an empty list of records that had read his personal data from the Digital Registries database
    Given In the database, a list of users who read his personal data is empty
    When The user triggers an action to receive a list od users who read his personal data
    And The request is sent
    Then The user receives an empty list because there are no records in the database about other users who read his personal data

  Scenario: The user is not able to receive data from the Digital Registries database
    When The user triggers an action to receive a list od users who read his personal data
    And The invalid request is sent
    Then Operation results in an error
