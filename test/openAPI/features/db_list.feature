@method=GET @endpoint=/databases
Feature: API endpoint that allows user to get information about all databases.

    @smoke @unit @positive
    Scenario: The user receives information about databases
      Given User wants to view information about all databases
      When User sends GET request with given Information-Mediator-Client header
      Then User receives a response from the /databases endpoint
      And The /databases endpoint response should be returned in a timely manner 15000ms
      And The /databases endpoint response should have status 200
      And The /databases endpoint response should have content-type: application/json header
      And The /databases endpoint response should match json schema
