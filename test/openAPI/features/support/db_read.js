const chai = require('chai');
const pactum = require('pactum');
const { Given, When, Then, Before, After } = require('@cucumber/cucumber');
const {
  localhost,
  databaseReadEndpoint,
  header,
  contentTypeHeader,
  databaseReadResponseSchema,
  defaultExpectedResponseTime,
} = require('./helpers/helpers');

chai.use(require('chai-json-schema'));

let specDatabaseRead;

const baseUrl = localhost + databaseReadEndpoint;
const endpointTag = { tags: `@endpoint=/${databaseReadEndpoint}` };

Before(endpointTag, () => {
  specDatabaseRead = pactum.spec();
});

// Scenario: User successfully obtains Digital Registries database information with schema version smoke type test
Given(
  'User wants to get the database information of Digital Registries with schema version',
  () =>
    'User wants to get the database information of Digital Registries with schema version'
);

When(
  'User sends GET request with given Information-Mediator-Client header and {string} as id',
  id =>
    specDatabaseRead
      .get(baseUrl)
      .withHeaders(header.key, header.value)
      .withPathParams('id', id)
);

Then(
  'User receives a response from the GET \\/database\\/id endpoint',
  async () => await specDatabaseRead.toss()
);

Then(
  'The GET \\/database\\/id endpoint response should be returned in a timely manner 15000ms',
  () =>
    specDatabaseRead
      .response()
      .to.have.responseTimeLessThan(defaultExpectedResponseTime)
);

Then('The GET \\/database\\/id endpoint response should have status 200', () =>
  specDatabaseRead.response().to.have.status(200)
);

Then(
  'The GET \\/database\\/id endpoint response should have content-type: application\\/json header',
  () =>
    specDatabaseRead
      .response()
      .should.have.header(contentTypeHeader.key, contentTypeHeader.value)
);

Then(
  'The GET \\/database\\/id endpoint response should match json schema',
  () =>
    chai
      .expect(specDatabaseRead._response.json)
      .to.be.jsonSchema(databaseReadResponseSchema)
);

//Scenario Outline: User successfully obtains Digital Registries database information with schema version

// "When", "Then" already written above

After(endpointTag, () => {
  specDatabaseRead.end();
});
