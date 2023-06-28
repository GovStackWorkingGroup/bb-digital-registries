@method=PUT @endpoint=/data/{registryname}/{versionnumber}/update-entries
Feature: API endpoint that updates multiple records in the registry database that match the input query.

  @smoke
  Scenario: Successfully updates multiple records in the database by first name smoke type test
    Given User wants to update multiple records in the database
    When User sends PUT request to /data/{registryname}/{versionnumber}/update-entries with given Information-Mediator-Client header, "registryname" as registryname and "111" as versionnumber
    And The request contains a payload with two objects: query object that contains content object with given: "Alina" as FirstName and write object that contains content object with given: "Jack" as FirstName
    Then User receives a response from the /data/{registryname}/{versionnumber}/update-entries endpoint
    And The /data/{registryname}/{versionnumber}/update-entries response should be returned in a timely manner 15000ms
    And The /data/{registryname}/{versionnumber}/update-entries response should have status 200
  
  @unit @positive
  Scenario Outline: Successfully updates multiple records in the database by first name
    Given User wants to update multiple records in the database
    When User sends PUT request to /data/{registryname}/{versionnumber}/update-entries with given Information-Mediator-Client header, "registryname" as registryname and "111" as versionnumber
    And The request contains a payload with two objects: query object that contains content object with given: "<FirstName>" as FirstName and write object that contains content object with given: "<UpdatedFirstName>" as FirstName
    Then User receives a response from the /data/{registryname}/{versionnumber}/update-entries endpoint
    And The /data/{registryname}/{versionnumber}/update-entries response should be returned in a timely manner 15000ms
    And The /data/{registryname}/{versionnumber}/update-entries response should have status 200

    Examples:
    | FirstName | UpdatedFirstName |
    | Casandra  | Tamara           |
    | Olga      | Alice            |

  
  @unit @positive
  Scenario: Successfully updates multiple records in the database
    Given User wants to update multiple records in the database
    When User sends PUT request to /data/{registryname}/{versionnumber}/update-entries with given Information-Mediator-Client header, "registryname" as registryname and "111" as versionnumber
    And The request contains a payload with two objects: query object that contains content object with given: "EE1112223331" as ID, "Billy" as FirstName, "Johnson" as LastName, "RR-1112223331" as BirthCertificateID and write object that contains content object with given: "EE1112223331" as ID, "Bob" as FirstName, "Son" as LastName, "RR-1112223331" as BirthCertificateID
    Then User receives a response from the /data/{registryname}/{versionnumber}/update-entries endpoint
    And The /data/{registryname}/{versionnumber}/update-entries response should be returned in a timely manner 15000ms
    And The /data/{registryname}/{versionnumber}/update-entries response should have status 200
