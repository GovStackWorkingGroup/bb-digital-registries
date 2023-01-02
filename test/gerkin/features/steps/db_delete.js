const pactum = require('pactum');
const { Given, When, Then, Before, After } = require('@cucumber/cucumber');
const { header, localhost } = require('./helpers/helpers');

let databaseSchemaId;
let specDatabaseDelete;

const baseUrl = id => `${localhost}database/${id}`;

Before(() => {
  specDatabaseDelete = pactum.spec();
});

// Scenario: The user successfully deletes the Digital Registries schema
Given(
  'User wants to delete the Digital Registries schema with id=12345',
  () => {
    databaseSchemaId = '12345';
    return databaseSchemaId;
  }
);

Given('The requested database schema exists', () => {
  return 'The requested database schema exists';
});

When(
  'The user triggers an action to delete the database schema with id=12345',
  () => {
    specDatabaseDelete
      .delete(baseUrl(databaseSchemaId))
      .withHeaders(`${header.key}`, `${header.value}`);
  }
);

Then(
  'Operation to a delete database schema finishes successfully',
  async () => {
    await specDatabaseDelete.toss();
    specDatabaseDelete.response().should.have.status(200);
    specDatabaseDelete.response().should.have.body('Success');
  }
);

// Scenario: The user is not able to delete the Digital Registries schema because schema does not exist
Given('User wants to delete the Digital Registries schema with id=12', () => {
  databaseSchemaId = '12';
  return databaseSchemaId;
});

Given('The requested database schema does not exists', () => {
  return 'The requested database schema does not exists';
});

When(
  'The user triggers an action to delete the database schema with id=12',
  () => {
    specDatabaseDelete
      .delete(baseUrl(databaseSchemaId))
      .withHeaders(`${header.key}`, `${header.value}`);
  }
);

Then(
  'Operation to delete a database schema finishes successfully',
  async () => {
    await specDatabaseDelete.toss();
    specDatabaseDelete.response().should.have.status(400);
    specDatabaseDelete.response().should.have.body('Failure');
  }
);

After(() => {
  specDatabaseDelete.end();
});
