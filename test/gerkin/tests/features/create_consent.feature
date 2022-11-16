Feature: Upon receiving the consent agreement ID from the Consent BB,  the MCC application stores information in Consent DB

Scenario Outline: Send form data to Registration BB CREATE API of CON DB.   
Given System has received Consent ID form Consent BB and stored it in the response field 
   When the MCC application receives Consent ID
   Then the MCC system stores <Consent ID> in the Consent ID field on the form
    And the MCC system makes a request to Registration BB CON DB CREATE API
    And fills the form data field with response information  Consent DB <ID>
  Examples:
    |ID|MCTS ID|Consent ID|
    |CON1|MCTS28|70899ddd-c698-47b5-995a-04de2406efcc|
