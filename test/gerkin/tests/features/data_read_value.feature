Feature: Searches and returns one record’s one field value.
  Request endpoint: GET /data/{code}/{version}/{uuid}/read-value/{field}.{ext}

  Background:
    Given database with the valid schema has been set up

  Scenario: Successfully get one field value from one record
    When I make a GET request with a valid payload which contains all required fields
    Then I receive a HTTP 200 response
    And I received the records as an object

  Scenario: Failure get one field value from one record because required datas are not provided
    When When I make a GET request with a invalid payload
    Then I receive a HTTP 400 response
    