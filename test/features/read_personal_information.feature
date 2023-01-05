Feature: The health care worker imports client personal data from a registry
#Background:
   # Given a government-accredited social health activist named "Sona", the health care worker
   # And a woman who has delivered her first baby named "Sowmya", the mother
   # And  the "Sona" met "Sowmya" and her family
    #And the mother has her identity proof (card, QR code, ID number, etc) available together with the required credentials
   # And the social health activist named "Sona" has mobile device with internet connectivity
    # And the mother and newborn have already been registered in a population registry
    # And the social health activist named "Sona" has authorization to use Registration system for registration purposes
    # And the "Sona" has authorization to make quries to Population registry via Registration system
Scenario Outline: import mothers pesonal information from national population registry to the e-service form
  Given Sona has entered <ID> in the Registration e-service registration form, national ID number field
   When "Sona" pushes a button "Import Mothers's information"
   Then the Registration system makes a request to population registry API
    And fills the form on the screen with Mothers data <ID>,<first>, <last>, <birth>
  Examples:
    | ID   | first  | last          | birth |
    | 500  | Sowmya | Krishnamurti  | 2024-11-21| 
