@method=POST @endpoint=/data/{registryname}/{versionnumber}/create
Feature: API endpoint that allows users to create a new record in the database.

  @smoke 
  Scenario: The user successfully creates a record in the database smoke test type

    Given The user wants to create a new record in the database
    When User sends POST request with given Information-Mediator-Client header, body, "registryname" as registryname and "111" as versionnumber
    And User provides body with parameters: "${ID_0}" as ID, "${FirstName_0}" as FirstName, "${LastName_0}" as LastName, "${BirthCertificateID_0}" as BirthCertificateID
    Then User receives a response from the POST /data/{registryname}/{versionnumber}/create endpoint
    And The POST /data/{registryname}/{versionnumber}/create endpoint response should be returned in a timely manner 15000ms
    And The POST /data/{registryname}/{versionnumber}/create endpoint response should have status 200
    And The POST /data/{registryname}/{versionnumber}/create response should have "content-type": "application/json" header
    And The POST /data/{registryname}/{versionnumber}/create endpoint response should match json schema

  @positive @unit
  Scenario Outline: The user successfully creates a record in the database

    Given The user wants to create a new record in the database
    When User sends POST request with given Information-Mediator-Client header, body, "registryname" as registryname and "111" as versionnumber
    And User provides parameters: "<ID>" as ID, "<FirstName>" as FirstName, "<LastName>" as LastName, "<BirthCertificateID>" as BirthCertificateID
    Then User receives a response from the POST /data/{registryname}/{versionnumber}/create endpoint
    And The POST /data/{registryname}/{versionnumber}/create endpoint response should be returned in a timely manner 15000ms
    And The POST /data/{registryname}/{versionnumber}/create endpoint response should have status 200
    And The POST /data/{registryname}/{versionnumber}/create response should have "content-type": "application/json" header
    And The POST /data/{registryname}/{versionnumber}/create endpoint response should match json schema

    Examples: Valid data
    | ID      | FirstName       | LastName      | BirthCertificateID |
    | ${ID_1} | ${FirstName_1}  | ${LastName_1} | ${BirthCertificateID_1} |
    | ${ID_2} | ${FirstName_2}  | ${LastName_2} | ${BirthCertificateID_2} |
    | ${ID_3} | ${FirstName_3}  | ${LastName_3} | ${BirthCertificateID_3} |
    | ${ID_4} | ${FirstName_4}  | ${LastName_4} | ${BirthCertificateID_4} |