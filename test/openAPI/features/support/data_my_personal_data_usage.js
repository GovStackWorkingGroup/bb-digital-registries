const pactum = require('pactum');
const { Given, When, Then, Before, After } = require('@cucumber/cucumber');
const { header, localhost } = require('./helpers/helpers');

let userID;
let databaseID;
let specDataMyPersonalDataUsage;

const baseUrl = `${localhost}data/MyPersonalDataUsage/1.0`;

const correctUrlRequest = (userID, databaseID) =>
  specDataMyPersonalDataUsage
    .get(baseUrl)
    .withHeaders(`${header.key}`, `${header.value}`)
    .withQueryParams('userID', userID)
    .withQueryParams('DatabaseID', databaseID);

Before(() => {
  specDataMyPersonalDataUsage = pactum.spec();
  databaseID = 'MCTS';
});

// Scenario: The user gets a list of all records that have read their personal data in the Digital Registries database
Given(
  'The user wants to check who has read his personal data in the Digital Registries database and there is a list of users who have done so',
  () => (userID = '282392302')
);

When(
  'The user sends a valid request and receives a list of users who have read his personal data',
  () => {
    correctUrlRequest(userID, databaseID);
  }
);

Then('The user receives a list of all records', async () => {
  await specDataMyPersonalDataUsage.toss();
  specDataMyPersonalDataUsage.response().should.have.status(200);
  specDataMyPersonalDataUsage.response().should.have.jsonLike([
    {
      ID: '1234567',
      ReaderID: userID,
      ReaderInitials: 'JD',
      ReaderInstitutionID: 'EE70049837',
      ReaderInstitutionName: 'East Hospital',
      ReaderApplicationName: 'East Hospital healthcare back office',
      SearchDateTime: '2017-07-21T17:32:28Z',
      Refrences: [
        {
          ReferenceID: databaseID,
        },
      ],
    },
  ]);
});

// Scenario: The user receives an empty list of records that have read his personal data from the Digital Registries database
Given(
  'The user wants to check who has read his personal data from Digital Registries database and there is an empty list of users who have done so',
  () => (userID = '748382347')
);

// "When" is already written in line 29-32

Then(
  'The user receives an empty list because there are no records in the database about other users who have read his personal data',
  async () => {
    await specDataMyPersonalDataUsage.toss();
    specDataMyPersonalDataUsage.response().should.have.status(200);
    specDataMyPersonalDataUsage.response().should.have.jsonLike([]);
  }
);

// Scenario: The user is unable to obtain data from the Digital Registries database due to an invalid request
Given(
  'The user wants to check who has read his personal data in the Digital Registries database',
  () => (userID = '3782347')
);

When(
  'The user sends an invalid request and receives a list of users who have read his personal data',
  () => {
    specDataMyPersonalDataUsage
      .get(baseUrl)
      .withQueryParams('userID', userID)
      .withQueryParams('DatabaseID', databaseID);
  }
);

Then('The operation to get a list of results is an error', async () => {
  await specDataMyPersonalDataUsage.toss();
  specDataMyPersonalDataUsage.response().should.have.status(400);
  specDataMyPersonalDataUsage
    .response()
    .should.have.body(
      '{\n  "Invalid format of Information-Mediator-Client, should match INSTANCE/CLASS/MEMBER/SUBSYSTEM"\n}'
    );
});

After(() => {
  specDataMyPersonalDataUsage.end();
});
