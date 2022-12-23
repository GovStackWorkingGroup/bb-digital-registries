const pactum = require('pactum');
const { Given, When, Then, Before, After } = require('@cucumber/cucumber');
const { header } = require('./helpers/helpers');

let searchedRecord;
let specDataReadValue = pactum.spec();

const baseUrl = uuid =>
  `http://localhost:3333/data/registry1/version1/${uuid}/read-value/User.FirstName`;

Before(() => {
  specDataReadValue = pactum.spec();
});

// Scenario: The user receives the first name of searched user from the Digital Registries database
Given(
  'The user wants to search for the first name of the user with UUID 2dcad39a-9abb-4552-954d-c62958d44ec5 in the Digital Registries database',
  () => {
    return (searchedRecord = '2dcad39a-9abb-4552-954d-c62958d44ec5');
  }
);

Given(`The record's first name is fullfill`, () => {
  return `The searched record's first name is fullfill`;
});

When(
  'The user triggers an action to receive the first name of searched user with UUID 2dcad39a-9abb-4552-954d-c62958d44ec5 from the database',
  () => {
    specDataReadValue
      .get(`${baseUrl(searchedRecord)}`)
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
  'The user wants to search for the first name of the user with UUID 3dcad39a-9abb-4552-954d-c62958d44ec9 in the Digital Registries database',
  () => {
    return (searchedRecord = '3dcad39a-9abb-4552-954d-c62958d44ec9');
  }
);

Given(`The record's first name is empty`, () => {
  return `The searched record's first name is empty`;
});

When(
  'The user triggers an action to receive the first name of searched user with UUID 3dcad39a-9abb-{int}-954d-c62958d44ec9 from the database',
  int => {
    specDataReadValue
      .get(`${baseUrl(searchedRecord)}`)
      .withHeaders(`${header.key}`, `${header.value}`);
  }
);

Then(
  'The user receives a message that the first name of the searched user is empty',
  async () => {
    await specDataReadValue.toss();
    specDataReadValue.response().should.have.status(200);
    specDataReadValue.response().should.have.jsonLike('');
  }
);

// Scenario: The user is not able to receive the first name of the user from the Digital Registries database because of an invalid request
Given(
  'The user wants to search for the first name of the user with UUID  in the Digital Registries database',
  () => {
    return (searchedRecord = '3dcad39a-9abb-4552-954d-c62958d44e');
  }
);

When(
  'The user triggers an action to receive the first name of searched user from the database',
  () => {
    specDataReadValue.get(`${baseUrl(searchedRecord)}`);
  }
);

Then(
  'Operation results for \\/data\\/registryname\\/versionnumber\\/uuid\\/read-value\\/field.ext is an error',
  async () => {
    await specDataReadValue.toss();
    specDataReadValue.response().should.have.status(400);
  }
);

After(() => {
  specDataReadValue.end();
});
