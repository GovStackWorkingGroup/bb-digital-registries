const { spec, response } = require('pactum');
const chai = require('chai');
const { Given, When, Then, Before, After } = require('@cucumber/cucumber');
const {
  header,
  localhost,
  defaultExpectedResponseTime,
  contentTypeHeader,
  dataUpdateResponseSchema,
  dataUpdateReadEndpoint
} = require('./helpers/helpers');

chai.use(require('chai-json-schema'));

const baseUrl = localhost + dataUpdateReadEndpoint;
const endpointTag = { tags: `@endpoint=/${dataUpdateReadEndpoint}` };

Before(endpointTag, () => {
  specDataUpdate = spec();
});

// Scenario: Successfully update user information record in database smoke type test

Given(
  /^User wants to update existing record in database$/,
  () => 'User wants to update existing record in database'
);

When(
  /^PUT request to check if the record exists in the database is sent with given path params "([^"]*)" as registryname and "([^"]*)" as versionnumber$/,
  (registryName, versionNumber) =>
    specDataUpdate
      .put(baseUrl)
      .withHeaders(header.key, header.value)
      .withPathParams({
        'registryname': registryName,
        'versionnumber': versionNumber
      })
);

When(/^the request contains a payload with given "([^"]*)" as ID "([^"]*)" as FirstName "([^"]*)" as LastName and "([^"]*)" as BirthCertificateID and the request overwrites the record with given "([^"]*)" as updatedID "([^"]*)" as updatedFirstName "([^"]*)" as updatedLastName and "([^"]*)" as updatedBirthCertificateID$/,
  (
    ID,
    FirstName,
    LastName,
    BirthCertificateID,
    updatedID,
    updatedFirstName,
    updatedLastName,
    updatedBirthCertificateID
  ) =>
    specDataUpdate
      .withJson({
        write: {
          query: {
            content: {
              ID: ID,
              FirstName: FirstName,
              LastName: LastName,
              BirthCertificateID: BirthCertificateID
            }
          },
          content: {
            ID: updatedID,
            FirstName: updatedFirstName,
            LastName: updatedLastName,
            BirthCertificateID: updatedBirthCertificateID
          }
        }
      })
);

Then(
  /^response from \/data\/\{registryname\}\/\{versionnumber\}\/update is received$/,
  async () => await specDataUpdate.toss()
);

Then(
  /^the response from \/data\/\{registryname\}\/\{versionnumber\}\/update should be returned in a timely manner 15000ms$/,
  () =>
    specDataUpdate
      .response()
      .to.have.responseTimeLessThan(defaultExpectedResponseTime)
);

Then(
  /^the response from \/data\/\{registryname\}\/\{versionnumber\}\/update should have status (\d+)$/,
  status =>
    specDataUpdate.response().to.have.status(status)
);

// Scenario: Successfully update user information record in database

// Given, When and Then is already written above

After(endpointTag, () => {
  specDataUpdate.end();
});
