const assert = require("assert");
const { Given, When, Then } = require("cucumber");
let app = require("../../../src/app");

Given('API input object is {string}, API endpoint is {string} and method used is {string}', function(input, endpoint, method) {  
  this.input = input;
  this.endpoint = endpoint;
  this.method = method;
});

When('I ask to receive a record', async function() {
  this.actualAnswer = await app.postMCTS(this.input, this.endpoint, this.method);
});

Then('I should get a record {string}', function(expectedAnswer) {
  assert.equal(this.actualAnswer, expectedAnswer);
});
