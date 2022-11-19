Feature: The health care worker imports client personal data from a registry
Scenario Outline: import mothers pesonal information from national population registry to the e-service form
  Given Sona has entered <ID> in the Registration e-service registration form, national ID number field
   When the social health activist named "Sona" pushes a button "Import Mothers's information"
   Then the Registration system makes a request to population registry API
    And fills the form on the screen with Mothers data <ID>,<first>, <last>, <birth>
  Examples:
    |ID|first|last|birth|
    |53|Sowmya|Krishnamurti|2022-11-01| 
    
    
curl -X 'POST' \
  'https://gdb.er3.ext.egovstack.net/data/crs/2.9/read' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJHOFhwMFNhUko3U1RBSkJvZGpFSjhVb3FnUXozZTVoQng1SEJXcXhfV3BZIn0.eyJleHAiOjE2Njg3NTcxNDYsImlhdCI6MTY2ODc1Njg0NiwiYXV0aF90aW1lIjoxNjY4NzU0OTk5LCJqdGkiOiI5MDkwYjM0Ny1hMTAxLTQ3ODQtYTFlNy1kZWM4YTdlZGI1NTkiLCJpc3MiOiJodHRwczovL2xvZ2luLmVyMy5leHQuZWdvdnN0YWNrLm5ldC9hdXRoL3JlYWxtcy9DSCIsImF1ZCI6WyJyZWFsbS1tYW5hZ2VtZW50Iiwic3RhdGlzdGljcy1iYWNrZW5kIiwic3RhdGlzdGljcy1mcm9udGVuZCIsImJwYS1iYWNrZW5kIiwiYnBhLWZyb250ZW5kIiwiYWNjb3VudCJdLCJzdWIiOiI2OTY4NzVmNi1iNjI1LTQxYzQtODgzMi1kMjRkZTE0Mzg3YzgiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJnZGItY2xpZW50Iiwic2Vzc2lvbl9zdGF0ZSI6IjkwYjYyYmFkLTExMDctNGQ1Mi05YzRmLWVhMWRlMzE2NzRiNyIsImFjciI6IjEiLCJhbGxvd2VkLW9yaWdpbnMiOlsiaHR0cHM6Ly9nZGIuZXIzLmV4dC5lZ292c3RhY2submV0Il0sInJlYWxtX2FjY2VzcyI6eyJyb2xlcyI6WyJEcmFmdCIsImRlZmF1bHQtcm9sZXMtY2giLCJzdXBlcl9tYXJpbyIsInBhcnRiIiwib2ZmbGluZV9hY2Nlc3MiLCJ1bWFfYXV0aG9yaXphdGlvbiIsInN1cGVyaW5zcGVjdG9yIiwic3lzYWRtaW4iXX0sInJlc291cmNlX2FjY2VzcyI6eyJyZWFsbS1tYW5hZ2VtZW50Ijp7InJvbGVzIjpbInZpZXctcmVhbG0iLCJtYW5hZ2UtdXNlcnMiLCJ2aWV3LXVzZXJzIiwibWFuYWdlLWNsaWVudHMiLCJxdWVyeS1ncm91cHMiLCJxdWVyeS11c2VycyJdfSwic3RhdGlzdGljcy1iYWNrZW5kIjp7InJvbGVzIjpbInN0YXRzIl19LCJzdGF0aXN0aWNzLWZyb250ZW5kIjp7InJvbGVzIjpbInN0YXRzIl19LCJicGEtYmFja2VuZCI6eyJyb2xlcyI6WyJCUEEiXX0sImJwYS1mcm9udGVuZCI6eyJyb2xlcyI6WyJCUEEiXX0sImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJtYW5hZ2UtYWNjb3VudC1saW5rcyIsInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoib3BlbmlkIGVtYWlsIHByb2ZpbGUiLCJzaWQiOiI5MGI2MmJhZC0xMTA3LTRkNTItOWM0Zi1lYTFkZTMxNjc0YjciLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwibmFtZSI6IkluZ21hciBWYWxpIiwicHJlZmVycmVkX3VzZXJuYW1lIjoiaW5nbWFyLmdvdnN0YWNrIiwiZ2l2ZW5fbmFtZSI6IkluZ21hciIsImZhbWlseV9uYW1lIjoiVmFsaSIsImVtYWlsIjoiaW5nbWFyLnZhbGlAZ21haWwuY29tIn0.cIRdyN1v7am_8NAm_4Arg825bET3Kv-JqQLjneAVZvfCo5s0v8KRpZEYsHp6-ryRBjELBgieou7pgeEwEtXwKv3HT1pDgRFdE1Uab2y1tFLrpmkhae7p9QITC7YDNLRfWRuyEtlC5pqK_n-noyTGuCjlx4zfPX2ViNKyQbrCgWtcsEUQBH2Xlelq5Miv6yYqeCG0YYsK44NGK76M0OxwFtZjCAIOQH2_6RbdKi81omE42uAvZDaNICcXfpg1S5bM7n6CdsxTajeFjZYjxwHzCQt6kuXlZ-rEOFLTxtt3wRUVWVhmjKW41drX82ojN69_VE3mzU1gCNqQVCwBTLK6qA' \
  -H 'Content-Type: application/json' \
  -d '{
  "query": {
    "content": {
      "National ID": "53"
      
      
    }
  }
}'


In response, the system returns the following information: 


{
  "receive": {
    "content": {
      "ID": "0409CC96-700A-4FB9-A22C-F56DC8A03BC1",
      "Father": {
        "Last names": "",
        "First names": "",
        "National ID": ""
      },
      "Gender": "Female",
      "Mother": {
        "Last names": "Riisikas",
        "First names": "Usha",
        "National ID": "47"
      },
      "Birthdate": "2022-11-01",
      "Full name": "Sowmya Krishnamurti",
      "Last names": "Krishnamurti",
      "First names": "Sowmya",
      "National ID": "53",
      "Nationality": {
        "key": "EST",
        "value": "Estonia"
      },
      "Nationality key": "EST",
      "Nationality value": "Estonia"
    },
    "created_at": "2022-11-18T07:37:34.678816Z",
    "modified_at": "2022-11-18T07:38:00.239776Z",
    "uuid": "6e5ea0ad-c990-40d9-be4b-d152f7ede16f"
  }
}
