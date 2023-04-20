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

// Scenario: Successfully receives a message that the record exists in database
Given(
  /^get the database users information of Digital Registries$/,
  () => 'get the database users information of Digital Registries'
  );

When(
  /^POST request with given path params "([^"]*)" as registryname and "([^"]*)" as versionnumber$/,
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
      .withBody({
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

Then(
  /^response should return status true for existing record$/,
  () =>
      chai
        .expect(specDataExist._response.json.answer.status).to.be.true
);

Then(
  /^response should return status false for non\-existing record$/,
  () =>
    chai
      .expect(specDataExist._response.json.answer.status).to.be.false
);

After(endpointTag, () => {
  specDataExist.end();
});
