Feature: API endpoint allowing users to remove a record from the Digital Registries database.
  Request endpoint: DELETE /data/{registryname}/{versionnumber}/{id}/delete

  Background:
    Given The user wants to remove a record that exists in the Digital Registries database

  Scenario: The user successfully removes a record from the Digital Registries database
    Given The record does exist in the database
    When The user triggers an action to delete the database record
    And The valid DELETE request is sent
    Then Operation finishes successfully

  Scenario: The user is not able to remove a record from the Digital Registries database because the record does not exist
    Given The record does not exist in the database
    When The user triggers an action to delete the database record
    And The valid DELETE request is sent
    Then Operation results in an error
