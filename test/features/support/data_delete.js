const pactum = require('pactum');
const { Given, When, Then, Before, After } = require('@cucumber/cucumber');
const { header, localhost } = require('./helpers/helpers');

let dataID;
let specDataDelete;

const baseUrl = `${localhost}data/registry1/version1/{id}/delete`;
const validRequestFunction = () =>
  specDataDelete
    .delete(baseUrl)
    .withHeaders(`${header.key}`, `${header.value}`)
    .withPathParams('id', dataID);

Before(() => {
  specDataDelete = pactum.spec();
});

// Scenario: The user successfully removes a record from the Digital Registries database
Given(
  'The user wants to remove the record from the Digital Registries database',
  () => (dataID = 'id231Q')
);

Given(
  'The record does exist in the database',
  () => 'The record does exist in the database'
);

When('The user triggers an action to delete the database record', () =>
  validRequestFunction()
);

Then('Operation to delete the record finishes successfully', async () => {
  await specDataDelete.toss();
  specDataDelete.response().should.have.status(200);
  specDataDelete.response().should.have.body('{\n  "Success"\n}');
});

// Scenario: The user is not able to remove a record from the Digital Registries database because the record does not exist
Given(
  'The user wants to remove the record which does not exist from the Digital Registries database',
  () => (dataID = 'ID001')
);

When(
  'The user triggers an action to delete the database the record which does not exist',
  () => validRequestFunction()
);

Then(
  'Operation results for deleting the record is an error because the record does not exist',
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
