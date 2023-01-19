const pactum = require('pactum');
const { Given, When, Then, Before, After } = require('@cucumber/cucumber');
const { header, localhost } = require('./helpers/helpers');

let databaseSchemaId;
let specDatabaseDelete;

const baseUrl = `${localhost}database/{id}`;

Before(() => {
  specDatabaseDelete = pactum.spec();
});

// Scenario: The user successfully deletes the Digital Registries schema
Given(
  'User wants to delete the Digital Registries schema and database schema exists',
  () => (databaseSchemaId = '12345')
);

When('The user triggers an action to delete the database schema', () => {
  specDatabaseDelete
    .delete(baseUrl)
    .withHeaders(`${header.key}`, `${header.value}`)
    .withPathParams('id', databaseSchemaId);
});

Then(
  'Operation to delete the database schema finishes successfully',
  async () => {
    await specDatabaseDelete.toss();
    specDatabaseDelete.response().should.have.status(200);
    specDatabaseDelete.response().should.have.body('Success');
  }
);

// Scenario: The user is not able to delete the Digital Registries schema because the schema does not exist
Given(
  'User wants to delete the Digital Registries schema and the database schema does not exist',
  () => (databaseSchemaId = '12')
);

// "When" is already written in line 20-25

Then(
  'Operation to delete a database schema returns an error because the schema does not exist',
  async () => {
    await specDatabaseDelete.toss();
    specDatabaseDelete.response().should.have.status(400);
    specDatabaseDelete.response().should.have.body('Failure');
  }
);

After(() => {
  specDatabaseDelete.end();
});
