Feature: API endpoint allowing users to update multiple records in the Digital Registries database.
  Request endpoint: PUT /data/{registryname}/{versionnumber}/update-entries

  Background:
    Given The user wants to update multiple records in the Digital Registries database

  Scenario: The user successfully updates two existing records in the Digital Registries database
    And The records exists in the database
    When The user triggers an action to update two records in the database
    And The request with a valid payload is sent
    And All requested records exists in the database
    Then All the requested records are updated
    And The user receives a success message

  Scenario: The user is not able to update two records which not exist in the Digital Registries database
    And The records does not exist in the database
    When The user triggers an action to update two records in the database
    And The request with a valid payload is sent
    And None of requested records exist in the database
    Then The user receives an error message

  Scenario: The user is not able to update two records in the Digital Registries database
    When The user triggers an action to update two records in the database
    And The request with an invalid payload is sent
    Then The user receives an error message
