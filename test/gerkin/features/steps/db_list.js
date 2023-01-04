const pactum = require('pactum');
const { Given, When, Then, Before, After } = require('@cucumber/cucumber');
const { header, localhost } = require('./helpers/helpers');

let specDatabaseRead;

const baseUrl = `${localhost}databases`;
const exampleResponseValue = {
  "id": 85,
  "name": "Mother and Child",
  "code": "MCTS",
  "databases": [
    {
      "id": 353,
      "version": "2.7",
      "name": "MCTS",
      "description": "Database holding information about MCTS objects",
      "institution": "Ministry of Social Affairs",
      "number_format": "{code}{indexNoByCode}",
      "schema": {
        "type": "object",
        "properties": {
          "ID": {
            "type": "string",
            "triggers": [
              {
                "conditions": [
                  {
                    "logic": "==",
                    "value": "",
                    "gate": "&&"
                  }
                ],
                "actions": [
                  {
                    "type": "set-value",
                    "value": "MCTS{indexNoByCode}",
                    "field_id": 1
                  }
                ]
              }
            ],
            "primaryKey": true,
            "readOnly": true,
            "description": "Registration ID",
            "example": "MCTS31",
            "id": 1
          },
          "Child": {
            "type": "string",
            "properties": {
              "ID": {
                "type": "string",
                "description": "Child ID",
                "example": "ID2",
                "id": 13
              }
            }
          }
        },
        "incrementIndex": 20,
        "required": [
          "ID"
        ]
      },
      "schema_tags": [
        {
          "name": "",
          "path": "/Child/Citizenship",
          "is_fulltext": true
        }
      ],
      "schema_flags": [
        {
          "name": "mandatory",
          "path": "/ID"
        }
      ],
      "fields_uniques": [
        [
          ""
        ]
      ],
      "is_draft": false,
      "is_disabled": false,
      "is_archived": false,
      "modified_at": "2021-10-03T08:35:01.775915Z",
      "by_user_name": "ingmar.dev",
      "by_user_auth_id": 1,
      "by_on_behalf_of_user_auth_id": null,
      "by_on_behalf_of_user_name": null,
      "generic_services": [
        {
          "service_id": 1,
          "name": "data-create",
          "is_visible": true,
          "used_count": 0
        }
      ],
      "data_index_increment": 0,
      "has_logo": false
    }
  ],
  "group_id": 10,
  "order": 76,
  "data_index_increment": 3
}

Before(() => {
  specDatabaseRead = pactum.spec();
});

// Background: The user wants to display information about all Digital Registries databases
Given(
  'The user wants to display information about all Digital Registries databases', () => {
  return 'The user wants to display information about all Digital Registries databases';
  }
);

// Scenario: The user receives information about Digital Registries databases
When(
  'The user triggers an action with a valid payload to display information about Digital Registries databases', () => {
    specDatabaseRead
      .get(baseUrl)
      .withHeaders(`${header.key}`, `${header.value}`);
});

Then('The user received a list of Digital Registries databases', async () => {
  await specDatabaseRead.toss();
  specDatabaseRead.response().should.have.status(200);
  specDatabaseRead.response().should.have.jsonLike(exampleResponseValue);
});

// Scenario: The user is not able to receive information for Digital Registries databases because of empty value in the header
When(
  'The user triggers an action with an invalid payload to display information about Digital Registries databases',
  () => {
    specDatabaseRead
      .get(baseUrl)
      .withHeaders(`${header.key}`, '');
  }
);

Then('The operation of receiving information about the databases of Digital Registers results with an error of the invalid header', async () => {
  await specDatabaseRead.toss();
  specDatabaseRead.response().should.have.status(400);
  specDatabaseRead.response().should.have.body('{"Invalid format of Information-Mediator-Client, should match INSTANCE/CLASS/MEMBER/SUBSYSTEM"}');
});


// Scenario: The user is not able to receive information for Digital Registries databases because of not including header
When(
  'The user triggers an action without a payload to display information about Digital Registries databases', () => {
    specDatabaseRead
    .get(baseUrl);
  }
);
  
Then('The operation of receiving information about the databases of Digital Registries results with an error', async () => {
  await specDatabaseRead.toss();
  specDatabaseRead.response().should.have.status(400);
  specDatabaseRead.response().should.have.body('{"Information-Mediator-Client required"}');
});

After(() => {
  specDatabaseRead.end();
});
