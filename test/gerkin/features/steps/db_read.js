const pactum = require('pactum');
const { Given, When, Then, Before, After } = require('@cucumber/cucumber');
const { header, localhost } = require('./helpers/helpers');

let specDataRead;

const baseUrl = `${localhost}database/{id}`;
  
Before(() => {
  specDataRead = pactum.spec();
});

// Background: The user wants to retrieve the Digital Registries database information with schema versions
Given(
  'The user wants to retrieve the Digital Registries database information with schema versions', () => {
  return 'The user wants to retrieve the Digital Registries database information with schema versions';
  }
);

// Scenario: The user successfully receives one Digital Registries database information with schema versions
When(
  'The user triggers an action with a valid payload to display one database schema versions', () => {
    specDataRead
      .get(`${baseUrl}`)
      .withHeaders(`${header.key}`, `${header.value}`)
      .withPathParams('id', 353);
  }
);

Then('The user received one database information with schema versions', async () => {
  await specDataRead.toss();
  specDataRead.response().should.have.status(200);
});

// Scenario: The user is not able to receive any Digital Registries database information with schema versions bacause of not providing route param
When(
  'The user triggers an action without a route param to display one database schema versions',
  () => {
    specDataRead
      .get(`${baseUrl}`)
      .withHeaders(`${header.key}`, `${header.value}`);
  }
);

Then('The operation to receive any Digital Registries database information with schema versions results with no route param error', async () => {
  await specDataRead.toss();
  specDataRead.response().should.have.status(400);
});


// Scenario: The user is not able to receive any Digital Registries database information with schema versions because of empty value in the header
When(
  'The user triggers an action with an invalid payload to display one database schema versions', () => {
  specDataRead
    .get(`${baseUrl}`);
  }
);
  
Then('The operation to receive any Digital Registries database information with schema versions results with wrong mediator error', async () => {
  await specDataRead.toss();
  specDataRead.response().should.have.status(400);
});

// Scenario: The user is not able to receive any Digital Registries database information with schema versions because of not including header
When(
    'The user triggers an action without a payload to display one database schema versions', () => {
    specDataRead
      .get(`${baseUrl}`);
    }
  );
    
  Then('The operation to receive any Digital Registries database information with schema versions results with no mediator error', async () => {
    await specDataRead.toss();
    specDataRead.response().should.have.status(400);
});

After(() => {
  specDataRead.end();
});
