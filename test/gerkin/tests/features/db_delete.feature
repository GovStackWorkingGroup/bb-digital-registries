Feature: API endpoint that allows user to delete database schema.
  Request endpoint: DELETE /database/{id}/

  Background:
    Given database with the valid schema has been set up

  Scenario: Successfully delete database schema
    When I make a DELETE request with a valid payload
    Then I receive a HTTP 200 response
    And I receive a "Success" message

  Scenario: Failure when delete database schema
    When I make a DELETE request with a invalid payload
    Then I receive a HTTP 400 response
