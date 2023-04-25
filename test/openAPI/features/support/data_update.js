const { spec } = require('pactum');
const chai = require('chai');
const { Given, When, Then, Before, After } = require('@cucumber/cucumber');
const {
  header,
  localhost,
  defaultExpectedResponseTime,
  dataUpdateReadEndpoint,
} = require('./helpers/helpers');

chai.use(require('chai-json-schema'));

const baseUrl = localhost + dataUpdateReadEndpoint;
const endpointTag = { tags: `@endpoint=/${dataUpdateReadEndpoint}` };

Before(endpointTag, () => {
  specDataUpdate = spec();
});

// Scenario: Successfully updates a record in the registry database smoke type test
Given(
  /^User wants to update an existing record in the database$/,
  () => 'User wants to update existing record in database'
);

When(
  /^PUT request to update a record in the database is sent with given path params "([^"]*)" as registryname and "([^"]*)" as versionnumber$/,
  (registryName, versionNumber) =>
    specDataUpdate
      .put(baseUrl)
      .withHeaders(header.key, header.value)
      .withPathParams({
        registryname: registryName,
        versionnumber: versionNumber,
      })
);

When(
  /^The request contains a payload with given "([^"]*)" as ID "([^"]*)" as FirstName "([^"]*)" as LastName and "([^"]*)" as BirthCertificateID and the request overwrites the record with given "([^"]*)" as ID "([^"]*)" as FirstName "([^"]*)" as LastName and "([^"]*)" as BirthCertificateID$/,
  (
    ID,
    FirstName,
    LastName,
    BirthCertificateID,
    overwritingID,
    overwritingFirstName,
    overwritingLastName,
    overwritingBirthCertificateID
  ) =>
    specDataUpdate.withJson({
      query: {
        content: {
          ID: ID,
          FirstName: FirstName,
          LastName: LastName,
          BirthCertificateID: BirthCertificateID,
        },
      },
      write: {
        content: {
          ID: overwritingID,
          FirstName: overwritingFirstName,
          LastName: overwritingLastName,
          BirthCertificateID: overwritingBirthCertificateID,
        },
      },
    })
);

Then(
  /^The response from \/data\/\{registryname\}\/\{versionnumber\}\/update is received$/,
  async () => await specDataUpdate.toss()
);

Then(
  /^The response from \/data\/\{registryname\}\/\{versionnumber\}\/update should be returned in a timely manner 15000ms$/,
  () =>
    specDataUpdate
      .response()
      .to.have.responseTimeLessThan(defaultExpectedResponseTime)
);

Then(
  /^The response from \/data\/\{registryname\}\/\{versionnumber\}\/update should have status (\d+)$/,
  status => specDataUpdate.response().to.have.status(status)
);

// Scenario Outline: Successfully updates a record in the registry database
// Given, When and Then are written in the aforementioned example

After(endpointTag, () => {
  specDataUpdate.end();
});
