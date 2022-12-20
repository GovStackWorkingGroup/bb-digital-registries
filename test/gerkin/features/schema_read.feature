@admin
Feature: API reads existing registry database schema
  Request endpoint: GET /api/V1/database/{id}
  see https://govstack.gitbook.io/specification/v/version-0.9.0/building-blocks/digital-registries/8-service-apis#8.11-database-schema-read

  Scenario: Successfully read schema
    Given Database <id> exists in registry
    When I send a request to read schema of <id>
    Then I receive a response HTTP 200 with the database info according to https://github.com/GovStackWorkingGroup/BuildingBlockAPI/blob/4ed5a083b6fcc84b2394d9c71b7ecc2126082c8f/DigitalRegistriesBB/GovStack_Digital_registries_BB_Database_API_template-1.1.0.json#L227

  Scenario: Fail to read schema of database that does not exist
    Given Database <id> does not exist in registry
    When I send a request to read schema of <id>
    Then I receive a HTTP 404 error response

  Scenario: Failed to read schema because access denied for this request
    TODO: is this a specific scenario here or is auth handled generically at a higher level?
