const { spec } = require('pactum');
const chai = require('chai');
const { When, Then, Given, Before, After } = require('@cucumber/cucumber');
const {
  header,
  localhost,
  dataListResponseSchema,
  defaultExpectedResponseTime,
  contentTypeHeader,
  dataListReadEndpoint,
} = require('./helpers/helpers');

chai.use(require('chai-json-schema'));
let specDataList;

const baseUrl = localhost + dataListReadEndpoint;
const endpointTag = { tags: `@endpoint=/${dataListReadEndpoint}` };

Before(() => {
  specDataList = spec();
});

// Successfully obtains database users information smoke type test
Given(
  'user wants to get the database users information',
  () => 'user wants to get the database users information'
);

When(
  /^send GET request with given Information\-Mediator\-Client header and "([^"]*)" as registryname and "([^"]*)" as versionnumber$/,
  (registryName, versionNumber) =>
    specDataList
      .get(baseUrl)
      .withHeaders(header.key, header.value)
      .withPathParams('registryname', registryName)
      .withPathParams('versionnumber', versionNumber)
);

Then(
  /^receive a response from the GET \/data\/\{registryname\}\/\{versionnumber\} endpoint$/,
  async () => await specDataList.toss()
);

Then(
  /^the response from \/data\/\{registryname\}\/\{versionnumber\} should be returned in a timely manner 15000ms$/,
  () =>
    specDataList
      .response()
      .to.have.responseTimeLessThan(defaultExpectedResponseTime)
);

Then(
  /^the response from \/data\/\{registryname\}\/\{versionnumber\} should have status (\d+)$/,
  status => specDataList.response().to.have.status(status)
);
Then(
  /^the response from \/data\/\{registryname\}\/\{versionnumber\} should have content\-type: "([^"]*)" as ContentType$/,
  (ContentType) =>
    specDataList
      .response()
      .should.have.header(contentTypeHeader.key, ContentType)
);
Then(
  /^the response from \/data\/\{registryname\}\/\{versionnumber\} should match json schema$/,
  () =>
    chai
      .expect(specDataList._response.json)
      .to.be.jsonSchema(dataListResponseSchema)
);

// Scenario Outline: Successfully obtains database users information

// Given is already written above
// When is already written above

When(
  /^filter users information by using query parameters "([^"]*)" as search and "([^"]*)" as filter and "([^"]*)" as ordering$/,
  (search, filter, ordering) => {
    specDataList.withQueryParams({
      search: search,
      filter: filter,
      ordering: ordering,
    });
  }
);

// Then is already written above

Then(
  /^the response from \/data\/\{registryname\}\/\{versionnumber\} is filtered by "([^"]*)" and "([^"]*)" provided in the query parameter$/,
  (search, filter) => {
    const nameFieldArray = specDataList._response.json.results.map(
      item => item.FirstName
    );

    nameFieldArray.map(nameField => chai.expect(nameField).equals(search));
  }
);

// Scenario: Receive an empty list from the Digital Registries database
Given(
  /^search for a specific value and the searched value does not exist in any record in the database$/,
  () =>
    'search for a specific value and the searched value does not exist in any record in the database'
);

// "When" is already written above

Then(/^results field should be an empty array$/, () => {
  const resultsArray = specDataList._response.json.results.map(field => field);

  chai.expect(resultsArray).to.have.length(0);
});

Then(/^results array length is consistent with count field value$/, () => {
  const resultsArray = specDataList._response.json.results.map(field => field);
  const countValue = specDataList._response.json.count;

  chai.expect(resultsArray).to.have.length(countValue);
});

After(endpointTag, () => {
  specDataList.end();
});
