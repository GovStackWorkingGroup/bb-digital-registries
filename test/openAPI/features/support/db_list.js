const chai = require('chai');
const pactum = require('pactum');
const { Given, When, Then, Before, After } = require('@cucumber/cucumber');
const {
  header,
  localhost,
  databasesEndpoint,
  defaultExpectedResponseTime,
  contentTypeHeader,
  databasesResponseSchema,
} = require('./helpers/helpers');

chai.use(require('chai-json-schema'));

let specDatabaseList;

const baseUrl = localhost + databasesEndpoint;
const endpointTag = { tags: `@endpoint=/${databasesEndpoint}` };

Before(endpointTag, () => {
  specDatabaseList = pactum.spec();
});

// Scenario: The user receives information about databases
Given(
  'User wants to view information about all databases',
  () => 'User wants to view information about all databases'
);

When(
  'User sends GET request with given Information-Mediator-Client header',
  () => specDatabaseList.get(baseUrl).withHeaders(header.key, header.value)
);

Then(
  'User receives a response from the \\/databases endpoint',
  async () => await specDatabaseList.toss()
);

Then(
  'The \\/databases endpoint response should be returned in a timely manner 15000ms',
  async () =>
    specDatabaseList
      .response()
      .to.have.responseTimeLessThan(defaultExpectedResponseTime)
);

Then('The \\/databases endpoint response should have status 200', async () =>
  specDatabaseList.response().to.have.status(200)
);

Then(
  'The \\/databases endpoint response should have content-type: application\\/json header',
  async () =>
    specDatabaseList
      .response()
      .should.have.header(contentTypeHeader.key, contentTypeHeader.value)
);

Then('The \\/databases endpoint response should match json schema', async () =>
  chai
    .expect(specDatabaseList._response.json)
    .to.be.jsonSchema(databasesResponseSchema)
);

After(endpointTag, () => {
  specDatabaseList.end();
});
