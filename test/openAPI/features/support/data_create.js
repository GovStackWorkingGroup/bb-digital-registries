const chai = require('chai');
const pactum = require('pactum');
const { Given, When, Then, Before, After } = require('@cucumber/cucumber');
const {
  header,
  localhost,
  dataCreateEndpoint,
  dataCreateRequestBody,
  defaultExpectedResponseTime,
  contentTypeHeader,
  dataCreateResponseSchema,
} = require('./helpers/helpers');
const data = require('../../testDefaultParameters.json');

chai.use(require('chai-json-schema'));

let specDataCreate;
let dataStore = {};
let variable3;
const baseUrl = localhost + dataCreateEndpoint;
const endpointTag = { tags: `@endpoint=/${dataCreateEndpoint}` };

Before(endpointTag, () => {
  specDataCreate = pactum.spec();
});

// Scenario: The user successfully creates a record in the database smoke test type
Given(
  'The user wants to create a new record in the database',
  () => {dataStore['ID_1'] = "This works"}
);

Given('the user has ID_1 equal to {string}}', function (string) {
  let actualID_1 = string === "${ID_1}" ? "tak" : "nie";
  dataStore['ID_1'] = "This doesnt work";
});

Given('the user sets abc value to 123', function () {
  variable3 = "XDXDXD";
});

When(
  'User sends POST request with given Information-Mediator-Client header, body, {string} as registryname and {string} as versionnumber',
  (registryname, versionnumber) =>
    specDataCreate
      .post(baseUrl)
      .withHeaders(header.key, header.value)
      .withPathParams({
        registryname: registryname,
        versionnumber: versionnumber,
      })
);

When(
  'User provides body with parameters: {string} as ID, {string} as Firstname, {string} as LastName, {string} BirthCertificateID',
  function (ID, Firstname, LastName, BirthCertificateID) {
    let actualID = (ID === '${ID_1}') ? dataStore['ID_1'] : dataStore['ID_1'];
    return specDataCreate.withBody({
      ID: actualID,
      Firstname: Firstname,
      LastName: LastName,
      BirthCertificateID: BirthCertificateID,
    });
  }
);

Then(
  'User receives a response from the POST \\/data\\/\\{registryname}\\/\\{versionnumber}\\/create endpoint',
  async () => await specDataCreate.toss()
);

Then(
  'The POST \\/data\\/\\{registryname}\\/\\{versionnumber}\\/create endpoint response should be returned in a timely manner 15000ms',
  () =>
    specDataCreate
      .response()
      .to.have.responseTimeLessThan(defaultExpectedResponseTime)
);

Then(
  'The POST \\/data\\/\\{registryname}\\/\\{versionnumber}\\/create endpoint response should have status 200',
  () => specDataCreate.response().to.have.status(200)
);

Then(
  'The POST \\/data\\/\\{registryname}\\/\\{versionnumber}\\/create endpoint response should have content-type: application\\/json header',
  () =>
    specDataCreate
      .response()
      .should.have.header(contentTypeHeader.key, contentTypeHeader.value)
);

Then(
  'The POST \\/data\\/\\{registryname}\\/\\{versionnumber}\\/create endpoint response should match json schema',
  () =>
    chai
      .expect(specDataCreate._response.json)
      .to.be.jsonSchema(dataCreateResponseSchema)
);

// Scenario: The user successfully creates a record in the database

// Already written above

After(endpointTag, () => {
  specDataCreate.end();
});
