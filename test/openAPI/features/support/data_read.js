const chai = require('chai');
const { spec } = require('pactum');
const { Given, When, Then, Before, After } = require('@cucumber/cucumber');
const {
  header,
  localhost,
  dataReadEndpoint,
  defaultExpectedResponseTime,
  dataReadResponseSchema,
  contentTypeHeader,
} = require('./helpers/helpers');

let specDataRead;

const baseUrl = localhost + dataReadEndpoint;
const endpointTag = { tags: `@endpoint=/${dataReadEndpoint}` };

Before(endpointTag, () => {
  specDataRead = spec();
});

// Scenario: User obtains a searched record from the database smoke type test
Given(
  'The user wants to search for a record in the database',
  () => 'The user wants to search for a record in the database'
);

When(
  'User sends POST \\/data\\/\\{registryname}\\/\\{versionnumber}\\/read request with given Information-Mediator-Client header, {string} as registryname, {string} as versionnumber, {string} as FirstName',
  (registryName, versionNumber, firstName) =>
    specDataRead
      .post(baseUrl)
      .withHeaders(header.key, header.value)
      .withPathParams({
        registryname: registryName,
        versionnumber: versionNumber,
      })
      .withJson({
        query: {
          content: {
            FirstName: firstName,
          },
        },
      })
);

Then(
  'User receives a response from the \\/data\\/\\{registryname}\\/\\{versionnumber}\\/read endpoint',
  async () => await specDataRead.toss()
);

Then(
  'The \\/data\\/\\{registryname}\\/\\{versionnumber}\\/read endpoint response should be returned in a timely manner 15000ms',
  () =>
    specDataRead
      .response()
      .to.have.responseTimeLessThan(defaultExpectedResponseTime)
);

Then(
  'The \\/data\\/\\{registryname}\\/\\{versionnumber}\\/read endpoint response should have status 200',
  () => specDataRead.response().should.have.status(200)
);

Then(
  'The \\/data\\/\\{registryname}\\/\\{versionnumber}\\/read endpoint response should have content-type: application\\/json header',
  () =>
    specDataRead
      .response()
      .should.have.header(contentTypeHeader.key, contentTypeHeader.value)
);

Then(
  'The \\/data\\/\\{registryname}\\/\\{versionnumber}\\/read endpoint response should match json schema',
  () =>
    chai
      .expect(specDataRead._response.json)
      .to.be.jsonSchema(dataReadResponseSchema)
);

// Scenario Outline: User obtains a searched record from the database
When(
  'User sends POST \\/data\\/\\{registryname}\\/\\{versionnumber}\\/read request with given Information-Mediator-Client header, {string} as registryname, {string} as versionnumber, {string} as {string}',
  (registryName, versionNumber, parameterValue, bodyParameter) =>
    specDataRead
      .post(baseUrl)
      .withHeaders(header.key, header.value)
      .withPathParams({
        registryname: registryName,
        versionnumber: versionNumber,
      })
      .withJson({
        query: {
          content: {
            [bodyParameter]: parameterValue,
          },
        },
      })
);

After(endpointTag, () => {
  specDataRead.end();
});
