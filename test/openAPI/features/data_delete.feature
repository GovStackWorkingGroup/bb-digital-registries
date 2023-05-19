@method=DELETE @endpoint=/data/{registryname}/{versionnumber}/{id}/delete
Feature: API endpoint that allows users to remove an entry from the database.

  @smoke
  Scenario: Successfully deletes a record from the database smoke type test
    Given The user wants to remove the record from the  database
    When User sends DELETE /data/{registryname}/{versionnumber}/{id}/delete request with given Information-Mediator-Client header, "registryname" as registryname and "111" as versionnumber, "EE378627348834" as ID
    Then User receives a response from the /data/{registryname}/{versionnumber}/{id}/delete endpoint
    And The /data/{registryname}/{versionnumber}/{id}/delete endpoint response should be returned in a timely manner 15000ms
    And The /data/{registryname}/{versionnumber}/{id}/delete endpoint response should have status 204

  @unit @positive
  Scenario Outline: Successfully deletes a record from the database
    Given The user wants to remove the record from the  database
    When User sends DELETE /data/{registryname}/{versionnumber}/{id}/delete request with given Information-Mediator-Client header, "registryname" as registryname and "111" as versionnumber, "<ID>" as ID
    Then User receives a response from the /data/{registryname}/{versionnumber}/{id}/delete endpoint
    And The /data/{registryname}/{versionnumber}/{id}/delete endpoint response should be returned in a timely manner 15000ms
    And The /data/{registryname}/{versionnumber}/{id}/delete endpoint response should have status 204

    Examples:
    | ID             |
    | EE378627348855 |
    | RR378627348834 |
    | DD378627348834 |
