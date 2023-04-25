@method=GET @endpoint=/data/{registryname}/{versionnumber}/update
Feature: API endpoint that allows users to update a new record in database.

  @smoke
    Scenario: Successfully update user information record in database smoke type test
    Given User wants to update existing record in database
    When PUT request to check if the record exists in the database is sent with given path params "registryname" as registryname and "111" as versionnumber
    And the request contains a payload with given "EE378627348834" as ID "John" as FirstName "Helmut" as LastName and "RR-1234567889" as BirthCertificateID and the request overwrites the record with given "EE378627348834" as updatedID "John" as updatedFirstName "Helmut" as updatedLastName and "RR-1234567889" as updatedBirthCertificateID
    Then response from /data/{registryname}/{versionnumber}/update is received
    And the response from /data/{registryname}/{versionnumber}/update should be returned in a timely manner 15000ms
    And the response from /data/{registryname}/{versionnumber}/update should have status 200

  @positive @unit
  Scenario Outline: Successfully update user information record in database
    Given User wants to update existing record in database
    When PUT request to check if the record exists in the database is sent with given path params "registryname" as registryname and "111" as versionnumber
    And the request contains a payload with given "EE378627348834" as ID "John" as FirstName "Helmut" as LastName and "RR-1234567889" as BirthCertificateID and the request overwrites the record with given "<updatedID>" as updatedID "<updatedFirstName>" as updatedFirstName "<updatedLastName>" as updatedLastName and "<updatedBirthCertificateID>" as updatedBirthCertificateID
    Then response from /data/{registryname}/{versionnumber}/update is received
    And the response from /data/{registryname}/{versionnumber}/update should be returned in a timely manner 15000ms
    And the response from /data/{registryname}/{versionnumber}/update should have status 200

    Examples:
      | updatedID | updatedFirstName | updatedLastName | updatedBirthCertificateID |
      | EE378627348833 | Jack | Black | RR-1234567880 |
      | EE378627348834 | John | Redwood | RR-1234567888 |
      | EE378627348835 | Bob | Rack | RR-1234567887 |
