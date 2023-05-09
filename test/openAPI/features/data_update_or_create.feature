@method=POST @endpoint=/data/{registryname}/{versionnumber}/update-or-create
Feature: API endpoint that updates existing record that matches with request body parameters, or creates a new one if the record was not found

  @smoke
  Scenario: The record is successfully created in the database smoke type test
    Given User wants to create a new record in the database
    When User sends POST request to /data/{registryname}/{versionnumber}/update-or-create with given Information-Mediator-Client header, "<registryname>" as registryname and "<versionnumber>" as versionnumber
    And The request contains a payload with query and write objects that both contain content object with given: "<ID>" as ID, "<FirstName>" as FirstName, "<LastName>" as LastName and "<BirthCertificateID>" as BirthCertificateID
    Then User receives a response from the /data/{registryname}/{versionnumber}/update-or-create endpoint
    And The /data/{registryname}/{versionnumber}/update-or-create response should be returned in a timely manner 15000ms
    And The /data/{registryname}/{versionnumber}/update-or-create response should have status 200
    And The /data/{registryname}/{versionnumber}/update-or-create response should have content-type: application/json header
    And The /data/{registryname}/{versionnumber}/update-or-create response should match json schema

    Examples:
    | registryname | versionnumber | ID             | FirstName | LastName | BirthCertificateID |
    | registryname | 111           | EE123456789012 | John      | Smith    | RR-1234567890      |
    | registryname | 111           | EE098765432109 | Ana       | Adams    | RR-0987654321      |


  @unit @positive
  Scenario: The existing record is successfully updated in the database
    Given User wants to update previously created record in the database
    When User sends POST request to /data/{registryname}/{versionnumber}/update-or-create with given Information-Mediator-Client header, "<registryname>" as registryname and "<versionnumber>" as versionnumber
    And The request contains a payload with query object that contains content object with given: "<ID>" as ID, "<FirstName>" as FirstName, "<LastName>" as LastName and "<BirthCertificateID>" as BirthCertificateID and write object that contains content object with given: "<UpdatedID>" as ID, "<UpdatedFirstName>" as FirstName, "<UpdatedLastName>" as LastName and "<UpdatedBirthCertificateID>" as BirthCertificateID
    Then User receives a response from the /data/{registryname}/{versionnumber}/update-or-create endpoint
    And The /data/{registryname}/{versionnumber}/update-or-create response should be returned in a timely manner 15000ms
    And The /data/{registryname}/{versionnumber}/update-or-create response should have status 200
    And The /data/{registryname}/{versionnumber}/update-or-create response should have content-type: application/json header
    And The /data/{registryname}/{versionnumber}/update-or-create response should match json schema
    And The /data/{registryname}/{versionnumber}/update-or-create response should contain "ID" property equals "<UpdatedID>"
    And The /data/{registryname}/{versionnumber}/update-or-create response should contain "FirstName" property equals "<UpdatedFirstName>"
    And The /data/{registryname}/{versionnumber}/update-or-create response should contain "LastName" property equals "<UpdatedLastName>"
    And The /data/{registryname}/{versionnumber}/update-or-create response should contain "BirthCertificateID" property equals "<UpdatedBirthCertificateID>"

    Examples:
    | registryname | versionnumber | ID             | FirstName | LastName | BirthCertificateID | UpdatedID      | UpdatedFirstName | UpdatedLastName | UpdatedBirthCertificateID | 
    | registryname | 111           | EE123456789012 | John      | Smith    | RR-1234567890      | EE123456789012 | Jack             | Sparrow         | RR-1234567890             |
    | registryname | 111           | EE098765432109 | Ana       | Adams    | RR-0987654321      | EE098765432109 | Emma             | Brown           | RR-0987654321             |
