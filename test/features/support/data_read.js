const pactum = require('pactum');
const { Given, When, Then, Before, After } = require('@cucumber/cucumber');
const { header, localhost } = require('./helpers/helpers');

let searchedRecord;
let specDataRead;

const baseUrl = `${localhost}data/registry1/version1/read`;

Before(() => {
  specDataRead = pactum.spec();
});

// Scenario: User obtains a searched record from the Digital Registries database
Given(
  'The user wants to search for a record in the Digital Registries database and the searched record exists in the database',
  () => (searchedRecord = 'John Benz')
);

When(
  'The user sends a valid request to search for a record in the database',
  () =>
    specDataRead
      .post(`${baseUrl}`)
      .withHeaders(`${header.key}`, `${header.value}`)
      .withBody({
        query: {
          content: {
            FirstName: searchedRecord,
          },
        },
      })
);

Then('The user receives a searched record', async () => {
  await specDataRead.toss();
  specDataRead.response().should.have.status(200);
  specDataRead.response().should.have.jsonLike({
    content: {
      ID: 'c473a46c-dd2d-42f5-aca3-f318d478d736',
      FirstName: 'John Benz',
      LastName: 'Wintheiser',
      BirthCertificateID: 'RR-4419523937',
    },
  });
});

// Scenario: The user does not receive a searched record from the Digital Registries database
Given(
  'The user wants to search for a record in the Digital Registries database and the searched record does not exist in the database',
  () => (searchedRecord = 'David Belt')
);

// "When" is already written in line 20-31

Then(
  'The user receives a message that there is no searched record in the database',
  async () => {
    await specDataRead.toss();
    specDataRead.response().should.have.status(404);
  }
);

// Scenario: The user is unable to obtain a searched record from the Digital Registries database because the request is invalid
Given(
  'The user wants to search for one record in the Digital Registries database',
  () => (searchedRecord = 'Ali Benz')
);

When(
  'The user sends an invalid request to search for a record in the Digital Registries database',
  () =>
    specDataRead.post(`${baseUrl}`).withBody({
      query: {
        content: {
          FirstName: searchedRecord,
        },
      },
    })
);

Then(
  'The result of the operation to obtain a searched record is an error',
  async () => {
    await specDataRead.toss();
    specDataRead.response().should.have.status(400);
  }
);

After(() => {
  specDataRead.end();
});
