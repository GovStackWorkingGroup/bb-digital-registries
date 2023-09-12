@method=POST @endpoint=/database/modify
Feature: API endpoint that allows user to create or modify database schema.

  @smoke @unit @positive
  Scenario: The user successfully creates a database schema

    Given User wants to create or modify the database schema
    When User sends POST request with given Information-Mediator-Client header and body
    Then User receives a response from the /database/modify endpoint
    And The /database/modify endpoint response should be returned in a timely manner 15000ms
    And The /database/modify endpoint response should have status 200
    And The /database/modify endpoint response should have content-type: "application/json" as ContentType
    And The /database/modify endpoint response should match json schema
