Feature: The health worker submits the registration application form and receives a confirmation (Membership ID) of the successful registration

Scenario Outline: Send form data to Registration CREATE API of MCTS DB.   
Given "Sona" has entered all required data in the Registration e-service registration form
   When "Sona" pushes a button "Send application"
   Then the MCC system makes a request to Registration BB MCTS DB CREATE API
    And fills the form data field with response information <MCTS ID>
  Examples:
    |MCTS ID|
    |MCTS4|
