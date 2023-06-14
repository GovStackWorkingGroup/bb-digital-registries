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
    And The /data/{registryname}/{versionnumber}/read response should contain "<body_parameter>" property equals "<parameter_value>"

    Examples:
    | body_parameter     | parameter_value |
    | ID                 | EE378129127223  |
    | FirstName          | Eva             |
    | LastName           | Smith           |
    | BirthCertificateID | EE6546273487865 |

  @unit @positive 
  Scenario: The user gets a searched record from the database when he specifies all parameters
    Given The user wants to search for a record in the database
    When User sends POST /data/{registryname}/{versionnumber}/read request with given Information-Mediator-Client header, "registryname" as registryname, "111" as versionnumber, "<FirstName>" as FirstName, "<LastName>" as LastName, "<ID>" as ID, "<BirthCertificateID>" as BirthCertificateID
    Then User receives a response from the /data/{registryname}/{versionnumber}/read endpoint
    And The /data/{registryname}/{versionnumber}/read endpoint response should be returned in a timely manner 15000ms
    And The /data/{registryname}/{versionnumber}/read endpoint response should have status 200
    And The /data/{registryname}/{versionnumber}/read endpoint response should have content-type: application/json header
    And The /data/{registryname}/{versionnumber}/read endpoint response should match json schema
    And The /data/{registryname}/{versionnumber}/read response should contain "FirstName" property equals "<FirstName>"
    And The /data/{registryname}/{versionnumber}/read response should contain "LastName" property equals "<LastName>"
    And The /data/{registryname}/{versionnumber}/read response should contain "ID" property equals "<ID>"
    And The /data/{registryname}/{versionnumber}/read response should contain "BirthCertificateID" property equals "<BirthCertificateID>"

    Examples:
    | FirstName | LastName | ID             | BirthCertificateID |
    | Billy     | Johnson  | EE378129127223 | RR-1112223331      |

  @unit @negative 
  Scenario: Receives a message that the record not found in the database
    Given The user wants to search for a record in the database
    When User sends POST /data/{registryname}/{versionnumber}/read request with given Information-Mediator-Client header, "registryname" as registryname, "111" as versionnumber, "NotExist" as FirstName
    Then User receives a response from the /data/{registryname}/{versionnumber}/read endpoint
    And The /data/{registryname}/{versionnumber}/read endpoint response should be returned in a timely manner 15000ms
    And The /data/{registryname}/{versionnumber}/read endpoint response should have status 404
    And The /data/{registryname}/{versionnumber}/read endpoint response should have content-type: application/json header
    And The /data/{registryname}/{versionnumber}/read endpoint response should match json schema with error message
