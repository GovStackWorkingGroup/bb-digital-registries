@method=PUT @endpoint=/data/{registryname}/{versionnumber}/update
Feature: API endpoint that allows users to update a record in the database.

Updates one existing record in the registry databas
  @smoke
    Scenario: Successfully updates a record in the registry database smoke type test
    Given User wants to update an existing record in the database
    When PUT request to update a record in the database is sent with given Information-Mediator-Client header and path params "registryname" as registryname and "111" as versionnumber
    And The request contains a payload with given "EE3784545277266" as ID "Philip" as FirstName "Red" as LastName and "RR-30045370099" as BirthCertificateID and the request overwrites the record with given "EE383838348834" as ID "Elsa" as FirstName "West" as LastName and "RR-1234007889" as BirthCertificateID
    Then The response from /data/{registryname}/{versionnumber}/update is received
    And The response from /data/{registryname}/{versionnumber}/update should be returned in a timely manner 15000ms
    And The response from /data/{registryname}/{versionnumber}/update should have status 200

  @positive @unit
  Scenario Outline: Successfully updates a record in the registry database
    Given User wants to update an existing record in the database
    When PUT request to update a record in the database is sent with given Information-Mediator-Client header and path params "registryname" as registryname and "111" as versionnumber
    And The request contains a payload with given "<ID>" as ID "<FirstName>" as FirstName "<LastName>" as LastName and "<BirthCertificateID>" as BirthCertificateID and the request overwrites the record with given "<updatedID>" as ID "<updatedFirstName>" as FirstName "<updatedLastName>" as LastName and "<updatedBirthCertificateID>" as BirthCertificateID
    Then The response from /data/{registryname}/{versionnumber}/update is received
    And The response from /data/{registryname}/{versionnumber}/update should be returned in a timely manner 15000ms
    And The response from /data/{registryname}/{versionnumber}/update should have status 200

    Examples:
    | ID               | FirstName | LastName | BirthCertificateID | updatedID        | updatedFirstName | updatedLastName | updatedBirthCertificateID |
    | EE34462734834865 | Alex      | Green    | RR-441124937       | EE34462734834865 | Jack             | Black           | RR-1234567880             |
    | EE61287673487865 | Alise     | Black    | RR-49075937        | EE61287673487865 | John             | Redwood         | RR-1234567888             |
    | EE6534523487865  | Zyra      | Blue     | RR-24523937        | EE6534523487865  | Bob              | Rack            | RR-1234567887             |
