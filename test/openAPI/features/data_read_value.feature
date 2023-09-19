@method=GET @endpoint=/data/{registryname}/{versionnumber}/{uuid}/read-value/{field}.{ext}
Feature: API endpoint that allows users to search for the field value of a record in the database.
  
  @smoke @unit @positive
  Scenario: The user gets the first name of the searched user from the database smoke type test
    Given The user wants to search for the user's first name of the user in the database
    When User sends GET request with given Information-Mediator-Client header, "registryname" as registryname and "111" as versionnumber, "80bcb084-fa17-11ed-be56-0242ac120002" as uuid, "FirstName" as field and "json" as ext
    Then User receives a response from the GET /data/{registryname}/{versionnumber}/{uuid}/read-value/{field}.{ext} endpoint
    And The GET /data/{registryname}/{versionnumber}/{uuid}/read-value/{field}.{ext} endpoint response should be returned in a timely manner 15000ms
    And The GET /data/{registryname}/{versionnumber}/{uuid}/read-value/{field}.{ext} endpoint response should have status 200
    And The GET /data/{registryname}/{versionnumber}/{uuid}/read-value/{field}.{ext} response should have "content-type": "application/json" header
    And The GET /data/{registryname}/{versionnumber}/{uuid}/read-value/{field}.{ext} endpoint response should match json schema
