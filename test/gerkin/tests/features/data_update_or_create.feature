Feature: API updates existing record if matching with input parameters is successful. If record is not found the API will create a new record.
  Request endpoint: POST /data/{code}/{version}/update-or-create

  Background:
    Given database with the valid schema has been set up

  Scenario: Successfully update two existing records
    When I make a PUT request with a valid payload which contains all required fields
    Then I receive a HTTP 200 response

  Scenario: Failure when update two existing record with wrong data
    When I make a PUT request with a invalid payload
    Then I receive a HTTP 400 response
    