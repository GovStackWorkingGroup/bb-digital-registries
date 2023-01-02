Feature: API endpoint allowing users to get information about Digital Registries databases.
  Request endpoint: GET /databases

    Background: The user wants to display information about all Digital Registries databases
      Given The user wants to display information about all Digital Registries databases

    Scenario: The user receives information about Digital Registries databases
      When The user triggers an action with a valid payload to display information about Digital Registries databases
      Then The user received a list of Digital Registries databases

    Scenario: The user is not able to receive information for Digital Registries databases because of empty value in the header
      When The user triggers an action with an invalid payload to display information about Digital Registries databases
      Then The operation to receive information for Digital Registries databases results with wrong mediator error

    Scenario: The user is not able to receive information for Digital Registries databases because of not including header
      When The user triggers an action without a payload to display information about Digital Registries databases
      Then The operation to receive information for Digital Registries databases results with no mediator error
