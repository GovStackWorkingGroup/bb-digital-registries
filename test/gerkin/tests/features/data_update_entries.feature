Feature: Updates multiple records in the registry database that match the input query.
  Request endpoint: PUT /data/{code}/{version}/update-entries

  Background:
    Given database with the valid schema has been set up

  Scenario: Successfully update two existing records
    When I make a PUT request with a valid payload which contains all required fields
    Then I receive a HTTP 200 response

  Scenario: Failure when update two existing record with wrong data
    When I make a PUT request with a invalid payload
    Then I receive a HTTP 400 response
