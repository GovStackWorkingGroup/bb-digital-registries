Feature: API endpoint allowing users to delete Digital registries schema.
  Request endpoint: DELETE /database/{id}/

  Scenario: The user successfully deletes the Digital Registries schema
    Given User wants to delete the Digital Registries schema with id=12345
    And The requested database schema exists
    When The user triggers an action to delete the database schema with id=12345
    Then Operation to a delete database schema finishes successfully

  Scenario: The user is not able to delete the Digital Registries schema because schema does not exist
    Given User wants to delete the Digital Registries schema with id=12
    And The requested database schema does not exists
    When The user triggers an action to delete the database schema with id=12
    Then Operation to delete a database schema finishes successfully
