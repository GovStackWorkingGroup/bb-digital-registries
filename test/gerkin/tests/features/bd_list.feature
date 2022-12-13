Feature: API endpoint that allows user to get information about all databases.
  Request endpoint: GET /databases/

  Background:
    Given database with the valid schema has been set up

  Scenario: Successfully get information about all databases
    When I make a GET request with a valid payload
    Then I receive a HTTP 200 response
    And I receive an array list with all databases

  Scenario: Failure get information about all databases
    When I make a GET request with a invalid payload
    Then I receive a HTTP 400 response
