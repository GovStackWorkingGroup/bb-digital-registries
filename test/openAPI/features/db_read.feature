@method=GET @endpoint=/database/{id}
Feature: API endpoint that allows user to get database information with database schema.

  @smoke 
  Scenario: User successfully obtains Digital Registries database information with schema version smoke type test
    Given User wants to get the database information of Digital Registries with schema version
    When User sends GET request with given Information-Mediator-Client header and "1" as id
    Then User receives a response from the GET /database/id endpoint
    And The GET /database/id endpoint response should be returned in a timely manner 15000ms
    And The GET /database/id endpoint response should have status 200
    And The GET /database/id endpoint response should have content-type: application/json header
    And The GET /database/id endpoint response should match json schema

  @unit @positive 
  Scenario Outline: User successfully obtains Digital Registries database information with schema version
    Given User wants to get the database information of Digital Registries with schema version
    When User sends GET request with given Information-Mediator-Client header and "<id>" as id
    Then User receives a response from the GET /database/id endpoint
    And The GET /database/id endpoint response should be returned in a timely manner 15000ms
    And The GET /database/id endpoint response should have status 200
    And The GET /database/id endpoint response should have content-type: application/json header
    And The GET /database/id endpoint response should match json schema

    Examples: Valid data
    | id         |
    | 123        |
    | 8438778473 |
    | 3287483474 |
    | 8484848484 |
