Feature: API endopoint allowing users to check who had read their personal data in the Digital Registries database.
  Request endpoint: GET /data/MyPersonalDataUsage/1.0/

  Scenario: The user receives a list with all records that had read his personal data in the Digital Registries database
    Given The user with id=282392302 wants to check who had read his personal data in the Digital Registries database
    And In the database, there is a list of users who read the user with id=282392302 personal data
    When The user with id=282392302 triggers an action to receive a list of users who read his personal data
    Then The user receives a list with all records

  Scenario: The user receives an empty list of records that had read his personal data from the Digital Registries database
    Given The user with id=748382347 wants to check who had read his personal data in the Digital Registries database
    And In the database there is an empty list of users who read the user with id=748382347 personal data
    When The user with id=748382347 triggers an action to receive a list od users who read his personal data
    Then The user with id=748382347 receives an empty list because there are no records in the database about other users who read his personal data

  Scenario: The user is not able to receive data from the Digital Registries database because of an invalid request
    Given The user with id=3782347 wants to check who had read his personal data in the Digital Registries database
    When The user with id=3782347 triggers an action to receive a list od users who read his personal data
    Then Operation to receive a list of results is an error
