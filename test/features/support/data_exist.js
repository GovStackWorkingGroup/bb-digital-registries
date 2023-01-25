const pactum = require('pactum');
const { Given, When, Then, Before, After } = require('@cucumber/cucumber');
const { header, localhost } = require('./helpers/helpers');

let searchedRecord;
let specDataExist;

const baseUrl = `${localhost}data/registry1/version1/exists`;

Before(() => {
  specDataExist = pactum.spec();
});

// Scenario: The user receives a message that the record exists in the Digital Registries database
Given(
  `The user wants to check if a record exists in the Digital Registries database`,
  () => (searchedRecord = 'John Helmut')
);

When(
  'The user triggers an action to check if a record exists in the database',
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

Then(
  'Operation to receive a message that a record exists in the database finishes successfully',
  async () => {
    await specDataExist.toss();
    specDataExist.response().should.have.status(200);
  }
);

Then(
  'The user receives information that a record exists in the database',
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
  `The user wants to check if the record exists in the Digital Registries database`,
  () => (searchedRecord = 'Adrien')
);

// "When" is already written in line 20-34

// "Then" is already written in line 36-42

Then(
  'The user receives information that the record does not exist in the database',
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
// Given already written in line 15-18

When(
  'The user triggers an action with an invalid request to check if the record exists in the database',
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

Then('Operation returns an error because of an invalid request', async () => {
  await specDataExist.toss();
  return specDataExist.response().should.have.status(400);
});

After(() => {
  specDataExist.end();
});
