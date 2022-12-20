Feature: API endpoint allowing users to update multiple records in the Digital Registries database.
  Request endpoint: PUT /data/{registryname}/{versionnumber}/update-entries

  Background:
    Given The user wants to update multiple records in the Digital Registries database

  Scenario: The user successfully updates two existing records in the Digital Registries database
    Given The records exist in the database
    When The user triggers an action to update two records in the database
    And The request with a valid payload is sent
    Then Operation finishes successfully

  Scenario: The user is not able to update two records which do not exist in the Digital Registries database
    Given The records do not exist in the database
    When The user triggers an action to update two records in the database
    And The request with a valid payload is sent
    Then Operation results in an error

  Scenario: The user is not able to update two records in the Digital Registries database
    When The user triggers an action to update two records in the database
    And The request with an invalid payload is sent
    Then Operation results in an error
