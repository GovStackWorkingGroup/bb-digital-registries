@data
Feature: API endpoint allowing users to create a new record in the Digital Registries database.
  Request endpoint: POST /data/{registryname}/{versionnumber}/create

  Scenario: The user successfully creates the record "John Smith" in the Digital Registries database
    Given The user wants to create a new record "John Smith" in the Digital Registries database
    When The user triggers an action to create a new record "John Smith" in the database
    Then Operation finishes successfully for create user "John Smith"

  Scenario: The user is not able to create a record in the database which not exist
    Given The user wants to create a new record "Anna Stock" in the Digital Registries database
    Given The database does not exist
    When The user triggers an action to create a new record "Anna Stock" in the database
    Then Operation results in an error for create "Anna Stock"

  Scenario: The user is not able to create a record in the Digital Registries database
    Given The user wants to create a new record "Emma Watson" in the Digital Registries database
    When The user triggers an action to create a new record "Emma Watson" in the database
    Then Operation results in an error for create "Emma Watson"
