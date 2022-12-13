Feature: API endpoint that allows user to create or modify database schema.
  Request endpoint: POST /database/modify/

  Background:
    Given database with the valid schema has been set up

  Scenario: Successfully create database schema
    When I make a POST request with a valid payload
    Then I receive a HTTP 200 response
    And I receive a schema as an object

  Scenario: Successfully modify database schema
    When I make a POST request with a valid payload
    Then I receive a HTTP 200 response
    And I receive a schema as an object

  Scenario: Failure when create database schema
    When I make a GET request with a invalid payload
    Then I receive a HTTP 400 response

  Scenario: Failure when modify database schema
    When I make a GET request with a invalid payload
    Then I receive a HTTP 400 response
