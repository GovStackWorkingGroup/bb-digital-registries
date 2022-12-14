Feature: API endpoint allowing users to get information about Digital Registries databases.
  Request endpoint: GET /databases/

  Background:
    Given The user wants to display information about all Digital Registries databases

  Scenario: The user receives information about Digital Registries databases
    When The user triggers an action to display information about Digital Registries databases
    And The request with a valid payload is sent
    Then The user received a list of Digital Registries databases

  Scenario: The user is not able to receive information about Digital Registries databases
    When The user triggers an action to display information about Digital Registries databases
    And The request with an invalid payload is sent
    Then The user received an error message
