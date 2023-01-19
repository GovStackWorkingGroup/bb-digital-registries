Feature: API endpoint allowing users to delete Digital registry schema.
  Request endpoint: DELETE /database/{id}/

  Scenario: The user successfully deletes the Digital Registries schema
    Given User wants to delete the Digital Registries schema and database schema exists
    When The user triggers an action to delete the database schema
    Then Operation to delete the database schema finishes successfully

  Scenario: The user is not able to delete the Digital Registries schema because the schema does not exist
    Given User wants to delete the Digital Registries schema and the database schema does not exist
    When The user triggers an action to delete the database schema
    Then Operation to delete a database schema returns an error because the schema does not exist
