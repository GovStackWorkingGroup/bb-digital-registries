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

// The user successfully deletes a record from the Digital Registries database
Given(
  'The user wants to remove the record from the Digital Registries database',
  () => (dataID = 'id231Q')
);

Given(
  'The record exists in the database',
  () => 'The record exists in the database'
);

When('The user sends a valid request to delete the database record', () =>
  validRequestFunction()
);

Then('The process to delete the record completes successfully', async () => {
  await specDataDelete.toss();
  specDataDelete.response().should.have.status(200);
  specDataDelete.response().should.have.body('{\n  "Success"\n}');
});

// Scenario: The user cannot remove a record from the Digital Registries database because it does not exist
Given(
  'The user wants to remove the record that does not exist from the Digital Registries database',
  () => (dataID = 'ID001')
);

When(
  'The user sends a valid request to delete the non-existent record from the database',
  () => validRequestFunction()
);

Then(
  'The result of the operation to delete the record is an error because the record does not exist',
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
