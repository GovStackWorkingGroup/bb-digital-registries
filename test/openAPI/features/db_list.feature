Feature: API endpoint through which users can retrieve information about Digital Registries databases.
  Request endpoint: GET /databases

    Background:
      Given User wants to view information about all Digital Registries databases

    Scenario: The user receives information about Digital Registries databases
      When The user sends a valid request to view information about Digital Registries databases
      Then The user has received a list of Digital Registries databases

    Scenario: The user is unable to obtain information about Digital Registries databases because the header is empty
      When The user sends an invalid request to view information about Digital Registries databases
      Then The result of an operation to receive information about the Digital Registers databases returns an error

    Scenario: The user is unable to receive information about Digital Registries databases because the header is not included
      When The user sends a request without payload to view information about Digital Registries databases
      Then The result of receiving information about databases of Digital Registries is an error
