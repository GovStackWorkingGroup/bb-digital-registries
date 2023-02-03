const pactum = require('pactum');
const { Given, When, Then, Before, After } = require('@cucumber/cucumber');
const { header, localhost } = require('./helpers/helpers');

let userVariables = {};
let specDataUpdateEntries;

const baseUrl = `${localhost}data/registry1/version1/update-entries`;
const validRequestFunction = () =>
  specDataUpdateEntries
    .put(baseUrl)
    .withHeaders(`${header.key}`, `${header.value}`)
    .withBody({
      query: {
        content: userVariables,
      },
      write: {
        content: userVariables,
      },
    });

Before(() => {
  specDataUpdateEntries = pactum.spec();
});

// Scenario: User successfully updates two existing records in the Digital Registries database
Given(
  'The user wants to update multiple records in the Digital Registries database and these records already exist',
  () =>
    (userVariables = {
      ID: 'EE378627348834',
      FirstName: 'Alfie',
      LastName: 'Grande',
      BirthCertificateID: 'RR-1234567889',
    })
);

When('The user sends a valid request to update records in the database', () =>
  validRequestFunction()
);

Then('The record update process completes successfully', async () => {
  await specDataUpdateEntries.toss();
  specDataUpdateEntries.response().should.have.status(200);
});

// Scenario: The user is unable to update two records that do not exist in the Digital Registries database
Given(
  'The user wants to update multiple records in the Digital Registries database and these records do not exist',
  () =>
    (userVariables = {
      ID: 'EE378627348834',
      FirstName: 'Jerry',
      LastName: 'Blake',
      BirthCertificateID: 'RR-1234567889',
    })
);

// "When" is already written in line 38-40

Then(
  `The result of an operation to update records returns an error`,
  async () => {
    await specDataUpdateEntries.toss();
    specDataUpdateEntries.response().should.have.status(404);
    specDataUpdateEntries
      .response()
      .should.have.body('{\n  "Record matching query not found."\n}');
  }
);

// Scenario: The user is unable to update two records in the Digital Registries database due to an invalid request
Given(
  'The user wants to update multiple records in the Digital Registries database',
  () =>
    (userVariables = {
      ID: 'EE378627348834',
      FirstName: 'Jasmine',
      LastName: 'Sun',
      BirthCertificateID: null,
    })
);

When(
  'The user sends an invalid request to update records in the database',
  () =>
    specDataUpdateEntries
      .put(baseUrl)
      .withHeaders(`${header.key}`, `${header.value}`)
      .withBody({
        query: {
          content: userVariables,
        },
      })
);

Then(
  `The result of an operation to update records returns an error because the request is invalid`,
  async () => {
    await specDataUpdateEntries.toss();
    specDataUpdateEntries.response().should.have.status(400);
    specDataUpdateEntries
      .response()
      .should.have.body('{\n  "Query not provided."\n}');
  }
);

// Scenario: The user is unable to update two records in the Digital Registries database because the user data is missing
// "Given" is already written in line 73-82

When(
  `The user sends an invalid request with missing user data to update records in the database`,
  () => validRequestFunction()
);

Then(
  `The result of an operation to update records returns an error because of missing users data`,
  async () => {
    await specDataUpdateEntries.toss();
    specDataUpdateEntries.response().should.have.status(400);
    specDataUpdateEntries
      .response()
      .should.have.bodyContains(
        'Invalid payload, query.content.FirstName, query.content.ID, query.content.LastName or query.content.BirthCertificateID not provided'
      );
  }
);

After(() => {
  specDataUpdateEntries.end();
});
