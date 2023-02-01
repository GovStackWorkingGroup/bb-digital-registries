const pactum = require('pactum');
const { Given, When, Then, Before, After } = require('@cucumber/cucumber');
const { header, localhost } = require('./helpers/helpers');

let databaseSchemaId;
let specDatabaseDelete;

const baseUrl = `${localhost}database/{id}`;

Before(() => {
  specDatabaseDelete = pactum.spec();
});

// Scenario: User successfully deletes the Digital Registries schema
Given(
  'The user wants to delete the Digital Registries schema and the database schema exists',
  () => (databaseSchemaId = '12345')
);

When('The user sends a valid request to delete the database schema', () =>
  specDatabaseDelete
    .delete(baseUrl)
    .withHeaders(`${header.key}`, `${header.value}`)
    .withPathParams('id', databaseSchemaId)
);

Then(
  'The operation to delete the database schema completes successfully',
  async () => {
    await specDatabaseDelete.toss();
    specDatabaseDelete.response().should.have.status(200);
    specDatabaseDelete.response().should.have.body('Success');
  }
);

// The user cannot delete the schema from Digital Registries because the schema does not exist
Given(
  'The user wants to delete the Digital Registries schema and the database schema does not exist',
  () => (databaseSchemaId = '12')
);

// "When" is already written in line 20-25

Then(
  'The operation to delete a database schema returns an error because the schema does not exist',
  async () => {
    await specDatabaseDelete.toss();
    specDatabaseDelete.response().should.have.status(400);
    specDatabaseDelete.response().should.have.body('Failure');
  }
);

After(() => {
  specDatabaseDelete.end();
});
