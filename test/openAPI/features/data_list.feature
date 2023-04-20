@method=GET @endpoint=/data/{registryname}/{versionnumber}/
Feature: API endpoint that allows to search multiple records in the database.

  @smoke
  Scenario: Successfully obtains database users information smoke type test
    Given user wants to get the database users information
    When send GET request with given Information-Mediator-Client header and "registryname" as registryname and "111" as versionnumber
    Then receive a response from the GET /data/{registryname}/{versionnumber} endpoint
    And the response from /data/{registryname}/{versionnumber} should be returned in a timely manner 15000ms
    And the response from /data/{registryname}/{versionnumber} should have status 200
    And the response from /data/{registryname}/{versionnumber} should have content-type: application/json header
    And the response from /data/{registryname}/{versionnumber} should match json schema
    And results array length is consistent with count field value

  @unit @positive
  Scenario Outline: Successfully obtains database users information
    Given user wants to get the database users information
    When send GET request with given Information-Mediator-Client header and "registryname" as registryname and "111" as versionnumber
    And filter users information by using query parameters "<search>" as search and "<filter>" as filter and "<ordering>" as ordering
    Then receive a response from the GET /data/{registryname}/{versionnumber} endpoint
    And the response from /data/{registryname}/{versionnumber} should be returned in a timely manner 15000ms
    And the response from /data/{registryname}/{versionnumber} should have status 200
    And the response from /data/{registryname}/{versionnumber} should have content-type: application/json header
    And the response from /data/{registryname}/{versionnumber} should match json schema
    And the response from /data/{registryname}/{versionnumber} is filtered by "<search>" and "<filter>" provided in the query parameter
    And results array length is consistent with count field value

    Examples: Valid data
      | filter | search | ordering |
      | FirstName | John | ascending |
      | FirstName | Alice | descending |
      | FirstName | Jack | ascending |
      | FirstName | Bob | descending |

  @unit @positive
  Scenario: Receive an empty list from the Digital Registries database
    Given search for a specific value and the searched value does not exist in any record in the database
    When send GET request with given Information-Mediator-Client header and "registryempty" as registryname and "111" as versionnumber
    Then receive a response from the GET /data/{registryname}/{versionnumber} endpoint
    And the response from /data/{registryname}/{versionnumber} should be returned in a timely manner 15000ms
    And the response from /data/{registryname}/{versionnumber} should have status 200
    And the response from /data/{registryname}/{versionnumber} should have content-type: application/json header
    And the response from /data/{registryname}/{versionnumber} should match json schema
    And receive an empty list because there is no record in the database
    And results array length is consistent with count field value
