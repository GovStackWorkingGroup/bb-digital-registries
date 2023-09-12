const chai = require('chai');
const { spec } = require('pactum');
const { Given, When, Then, Before, After } = require('@cucumber/cucumber');
const {
  header,
  localhost,
  contentTypeHeader,
  defaultExpectedResponseTime,
  dataUpdateOrCreateEndpoint,
  dataUpdateOrCreateResponseSchema,
} = require('./helpers/helpers');

chai.use(require('chai-json-schema'));

let specDataUpdateOrCreate;

const baseUrl = localhost + dataUpdateOrCreateEndpoint;
const endpointTag = { tags: `@endpoint=/${dataUpdateOrCreateEndpoint}` };

Before(endpointTag, () => {
  specDataUpdateOrCreate = spec();
});

// Scenario: The record is successfully created in the database smoke type test
Given(
  'User wants to create a new record in the database',
  () => 'User wants to create a new record in the database'
);

When(
  /^User sends POST request to \/data\/{registryname}\/{versionnumber}\/update-or-create with given Information-Mediator-Client header, "([^"]*)" as registryname and "([^"]*)" as versionnumber$/,
  (registryName, versionNumber) =>
    specDataUpdateOrCreate
      .post(baseUrl)
      .withHeaders(header.key, header.value)
      .withPathParams({
        registryname: registryName,
        versionnumber: versionNumber,
      })
);

When(
  /^The request contains a payload with query and write objects that both contain content object with given: "([^"]*)" as ID, "([^"]*)" as FirstName, "([^"]*)" as LastName and "([^"]*)" as BirthCertificateID$/,
  (ID, FirstName, LastName, BirthCertificateID) =>
    specDataUpdateOrCreate.withJson({
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
          ID: ID,
          FirstName: FirstName,
          LastName: LastName,
          BirthCertificateID: BirthCertificateID,
        },
      },
    })
);

Then(
  /^User receives a response from the \/data\/{registryname}\/{versionnumber}\/update-or-create endpoint$/,
  async () => await specDataUpdateOrCreate.toss()
);

Then(
  /^The \/data\/{registryname}\/{versionnumber}\/update-or-create response should be returned in a timely manner 15000ms$/,
  () =>
    specDataUpdateOrCreate
      .response()
      .to.have.responseTimeLessThan(defaultExpectedResponseTime)
);

Then(
  /^The \/data\/{registryname}\/{versionnumber}\/update-or-create response should have status (\d+)$/,
  status => specDataUpdateOrCreate.response().to.have.status(status)
);

Then(
  /^The \/data\/{registryname}\/{versionnumber}\/update-or-create response should have content-type: {string} as ContentType$/,
  (ContentType) =>
    specDataUpdateOrCreate
      .response()
      .should.have.header(contentTypeHeader.key)
      .and.include(ContentType)
);

Then(
  /^The \/data\/{registryname}\/{versionnumber}\/update-or-create response should match json schema$/,
  () =>
    chai
      .expect(specDataUpdateOrCreate._response.json)
      .to.be.jsonSchema(dataUpdateOrCreateResponseSchema)
);

// Scenario: The existing record is successfully updated in the database
// Others When, Then for this scenario are written in the aforementioned example
Given(
  'User wants to update previously created record in the database',
  () => 'User wants to update previously created record in the database'
);

When(
  /^The request contains a payload with query object that contains content object with given: "([^"]*)" as ID, "([^"]*)" as FirstName, "([^"]*)" as LastName and "([^"]*)" as BirthCertificateID and write object that contains content object with given: "([^"]*)" as ID, "([^"]*)" as FirstName, "([^"]*)" as LastName and "([^"]*)" as BirthCertificateID$/,
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
    specDataUpdateOrCreate.withJson({
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

Then(
  /^The \/data\/{registryname}\/{versionnumber}\/update-or-create response should contain "([^"]*)" property equals "([^"]*)"$/,
  (propertyName, updatedValueOfProperty) =>
    chai
      .expect(specDataUpdateOrCreate._response.json.content[propertyName])
      .to.be.equal(updatedValueOfProperty)
);

After(endpointTag, () => {
  specDataUpdateOrCreate.end();
});
