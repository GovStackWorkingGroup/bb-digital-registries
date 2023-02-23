const pactum = require('pactum');
const { Given, When, Then, Before, After } = require('@cucumber/cucumber');
const { header, localhost } = require('./helpers/helpers');

let specDatabaseRead;

const baseUrl = `${localhost}database/{id}`;
const exampleResponseValue = {
  id: 353,
  version: '2.7',
  name: 'MCTS',
  description: 'Database holding information about MCTS objects',
  institution: 'Ministry of Social Affairs',
  number_format: '{code}{indexNoByCode}',
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
    incrementIndex: 20,
    required: ['ID'],
  },
  schema_tags: [
    {
      name: '',
      path: '/Child/Citizenship',
      is_fulltext: true,
    },
  ],
  schema_flags: [
    {
      name: 'mandatory',
      path: '/ID',
    },
  ],
  fields_uniques: [['']],
  is_draft: false,
  is_disabled: false,
  is_archived: false,
  modified_at: '2021-10-03T08:35:01.775915Z',
  by_user_name: 'ingmar.dev',
  by_user_auth_id: 1,
  by_on_behalf_of_user_auth_id: null,
  by_on_behalf_of_user_name: null,
  generic_services: [
    {
      service_id: 1,
      name: 'data-create',
      is_visible: true,
      used_count: 0,
    },
  ],
  data_index_increment: 0,
  has_logo: false,
};

Before(() => {
  specDatabaseRead = pactum.spec();
});

// Background: User wants to get the database information of Digital Registries with schema version
Given(
  'User wants to get the database information of Digital Registries with schema version',
  () =>
    'User wants to get the database information of Digital Registries with schema version'
);

// Scenario: User successfully obtains Digital Registries database information with schema version
When('The user sends a valid request to view a database schema version', () =>
  specDatabaseRead
    .get(baseUrl)
    .withHeaders(`${header.key}`, `${header.value}`)
    .withPathParams('id', 353)
);

Then(
  'The user has received a database information with schema version',
  async () => {
    await specDatabaseRead.toss();
    specDatabaseRead.response().should.have.status(200);
    specDatabaseRead.response().should.have.jsonLike(exampleResponseValue);
  }
);

// Scenario: The user cannot get database information from Digital Registries with the schema version because he did not specify a route parameter
When(
  'The user sends an invalid request without routing parameters to view a database schema version',
  () =>
    specDatabaseRead
      .get(baseUrl)
      .withHeaders(`${header.key}`, `${header.value}`)
);

Then(
  'The result of an operation to receive database information from Digital Registries with schema version returns an invalid route param error',
  async () => {
    await specDatabaseRead.toss();
    specDatabaseRead.response().should.have.status(400);
    specDatabaseRead.response().should.have.body('{"Invalid route param id"}');
  }
);

// Scenario: The user is unable to receive database information from Digital Registries with schema version because no header is included
When(
  'The user sends an invalid request to view a database schema version',
  () => specDatabaseRead.get(baseUrl).withHeaders(`${header.key}`, '')
);

Then(
  'The result of an operation to receive database information from Digital Registries with the schema version returns an error',
  async () => {
    await specDatabaseRead.toss();
    specDatabaseRead.response().should.have.status(400);
    specDatabaseRead
      .response()
      .should.have.body(
        '{"Invalid format of Information-Mediator-Client, should match INSTANCE/CLASS/MEMBER/SUBSYSTEM"}'
      );
  }
);

// Scenario: The user cannot receive Digital Registries database information with the schema version because there is no header included
When(
  'The user sends an invalid request with no payload to view a database schema version',
  () => specDatabaseRead.get(baseUrl)
);

Then(
  'The result of receiving Digital Registries database information with the schema version is an error',
  async () => {
    await specDatabaseRead.toss();
    specDatabaseRead.response().should.have.status(400);
    specDatabaseRead
      .response()
      .should.have.body('{"Information-Mediator-Client required"}');
  }
);

After(() => {
  specDatabaseRead.end();
});