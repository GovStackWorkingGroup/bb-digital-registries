const pactum = require('pactum');
const { When, Then, Given, After, Before } = require('@cucumber/cucumber');
const { header, localhost } = require('./helpers/helpers');

let searchedName;
let specDataList;

const baseUrl = `${localhost}data/registry1/version1`;

Before(() => {
  specDataList = pactum.spec();
});

// Scenario: The user receives a list with all searched records in the Digital Registries database
Given(
  'The user wants to search for a specific value and the searched value exists in several records in the database',
  () => (searchedName = 'John')
);

When('The user triggers an action to search in the database', () => {
  specDataList
    .get(`${baseUrl}?filter=FirstName&search=${searchedName}`)
    .withHeaders(`${header.key}`, `${header.value}`);
});

Then(
  'The user receives a list with all records including searched value',
  async () => {
    await specDataList.toss();
    specDataList.response().should.have.status(200);
    specDataList.response().should.have.jsonLike({
      results: [
        {
          FirstName: searchedName,
        },
      ],
    });
  }
);

// Scenario: The user receives an empty list from the Digital Registries database
Given(
  'The user wants to search for a specific value and the searched value does not exist in any record in the database',
  () => (searchedName = 'Adrien')
);

// "When" is already written in line 20-24

Then(
  'The user receives an empty list because there is no record including the searched value in the database',
  async () => {
    await specDataList.toss();
    specDataList.response().should.have.status(200);
    specDataList.response().should.have.jsonLike({
      results: [],
    });
  }
);

// Scenario: The user is not able to search for the records in the Digital Registries database because of an invalid request
// "Given" is already written in line 15-18

When(
  'The user triggers an action to search in the database and send an invalid request',
  () => {
    specDataList.get(`${baseUrl}?filter=FirstName&search=${searchedName}`);
  }
);

Then(
  'Operation results in an error because of an invalid request',
  async () => {
    await specDataList.toss();
    specDataList.response().should.have.status(400);
  }
);

After(() => {
  specDataList.end();
});
