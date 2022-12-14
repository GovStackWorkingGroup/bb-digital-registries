Feature: API endpoint allowing users to remove a record from the Digital Registries database.
  Request endpoint: DELETE /data/{registryname}/{versionnumber}/{id}/delete

  Background:
    Given The user wants to remove a record which exists in the Digital Registries database

  Scenario: The user successfully removes a record from the Digital Registries database
    And The record does exist in the database
    When The user triggers an action to delete the database record
    And The valid DELETE request is sent
    And The record exists in the database
    Then The record is removed from the database
    And The user receives a success message

  Scenario: The user is not able to remove a record from the Digital Registries database because the record does not exist
    And The record does not exist in the database
    When The user triggers an action to delete the database record
    And The valid DELETE request is sent
    And The record does not exist in the database
    Then The user receives an error message
