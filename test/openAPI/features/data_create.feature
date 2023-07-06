@method=POST @endpoint=/data/{registryname}/{versionnumber}/create
Feature: API endpoint that allows users to create a new record in the database.

  @smoke 
  Scenario: The user successfully creates a record in the database smoke test type

    Given The user wants to create a new record in the database
    When User sends POST request with given Information-Mediator-Client header, body, "registryname" as registryname and "111" as versionnumber
    And User provides body with parameters: ${ID_1} as ID, "Anna" as Firstname, "Stock" as LastName, "RR-1234567999" BirthCertificateID
    Then User receives a response from the POST /data/{registryname}/{versionnumber}/create endpoint
    And The POST /data/{registryname}/{versionnumber}/create endpoint response should be returned in a timely manner 15000ms
    And The POST /data/{registryname}/{versionnumber}/create endpoint response should have status 200
    And The POST /data/{registryname}/{versionnumber}/create endpoint response should have content-type: application/json header
    And The POST /data/{registryname}/{versionnumber}/create endpoint response should match json schema

  @positive @unit
  Scenario: The user successfully creates a record in the database

    Given The user wants to create a new record in the database
    When User sends POST request with given Information-Mediator-Client header, body, "registryname" as registryname and "111" as versionnumber
    And User provides body with parameters: "<ID>" as ID, "<Firstname>" as Firstname, "<LastName>" as LastName, "<BirthCertificateID>" BirthCertificateID
    Then User receives a response from the POST /data/{registryname}/{versionnumber}/create endpoint
    And The POST /data/{registryname}/{versionnumber}/create endpoint response should be returned in a timely manner 15000ms
    And The POST /data/{registryname}/{versionnumber}/create endpoint response should have status 200
    And The POST /data/{registryname}/{versionnumber}/create endpoint response should have content-type: application/json header
    And The POST /data/{registryname}/{versionnumber}/create endpoint response should match json schema

    Examples: Valid data
    | ID         |Firstname | LastName | BirthCertificateID
    | EE34534123 | Zofia    | Don      | RR-5465679229
    | EE38778473 | Elsa     | Smith    | RR-1234537999
    | RR87483474 | Nick     | Evans    | RR-7898797999
    | PP84848484 | Thomas   | Johnson  | RR-8534567781
