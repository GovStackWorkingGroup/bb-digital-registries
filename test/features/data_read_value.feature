Feature: API endpoint that allows users to search for the field value of a record in the Digital Registries database.
  Request endpoint: GET /data/{registryname}/{versionnumber}/{uuid}/read-value/{field}.{ext}

  Scenario: The user gets the first name of the searched user from the Digital Registries database
    Given The user wants to search for the user's first name of the user in the Digital Registries database and the first name of the record is matched
    When The user sends a valid request to obtain the first name of the searched user from the database
    Then The user receives the first name of the searched user

  Scenario: The user does not receive the first name of searched user from the Digital Registries database
    Given The user wants to search for the first name of the user in the Digital Registries database and the first name of the record is empty
    When The user sends a valid request to obtain the first name of the searched user from the database
    Then The user receives a message that the first name of the searched user is empty

  Scenario: The user is unable to obtain the user's first name from the Digital Registries database because the request is invalid
    Given The user wants to search for the user's first name in the Digital Registries database
    When The user sends an invalid request to get the first name of the searched user from the Digital Registries database
    Then The result of the operation to receive the user's first name is an error


Scenario:. The user is unable to obtain the user's first name from the Digital Registries database because the request is invalid. 
Given. The user wants to search for the user's first name in the Digital Registries database. 
When. The user sends an invalid request to get the first name of the searched user from the Digital Registries database. 
Then. The result of the operation to receive the user's first name is an error.