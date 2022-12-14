Feature: API endpoint allowing users to update multiple records in the Digital Registries database.
  Request endpoint: PUT /data/{registryname}/{versionnumber}/update-entries

  Background:
    Given The user wants to update multiple records in the Digital Registries database

  Scenario: The user successfully updates two existing records in the Digital Registries database
    When The user triggers an action to update two records in the database
    And The request with a valid payload is sent
    Then The user receives a success message

  Scenario: The user is not able to update two records in the Digital Registries database
    When The user triggers an action to update two records in the database
    And The request with an invalid payload is sent
    Then The user receives an error message
