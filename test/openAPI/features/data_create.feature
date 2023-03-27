@method=POST @endpoint=/data/{registryname}/{versionnumber}/create
Feature: API endpoint that allows users to create a new record in the database.

  @smoke @positive @unit
  Scenario: The user successfully creates a record in the database

    Given The user wants to create a new record in the database
    When User sends POST request with given Information-Mediator-Client header, body, "registryname" as registryname and "111" as versionnumber
    Then User receives a response from the POST /data/{registryname}/{versionnumber}/create endpoint
    And The POST /data/{registryname}/{versionnumber}/create endpoint response should be returned in a timely manner 15000ms
    And The POST /data/{registryname}/{versionnumber}/create endpoint response should have status 200
    And The POST /data/{registryname}/{versionnumber}/create endpoint response should have content-type: application/json header
    And The POST /data/{registryname}/{versionnumber}/create endpoint response should match json schema
