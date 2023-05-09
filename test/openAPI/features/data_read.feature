@method=POST @endpoint=/data/{registryname}/{versionnumber}/read
Feature: API endpoint that allows users to search for a record in the database.

  @smoke
  Scenario: User obtains a searched record from the database smoke type test
    Given The user wants to search for a record in the database
    When User sends POST /data/{registryname}/{versionnumber}/read request with given Information-Mediator-Client header, "registryname" as registryname, "111" as versionnumber, "John Helmut" as FirstName
    Then User receives a response from the /data/{registryname}/{versionnumber}/read endpoint
    And The /data/{registryname}/{versionnumber}/read endpoint response should be returned in a timely manner 15000ms
    And The /data/{registryname}/{versionnumber}/read endpoint response should have status 200
    And The /data/{registryname}/{versionnumber}/read endpoint response should have content-type: application/json header
    And The /data/{registryname}/{versionnumber}/read endpoint response should match json schema

  @unit @positive 
  Scenario Outline: User obtains a searched record from the database
    Given The user wants to search for a record in the database
    When User sends POST /data/{registryname}/{versionnumber}/read request with given Information-Mediator-Client header, "registryname" as registryname, "111" as versionnumber, "<parameter_value>" as "<body_parameter>"
    Then User receives a response from the /data/{registryname}/{versionnumber}/read endpoint
    And The /data/{registryname}/{versionnumber}/read endpoint response should be returned in a timely manner 15000ms
    And The /data/{registryname}/{versionnumber}/read endpoint response should have status 200
    And The /data/{registryname}/{versionnumber}/read endpoint response should have content-type: application/json header
    And The /data/{registryname}/{versionnumber}/read endpoint response should match json schema

    Examples:
    | body_parameter     | parameter_value                      |
    | ID                 | c473a46c-dd2d-42f5-aca3-f318d478d555 |
    | FirstName          | Eva                                  |
    | LastName           | Smith                                |
    | BirthCertificateID | EE-4419523937                        |
