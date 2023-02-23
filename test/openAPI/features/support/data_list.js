const pactum = require('pactum');
const { When, Then, Given, After, Before } = require('@cucumber/cucumber');
const { header, localhost } = require('./helpers/helpers');

let searchedName;
let specDataList;

const baseUrl = `${localhost}data/registry1/version1`;

Before(() => {
  specDataList = pactum.spec();
});

// Scenario: The user gets a list of all searched records in the Digital Registries database
Given(
  'The user wants to search for a specific value and the searched value exists in multiple records in the database',
  () => (searchedName = 'John')
);

When('The user sends a valid request to search the database', () =>
  specDataList
    .get(`${baseUrl}?filter=FirstName&search=${searchedName}`)
    .withHeaders(`${header.key}`, `${header.value}`)
);

Then(
  'The user receives a list of all records that contain the searched value',
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
  'The user receives an empty list because there is no record in the database that contains the searched value',
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

When('The user sends an invalid request to search the database', () =>
  specDataList.get(`${baseUrl}?filter=FirstName&search=${searchedName}`)
);

Then('The operation results in an error due to an invalid query', async () => {
  await specDataList.toss();
  specDataList.response().should.have.status(400);
});

After(() => {
  specDataList.end();
});
