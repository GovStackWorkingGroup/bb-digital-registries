const pactum = require('pactum');
const { Given, When, Then, Before, After } = require('@cucumber/cucumber');
const { header, localhost } = require('./helpers/helpers');

let dataID;
let specDataDelete;

const baseUrl = id => `${localhost}data/registry1/version1/${id}/delete`;

Before(() => {
  specDataDelete = pactum.spec();
});

// Scenario: The user successfully removes a record from the Digital Registries database
Given(
  'The user wants to remove record with id=ID1234 from the Digital Registries database',
  () => {
    dataID = 'ID1234';
    return dataID;
  }
);
Given('The record with id=ID1234 does exist in the database', () => {
  return 'The record with id=ID1234 does exist in the database';
});

When(
  'The user triggers an action to delete the database record with with id=ID1234',
  () => {
    specDataDelete
      .delete(`${baseUrl(dataID)}`)
      .withHeaders(`${header.key}`, `${header.value}`);
  }
);

Then(
  'Operation to delete record with with id=ID1234 finishes successfully',
  async () => {
    await specDataDelete.toss();
    specDataDelete.response().should.have.status(200);
    specDataDelete.response().should.have.body('{\n  "Success"\n}');
  }
);

// Scenario: The user is not able to remove a record from the Digital Registries database because the record does not exist
Given(
  'The user wants to remove record with id=ID001 from the Digital Registries database',
  () => {
    dataID = 'ID001';
  }
);

Given('The record with id=ID001 does not exist in the database', () => {
  return 'The record with id=ID001 does not exist in the database';
});

When(
  'The user triggers an action to delete the database record with id=ID001',
  () => {
    specDataDelete
      .delete(`${baseUrl(dataID)}`)
      .withHeaders(`${header.key}`, `${header.value}`);
  }
);

Then(
  'Operation results to delete record with id=ID001 is an error',
  async () => {
    await specDataDelete.toss();
    specDataDelete.response().should.have.status(404);
    specDataDelete
      .response()
      .should.have.body('{\n  "Provided id does not exist in the database"\n}');
  }
);

After(() => {
  specDataDelete.end();
});
