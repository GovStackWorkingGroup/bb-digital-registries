@method=GET @endpoint=/data/{registryname}/{versionnumber}/update
Feature: API endpoint that allows users to update a record in the database.

Updates one existing record in the registry databas
  @smoke
    Scenario: Successfully updates a record in the registry database smoke type test
    Given User wants to update an existing record in the database
    When PUT request to update a record in the database is sent with given path params "registryname" as registryname and "111" as versionnumber
    And The request contains a payload with given "EE378627348834" as ID "John" as FirstName "Helmut" as LastName and "RR-1234567889" as BirthCertificateID and the request overwrites the record with given "EE378627348834" as ID "John" as FirstName "Helmut" as LastName and "RR-1234567889" as BirthCertificateID
    Then The response from /data/{registryname}/{versionnumber}/update is received
    And The response from /data/{registryname}/{versionnumber}/update should be returned in a timely manner 15000ms
    And The response from /data/{registryname}/{versionnumber}/update should have status 200

  @positive @unit
  Scenario Outline: Successfully updates a record in the registry database
    Given User wants to update an existing record in the database
    When PUT request to update a record in the database is sent with given path params "registryname" as registryname and "111" as versionnumber
    And The request contains a payload with given "EE378627348834" as ID "John" as FirstName "Helmut" as LastName and "RR-1234567889" as BirthCertificateID and the request overwrites the record with given "EE378627348834" as ID "<updatedFirstName>" as FirstName "<updatedLastName>" as LastName and "<updatedBirthCertificateID>" as BirthCertificateID
    Then The response from /data/{registryname}/{versionnumber}/update is received
    And The response from /data/{registryname}/{versionnumber}/update should be returned in a timely manner 15000ms
    And The response from /data/{registryname}/{versionnumber}/update should have status 200

    Examples:
      | updatedFirstName | updatedLastName | updatedBirthCertificateID |
      | Jack | Black | RR-1234567880 |
      | John | Redwood | RR-1234567888 |
      | Bob | Rack | RR-1234567887 |
