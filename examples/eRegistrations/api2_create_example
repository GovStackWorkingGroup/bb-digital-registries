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
  -H 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJHOFhwMFNhUko3U1RBSkJvZGpFSjhVb3FnUXozZTVoQng1SEJXcXhfV3BZIn0.eyJleHAiOjE2Njg3NjE1NDMsImlhdCI6MTY2ODc2MTI0MywiYXV0aF90aW1lIjoxNjY4NzYwNDYzLCJqdGkiOiI4YzI1NTUxNC01YzdhLTRlNDMtOTUxOS1mMjk2MTIwYTdkNDQiLCJpc3MiOiJodHRwczovL2xvZ2luLmVyMy5leHQuZWdvdnN0YWNrLm5ldC9hdXRoL3JlYWxtcy9DSCIsImF1ZCI6WyJyZWFsbS1tYW5hZ2VtZW50Iiwic3RhdGlzdGljcy1iYWNrZW5kIiwic3RhdGlzdGljcy1mcm9udGVuZCIsImJwYS1iYWNrZW5kIiwiYnBhLWZyb250ZW5kIiwiYWNjb3VudCJdLCJzdWIiOiI2OTY4NzVmNi1iNjI1LTQxYzQtODgzMi1kMjRkZTE0Mzg3YzgiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJnZGItY2xpZW50Iiwic2Vzc2lvbl9zdGF0ZSI6ImYyZTA1MDgzLWZlOTktNGY0NS1iYmY1LTM5N2I1MTgyZDA1NSIsImFjciI6IjAiLCJhbGxvd2VkLW9yaWdpbnMiOlsiaHR0cHM6Ly9nZGIuZXIzLmV4dC5lZ292c3RhY2submV0Il0sInJlYWxtX2FjY2VzcyI6eyJyb2xlcyI6WyJEcmFmdCIsImRlZmF1bHQtcm9sZXMtY2giLCJzdXBlcl9tYXJpbyIsInBhcnRiIiwib2ZmbGluZV9hY2Nlc3MiLCJ1bWFfYXV0aG9yaXphdGlvbiIsInN1cGVyaW5zcGVjdG9yIiwic3lzYWRtaW4iXX0sInJlc291cmNlX2FjY2VzcyI6eyJyZWFsbS1tYW5hZ2VtZW50Ijp7InJvbGVzIjpbInZpZXctcmVhbG0iLCJtYW5hZ2UtdXNlcnMiLCJ2aWV3LXVzZXJzIiwibWFuYWdlLWNsaWVudHMiLCJxdWVyeS1ncm91cHMiLCJxdWVyeS11c2VycyJdfSwic3RhdGlzdGljcy1iYWNrZW5kIjp7InJvbGVzIjpbInN0YXRzIl19LCJzdGF0aXN0aWNzLWZyb250ZW5kIjp7InJvbGVzIjpbInN0YXRzIl19LCJicGEtYmFja2VuZCI6eyJyb2xlcyI6WyJCUEEiXX0sImJwYS1mcm9udGVuZCI6eyJyb2xlcyI6WyJCUEEiXX0sImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJtYW5hZ2UtYWNjb3VudC1saW5rcyIsInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoib3BlbmlkIGVtYWlsIHByb2ZpbGUiLCJzaWQiOiJmMmUwNTA4My1mZTk5LTRmNDUtYmJmNS0zOTdiNTE4MmQwNTUiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwibmFtZSI6IkluZ21hciBWYWxpIiwicHJlZmVycmVkX3VzZXJuYW1lIjoiaW5nbWFyLmdvdnN0YWNrIiwiZ2l2ZW5fbmFtZSI6IkluZ21hciIsImZhbWlseV9uYW1lIjoiVmFsaSIsImVtYWlsIjoiaW5nbWFyLnZhbGlAZ21haWwuY29tIn0.DKMYLkmwoqtpPqdLdqO8RqFffs-9Wej6LyWFTzVp0AyeWsEqFsuPZa3uETtxEy8LcXxDNk0_7j4TeoWsFatEiZt43f61oILPeii3L3z69ockNFjEDI--A28aOqnnfKGB6OBI1IJR5KNJoexJYuhGgAY_2esrUw0gMAIL517VUUWqV-bFfvZ1JLm4UH7IlueeGFlTJeWvNvWABl0HtbZJwB3IrUp5izUIg-uGIDNsSts3EtyY-a13ooPU-a4DGbu0cpn3JdhKSnhONhv78_DqXCW2k__K85zujper_XaVdRRobOz_yHgAEBvqjcER2i9J3l2cY3vy7XnJh4jwcrnYXA' \
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
