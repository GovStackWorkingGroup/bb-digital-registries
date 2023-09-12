const chai = require('chai');
const pactum = require('pactum');
const { Given, When, Then, Before, After } = require('@cucumber/cucumber');
const {
  header,
  localhost,
  dataCreateEndpoint,
  dataCreateRequestBody,
  defaultExpectedResponseTime,
  contentTypeHeader,
  dataCreateResponseSchema,
  replaceKeyWithValueFromJson,
} = require('./helpers/helpers');

chai.use(require('chai-json-schema'));

let specDataCreate;
const baseUrl = localhost + dataCreateEndpoint;
const endpointTag = { tags: `@endpoint=/${dataCreateEndpoint}` };

Before(endpointTag, () => {
  specDataCreate = pactum.spec();
});

// Scenario: The user successfully creates a record in the database smoke test type
Given(
  'The user wants to create a new record in the database',
  () => 'The user wants to create a new record in the database'
);

When(
  'User sends POST request with given Information-Mediator-Client header, body, {string} as registryname and {string} as versionnumber',
  (registryname, versionnumber) =>
    specDataCreate
      .post(baseUrl)
      .withHeaders(header.key, header.value)
      .withPathParams({
        registryname: registryname,
        versionnumber: versionnumber,
      })
);

When(
  'User provides body with parameters: {string} as ID, {string} as FirstName, {string} as LastName, {string} as BirthCertificateID',
  function (ID, FirstName, LastName, BirthCertificateID) {
    return specDataCreate.withBody({
      write: {
        content: {
          ID: replaceKeyWithValueFromJson(ID),
          FirstName: replaceKeyWithValueFromJson(FirstName),
          LastName: replaceKeyWithValueFromJson(LastName),
          BirthCertificateID: replaceKeyWithValueFromJson(BirthCertificateID),
        }
      }
    });
  }
);

When(
  'User provides parameters: {string} as ID, {string} as FirstName, {string} as LastName, {string} as BirthCertificateID',
  function (ID, FirstName, LastName, BirthCertificateID) {
    return specDataCreate.withBody({
      write: {
        content: {
          ID: replaceKeyWithValueFromJson(ID),
          FirstName: replaceKeyWithValueFromJson(FirstName),
          LastName: replaceKeyWithValueFromJson(LastName),
          BirthCertificateID: replaceKeyWithValueFromJson(BirthCertificateID),
        }
      }
    });
  }
);

Then(
  'User receives a response from the POST \\/data\\/\\{registryname}\\/\\{versionnumber}\\/create endpoint',
  async () => await specDataCreate.toss()
);

Then(
  'The POST \\/data\\/\\{registryname}\\/\\{versionnumber}\\/create endpoint response should be returned in a timely manner 15000ms',
  () =>
    specDataCreate
      .response()
      .to.have.responseTimeLessThan(defaultExpectedResponseTime)
);

Then(
  'The POST \\/data\\/\\{registryname}\\/\\{versionnumber}\\/create endpoint response should have status 200',
  () => specDataCreate.response().to.have.status(200)
);

Then(
  'The POST \\/data\\/\\{registryname}\\/\\{versionnumber}\\/create endpoint response should have content-type: {string} as ContentType',
  function (ContentType) {
    const actualContentType = specDataCreate.response().headers[contentTypeHeader.key];
    chai.expect(actualContentType).to.include(ContentType);
  }
);

Then(
  'The POST \\/data\\/\\{registryname}\\/\\{versionnumber}\\/create endpoint response should match json schema',
  () =>
    chai
      .expect(specDataCreate._response.json)
      .to.be.jsonSchema(dataCreateResponseSchema)
);

// Scenario: The user successfully creates a record in the database

// Already written above

After(endpointTag, () => {
  specDataCreate.end();
});
