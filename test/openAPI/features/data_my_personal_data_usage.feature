@method=GET @endpoint=/data/MyPersonalDataUsage/1.0
Feature: API endpoint that allows users to check who has read their personal data.

The purpose of this API is to make personal data protection better and make BB personal 
data usage transparent by showing who has looked at personal data of the user.

  @smoke @unit @positive
  Scenario: The user gets a list of all records that have read his personal data smoke test type
    Given The user wants to check who has read his personal data
    When User sends GET /data/MyPersonalDataUsage/1.0 request with given Information-Mediator-Client header, "EE378129277266" as userID and "MCTS" as DatabaseID
    Then User receives a response from the /data/MyPersonalDataUsage/1.0 endpoint
    And The /data/MyPersonalDataUsage/1.0 endpoint response should be returned in a timely manner 15000ms
    And The /data/MyPersonalDataUsage/1.0 endpoint response should have status 200
    And The /data/MyPersonalDataUsage/1.0 endpoint response should have content-type: application/json header
    And The /data/MyPersonalDataUsage/1.0 endpoint response should match json schema

  @unit @positive
  Scenario Outline: The user gets a list of all records that have read his personal data
    Given The user wants to check who has read his personal data
    When User sends GET /data/MyPersonalDataUsage/1.0 request with given Information-Mediator-Client header, "<userID>" as userID and "<DatabaseID>" as DatabaseID
    Then User receives a response from the /data/MyPersonalDataUsage/1.0 endpoint
    And The /data/MyPersonalDataUsage/1.0 endpoint response should be returned in a timely manner 15000ms
    And The /data/MyPersonalDataUsage/1.0 endpoint response should have status 200
    And The /data/MyPersonalDataUsage/1.0 endpoint response should have content-type: application/json header
    And The /data/MyPersonalDataUsage/1.0 endpoint response should match json schema

    Examples:
    | userID         | DatabaseID |
    | EE378129127223 | MCTS       |
    | EE334569121212 | MCTS       |
    | EE390029120500 | MCTS       |

  @unit @negative
  Scenario: The user is not able to gets a list of all records that have read his personal data because of the invalid userID parameter
    Given The user wants to check who has read his personal data
    When User sends GET /data/MyPersonalDataUsage/1.0 request with given Information-Mediator-Client header, "..." as invalid userID and "MCTS" as DatabaseID
    Then User receives a response from the /data/MyPersonalDataUsage/1.0 endpoint
    And The /data/MyPersonalDataUsage/1.0 endpoint response should be returned in a timely manner 15000ms
    And The /data/MyPersonalDataUsage/1.0 endpoint response should have status 400

  @unit @negative
  Scenario: The user is not able to gets a list of all records that have read his personal data because of the invalid DatabaseID parameter
    Given The user wants to check who has read his personal data
    When User sends GET /data/MyPersonalDataUsage/1.0 request with given Information-Mediator-Client header, "EE378129277266" as userID and "..." as invalid DatabaseID
    Then User receives a response from the /data/MyPersonalDataUsage/1.0 endpoint
    And The /data/MyPersonalDataUsage/1.0 endpoint response should be returned in a timely manner 15000ms
    And The /data/MyPersonalDataUsage/1.0 endpoint response should have status 400
