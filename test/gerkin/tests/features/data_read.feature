Feature: Searches and returns one record.
  Request endpoint: POST /data/{code}/{version}/read

  Background:
    Given database with the valid schema has been set up

  Scenario: Receive one existing record from the database
    When I make a POST request with a valid payload and ID <ID>
    Then I receive a HTTP 200 response
    And I receive one records as an object

    Examples:
    | ID    |
    | MCTS1 |
    | MCTS2 |

  Scenario: Not receive record from the database if record not exist
    When I make a POST request with a valid payload and ID <ID>
    Then I receive no record

    Examples:
    | ID    |
    | MCTS3 |
    | MCTS4 |

  Scenario: Failure get records when Information-Mediator-Client is not provide
    When When I make a GET request without Description Information-Mediator-Client
    Then I receive a HTTP 400 response
