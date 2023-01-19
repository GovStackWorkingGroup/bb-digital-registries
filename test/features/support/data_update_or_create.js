const pactum = require('pactum');
const { Given, When, Then, Before, After } = require('@cucumber/cucumber');
const { header, localhost } = require('./helpers/helpers');

let userVariables = {};
let specDataUpdateOrCreate;

const baseUrl = `${localhost}data/registry1/version1/update-or-create`;

Before(() => {
  specDataUpdateOrCreate = pactum.spec();
});

// Scenario: The user successfully creates a new record in the Digital Registries database
Given(
  'The user wants to create a new record or update an existing one if already exists in the Digital Registries database',
  () =>
    (userVariables = {
      ID: 'EE378627348834',
      FirstName: 'Jon',
      LastName: 'Snake',
      BirthCertificateID: 'RR-1234567889',
    })
);

Given(
  'The requested record does not exist in the database',
  () => 'The requested record "Jon Snake" does not exist in the database'
);

When(
  'The user triggers an action to create or update a record in the database',
  () => {
    specDataUpdateOrCreate
      .post(baseUrl)
      .withHeaders(`${header.key}`, `${header.value}`)
      .withBody({
        query: {
          content: userVariables,
        },
        write: {
          content: userVariables,
        },
      });
  }
);

Then('Operation to create the new record finishes successfully', async () => {
  await specDataUpdateOrCreate.toss();
  specDataUpdateOrCreate.response().should.have.status(200);
  specDataUpdateOrCreate.response().should.have.jsonLike({
    content: userVariables,
  });
});

// Scenario: The user successfully updates the already existing record in the Digital Registries database
Given(
  'The user wants to update an existing record in the Digital Registries database',
  () =>
    (userVariables = {
      ID: 'EE378627348834',
      FirstName: 'Johny',
      LastName: 'Small',
      BirthCertificateID: 'RR-1234567889',
    })
);

Given(
  'The requested record already exists in the database',
  () => 'The requested record "Johny Small" already exists in the database'
);

// "When" is already written in line 31-46

Then('Operation to update the record finishes successfully', async () => {
  await specDataUpdateOrCreate.toss();
  specDataUpdateOrCreate.response().should.have.status(200);
  specDataUpdateOrCreate.response().should.have.jsonLike({
    content: userVariables,
  });
});

// Scenario: The user is not able to create/update a record in the Digital Registries database because of an invalid request
// "Given" already writtennin the line 15-24

When(
  'The user triggers an action to create or update a record in the database with an invalid request',
  () => {
    specDataUpdateOrCreate
      .post(baseUrl)
      .withHeaders(`${header.key}`, `${header.value}`)
      .withBody({
        query: {
          content: userVariables,
        },
      });
  }
);

Then(
  `The result of an operation to create\\/update the record returns an error because of an invalid request`,
  async () => {
    await specDataUpdateOrCreate.toss();
    specDataUpdateOrCreate.response().should.have.status(400);
    specDataUpdateOrCreate
      .response()
      .should.have.body('{\n  "Query not provided."\n}');
  }
);

After(() => {
  specDataUpdateOrCreate.end();
});
