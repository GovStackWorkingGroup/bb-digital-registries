@method=GET @endpoint=/data/{registryname}/{versionnumber}/exists
Feature: API endpoint that allows users to check if an entry exists in the database.

  @smoke @positive @unit
    Scenario: Successfully receives a message that the record exists in database smoke type test
    Given user wants to check if the searched record exists in the database
    When send POST request to check if the record exist in the database is sent with given path params "registryname" as registryname and "111" as versionnumber
    And given body "ID" as ID and "John" as FirstName and "LastName" as LastName and "BirthertificateID" as BirthCertificateID
    Then the response from /data/{registryname}/{versionnumber}/exist is received
    And the response from /data/{registryname}/{versionnumber}/exists should be returned in a timely manner 15000ms
    And the response from /data/{registryname}/{versionnumber}/exists should have status 200
    And the response from /data/{registryname}/{versionnumber}/exists should have content-type: application/json header
    And the response from /data/{registryname}/{versionnumber}/exists should match json schema
    And the response from /data/{registryname}/{versionnumber}/exists should return status true for existing record

  @negative @unit
    Scenario Outline: Successfully receives a message that the record not exists in database
    Given user wants to check if the searched record exists in the database
    When send POST request to check if the record exist in the database is sent with given path params "registryname" as registryname and "111" as versionnumber
    And given body "ID" as ID and "<FirstName>" as FirstName and "LastName" as LastName and "BirthCertificateID" as BirthCertificateID
    Then the response from /data/{registryname}/{versionnumber}/exist is received
    And the response from /data/{registryname}/{versionnumber}/exists should be returned in a timely manner 15000ms
    And the response from /data/{registryname}/{versionnumber}/exists should have status 200
    And the response from /data/{registryname}/{versionnumber}/exists should have content-type: application/json header
    And the response from /data/{registryname}/{versionnumber}/exists should match json schema
    And the response from /data/{registryname}/{versionnumber}/exists should return status false for non-existing record

    Examples:
      | FirstName |
      | Mike |
      | Thomas |
      | Brook |
      | Alice |
