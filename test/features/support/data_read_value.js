const pactum = require('pactum');
const { Given, When, Then, Before, After } = require('@cucumber/cucumber');
const { header, localhost } = require('./helpers/helpers');

let searchedRecord;
let searchedFieldParameter;
let searchedFieldExt;
let specDataReadValue;

const baseUrl = (uuid, field, ext) =>
  `${localhost}data/registry1/version1/${uuid}/read-value/${field}.${ext}`;

Before(() => {
  specDataReadValue = pactum.spec();
  searchedFieldParameter = 'User';
  searchedFieldExt = 'FirstName';
});

// Scenario: The user receives the first name of searched user from the Digital Registries database
Given(
  "The user wants to search for the first name of the user in the Digital Registries database and the record's first name is fulfilled",
  () => (searchedRecord = '2dcad39a-9abb-4552-954d-c62958d44ec5')
);

When(
  'The user triggers an action to receive the first name of searched user from the database',
  () => {
    specDataReadValue
      .get(
        `${baseUrl(searchedRecord, searchedFieldParameter, searchedFieldExt)}`
      )
      .withHeaders(`${header.key}`, `${header.value}`);
  }
);

Then('The user receives the first name of the searched user', async () => {
  await specDataReadValue.toss();
  specDataReadValue.response().should.have.status(200);
  specDataReadValue.response().should.have.jsonLike('John Helmut');
});

// Scenario: The user does not receive the first name of searched user from the Digital Registries database
Given(
  "The user wants to search for the first name of the user in the Digital Registries database and the record's first name is empty",
  () => (searchedRecord = '3dcad39a-9abb-4552-954d-c62958d44ec9')
);

// "When" is already written in line 25-34

Then(
  'The user receives a message that the first name of the searched user is empty',
  async () => {
    await specDataReadValue.toss();
    specDataReadValue.response().should.have.status(200);
    specDataReadValue.response().should.have.jsonLike('');
  }
);

// // Scenario: The user is not able to receive the first name of the user from the Digital Registries database because of an invalid request
Given(
  'The user wants to search for the first name of the user in the Digital Registries database',
  () => (searchedRecord = '3dcad39a-9abb-4552-954d-c62958d44e')
);

When(
  'The user triggers an action with an invalid request to receive the first name of searched user from the Digital Registries database',
  () => {
    specDataReadValue.get(
      `${baseUrl(searchedRecord, searchedFieldParameter, searchedFieldExt)}`
    );
  }
);

Then(
  'Operation results for receive the first name of the user is an error',
  async () => {
    await specDataReadValue.toss();
    specDataReadValue.response().should.have.status(400);
  }
);

After(() => {
  specDataReadValue.end();
});
