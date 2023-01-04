Feature: API endpoint allowing users to get information about Digital Registries databases.
  Request endpoint: GET /databases

    Background:
      Given The user wants to display information about all Digital Registries databases

    Scenario: The user receives information about Digital Registries databases
      When The user triggers an action with a valid payload to display information about Digital Registries databases
      Then The user received a list of Digital Registries databases

    Scenario: The user is not able to receive information for Digital Registries databases because of empty value in the header
      When The user triggers an action with an invalid payload to display information about Digital Registries databases
      Then The operation of receiving information about the databases of Digital Registers results with an error of the invalid header

    Scenario: The user is not able to receive information for Digital Registries databases because of not including header
      When The user triggers an action without a payload to display information about Digital Registries databases
      Then The operation of receiving information about the databases of Digital Registries results with an error
