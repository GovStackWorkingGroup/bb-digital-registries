const chai = require('chai');
const { spec } = require('pactum');
const { Given, When, Then, Before, After } = require('@cucumber/cucumber');
const {
  header,
  localhost,
  dataReadValueEndpoint,
  contentTypeHeader,
  defaultExpectedResponseTime,
} = require('./helpers/helpers');

chai.use(require('chai-json-schema'));

let specDataReadValue;

const baseUrl = localhost + dataReadValueEndpoint;
const endpointTag = { tags: `@endpoint=/${dataReadValueEndpoint}` };

Before(endpointTag, () => {
  specDataReadValue = spec();
});

// Scenario: The user gets the first name of the searched user from the database smoke type test
Given(
  "The user wants to search for the user's first name of the user in the database",
  () =>
    "The user wants to search for the user's first name of the user in the database"
);

When(
  'User sends GET request with given Information-Mediator-Client header, {string} as registryname and {string} as versionnumber, {string} as uuid, {string} as field and {string} as ext',
  (registryname, versionnumber, uuid, field, ext) =>
    specDataReadValue
      .get(baseUrl)
      .withHeaders(header.key, header.value)
      .withPathParams({
        registryname: registryname,
        versionnumber: versionnumber,
        uuid: uuid,
        field: field,
        ext: ext,
      })
);

Then(
  'User receives a response from the GET \\/data\\/\\{registryname}\\/\\{versionnumber}\\/\\{uuid}\\/read-value\\/\\{field}.\\{ext} endpoint',
  async () => await specDataReadValue.toss()
);

Then(
  'The GET \\/data\\/\\{registryname}\\/\\{versionnumber}\\/\\{uuid}\\/read-value\\/\\{field}.\\{ext} endpoint response should be returned in a timely manner 15000ms',
  () =>
    specDataReadValue
      .response()
      .to.have.responseTimeLessThan(defaultExpectedResponseTime)
);

Then(
  'The GET \\/data\\/\\{registryname}\\/\\{versionnumber}\\/\\{uuid}\\/read-value\\/\\{field}.\\{ext} endpoint response should have status 200',
  () => specDataReadValue.response().should.have.status(200)
);

Then(
  'The GET \\/data\\/\\{registryname}\\/\\{versionnumber}\\/\\{uuid}\\/read-value\\/\\{field}.\\{ext} endpoint response should have content-type: application\\/json header',
  () =>
    specDataReadValue
      .response()
      .should.have.header(contentTypeHeader.key, contentTypeHeader.value)
);

Then(
  'The GET \\/data\\/\\{registryname}\\/\\{versionnumber}\\/\\{uuid}\\/read-value\\/\\{field}.\\{ext} endpoint response should match json schema',
  () =>
    chai
      .expect(specDataReadValue._response.json)
      .to.be.jsonSchema({ type: 'string' })
);

After(endpointTag, () => {
  specDataReadValue.end();
});
