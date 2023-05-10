const { spec } = require('pactum');
const { Given, When, Then, Before, After } = require('@cucumber/cucumber');
const {
  header,
  localhost,
  dataDeleteEndpoint,
  defaultExpectedResponseTime,
} = require('./helpers/helpers');

let specDataDelete;

const baseUrl = localhost + dataDeleteEndpoint;
const endpointTag = { tags: `@endpoint=/${dataDeleteEndpoint}` };

Before(endpointTag, () => {
  specDataDelete = spec();
});

// Successfully deletes a record from the database smoke type test
Given(
  'The user wants to remove the record from the  database',
  () => 'The user wants to remove the record from the  database'
);

When(
  'User sends DELETE \\/data\\/\\{registryname}\\/\\{versionnumber}\\/\\{id}\\/delete request with given Information-Mediator-Client header, {string} as registryname and {string} as versionnumber, {string} as ID',
  (registryName, versionNumber, id) =>
    specDataDelete
      .delete(baseUrl)
      .withHeaders(header.key, header.value)
      .withPathParams({
        registryname: registryName,
        versionnumber: versionNumber,
        ID: id,
      })
);

Then(
  'User receives a response from the \\/data\\/\\{registryname}\\/\\{versionnumber}\\/\\{id}\\/delete endpoint',
  async () => await specDataDelete.toss()
);

Then(
  'The \\/data\\/\\{registryname}\\/\\{versionnumber}\\/\\{id}\\/delete endpoint response should be returned in a timely manner 15000ms',
  () =>
    specDataDelete
      .response()
      .to.have.responseTimeLessThan(defaultExpectedResponseTime)
);

Then(
  'The \\/data\\/\\{registryname}\\/\\{versionnumber}\\/\\{id}\\/delete endpoint response should have status 204',
  () => specDataDelete.response().should.have.status(204)
);

// Scenario Outline: Successfully deletes a record from the database
// Others Given, When and Then are written in the aforementioned example

After(endpointTag, () => {
  specDataDelete.end();
});
