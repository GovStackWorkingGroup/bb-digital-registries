const chai = require('chai');
const pactum = require('pactum');
const { Given, When, Then, Before, After } = require('@cucumber/cucumber');
const {
  localhost,
  databaseModifyEndpoint,
  header,
  databaseModifyBody,
  defaultExpectedResponseTime,
  databaseModifyResponseSchema,
  contentTypeHeader,
} = require('./helpers/helpers');

chai.use(require('chai-json-schema'));

let specDatabaseModify;

const baseUrl = localhost + databaseModifyEndpoint;
const endpointTag = { tags: `@endpoint=/${databaseModifyEndpoint}` };

Before(endpointTag, () => {
  specDatabaseModify = pactum.spec();
});

// Scenario: The user successfully creates a database schema
Given(
  'User wants to create or modify the database schema',
  () => 'User wants to create or modify the database schema'
);

When(
  'User sends POST request with given Information-Mediator-Client header and body',
  () =>
    specDatabaseModify
      .post(baseUrl)
      .withHeaders(header.key, header.value)
      .withBody(databaseModifyBody)
);

Then(
  'User receives a response from the \\/database\\/modify endpoint',
  async () => await specDatabaseModify.toss()
);

Then(
  'The \\/database\\/modify endpoint response should be returned in a timely manner 15000ms',
  () =>
    specDatabaseModify
      .response()
      .to.have.responseTimeLessThan(defaultExpectedResponseTime)
);

Then('The \\/database\\/modify endpoint response should have status 200', () =>
  specDatabaseModify.response().to.have.status(200)
);

Then(
  'The \\/database\\/modify endpoint response should have content-type: "application/json" as ContentType',
  (ContentType) =>
    specDatabaseModify
      .response()
      .should.have.header(contentTypeHeader.key)
      .and.include(ContentType)
);

Then(
  'The \\/database\\/modify endpoint response should match json schema',
  () =>
    chai
      .expect(specDatabaseModify._response.json)
      .to.be.jsonSchema(databaseModifyResponseSchema)
);

After(endpointTag, () => {
  specDatabaseModify.end();
});
