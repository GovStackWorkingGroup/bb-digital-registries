Feature: API endpoint that allows users to update multiple records in the Digital Registries database.
  Request endpoint: PUT /data/{registryname}/{versionnumber}/update-entries

  Scenario: User successfully updates two existing records in the Digital Registries database
    Given The user wants to update multiple records in the Digital Registries database and these records already exist
    When The user sends a valid request to update records in the database
    Then The record update process completes successfully

  Scenario: The user is unable to update two records that do not exist in the Digital Registries database
    Given The user wants to update multiple records in the Digital Registries database and these records do not exist
    When The user sends a valid request to update records in the database
    Then The result of an operation to update records returns an error

  Scenario: The user is unable to update two records in the Digital Registries database due to an invalid request
    Given The user wants to update multiple records in the Digital Registries database
    When The user sends an invalid request to update records in the database
    Then The result of an operation to update records returns an error because the request is invalid

  Scenario: The user is not able to update two records in the Digital Registries database because of missing users data
    Given The user wants to update multiple records in the Digital Registries database
    When The user sends an invalid request with missing user data to update records in the database
    Then The result of an operation to update records returns an error because of missing users data
