const chai = require('chai');
const { spec } = require('pactum');
const { Given, When, Then, Before, After } = require('@cucumber/cucumber');
const {
  header,
  localhost,
  defaultExpectedResponseTime,
  dataUpdateEntriesEndpoint,
} = require('./helpers/helpers');

chai.use(require('chai-json-schema'));

const baseUrl = localhost + dataUpdateEntriesEndpoint;
const endpointTag = { tags: `@endpoint=/${dataUpdateEntriesEndpoint}` };

Before(endpointTag, () => {
  specDataUpdateEntries = spec();
});

// Scenario: Successfully updates multiple records in the database by first name smoke type test
Given(
  'User wants to update multiple records in the database',
  () => 'User wants to update multiple records in the database'
);

When(
  /^User sends PUT request to \/data\/{registryname}\/{versionnumber}\/update-entries with given Information-Mediator-Client header, "([^"]*)" as registryname and "([^"]*)" as versionnumber$/,
  (registryName, versionNumber) =>
    specDataUpdateEntries
      .put(baseUrl)
      .withHeaders(header.key, header.value)
      .withPathParams({
        registryname: registryName,
        versionnumber: versionNumber,
      })
);

When(
  /^The request contains a payload with two objects: query object that contains content object with given: "([^"]*)" as FirstName and write object that contains content object with given: "([^"]*)" as FirstName$/,
  (FirstName, UpdatedFirstName) =>
    specDataUpdateEntries.withJson({
      query: {
        content: {
          FirstName: FirstName,
        },
      },
      write: {
        content: {
          FirstName: UpdatedFirstName,
        },
      },
    })
);

Then(
  /^User receives a response from the \/data\/{registryname}\/{versionnumber}\/update-entries endpoint$/,
  async () => await specDataUpdateEntries.toss()
);

Then(
  /^The \/data\/{registryname}\/{versionnumber}\/update-entries response should be returned in a timely manner 15000ms$/,
  () =>
    specDataUpdateEntries
      .response()
      .to.have.responseTimeLessThan(defaultExpectedResponseTime)
);

Then(
  /^The \/data\/{registryname}\/{versionnumber}\/update-entries response should have status (\d+)$/,
  status => specDataUpdateEntries.response().to.have.status(status)
);

// Scenario Outline: Successfully updates multiple records in the database by first name
// All Given When Then are the same as for the afoementioned smoke type test

// Scenario: Successfully updates multiple records in the database
// Others Given When Then are written in the afoementioned smoke type test example
When(
  /^The request contains a payload with two objects: query object that contains content object with given: "([^"]*)" as ID, "([^"]*)" as FirstName, "([^"]*)" as LastName, "([^"]*)" as BirthCertificateID and write object that contains content object with given: "([^"]*)" as ID, "([^"]*)" as FirstName, "([^"]*)" as LastName, "([^"]*)" as BirthCertificateID$/,
  (
    ID,
    FirstName,
    LastName,
    BirthCertificateID,
    UpdatedID,
    UpdatedFirstName,
    UpdatedLastName,
    UpdatedBirthCertificateID
  ) =>
    specDataUpdateEntries.withJson({
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
          ID: UpdatedID,
          FirstName: UpdatedFirstName,
          LastName: UpdatedLastName,
          BirthCertificateID: UpdatedBirthCertificateID,
        },
      },
    })
);

After(endpointTag, () => {
  specDataUpdateEntries.end();
});
