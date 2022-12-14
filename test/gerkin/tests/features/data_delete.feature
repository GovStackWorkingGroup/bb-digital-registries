Feature: API endpoint allowing users to remove a record from the Digital Registries database.
  Request endpoint: DELETE /data/{registryname}/{versionnumber}/{id}/delete

  Background:
    Given The user wants to remove a record which exist in the Digital Registries database

  Scenario: The user successfully removes a record from the Digital Registries schema
    When The user triggers an action to delete a database schema
    And The request with a valid payload is sent
    Then The user receives a success message

  Scenario: The user is not able to delete the Digital Registries schema
    When The user triggers an action to delete a database schema
    And The request with an invalid payload is sent
    Then The user receivess an error message

    