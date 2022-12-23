const pactum = require('pactum');
const { Given, When, Then, Before, After } = require('@cucumber/cucumber');

let searchedRecord;
let specDataRead = pactum.spec();

const baseUrl = 'http://localhost:3333/data/registry1/version1/read';
const header = {
  key: 'Information-Mediator-Client',
  value: 'INSTANCE/CLASS/MEMBER/SUBSYSTEM',
};

Before(() => {
  specDataRead = pactum.spec();
});

// Scenario: The user receives one searched record from the Digital Registries database
Given(
  'The user wants to search for one record "John Benz" in the Digital Registries database',
  () => {
    return (searchedRecord = 'John Benz');
  }
);

Given('The searched record exists in the database', () => {
  return 'The searched record exists in the database';
});

When(
  'The user triggers an action to search record "John Benz" in the database',
  () => {
    specDataRead
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

//   Scenario: The user does not receive searched record from the Digital Registries database
Given(
  'The user wants to search for one record "David Belt" in the Digital Registries database',
  () => {
    return (searchedRecord = 'David Belt');
  }
);

Given('The searched record does not exist in the database', () => {
  return 'The searched record does not exist in the database';
});

When(
  'The user triggers an action to search record "David Belt" in the database',
  () => {
    specDataRead
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
  'The user receives a message that there is no searched record in the database',
  async () => {
    await specDataRead.toss();
    specDataRead.response().should.have.status(404);
  }
);

//   Scenario: The user is not able to receive one searched record from the Digital Registries database because of an invalid request
Given(
  'The user wants to search for one record "Ali Benz" in the Digital Registries database',
  () => {
    return (searchedRecord = 'Ali Benz');
  }
);
When('The user triggers an action to search a record in the database', () => {
  specDataRead.post(`${baseUrl}`).withBody({
    query: {
      content: {
        FirstName: searchedRecord,
      },
    },
  });
});

Then('Operation results for {string} is an error', async string => {
  await specDataRead.toss();
  specDataRead.response().should.have.status(400);
});

After(() => {
  specDataRead.end();
});
