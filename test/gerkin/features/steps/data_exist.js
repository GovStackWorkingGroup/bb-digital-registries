const pactum = require('pactum');
const { Given, When, Then, Before, After } = require('@cucumber/cucumber');
const { header, localhost } = require('./helpers/helpers');

let searchedRecord;
let specDataExist = pactum.spec();

const baseUrl = `${localhost}data/registry1/version1/exists`;

Before(() => {
  specDataExist = pactum.spec();
});

// Scenario: The user receives a message that the record exists in the Digital Registries database
Given(
  `The user wants to check if a record with the first name "John Helmut" exists in the Digital Registries database`,
  () => {
    return (searchedRecord = 'John Helmut');
  }
);

Given(
  `The record with the first name "John Helmut" is available in the database`,
  () => {
    return `The record with the first name "John Helmut" is available in the database`;
  }
);

When(
  'The user triggers an action to check if the record with the first name "John Helmut" already exists in the database',
  () => {
    specDataExist
      .post(`${baseUrl}`)
      .withHeaders(`${header.key}`, `${header.value}`)
      .withBody({
        query: {
          content: {
            FirstName: searchedRecord,
          },
        },
      });
  }
);

Then('Operation finishes for {string} successfully', async string => {
  await specDataExist.toss();
  specDataExist.response().should.have.status(200);
});

Then(
  'The user receives an information that the record exists in the database',
  () => {
    specDataExist.response().should.have.jsonLike({
      answer: {
        status: true,
        message: 'Object found from database',
      },
    });
  }
);

// Scenario: The user receives the message that the record does not exist in the Digital Registries database
Given(
  `The user wants to check if a record with the first name "Adrien" exists in the Digital Registries database`,
  () => {
    return (searchedRecord = 'Adrien');
  }
);

Given(
  `The record with the first name "Adrien" is not available in the database`,
  () => {
    return `The record with the first name "Adrien" is not available in the database`;
  }
);

When(
  `The user triggers an action to check if the record with the first name "Adrien" exists in the database`,
  () => {
    specDataExist
      .post(`${baseUrl}`)
      .withHeaders(`${header.key}`, `${header.value}`)
      .withBody({
        query: {
          content: {
            FirstName: searchedRecord,
          },
        },
      });
  }
);

Then('Operation for {string} finishes successfully', async string => {
  await specDataExist.toss();
  specDataExist.response().should.have.status(200);
});

Then(
  'The user receives an information that the record does not exist in the database',
  () => {
    specDataExist.response().should.have.jsonLike({
      answer: {
        status: false,
        message: 'Object not found from database',
      },
    });
  }
);

// Scenario: The user is not able to check if the record exists in the Digital Registries database because of an invalid request
Given(
  `The user wants to check if a record with the first name "Anna" exists in the Digital Registries database`,
  () => {
    return (searchedRecord = 'Anna');
  }
);

When(
  'The user triggers an action to check if the record with the first name "Anna" exists in the database',
  () => {
    specDataExist.post(`${baseUrl}`).withBody({
      query: {
        content: {
          FirstName: searchedRecord,
        },
      },
    });
  }
);

Then(
  'Operation results for \\/data\\/registryname\\/versionnumber\\/exists is an error',
  async () => {
    await specDataExist.toss();
    return specDataExist.response().should.have.status(400);
  }
);

After(() => {
  specDataExist.end();
});
