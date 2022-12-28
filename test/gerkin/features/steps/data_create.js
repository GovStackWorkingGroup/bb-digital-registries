const pactum = require('pactum');
const { Given, When, Then, Before, After } = require('@cucumber/cucumber');
const { header, localhost } = require('./helpers/helpers');

let newUser = {
  ID: '',
  FirstName: '',
  LastName: '',
  BirthCertificateID: '',
};
let specDataCreate = pactum.spec();

const baseUrl = registryname =>
  `${localhost}data/${registryname}/version1/create`;

Before(() => {
  specDataCreate = pactum.spec();
});

// Scenario: The user successfully creates the record "John Smith" in the Digital Registries database
Given(
  'The user wants to create a new record "John Smith" in the Digital Registries database',
  () => {
    const newUser = {
      ID: 'EE378627348834',
      FirstName: 'John',
      LastName: 'Smith',
      BirthCertificateID: 'RR-1234567889',
    };

    return newUser;
  }
);

When(
  'The user triggers an action to create a new record "John Smith" in the database',
  () => {
    specDataCreate
      .post(`${baseUrl('registry1')}`)
      .withHeaders(`${header.key}`, `${header.value}`)
      .withBody({
        write: {
          content: newUser,
        },
      });
  }
);

Then(
  'Operation finishes successfully for create user "John Smith"',
  async () => {
    await specDataCreate.toss();
    specDataCreate.response().should.have.status(200);
    specDataCreate.response().should.have.jsonLike({
      content: newUser,
    });
  }
);

// Scenario: The user is not able to create a record in the database which not exist
Given(
  'The user wants to create a new record "Anna Stock" in the Digital Registries database',
  () => {
    const newUser = {
      ID: 'EE378627342345',
      FirstName: 'Anna',
      LastName: 'Stock',
      BirthCertificateID: 'RR-1234567999',
    };

    return newUser;
  }
);

Given('The database does not exist', () => {
  return 'The database does not exist';
});

When(
  'The user triggers an action to create a new record "Anna Stock" in the database',
  () => {
    specDataCreate
      .post(`${baseUrl('registry2')}`)
      .withHeaders(`${header.key}`, `${header.value}`)
      .withBody({
        write: {
          content: newUser,
        },
      });
  }
);

Then('Operation results in an error for create "Anna Stock"', async () => {
  await specDataCreate.toss();
  specDataCreate.response().should.have.status(400);
  specDataCreate
    .response()
    .should.have.jsonLike('Invalid payload, registry name not exist');
});

// Scenario: The user is not able to create a record in the Digital Registries database
Given(
  'The user wants to create a new record "Emma Watson" in the Digital Registries database',
  () => {
    const newUser = {
      ID: 'EE378627342345',
      FirstName: 'Emma',
      LastName: 'Watson',
      BirthCertificateID: 'RR-1234567999',
    };

    return newUser;
  }
);

When(
  'The user triggers an action to create a new record "Emma Watson" in the database',
  () => {
    specDataCreate
      .post(`${baseUrl('registry1')}`)
      .withHeaders(`${header.key}`, `${header.value}`)
      .withBody({});
  }
);

Then('Operation results in an error for create "Emma Watson"', async () => {
  await specDataCreate.toss();
  specDataCreate.response().should.have.status(400);
});

After(() => {
  specDataCreate.end();
});
