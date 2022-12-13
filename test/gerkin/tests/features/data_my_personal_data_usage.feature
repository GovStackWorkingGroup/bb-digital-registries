Feature: Allows a user to see who has read their personal data..
  Request endpoint: GET /data/MyPersonalDataUsage/{version}/

  Background:
    Given database with the valid schema has been set up

  Scenario: Successfully get a list with all users which read my personal data
    When I make a GET request with a valid payload which contains all required fields
    Then I receive a HTTP 200 response
    And I received the records as an object

  Scenario: Failure get a list with all users which read my personal because required datas are not provided
    When When I make a GET request with a invalid payload
    Then I receive a HTTP 400 response
    