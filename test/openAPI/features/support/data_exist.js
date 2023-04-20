const { spec } = require('pactum');
const chai = require('chai');
const { When, Then, Given, Before, After } = require('@cucumber/cucumber');
const {
  header,
  localhost,
  dataExistReadEndpoint,
  defaultExpectedResponseTime,
  contentTypeHeader,
  dataExistResponseSchema
} = require('./helpers/helpers');

chai.use(require('chai-json-schema'));

const baseUrl = localhost + dataExistReadEndpoint;
const endpointTag = { tags: `@endpoint=/${dataExistReadEndpoint}` };

Before(endpointTag, () => {
  specDataExist = spec();
});

// Scenario: Successfully receives a message that the record exists in database smoke type test
Given(
  /^user wants to check if the searched record exists in the database$/,
  () => 'user wants to check if the searched record exists in the database'
  );

When(
  /^send POST request to check if record exist in database with given path params "([^"]*)" as registryname and "([^"]*)" as versionnumber$/,
  (registryName, versionNumber) =>
    specDataExist
      .post(baseUrl)
      .withHeaders(header.key, header.value)
      .withPathParams({
        'registryname': registryName,
        'versionnumber': versionNumber
      })
  );

When(
  /^given body "([^"]*)" as ID and "([^"]*)" as FirstName and "([^"]*)" as LastName and "([^"]*)" as BirthCertificateID$/,
  (ID, FirstName, LastName, BirthCertificateID) =>
    specDataExist
      .withJson({
        ID: ID,
        FirstName: FirstName,
        LastName: LastName,
        BirthCertificateID: BirthCertificateID
      })
);

Then(
  /^response from \/data\/\{registryname\}\/\{versionnumber\}\/exist is received$/,
  async () => await specDataExist.toss()
);

Then(
  /^response should be returned in a timely manner 15000ms$/,
  () =>
    specDataExist
      .response()
      .to.have.responseTimeLessThan(defaultExpectedResponseTime)
);

Then(
  /^response should have status (\d+)$/,
  status => {
    specDataExist.response().to.have.status(status);
  }
);

Then(
  /^response should have content\-type: application\/json header$/,
  () =>
    specDataExist
      .response()
      .should.have.header(contentTypeHeader.key, contentTypeHeader.value)
);

Then(
  /^response should match json schema$/,
  () =>
    chai
      .expect(specDataExist._response.json)
      .to.be.jsonSchema(dataExistResponseSchema)
);



// Scenario: Successfully receives a message that the record exists in database

// Given is already written above
// When is already written above
// Then is already written above

Then(
  /^response should return status true for existing record$/,
  () =>
    chai
      .expect(specDataExist._response.json.answer.status).to.be.true
);

// Scenario: Successfully receives a message that the record not exists in database

// Given is already written above
// When is already written above
// Then is already written above

Then(
  /^response should return status false for non\-existing record$/,
  () =>
    chai
      .expect(specDataExist._response.json.answer.status).to.be.false
);

After(endpointTag, () => {
  specDataExist.end();
});
