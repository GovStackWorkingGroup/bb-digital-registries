const chai = require('chai');
const pactum = require('pactum');
const { Given, When, Then, Before, After } = require('@cucumber/cucumber');
const {
  header,
  localhost,
  defaultExpectedResponseTime,
  contentTypeHeader,
  dataMyPersonalDataUsageEndpoint,
  dataMyPersonalDataUsageResponseSchema,
} = require('./helpers/helpers');

chai.use(require('chai-json-schema'));

let specDataMyPersonalDataUsage;
let returnedReaderId;
let returnedReferanceArray;

const baseUrl = localhost + dataMyPersonalDataUsageEndpoint;
const endpointTag = { tags: `@endpoint=/${dataMyPersonalDataUsageEndpoint}` };

Before(endpointTag, () => {
  specDataMyPersonalDataUsage = pactum.spec();
});

// Scenario: The user gets a list of all records that have read their personal data smoke test type
Given(
  'The user wants to check who has read his personal data',
  () => 'The user wants to check who has read his personal data'
);

When(
  'User sends GET \\/data\\/MyPersonalDataUsage\\/1.0 request with given Information-Mediator-Client header, {string} as userID and {string} as DatabaseID',
  (userId, databaseId) => {
    specDataMyPersonalDataUsage
      .get(baseUrl)
      .withHeaders(header.key, header.value)
      .withQueryParams('userID', userId)
      .withQueryParams('DatabaseID', databaseId);
  }
);

Then(
  'User receives a response from the \\/data\\/MyPersonalDataUsage\\/1.0 endpoint',
  async () => await specDataMyPersonalDataUsage.toss()
);

Then(
  'The \\/data\\/MyPersonalDataUsage\\/1.0 endpoint response should be returned in a timely manner 15000ms',
  () =>
    specDataMyPersonalDataUsage
      .response()
      .to.have.responseTimeLessThan(defaultExpectedResponseTime)
);

Then(
  'The \\/data\\/MyPersonalDataUsage\\/1.0 endpoint response should have status 200',
  () => specDataMyPersonalDataUsage.response().should.have.status(200)
);

Then(
  'The \\/data\\/MyPersonalDataUsage\\/1.0 endpoint response should have content-type: application\\/json header',
  () =>
    specDataMyPersonalDataUsage
      .response()
      .should.have.header(contentTypeHeader.key, contentTypeHeader.value)
);

Then(
  'The \\/data\\/MyPersonalDataUsage\\/1.0 endpoint response should match json schema',
  () =>
    chai
      .expect(specDataMyPersonalDataUsage._response.json)
      .to.be.jsonSchema(dataMyPersonalDataUsageResponseSchema)
);

//Scenario Outline: The user gets a list of all records that have read their personal data
// Others Given, When and Then are written in the aforementioned example
Then(
  'The \\/data\\/MyPersonalDataUsage\\/1.0 response ReaderID field should be {string}',
  userId => {
    returnedReaderId = specDataMyPersonalDataUsage._response.json
      .map(object => object.ReaderID)
      .toString();
    chai.expect(returnedReaderId).to.be.equals(userId);
  }
);

// Scenario: The user is not able to gets a list of all records that have read their personal data because of the invalid userID parameter
// Others Given, When and Then are written in the aforementioned example
When(
  'User sends GET \\/data\\/MyPersonalDataUsage\\/1.0 request with given Information-Mediator-Client header, {string} as invalid userID and {string} as DatabaseID',
  (userId, databaseId) => {
    specDataMyPersonalDataUsage
      .get(baseUrl)
      .withHeaders(header.key, header.value)
      .withQueryParams('userID', userId)
      .withQueryParams('DatabaseID', databaseId);
  }
);
Then(
  'The \\/data\\/MyPersonalDataUsage\\/1.0 endpoint response should have status 400',
  () => specDataMyPersonalDataUsage.response().should.have.status(400)
);

// Scenario: The user is not able to gets a list of all records that have read their personal data because of the invalid DatabaseID parameter
// Others Given, When and Then are written in the aforementioned example
When(
  'User sends GET \\/data\\/MyPersonalDataUsage\\/1.0 request with given Information-Mediator-Client header, {string} as userID and {string} as invalid DatabaseID',
  (userId, databaseId) => {
    specDataMyPersonalDataUsage
      .get(baseUrl)
      .withHeaders(header.key, header.value)
      .withQueryParams('userID', userId)
      .withQueryParams('DatabaseID', databaseId);
  }
);

After(endpointTag, () => {
  specDataMyPersonalDataUsage.end();
});
