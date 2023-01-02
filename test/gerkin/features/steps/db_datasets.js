const pactum = require('pactum');
const { Given, When, Then, Before, After } = require('@cucumber/cucumber');
const { header, localhost } = require('./helpers/helpers');

let specDataRead;

const baseUrl = `${localhost}databases`;

Before(() => {
  specDataRead = pactum.spec();
});

// Background: The user wants to display information about all Digital Registries databases
Given(
  'The user wants to display information about all Digital Registries databases', () => {
  return 'The user wants to display information about all Digital Registries databases';
  }
);

// Scenario: The user receives information about Digital Registries databases
When(
  'The user triggers an action with a valid payload to display information about Digital Registries databases', () => {
    specDataRead
      .get(`${baseUrl}`)
      .withHeaders(`${header.key}`, `${header.value}`);
  }
);

Then('The user received a list of Digital Registries databases', async () => {
  await specDataRead.toss();
  specDataRead.response().should.have.status(200);
});

// Scenario: The user is not able to receive information for Digital Registries databases because of empty value in the header
When(
  'The user triggers an action with an invalid payload to display information about Digital Registries databases',
  () => {
    specDataRead
      .get(`${baseUrl}`)
      .withHeaders(`${header.key}`, '');
  }
);

Then('The operation to receive information for Digital Registries databases results with wrong mediator error', async () => {
  await specDataRead.toss();
  specDataRead.response().should.have.status(400);
});


// Scenario: The user is not able to receive information for Digital Registries databases because of not including header
When(
  'The user triggers an action without a payload to display information about Digital Registries databases', () => {
  specDataRead
    .get(`${baseUrl}`);
  }
);
  
Then('The operation to receive information for Digital Registries databases results with no mediator error', async () => {
  await specDataRead.toss();
  specDataRead.response().should.have.status(400);
});

After(() => {
  specDataRead.end();
});
