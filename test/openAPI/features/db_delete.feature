@method=DELETE @endpoint=/database/{id}
Feature: API endpoint that allows user to delete database schema

  @smoke @positive @unit
    Scenario: User successfully deletes the Digital Registries schema smoke type test
      Given User wants to delete the Digital Registries schema
      When The DELETE request with given Information-Mediator-Client header and "75858" as id is sent
      Then User receives a response from the DELETE /database/id endpoint
      And The DELETE /database/id endpoint response should be returned in a timely manner 15000ms
      And The DELETE /database/id endpoint response should have status 200
      And The DELETE /database/id response should have "content-type": "application/json" header
      And The DELETE /database/id endpoint response should match json schema

  @positive @unit
    Scenario Outline: User successfully deletes the Digital Registries schema
      Given User wants to delete the Digital Registries schema
      When The DELETE request with given Information-Mediator-Client header and "<id>" as id is sent
      Then User receives a response from the DELETE /database/id endpoint
      And The DELETE /database/id endpoint response should be returned in a timely manner 15000ms
      And The DELETE /database/id response should have "content-type": "application/json" header
      And The DELETE /database/id endpoint response should match json schema
      And The DELETE /database/id endpoint response should have body "Success"

    Examples: Valid data
    | id     |
    | 6745   |
    | 896756 |
    | 234234 |
