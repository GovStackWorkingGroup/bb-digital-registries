Feature: API endpoint allowing users to update multiple records in the Digital Registries database.
  Request endpoint: PUT /data/{registryname}/{versionnumber}/update-entries

  Scenario: The user successfully updates two existing records in the Digital Registries database
    Given The user wants to update multiple records in the Digital Registries database and those records exist
    When The user triggers an action to update records in the database
    Then Operation to update records finishes successfully

  Scenario: The user is not able to update two records that do not exist in the Digital Registries database
    Given The user wants to update multiple records in the Digital Registries database and those records do not exist
    When The user triggers an action to update records in the database
    Then The result of an operation to update records returns an error

  Scenario: The user is not able to update two records in the Digital Registries database because of an invalid request
    Given The user wants to update multiple records in the Digital Registries database
    When The user triggers an action to update records in the database with an invalid request
    Then The result of an operation to update records returns an error because of the invalid request

  Scenario: The user is not able to update two records in the Digital Registries database because of missing users data
    Given The user wants to update multiple records in the Digital Registries database
    When The user triggers an action to update records in the database with missing users data
    Then The result of an operation to update records returns an error because of missing users data
