const pactum = require('pactum');
const { Given, When, Then, Before, After } = require('@cucumber/cucumber');
const { header, localhost } = require('./helpers/helpers');

let newUserVariables;
let specDataCreate;

const baseUrl = registryname =>
  `${localhost}data/${registryname}/version1/create`;

Before(() => {
  specDataCreate = pactum.spec();
});

// Scenario: The user successfully creates a record in the Digital Registries database
Given(
  'The user wants to create a new record in the Digital Registries database',
  () =>
    (newUserVariables = {
      ID: 'EE378627348834',
      FirstName: 'John',
      LastName: 'Smith',
      BirthCertificateID: 'RR-1234567889',
    })
);

When(
  'The user sends a valid request to create a new record in the database',
  () => {
    specDataCreate
      .post(`${baseUrl('registry1')}`)
      .withHeaders(`${header.key}`, `${header.value}`)
      .withBody({
        write: {
          content: newUserVariables,
        },
      });
  }
);

Then('The process to create a new record completes successfully', async () => {
  await specDataCreate.toss();
  specDataCreate.response().should.have.status(200);
  specDataCreate.response().should.have.jsonLike({
    content: newUserVariables,
  });
});

// Scenario: The user is unable to create a record in the database that does not exist
Given(
  'The user wants to create a new record in the Digital Registries database that does not exist',
  () =>
    (newUserVariables = {
      ID: 'EE378627342345',
      FirstName: 'Anna',
      LastName: 'Stock',
      BirthCertificateID: 'RR-1234567999',
    })
);

When(
  'The user sends a valid request to create a new record in the database that does not exist',
  () => {
    specDataCreate
      .post(`${baseUrl('registry2')}`)
      .withHeaders(`${header.key}`, `${header.value}`)
      .withBody({
        write: {
          content: newUserVariables,
        },
      });
  }
);

Then(
  'The result of the operation is an error because the database does not exist',
  async () => {
    await specDataCreate.toss();
    specDataCreate.response().should.have.status(404);
    specDataCreate
      .response()
      .should.have.body(
        '{\n  "Invalid payload, registry name does not exist"\n}\n'
      );
  }
);

// Scenario: The user is unable to create a record in the Digital Registries database because of an invalid request
// "Given" already written in line 16-25

When(
  'The user sends an invalid request to create a new record in the database',
  () => {
    specDataCreate
      .post(`${baseUrl('registry1')}`)
      .withHeaders(`${header.key}`, `${header.value}`)
      .withBody({});
  }
);

Then(
  'The result of the operation is an error due to an invalid request',
  async () => {
    await specDataCreate.toss();
    specDataCreate.response().should.have.status(400);
    specDataCreate
      .response()
      .should.have.body(
        '{\n  "Invalid payload, write.content not provided"\n}'
      );
  }
);

After(() => {
  specDataCreate.end();
});
