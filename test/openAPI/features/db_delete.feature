Feature: API endpoint that allows users to clear the schema of Digital Registries schema.
  Request endpoint: DELETE /database/{id}/

  Scenario: User successfully deletes the Digital Registries schema
    Given The user wants to delete the Digital Registries schema and the database schema exists
    When The user sends a valid request to delete the database schema
    Then The operation to delete the database schema completes successfully

  Scenario: The user cannot delete the schema from Digital Registries because the schema does not exist
    Given The user wants to delete the Digital Registries schema and the database schema does not exist
    When The user sends a valid request to delete the database schema
    Then The operation to delete a database schema returns an error because the schema does not exist
