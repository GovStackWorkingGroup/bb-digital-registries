Feature: Updates one existing record in the registry database.
  Request endpoint: PUT /data/{code}/{version}/update

  Background:
    Given database with the valid schema has been set up

  Scenario: Successfully update one existing record
    When I make a PUT request with a valid payload
    Then I receive a HTTP 200 response

  Scenario: Failure when update one existing record with wrong data
    When I make a PUT request with a invalid payload
    Then I receive a HTTP 400 response
