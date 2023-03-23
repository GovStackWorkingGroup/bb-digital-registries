@method=POST @endpoint=/database/modify
Feature: API endpoint that allows users to create or modify the Digital Registries database schema.

  @smoke
  Scenario: The user successfully creates the Digital Registries database schema smoke test type

    Given User wants to create or modify the Digital Registries database schema
    When User sends POST request with given Information-Mediator-Client header
    Then User receives a response from the /database/modify endpoint
    And The /database/modify endpoint response should be returned in a timely manner 15000ms
    And The /database/modify endpoint response should have status 200
    And The /database/modify endpoint response should have content-type: application/json header
    And The /database/modify endpoint response should match json schema

  @unit @positive 
  Scenario Outline: The user successfully creates the Digital Registries database schema

    Given User wants to create or modify the Digital Registries database schema
    When User sends POST request with given Information-Mediator-Client header and body
    Then User receives a response from the /database/modify endpoint
    And The /database/modify endpoint response should be returned in a timely manner 15000ms
    And The /database/modify endpoint response should have status 200
    And The /database/modify endpoint response should have content-type: application/json header
    And The /database/modify endpoint response should match json schema
