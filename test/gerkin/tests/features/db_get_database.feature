Feature: API endpoint that allows user to get database information with schema.
  Request endpoint: GET /database/{id}/

  Background:
    Given database with the valid schema has been set up

  Scenario: Successfully get database information with schema
    When I make a GET request with a valid payload
    Then I receive a HTTP 200 response
    And I receive a schema as an object

  Scenario: Failure get database information with schema
    When I make a GET request with a invalid payload
    Then I receive a HTTP 400 response
