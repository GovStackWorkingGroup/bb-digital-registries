@data
Feature: Create new record in registry
  Request endpoint: POST /data/{code}/{version}/create
  see https://govstack.gitbook.io/specification/v/version-0.9.0/building-blocks/digital-registries/8-service-apis#docs-internal-guid-f400fe68-7fff-bffb-3d00-0b067c81eb40

  A Registration BB application makes a request to the Digital Registries BB API to create a new record
  # TODO: merge create_mcts_record.feature into this feature and remove one file

  Background:
    Given database with the valid schema has been set up

  Scenario: Successfully create new record
    Send form data to Registration CREATE API of MCTS DB.
    Given "Sona" has entered all required data in the Registration e-service registration form
    When "Sona" pushes a button "Send application"
    Then the MCC system makes a request to Registration BB MCTS DB CREATE API
    And fills the form data field with response information <MCTS ID>

  Scenario: Trying to create record that already exists
    TODO: do we verify some kind of "duplicate" definition? (e.g. a citizen ID that should be unique across records)
    Given I have made a successful CREATE request for a new record with <unique-record-id> before
    When I make a CREATE request identical to the earlier one, with the same <unique-record-id>
    Then ???

  Scenario: Trying to create new record in non-existing database
    Given database <id> does not exist
    When I make a CREATE request to /data/<id>/3.0/create
    Then I receive a HTTP 400 response (TODO: what is the exact response here? seems missing from the OpenAPI spec so far)
