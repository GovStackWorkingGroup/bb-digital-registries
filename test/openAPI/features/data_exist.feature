@method=GET @endpoint=/data/{registryname}/{versionnumber}/exists
Feature: API endpoint that allows users to check if an entry exists in the database.

  @smoke
    Scenario: Successfully receives a message that the record exists in database
    Given get the database users information of Digital Registries
    When POST request with given path params "registryname" as registryname and "111" as versionnumber
    And given body "ID" as ID and "FirstName" as FirstName and "LastName" as LastName and "BirthertificateID" as BirthCertificateID
    Then response from /data/{registryname}/{versionnumber}/exist is received
    And response should be returned in a timely manner 15000ms
    And response should have status 200
    And response should have content-type: application/json header
    And response should match json schema

  @positive @unit
    Scenario: Successfully receive status value true for existing record
    Given get the database users information of Digital Registries
    When POST request with given path params "registryname" as registryname and "111" as versionnumber
    And given body "ID" as ID and "John" as FirstName and "LastName" as LastName and "BirthertificateID" as BirthCertificateID
    Then response from /data/{registryname}/{versionnumber}/exist is received
    And response should be returned in a timely manner 15000ms
    And response should have status 200
    And response should have content-type: application/json header
    And response should match json schema
    And response should return status true for existing record

  @positive @unit
    Scenario: Successfully receive status value false for non-existing record
    Given get the database users information of Digital Registries
    When POST request with given path params "registryname" as registryname and "111" as versionnumber
    And given body "ID" as ID and "Jack" as FirstName and "LastName" as LastName and "BirthertificateID" as BirthCertificateID
    Then response from /data/{registryname}/{versionnumber}/exist is received
    And response should be returned in a timely manner 15000ms
    And response should have status 200
    And response should have content-type: application/json header
    And response should match json schema
    And response should return status false for non-existing record
