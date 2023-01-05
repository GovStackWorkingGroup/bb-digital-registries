const pactum = require('pactum');
const { Given, When, Then, Before, After } = require('@cucumber/cucumber');
const { header, localhost } = require('./helpers/helpers');

let userActualVariables = {};
let userUpdateVariables = {};
let specDataUpdate = pactum.spec();

const baseUrl = `${localhost}data/registry1/version1/update`;

Before(() => {
  specDataUpdate = pactum.spec();
});

// Scenario: The user successfully updates the record in the Digital Registries database
Given(
  'The user wants to update a record "John Helmut Smith Carry" in the Digital Registries database',
  () => {
    userActualVariables = {
      ID: 'EE378627348834',
      FirstName: 'John Helmut',
      LastName: 'Smith Carry',
      BirthCertificateID: 'RR-1234567889',
    };

    userUpdateVariables = {
      ID: 'EE378627348834',
      FirstName: 'John Helmut',
      LastName: 'Lasocki',
      BirthCertificateID: 'RR-1234567889',
    };

    return userActualVariables, userUpdateVariables;
  }
);

Given('The record "John Helmut Smith Carry" exists in the database', () => {
  return 'The record "John Helmut Smith Carry" exists in the database ';
});

When(
  'The user triggers an action to update the record "John Helmut Smith Carry" in the database',
  () => {
    specDataUpdate
      .put(`${baseUrl}`)
      .withHeaders(`${header.key}`, `${header.value}`)
      .withBody({
        query: {
          content: userActualVariables,
        },
        write: {
          content: userUpdateVariables,
        },
      });
  }
);

Then(
  'Operation to update the record "John Helmut Smith Carry" finishes successfully',
  async () => {
    await specDataUpdate.toss();
    specDataUpdate.response().should.have.status(200);
    specDataUpdate.response().should.have.jsonLike({
      content: userUpdateVariables,
    });
  }
);

// Scenario: The user is not able to udpate the record, because the record does not exist in the Digital Registries database
Given(
  'The user wants to update the record "Anna Smith" in the Digital Registries database',
  () => {
    userActualVariables = {
      ID: 'EE378627348855',
      FirstName: 'Anna',
      LastName: 'Smith',
      BirthCertificateID: 'RR-1234567880',
    };

    userUpdateVariables = {
      ID: 'EE378627348855',
      FirstName: 'Jasmine',
      LastName: 'Lasocki',
      BirthCertificateID: 'RR-1234567880',
    };
  }
);

Given('The record "Anna Smith" does not exist in the database', () => {
  return 'The record "Anna Smith" does not exist in the database';
});

When(
  'The user triggers an action to update the record "Anna Smith" in the database',
  () => {
    specDataUpdate
      .put(`${baseUrl}`)
      .withHeaders(`${header.key}`, `${header.value}`)
      .withBody({
        query: {
          content: userActualVariables,
        },
        write: {
          content: userUpdateVariables,
        },
      });
  }
);

Then('Operation results to update "Anna Smith" is an error', async () => {
  await specDataUpdate.toss();
  specDataUpdate.response().should.have.status(404);
  specDataUpdate
    .response()
    .should.have.body('{\n  "Record matching query not found."\n}');
});

// Scenario: The user is not able to update a record in the Digital Registries database because of an invalid request
Given(
  'The user wants to update a record in the Digital Registries database',
  () => {
    userActualVariables = {
      ID: 'EE378627348833',
      FirstName: 'John Helmut',
      LastName: 'Smith',
      BirthCertificateID: 'RR-1234567880',
    };
  }
);

When(
  'The user triggers an action to update a new record in the database',
  () => {
    specDataUpdate
      .put(`${baseUrl}`)
      .withHeaders(`${header.key}`, `${header.value}`);
  }
);

Then('Operation results to update a record is an error', async () => {
  await specDataUpdate.toss();
  specDataUpdate.response().should.have.status(400);
  specDataUpdate.response().should.have.body('{\n  "Query not provided."\n}');
});

After(() => {
  specDataUpdate.end();
});
