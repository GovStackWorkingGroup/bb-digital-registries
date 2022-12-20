const { spec, expect, stores } = require('pactum');
const { When, Then, Given, After } = require('@cucumber/cucumber');

const firstSearchedName = 'John';
const secondSearchedName = 'Adrien';
const baseUrl = 'http://localhost:3333/data/registry1/version1';
const header = {
  key: 'Information-Mediator-Client',
  value: 'INSTANCE/CLASS/MEMBER/SUBSYSTEM',
};

// scenario 1
Given('The user wants to search for "John Helmut" in the database', () => {
  return firstSearchedName;
});

Given('The searched value exists in several records in the database', () => {
  return 'Searched value does exist in the database';
});

When(
  'The user triggers an action to search "John Helmut" in the database',
  async () => {
    await spec()
      .get(`${baseUrl}1?filter=FirstName&search=${firstSearchedName}`)
      .withHeaders(`${header.key}`, `${header.value}`)
      .expectStatus(200);
  }
);

When('The request with a valid payload is sent', () => {
  return true;
});

Then(
  'The user receives a list with all records including "John Helmut"',
  async () => {
    await spec()
      .get(`${baseUrl}?filter=FirstName&search=${firstSearchedName}`)
      .withHeaders(`${header.key}`, `${header.value}`)
      .expectStatus(200)
      .expectJsonLike({
        results: [
          {
            FirstName: 'John',
          },
        ],
      });
  }
);

// scenario 2
Given('The user wants to search for "Adrien" in the database', () => {
  return secondSearchedName;
});

Given('The searched value does not exist in any record in the database', () => {
  return 'Searched value does not exist in the database';
});

When(
  'The user triggers an action to search "Adrien" in the database',
  async () => {
    await spec()
      .get(`${baseUrl}?filter=FirstName&search=${secondSearchedName}`)
      .withHeaders(`${header.key}`, `${header.value}`)
      .expectStatus(200);
  }
);

Then(
  'The user receives an empty list because there is no record including "Adrien" in the database',
  async () => {
    await spec()
      .get(`${baseUrl}?filter=FirstName&search=${secondSearchedName}`)
      .withHeaders(`${header.key}`, `${header.value}`)
      .expectStatus(200)
      .expectJsonLike({
        results: [],
      });
  }
);

// scenario 3
When('The request with an invalid payload is sent', async () => {
  await spec()
    .get(`${baseUrl}?filter=FirstName&search=${firstSearchedName}`)
    .expectStatus(400);
});

Then('Operation results in an error', () => {
  return 'Error';
});

After(scenario => {
  console.log(scenario.result.status);
});
