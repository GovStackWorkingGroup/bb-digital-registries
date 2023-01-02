const pactum = require('pactum');
const { Given, When, Then, Before, After } = require('@cucumber/cucumber');
const { header, localhost } = require('./helpers/helpers');

let userVariables = {};
let specDataUpdateEntries;

const baseUrl = `${localhost}data/registry1/version1/update-entries`;

Before(() => {
  specDataUpdateEntries = pactum.spec();
});

// Scenario: The user successfully updates two existing records in the Digital Registries database
Given(
  'The user wants to update multiple records with first name "Alfie" in the Digital Registries database',
  () => {
    userVariables = {
      ID: 'EE378627348834',
      FirstName: 'Alfie',
      LastName: 'Grande',
      BirthCertificateID: 'RR-1234567889',
    };

    return userVariables;
  }
);

Given('The records with first name "Alfie" exist in the database', () => {
  return 'The records with first name "Alfie" exist in the database';
});

When(
  'The user triggers an action to update records with first name "Alfie" in the database',
  () => {
    specDataUpdateEntries
      .put(`${baseUrl}`)
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
  'Operation to update records with first name "Alfie" finishes successfully',
  async () => {
    await specDataUpdateEntries.toss();
    specDataUpdateEntries.response().should.have.status(200);
  }
);

// Scenario: The user is not able to update two records which do not exist in the Digital Registries database
Given(
  'The user wants to update multiple records with first name "Jerry" in the Digital Registries database',
  () => {
    userVariables = {
      ID: 'EE378627348834',
      FirstName: 'Jerry',
      LastName: 'Blake',
      BirthCertificateID: 'RR-1234567889',
    };

    return userVariables;
  }
);

Given(
  'The records with first name "Jerry" do not exist in the database',
  () => {
    return 'The records with first name "Jerry" do not exist in the database';
  }
);

When(
  'The user triggers an action to update records with first name "Jerry" in the database',
  () => {
    specDataUpdateEntries
      .put(`${baseUrl}`)
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
  `The result of an operation to update records with the first name 'Jerry' returns an error`,
  async () => {
    await specDataUpdateEntries.toss();
    specDataUpdateEntries.response().should.have.status(404);
    specDataUpdateEntries
      .response()
      .should.have.body('{\n  "Record matching query not found."\n}');
  }
);

// Scenario: The user is not able to update two records in the Digital Registries database because of an invalid request
Given(
  'The user wants to update multiple records with name "Jasmine" in the Digital Registries database',
  () => {
    userVariables = {
      ID: 'EE378627348834',
      FirstName: 'Jasmine',
      LastName: 'Sun',
      BirthCertificateID: 'RR-1234567889',
    };

    return userVariables;
  }
);

When(
  'The user triggers an action to update records with name "Jasmine" in the database',
  () => {
    specDataUpdateEntries
      .put(`${baseUrl}`)
      .withHeaders(`${header.key}`, `${header.value}`)
      .withBody({
        query: {
          content: userVariables,
        },
      });
  }
);

Then(
  `The result of an operation to update records with the first name "Jasmine" returns an error`,
  async () => {
    await specDataUpdateEntries.toss();
    specDataUpdateEntries.response().should.have.status(400);
    specDataUpdateEntries
      .response()
      .should.have.body('{\n  "Query not provided."\n}');
  }
);
// Scenario: The user is not able to update two records in the Digital Registries database because of a missing users data
Given(
  `The user wants to update multiple records with name "Joanna" in the Digital Registries database`,
  () => {
    userVariables = {
      ID: 'EE378623348834',
      FirstName: 'Joanna',
      LastName: 'Moon',
      BirthCertificateID: null,
    };

    return userVariables;
  }
);

When(
  `The user triggers an action to update records with name "Joanna" in the database`,
  () => {
    specDataUpdateEntries
      .put(`${baseUrl}`)
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
  `The result of an operation to update records with the first name "Joanna" returns an error`,
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
