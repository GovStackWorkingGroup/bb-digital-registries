Feature: API endpoint allowing users to create a new record if it not exists in the Digital Registries database or update records if already exists.
  Request endpoint: POST /data/{registryname}/{versionnumber}/update-or-create

  Scenario: The user successfully creates new record in the Digital Registries database
    Given The user wants to create a new record "Jon Snake" or update an existing one if already exists in the Digital Registries database
    And The requested record "Jon Snake" does not exist in the database
    When The user triggers an action to create or update record "Jon Snake" in the database
    Then Operation to create "Jon Snake" finishes successfully

  Scenario: The user successfully updates the already existing record in the Digital Registries database
    Given The user wants to create a new record "Johny Small" or update an existing one if already exists in the Digital Registries database
    And The requested record "Johny Small" already exists in the database
    When The user triggers an action to create or update record "Johny Small" in the database
    Then Operation to update record "Johny Small" finishes successfully

  Scenario: The user is not able to create/update a record in the Digital Registries database
    Given Given The user wants to create record "Ali Smith" or update an existing one if already exists in the Digital Registries database
    When The user triggers an action to create record "Ali Smith" in the database
    Then The result of an operation to create/update record 'Ali Smith' returns an error
