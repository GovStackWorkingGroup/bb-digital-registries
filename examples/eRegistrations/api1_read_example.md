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
  -H 'Authorization: Bearer <ACCESS_TOKEN>' \
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
