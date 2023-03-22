@method=GET @endpoint=/databases
Feature: API endpoint through which users can retrieve information about Digital Registries databases.

    @smoke @unit @positive
    Scenario: The user receives information about Digital Registries databases
      Given User wants to view information about all Digital Registries databases
      When User sends GET request with given Information-Mediator-Client header
      Then User receives a response from the /databases endpoint
      And The /databases endpoint response should be returned in a timely manner 15000ms
      And The /databases endpoint response should have status 200
      And The /databases endpoint response should have content-type: application/json header
      And The /databases endpoint response should match json schema
