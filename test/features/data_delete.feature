Feature: API endpoint that allows users to remove an entry from the Digital Registries database.
  Request endpoint: DELETE /data/{registryname}/{versionnumber}/{id}/delete

  Scenario: The user successfully deletes a record from the Digital Registries database
    Given The user wants to remove the record from the Digital Registries database
    And The record exists in the database
    When The user sends a valid request to delete the database record
    Then The process to delete the record completes successfully

  Scenario: The user cannot remove a record from the Digital Registries database because it does not exist
    Given The user wants to remove the record that does not exist from the Digital Registries database
    When The user sends a valid request to delete the non-existent record from the database
    Then The result of the operation to delete the record is an error because the record does not exist
