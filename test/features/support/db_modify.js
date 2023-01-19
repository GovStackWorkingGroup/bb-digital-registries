const pactum = require('pactum');
const { Given, When, Then, Before, After } = require('@cucumber/cucumber');
const { header, localhost } = require('./helpers/helpers');

let databaseSchemaVariables = {};
let specDatabaseModify;

const baseUrl = `${localhost}database/modify`;
const serverResponseBody = {
  type: 'object',
  properties: {
    ID: {
      type: 'string',
      triggers: [
        {
          conditions: [
            {
              logic: '==',
              value: '',
              gate: '&&',
            },
          ],
          actions: [
            {
              type: 'set-value',
              value: 'MCTS{indexNoByCode}',
              field_id: 1,
            },
          ],
        },
      ],
      primaryKey: true,
      readOnly: true,
      description: 'Registration ID',
      example: 'MCTS31',
      id: 1,
    },
    Child: {
      type: 'string',
      properties: {
        ID: {
          type: 'string',
          description: 'Child ID',
          example: 'ID2',
          id: 13,
        },
      },
    },
  },
  incrementIndex: 20,
  required: ['ID'],
};

Before(() => {
  specDatabaseModify = pactum.spec();
});

// Background
Given(
  'The user wants to create or modify the Digital Registries database schema',
  () => {
    databaseSchemaVariables = {
      group_name: 'Test',
      catalog_name: 'Mother and Child',
      code: 'MCR',
      schema: {
        type: 'object',
        properties: {
          ID: {
            type: 'string',
            triggers: [
              {
                conditions: [
                  {
                    logic: '==',
                    value: '',
                    gate: '&&',
                  },
                ],
                actions: [
                  {
                    type: 'set-value',
                    value: 'MCTS{indexNoByCode}',
                    field_id: 1,
                  },
                ],
              },
            ],
            primaryKey: true,
            readOnly: true,
            description: 'Registration ID',
            example: 'MCTS31',
            id: 1,
          },
          Child: {
            type: 'string',
            properties: {
              ID: {
                type: 'string',
                description: 'Child ID',
                example: 'ID2',
                id: 13,
              },
            },
          },
        },
        incrementIndex: 30,
        required: ['ID'],
      },
    };

    return databaseSchemaVariables;
  }
);

// Scenario: The user successfully creates the Digital Registries database schema
Given('The requested database schema does not exist in the database', () => {
  return 'The requested database schema does not exist in the database';
});

When('The user triggers an action to create a database schema', () => {
  specDatabaseModify
    .post(baseUrl)
    .withHeaders(`${header.key}`, `${header.value}`)
    .withBody(databaseSchemaVariables);
});

Then(
  'Operation to create a new database schema finishes successfully',
  async () => {
    await specDatabaseModify.toss();
    specDatabaseModify.response().should.have.status(200);
    specDatabaseModify.response().should.have.jsonLike(serverResponseBody);
  }
);

// Scenario: The user successfully modifies the Digital Registries database schema
Given('The requested database schema exists in the database', () => {
  return 'The requested database schema exists in the database';
});

When('The user triggers an action to modify a database schema', () => {
  specDatabaseModify
    .post(baseUrl)
    .withHeaders(`${header.key}`, `${header.value}`)
    .withBody(databaseSchemaVariables);
});

Then(
  'Operation to modify a database schema finishes successfully',
  async () => {
    await specDatabaseModify.toss();
    specDatabaseModify.response().should.have.status(200);
    specDatabaseModify.response().should.have.jsonLike(serverResponseBody);
  }
);

// Scenario: The user is not able to modify the Digital Registries database schema because of an invalid request
When(
  'The user triggers an action to modify the already existing database schema',
  () => {
    specDatabaseModify
      .post(baseUrl)
      .withHeaders(`${header.key}`, `${header.value}`)
      .withBody(databaseSchemaVariables.schema);
  }
);

Then('Operation results to modify a database schema is an error', async () => {
  await specDatabaseModify.toss();
  specDatabaseModify.response().should.have.status(400);
  specDatabaseModify
    .response()
    .should.have.body(
      'At least `group_name`, `catalog_name`, `code` and `schema` fields are required in request payload'
    );
});

After(() => {
  specDatabaseModify.end();
});
