Feature: Remove record from the database.
  Request endpoint: DELETE /data/{code}/{version}/delete

  Background:
    Given database with the valid schema has been set up

  Scenario: Successfully delete existing record
    When I make a DELETE request with a valid payload ID <ID>
    Then I receive a HTTP 204 response

  Scenario: Failure when delete existing record
    When I make a DELETE request with a invalid payload
    Then I receive a HTTP 400 response

    Examples:
    | ID    |
    | MCTS1 |
    | MCTS2 |
    