const chai = require('chai');
const { spec } = require('pactum');
const { Given, When, Then, Before, After } = require('@cucumber/cucumber');
const {
  localhost,
  header,
  contentTypeHeader,
  defaultExpectedResponseTime,
  databaseDeleteEndpoint,
  databaseDeleteResponseSchema,
} = require('./helpers/helpers');

chai.use(require('chai-json-schema'));

let specDatabaseDelete;

const baseUrl = localhost + databaseDeleteEndpoint;
const endpointTag = { tags: `@endpoint=/${databaseDeleteEndpoint}` };

Before(endpointTag, () => {
  specDatabaseDelete = spec();
});

// Scenario: User successfully deletes the Digital Registries schema smoke type test
Given(
  'User wants to delete the Digital Registries schema',
  () => 'User wants to delete the Digital Registries schema'
);

When(
  'The DELETE request with given Information-Mediator-Client header and {string} as id is sent',
  id =>
    specDatabaseDelete
      .delete(baseUrl)
      .withHeaders(header.key, header.value)
      .withPathParams('id', Number.parseInt(id))
);

Then(
  'User receives a response from the DELETE \\/database\\/id endpoint',
  async () => await specDatabaseDelete.toss()
);

Then(
  'The DELETE \\/database\\/id endpoint response should be returned in a timely manner 15000ms',
  () =>
    specDatabaseDelete
      .response()
      .to.have.responseTimeLessThan(defaultExpectedResponseTime)
);

Then(
  'The DELETE \\/database\\/id endpoint response should have status 200',
  () => specDatabaseDelete.response().should.have.status(200)
);

Then(
  'The DELETE \\/database\\/id endpoint response should have content-type: {string} as ContentType',
  (ContentType) =>
    specDatabaseDelete
      .response()
      .should.have.header(contentTypeHeader.key)
      .and.include(ContentType)
);

Then(
  'The DELETE \\/database\\/id endpoint response should match json schema',
  () =>
    chai
      .expect(specDatabaseDelete._response.json)
      .to.be.jsonSchema(databaseDeleteResponseSchema)
);

// Scenario Outline: User successfully deletes the Digital Registries schema
// others Given, When, Then for this scenario are written in the aforementioned example

Then(
  'The DELETE \\/database\\/id endpoint response should have body {string}',
  responseBody => specDatabaseDelete.response().to.have.body(responseBody)
);

After(endpointTag, () => {
  specDatabaseDelete.end();
});
