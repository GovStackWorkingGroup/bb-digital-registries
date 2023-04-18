@method=GET @endpoint=/data/{registryname}/{versionnumber}/
Feature: API endpoint that allows users to search multiple records in Digital Registries database.

  @smoke
  Scenario: User successfully obtains database users information with database schema smoke type test
    Given User wants to get the database users information of Digital Registries
    When User sends GET request with given Information-Mediator-Client header and "registryname" as registryname and "111" as versionnumber
    Then User receives a response from the GET /data/{registryname}/{versionnumber} endpoint
    And The GET /data/{registryname}/{versionnumber}/ endpoint response should be returned in a timely manner 15000ms
    And The GET /data/{registryname}/{versionnumber}/ endpoint response should have status 200
    And The GET /data/{registryname}/{versionnumber}/ endpoint response should have content-type: application/json header
    And The GET /data/{registryname}/{versionnumber}/ endpoint response should match json schema

  @unit @positive
  Scenario Outline: User successfully obtains database users information  with database schema
    Given User wants to get the database users information of Digital Registries
    When User sends GET request with given Information-Mediator-Client header and "registryname" as registryname and "111" as versionnumber
    And User filters users informations by using query parameters "<search>" as search and "<filter>" as filter and "<ordering>" as ordering
    Then User receives a response from the GET /data/{registryname}/{versionnumber} endpoint
    And The GET /data/{registryname}/{versionnumber}/ endpoint response should be returned in a timely manner 15000ms
    And The GET /data/{registryname}/{versionnumber}/ endpoint response should have status 200
    And The GET /data/{registryname}/{versionnumber}/ endpoint response should have content-type: application/json header
    And The GET /data/{registryname}/{versionnumber}/ endpoint response should match json schema
    Examples: Valid data
      | search | filter | ordering |
      | John | Black | ASC |
      | Alice | Wonderland | DESC |
      | Jack | Reed | ascending |
      | Thomas | Rietler | descending |

  @unit @positive
  Scenario: The user receives an empty list from the Digital Registries database
    Given The user wants to search for a specific value and the searched value does not exist in any record in the database
    When User sends GET request with given Information-Mediator-Client header and "registryname" as registryname and "111" as versionnumber
    And User filters users informations by using query parameters "John" as search and "John" as filter and "ASC" as ordering
    Then The user receives an empty list because there is no record in the database that contains the searched value
