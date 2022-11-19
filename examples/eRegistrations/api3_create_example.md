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
  
  
  
  curl -X 'POST' \
  'https://gdb.er3.ext.egovstack.net/data/con/1.1/create' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJHOFhwMFNhUko3U1RBSkJvZGpFSjhVb3FnUXozZTVoQng1SEJXcXhfV3BZIn0.eyJleHAiOjE2NjgyODU0MzUsImlhdCI6MTY2ODI4NTEzNSwiYXV0aF90aW1lIjoxNjY4MjgxNTk5LCJqdGkiOiJmYmFkMzYyNC03ZGQ2LTQwMTItOGVkZi05MjM4NzE0OTYwNDEiLCJpc3MiOiJodHRwczovL2xvZ2luLmVyMy5leHQuZWdvdnN0YWNrLm5ldC9hdXRoL3JlYWxtcy9DSCIsImF1ZCI6WyJyZWFsbS1tYW5hZ2VtZW50Iiwic3RhdGlzdGljcy1iYWNrZW5kIiwic3RhdGlzdGljcy1mcm9udGVuZCIsImJwYS1iYWNrZW5kIiwiYnBhLWZyb250ZW5kIiwiYWNjb3VudCJdLCJzdWIiOiI0M2M1OGJkMC0xZTU3LTQ5M2EtYjhmYi1kYzM4NDAxMjMyNzQiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJnZGItY2xpZW50Iiwic2Vzc2lvbl9zdGF0ZSI6IjAwNDdlZTY2LWY3MmItNDBkNS05MWFkLTU0MTQ3YTFhYTRjMiIsImFjciI6IjAiLCJhbGxvd2VkLW9yaWdpbnMiOlsiaHR0cHM6Ly9nZGIuZXIzLmV4dC5lZ292c3RhY2submV0Il0sInJlYWxtX2FjY2VzcyI6eyJyb2xlcyI6WyJEcmFmdCIsImRlZmF1bHQtcm9sZXMtY2giLCJzdXBlcl9tYXJpbyIsInBhcnRiIiwib2ZmbGluZV9hY2Nlc3MiLCJ1bWFfYXV0aG9yaXphdGlvbiIsInN1cGVyaW5zcGVjdG9yIiwic3lzYWRtaW4iXX0sInJlc291cmNlX2FjY2VzcyI6eyJyZWFsbS1tYW5hZ2VtZW50Ijp7InJvbGVzIjpbInZpZXctcmVhbG0iLCJtYW5hZ2UtdXNlcnMiLCJ2aWV3LXVzZXJzIiwibWFuYWdlLWNsaWVudHMiLCJxdWVyeS1ncm91cHMiLCJxdWVyeS11c2VycyJdfSwic3RhdGlzdGljcy1iYWNrZW5kIjp7InJvbGVzIjpbInN0YXRzIl19LCJzdGF0aXN0aWNzLWZyb250ZW5kIjp7InJvbGVzIjpbInN0YXRzIl19LCJicGEtYmFja2VuZCI6eyJyb2xlcyI6WyJCUEEiXX0sImJwYS1mcm9udGVuZCI6eyJyb2xlcyI6WyJCUEEiXX0sImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJtYW5hZ2UtYWNjb3VudC1saW5rcyIsInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoib3BlbmlkIGVtYWlsIHByb2ZpbGUiLCJzaWQiOiIwMDQ3ZWU2Ni1mNzJiLTQwZDUtOTFhZC01NDE0N2ExYWE0YzIiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwibmFtZSI6IlN1cGVyIE1hcmlvIiwicHJlZmVycmVkX3VzZXJuYW1lIjoic3VwZXJtYXJpbyIsImdpdmVuX25hbWUiOiJTdXBlciIsImZhbWlseV9uYW1lIjoiTWFyaW8iLCJlbWFpbCI6ImluZ21hci52YWxpKzFAZ21haWwuY29tIn0.aOm8nnQ-GlQqoIFKK6hVedyjUChAnekgmpybD-h-gQ9HmQxLhqWNi1qmRelr2_rQujthvQJZaOuhm-Bx4D5Va8Cn8inyIuDg9CCff51_Jqwpiuea2uNfmrZgFRXkbhVTGo6FwfMY31KYgzl5KQhXJOh033-JPC58luxcnKTkaPTp1ZQd-GX3KSmJ745ENh4JRKRB3Rt0YH5uW8XPkiZV1UWC_5N2roXOvOIHjxZ6tkYlYINkAmjXpXky9qtU_KQYlRoC4n7_QCC_z0VpItGCKQR4QQVb7O407kJHV7O4ON4lzYizBSubtbOPtc6Fn3veihTNiWu4tWu05SgkErP1_A' \
  -H 'Content-Type: application/json' \
  -d '{
  "write": {
    "content": {
      "MCTS ID": "MCTS4",
      "Consent ID": "70899ddd-c698-47b5-995a-04de2406efcc "
    }
  }
}'
  
  
Response: 


{
  "receive": {
    "content": {
      "MCTS ID": "MCTS4",
      "Consent ID": "70899ddd-c698-47b5-995a-04de2406efcc",
      "ID": "CON1"
    },
    "created_at": "2022-11-12T20:35:43.672125Z",
    "modified_at": "2022-11-12T20:35:43.672172Z",
    "uuid": "dd033698-5423-430a-a0ae-0182b40cbf38"
  }
}
  
  
  
