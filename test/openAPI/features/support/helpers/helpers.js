module.exports = {
  localhost: 'http://localhost:3333/',
  contentTypeHeader: {
    key: 'content-type',
    value: 'application/json; charset=utf-8',
  },
  header: {
    key: 'Information-Mediator-Client',
    value: 'INSTANCE/CLASS/MEMBER/SUBSYSTEM',
  },
  defaultExpectedResponseTime: 15000,
  databaseDeleteEndpoint: 'database/{id}',
  databaseDeleteResponseSchema: { type: 'string' },
};
