const chai = require('chai');
const pactum = require('pactum');
const { Given, When, Then, Before, After } = require('@cucumber/cucumber');
const {
  localhost,
  databaseModifyEndpoint,
  header,
  databaseModifyBody,
  defaultExpectedResponseTime,
  acceptHeader,
  databaseModifyResponseSchema,
} = require('./helpers/helpers');

chai.use(require('chai-json-schema'));

let specDatabaseModify;

const baseUrl = localhost + databaseModifyEndpoint;
const endpointTag = { tags: `@endpoint=/${databaseModifyEndpoint}` };

Before(endpointTag, () => {
  specDatabaseModify = pactum.spec();
});

// Scenario: The user successfully creates the Digital Registries database schema smoke test type
Given(
  'User wants to create or modify the Digital Registries database schema',
  () => 'User wants to create or modify the Digital Registries database schema'
);

When(
  'User sends POST request with given Information-Mediator-Client header',
  () => specDatabaseModify.post(baseUrl).withHeaders(header.key, header.value)
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
  'The \\/database\\/modify endpoint response should have content-type: application\\/json header',
  () =>
    specDatabaseModify
      .response()
      .should.have.header(acceptHeader.key, acceptHeader.value)
);

Then(
  'The \\/database\\/modify endpoint response should match json schema',
  () =>
    chai
      .expect(specDatabaseModify._response.json)
      .to.be.jsonSchema(databaseModifyResponseSchema)
);

// Scenario Outline: The user successfully creates the Digital Registries database schema

// "Given" already written above

When(
  'User sends POST request with given Information-Mediator-Client header and body',
  () =>
    specDatabaseModify
      .post(baseUrl)
      .withHeaders(header.key, header.value)
      .withBody(databaseModifyBody)
);

// "Then" already written above

After(endpointTag, () => {
  specDatabaseModify.end();
});
