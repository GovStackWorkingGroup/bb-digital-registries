Feature: API endpoint allowing users to update a new record in the Digital Registries database.
  Request endpoint: PUT /data/{registryname}/{versionnumber}/update

  Scenario: The user successfully updates the record in the Digital Registries database
    Given The user wants to update a record "John Helmut Smith Carry" in the Digital Registries database
    And The record "John Helmut Smith Carry" exists in the database 
    When The user triggers an action to update the record "John Helmut Smith Carry" in the database
    Then Operation to update the record "John Helmut Smith Carry" finishes successfully

  Scenario: The user is not able to udpate the record, because the record does not exist in the Digital Registries database
    Given The user wants to update the record "Anna Smith" in the Digital Registries database
    And The record "Anna Smith" does not exist in the database 
    When The user triggers an action to update the record "Anna Smith" in the database
    Then Operation results to update "Anna Smith" is an error

  Scenario: The user is not able to update a record in the Digital Registries database because of an invalid request
    Given The user wants to update a record in the Digital Registries database
    When The user triggers an action to update a new record in the database
    Then Operation results to update a record is an error
