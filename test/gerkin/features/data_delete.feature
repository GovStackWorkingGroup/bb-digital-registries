Feature: API endpoint allowing users to remove a record from the Digital Registries database.
  Request endpoint: DELETE /data/{registryname}/{versionnumber}/{id}/delete

  Scenario: The user successfully removes a record from the Digital Registries database
    Given The user wants to remove record with id=ID1234 from the Digital Registries database
    And The record with id=ID1234 does exist in the database
    When The user triggers an action to delete the database record with with id=ID1234
    Then Operation to delete record with with id=ID1234 finishes successfully

  Scenario: The user is not able to remove a record from the Digital Registries database because the record does not exist
    Given The user wants to remove record with id=ID001 from the Digital Registries database
    And The record with id=ID001 does not exist in the database
    When The user triggers an action to delete the database record with id=ID001
    Then Operation results to delete record with id=ID001 is an error
