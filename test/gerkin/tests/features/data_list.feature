Feature: Searches and returns multiple records as an array-list.
  Request endpoint: GET /data/{code}/{version}/

  Background:
    Given database with the valid schema has been set up

  Scenario: Successfully get multiple records as an array-list
    When I make a GET request with a valid Description Information-Mediator-Client
    Then I receive a HTTP 200 response
    And I received the records as an array-list

  Scenario: Successfully get all records with name "John"
    When I make a GET request with a valid Description Information-Mediator-Client and search "John"
    Then I received the records which includes "John" as an array-list

  Scenario: Failure get records when Information-Mediator-Client is not provide
    When When I make a GET request without Description Information-Mediator-Client
    Then I receive a HTTP 400 response
