Feature: API endpoint that allows users to check who has read their personal data in the Digital Registries database.
  Request endpoint: GET /data/MyPersonalDataUsage/1.0/

  Scenario: The user gets a list of all records that have read their personal data in the Digital Registries database
    Given The user wants to check who has read his personal data in the Digital Registries database and there is a list of users who have done so
    When The user sends a valid request and receives a list of users who have read his personal data
    Then The user receives a list of all records

  Scenario: The user receives an empty list of records that have read his personal data from the Digital Registries database
    Given The user wants to check who has read his personal data from Digital Registries database and there is an empty list of users who have done so
    When The user sends a valid request and receives a list of users who have read his personal data
    Then The user receives an empty list because there are no records in the database about other users who have read his personal data

  Scenario: The user is unable to obtain data from the Digital Registries database due to an invalid request
    Given The user wants to check who has read his personal data in the Digital Registries database
    When The user sends an invalid request and receives a list of users who have read his personal data
    Then The operation to get a list of results is an error
