Feature: Searches records based on input parameters and returns boolean answer.
  Request endpoint: POST /data/{code}/{version}/exist

  Background:
    Given database with the valid schema has been set up

  Scenario: Receive "true" when record exist
    When I make a POST request with a valid payload and ID <id>
    Then I receive a HTTP 200 response with the response <status>

    Examples:
    | id    | status |
    | MCTS1 | true   |
    | MCTS2 | true   |

  Scenario: Receive "false" when record not exist
    When I make a POST request with a valid payload and ID <id>
    Then I receive a HTTP 200 response with the response <status>

    Examples:
    | id    | status |
    | MCTS3 | false  |
    | MCTS4 | false  |

  Scenario: Failure get boolean answer when Information-Mediator-Client is not provide
    When I make a POST request with a invalid payload
    Then I receive a HTTP 400 response
