Feature: API endpoint allowing users to update multiple records in the Digital Registries database.
  Request endpoint: PUT /data/{registryname}/{versionnumber}/update-entries

  Scenario: The user successfully updates two existing records in the Digital Registries database
    Given The user wants to update multiple records with first name "Alfie" in the Digital Registries database
    And The records with first name "Alfie" exist in the database
    When The user triggers an action to update records with first name "Alfie" in the database
    Then Operation to update records with first name "Alfie" finishes successfully

  Scenario: The user is not able to update two records which do not exist in the Digital Registries database
    Given The user wants to update multiple records with first name "Jerry" in the Digital Registries database
    And The records with first name "Jerry" do not exist in the database
    When The user triggers an action to update records with first name "Jerry" in the database
    Then The result of an operation to update records with the first name 'Jerry' returns an error

  Scenario: The user is not able to update two records in the Digital Registries database because of an invalid request
    Given The user wants to update multiple records with name "Jasmine" in the Digital Registries database
    When The user triggers an action to update records with name "Jasmine" in the database
    Then The result of an operation to update records with the first name "Jasmine" returns an error

  Scenario: The user is not able to update two records in the Digital Registries database because of a missing users data
    Given The user wants to update multiple records with name "Joanna" in the Digital Registries database
    When The user triggers an action to update records with name "Joanna" in the database
    Then The result of an operation to update records with the first name "Joanna" returns an error
