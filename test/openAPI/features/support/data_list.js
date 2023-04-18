const { spec } = require('pactum');
const chai = require('chai');
const { When, Then, Given, Before } = require('@cucumber/cucumber');
const {
  header,
  localhost,
  dataListResponseSchema,
  defaultExpectedResponseTime,
  contentTypeHeader, dataListReadEndpoint
} = require('./helpers/helpers');
chai.use(require('chai-json-schema'));

let specDataList;

const baseUrl = localhost + dataListReadEndpoint;

Before(() => {
  specDataList = spec();
});

// User successfully obtains database users information with database schema smoke type test
Given(
  'User wants to get the database users information of Digital Registries',
  () => 'User wants to get the database users information of Digital Registries'
);

When(/^User sends GET request with given Information\-Mediator\-Client header and "([^"]*)" as registryname and "([^"]*)" as versionnumber$/,  (registryName, versionNumber) =>
  specDataList
    .get(baseUrl)
    .withHeaders(header.key, header.value)
    .withPathParams('registryname', registryName)
    .withPathParams('versionnumber', versionNumber)
);

Then(
  /^User receives a response from the GET \/data\/\{registryname\}\/\{versionnumber\} endpoint$/,
  async () => await specDataList.toss()
);

Then(
  /^The GET \/data\/\{registryname\}\/\{versionnumber\}\/ endpoint response should be returned in a timely manner 15000ms$/,
  () => specDataList.response().to.have.responseTimeLessThan(defaultExpectedResponseTime)
);

Then(
  /^The GET \/data\/\{registryname\}\/\{versionnumber\}\/ endpoint response should have status (\d+)$/,
  (status) => specDataList.response().to.have.status(status)
);
Then(
  /^The GET \/data\/\{registryname\}\/\{versionnumber\}\/ endpoint response should have content\-type: application\/json header$/,
  () => specDataList.response().should.have.header(contentTypeHeader.key, contentTypeHeader.value)
  );
Then(
  /^The GET \/data\/\{registryname\}\/\{versionnumber\}\/ endpoint response should match json schema$/,
  () =>
    chai
      .expect(specDataList._response.json)
      .to.be.jsonSchema(dataListResponseSchema)
  );


// Scenario Outline: User successfully obtains database users information  with database schema

// Given is already written in line 23-26
// When is already written in line 28-35

When(/^User filters users informations by using query parameters "([^"]*)" as search and "([^"]*)" as filter and "([^"]*)" as ordering$/,
  (search, filter, ordering) =>
    specDataList
      .withQueryParams({
        search: search,
        filter: filter,
        ordering: ordering
      })
);

// Then is already written in line 37-61


// Scenario: The user receives an empty list from the Digital Registries database
Given(
  'The user wants to search for a specific value and the searched value does not exist in any record in the database',
  () => 'The user wants to search for a specific value and the searched value does not exist in any record in the database'
);

// "When" is already written in line 28-35 and 70-78

Then(
  'The user receives an empty list because there is no record in the database that contains the searched value',
  () => {
    specDataList.response().should.have.jsonLike({
      results: [],
    });
  }
);
