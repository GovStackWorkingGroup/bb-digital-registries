const pactum = require('pactum');
const { Given, When, Then, Before, After } = require('@cucumber/cucumber');
const { header, localhost } = require('./helpers/helpers');

let userID;
let databaseID;
let specDataMyPersonalDataUsage;

const baseUrl = `${localhost}data/MyPersonalDataUsage/1.0`;

const correctUrlRequest = (userID, databaseID) =>
  specDataMyPersonalDataUsage
    .get(`${baseUrl}`)
    .withHeaders(`${header.key}`, `${header.value}`)
    .withQueryParams('userID', userID)
    .withQueryParams('DatabaseID', databaseID);

Before(() => {
  specDataMyPersonalDataUsage = pactum.spec();
  databaseID = 'MCTS';
});

// Scenario: The user receives a list with all records that had read his personal data in the Digital Registries database
Given(
  'The user with id=282392302 wants to check who had read his personal data in the Digital Registries database',
  () => {
    userID = '282392302';
    return userID;
  }
);

Given(
  'In the database, there is a list of users who read the user with id=282392302 personal data',
  () => {
    return 'In the database, there is a list of users who read his personal data';
  }
);

When(
  'The user with id=282392302 triggers an action to receive a list of users who read his personal data',
  () => {
    correctUrlRequest(userID, databaseID);
  }
);

Then('The user receives a list with all records', async () => {
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

// Scenario: The user receives an empty list of records that had read his personal data from the Digital Registries database
Given(
  'The user with id=748382347 wants to check who had read his personal data in the Digital Registries database',
  () => {
    userID = '748382347';
    return userID;
  }
);

Given(
  'In the database there is an empty list of users who read the user with id=748382347 personal data',
  () => {
    return 'In the database there is an empty list of users who read the user with id=748382347 personal data';
  }
);

When(
  'The user with id=748382347 triggers an action to receive a list od users who read his personal data',
  () => {
    correctUrlRequest(userID, databaseID);
  }
);

Then(
  'The user with id=748382347 receives an empty list because there are no records in the database about other users who read his personal data',
  async () => {
    await specDataMyPersonalDataUsage.toss();
    specDataMyPersonalDataUsage.response().should.have.status(200);
    specDataMyPersonalDataUsage.response().should.have.jsonLike([]);
  }
);

// Scenario: The user is not able to receive data from the Digital Registries database because of an invalid request
Given(
  'The user with id=3782347 wants to check who had read his personal data in the Digital Registries database',
  () => {
    userID = '3782347';
    return userID;
  }
);

When(
  'The user with id=3782347 triggers an action to receive a list od users who read his personal data',
  () => {
    specDataMyPersonalDataUsage
      .get(`${baseUrl}`)
      .withQueryParams('userID', userID)
      .withQueryParams('DatabaseID', databaseID);
  }
);

Then('Operation to receive a list of results is an error', async () => {
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
