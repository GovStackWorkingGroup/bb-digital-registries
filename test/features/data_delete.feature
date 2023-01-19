Feature: API endpoint allowing users to remove a record from the Digital Registries database.
  Request endpoint: DELETE /data/{registryname}/{versionnumber}/{id}/delete

  Scenario: The user successfully removes a record from the Digital Registries database
    Given The user wants to remove the record from the Digital Registries database
    And The record does exist in the database
    When The user triggers an action to delete the database record
    Then Operation to delete the record finishes successfully

  Scenario: The user is not able to remove a record from the Digital Registries database because the record does not exist
    Given The user wants to remove the record which does not exist from the Digital Registries database
    When The user triggers an action to delete the database the record which does not exist
    Then Operation results for deleting the record is an error because the record does not exist
