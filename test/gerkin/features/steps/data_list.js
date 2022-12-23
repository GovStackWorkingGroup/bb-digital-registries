const pactum = require('pactum');
const { When, Then, Given, After, Before } = require('@cucumber/cucumber');
const { header } = require('./helpers/helpers');

let searchedName;
let specDataList = pactum.spec();

const baseUrl = 'http://localhost:3333/data/registry1/version1';

Before(() => {
  specDataList = pactum.spec();
});

// Scenario: The user receives a list with all records including "John" in the Digital Registries database
Given('The user wants to search for "John" in the database', () => {
  return (searchedName = 'John');
});

Given('The searched value exists in several records in the database', () => {
  return 'Searched value does exist in the database';
});

When('The user triggers an action to search "John" in the database', () => {
  specDataList
    .get(`${baseUrl}?filter=FirstName&search=${searchedName}`)
    .withHeaders(`${header.key}`, `${header.value}`);
});

Then(
  'The user receives a list with all records including {string}',
  async string => {
    await specDataList.toss();
    specDataList.response().should.have.status(200);
    specDataList.response().should.have.jsonLike({
      results: [
        {
          FirstName: string,
        },
      ],
    });
  }
);

// Scenario: The user receives an empty list from the Digital Registries database
Given('The user wants to search for "Adrien" in the database', () => {
  return (searchedName = 'Adrien');
});

Given('The searched value does not exist in any record in the database', () => {
  return 'Searched value does not exist in the database';
});

When('The user triggers an action to search "Adrien" in the database', () => {
  specDataList
    .get(`${baseUrl}?filter=FirstName&search=${searchedName}`)
    .withHeaders(`${header.key}`, `${header.value}`);
});

Then(
  'The user receives an empty list because there is no record including "Adrien" in the database',
  async () => {
    await specDataList.toss();
    specDataList.response().should.have.status(200);
    specDataList.response().should.have.jsonLike({
      results: [],
    });
  }
);

// Scenario: The user is not able to search for the records in the Digital Registries database because on an invalid request
Given('The user wants to search for "Anna" in the database', () => {
  return (searchedName = 'Anna');
});

When(
  'The user triggers an action to search "Anna" in the database and sent an invalid request',
  () => {
    specDataList.get(`${baseUrl}?filter=FirstName&search=${searchedName}`);
  }
);

Then('Operation results in an error', async () => {
  await specDataList.toss();
  specDataList.response().should.have.status(400);
});

After(() => {
  specDataList.end();
});
