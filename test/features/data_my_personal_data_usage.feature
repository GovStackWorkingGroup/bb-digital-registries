Feature: API endpoint allowing users to check who had read their personal data in the Digital Registries database.
  Request endpoint: GET /data/MyPersonalDataUsage/1.0/

  Scenario: The user receives a list with all records that had read his personal data in the Digital Registries database
    Given The user wants to check who had read his personal data in the Digital Registries database and there is a list of users who did it
    When The user triggers an action to receive a list of users who read his personal data
    Then The user receives a list with all records

  Scenario: The user receives an empty list of records that had read his personal data from the Digital Registries database
    Given The user wants to check who had read his personal data in the Digital Registries database and there is an empty list of users who did it
    When The user triggers an action to receive a list of users who read his personal data
    Then The user receives an empty list because there are no records in the database about other users who read his personal data

  Scenario: The user is not able to receive data from the Digital Registries database because of an invalid request
    Given The user wants to check who had read his personal data in the Digital Registries database
    When The user triggers an action to receive a list of users who read his personal data with an invalid request
    Then Operation to receive a list of results is an error
