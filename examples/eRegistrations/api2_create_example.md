Feature: The health worker submits the registration application form and receives a confirmation (Membership ID) of the successful registration

Scenario Outline: Send form data to Registration CREATE API of MCTS DB.   
Given Sona has entered all required data in the Registration e-service registration form
   When the social health activist named "Sona" pushes a button "Send application"
   Then the MCC system makes a request to Registration BB MCTS DB CREATE API
    And fills the form data field with response information <MCTS ID>
  Examples:
    |MCTS ID|
    |MCTS4|
    
    
    curl -X 'POST' \
  'https://gdb.er3.ext.egovstack.net/data/mcts/2.0/create' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer <ACCESS_TOKEN>' \
  -H 'Content-Type: application/json' \
  -d '{
  "write": {
    "content": {
     
      "Child": {
        "National ID number": "10",
        "First names": "Usha Lee",
        "Last names": "Bajaj",
        "Birthdate": "2021-10-02",
        "Address": "Longroad 123, Welltown, Ethiopia",
        "Nationality": "Finland"
      },
      "Caretaker": {
        "National ID number": "4",
        "First names": "Sowmya",
        "Last names": "Bajaj",
        "Birthdate": "2021-10-03",
        "Phone": "+3725278511",
        "Email": "test@test.et",
        "Nationality": "Estonia",
        "Address": "Longroad 123, Welltown, Ethiopia"
      }
    }
  }
}'

Response


{
  "receive": {
    "content": {
      "Child": {
        "National ID number": "10",
        "First names": "Usha Lee",
        "Last names": "Bajaj",
        "Birthdate": "2021-10-02",
        "Address": "Longroad 123, Welltown, Ethiopia",
        "Nationality": "Finland"
      },
      "Caretaker": {
        "National ID number": "4",
        "First names": "Sowmya",
        "Last names": "Bajaj",
        "Birthdate": "2021-10-03",
        "Phone": "+3725278511",
        "Email": "test@test.et",
        "Nationality": "Estonia",
        "Address": "Longroad 123, Welltown, Ethiopia"
      },
      "ID": "MCTS29"
    },
    "created_at": "2022-11-18T08:51:05.055279Z",
    "modified_at": "2022-11-18T08:51:05.055311Z",
    "uuid": "f1114818-c6e1-419c-8492-b46a4ee6bda2"
  }
}
