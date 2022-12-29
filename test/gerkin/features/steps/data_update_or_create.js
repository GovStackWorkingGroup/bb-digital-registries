const pactum = require('pactum');
const { Given, When, Then, Before, After } = require('@cucumber/cucumber');
const { header, localhost } = require('./helpers/helpers');

let userVariables = {};
let specDataUpdateOrCreate;

const baseUrl = `${localhost}data/registry1/version1/update-or-create`;

Before(() => {
  specDataUpdateOrCreate = pactum.spec();
});

// Scenario: The user successfully creates new record in the Digital Registries database
Given(
  'The user wants to create a new record "Jon Snake" or update an existing one if already exists in the Digital Registries database',
  () => {
    userVariables = {
      ID: 'EE378627348834',
      FirstName: 'Jon',
      LastName: 'Snake',
      BirthCertificateID: 'RR-1234567889',
    };

    return userVariables;
  }
);

Given('The requested record "Jon Snake" does not exist in the database', () => {
  return 'The requested record "Jon Snake" does not exist in the database';
});

When(
  'The user triggers an action to create record "Jon Snake" in the database',
  () => {
    specDataUpdateOrCreate
      .post(`${baseUrl}`)
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

Then('Operation to create "Jon Snake" finishes successfully', async () => {
  await specDataUpdateOrCreate.toss();
  specDataUpdateOrCreate.response().should.have.status(200);
  specDataUpdateOrCreate.response().should.have.jsonLike({
    content: userVariables,
  });
});

// Scenario: The user successfully updates the already existing record in the Digital Registries database
Given(
  'The user wants to create a new record "Johny Small" or update an existing one if already exists in the Digital Registries database',
  () => {
    userVariables = {
      ID: 'EE378627348834',
      FirstName: 'Johny',
      LastName: 'Small',
      BirthCertificateID: 'RR-1234567889',
    };

    return userVariables;
  }
);

Given(
  'The requested record "Johny Small" already exists in the database',
  () => {
    return 'The requested record "Johny Small" already exists in the database';
  }
);

When(
  'The user triggers an action to update record "Johny Small" in the database',
  () => {
    specDataUpdateOrCreate
      .post(`${baseUrl}`)
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

Then(
  'Operation to update record "Johny Small" finishes successfully',
  async () => {
    await specDataUpdateOrCreate.toss();
    specDataUpdateOrCreate.response().should.have.status(200);
    specDataUpdateOrCreate.response().should.have.jsonLike({
      content: userVariables,
    });
  }
);

// Scenario: The user is not able to create/update a record in the Digital Registries database because of an invalid request
Given(
  'Given The user wants to create record "Ali Smith" or update an existing one if already exists in the Digital Registries database',
  () => {
    userVariables = {
      ID: 'EE378627348834',
      FirstName: 'Ali',
      LastName: 'Smith',
      BirthCertificateID: 'RR-1234567889',
    };
  }
);

When(
  'The user triggers an action to create record "Ali Smith" in the database',
  () => {
    specDataUpdateOrCreate
      .post(`${baseUrl}`)
      .withHeaders(`${header.key}`, `${header.value}`)
      .withBody({
        query: {
          content: userVariables,
        },
      });
  }
);

Then(
  'Operation results to create\\/update record {string} in an error',
  async string => {
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
