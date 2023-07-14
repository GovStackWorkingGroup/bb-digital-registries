function replaceKeyWithValueFromJson(key) {
  let processedKey = key.replace('${', '').replace('}', '');
  return jsonData[processedKey] || key;
}

module.exports = {
  localhost: 'http://localhost:3333/',
  contentTypeHeader: {
    key: 'content-type',
    value: 'application/json; charset=utf-8',
  },
  header: {
    key: 'Information-Mediator-Client',
    value: 'eGovStack/GOV/90000009/digitalregistries',
  },
  defaultExpectedResponseTime: 15000,
  // db_delete
  databaseDeleteEndpoint: 'database/{id}',
  databaseDeleteResponseSchema: { type: 'string' },
  // db_read
  databaseReadEndpoint: 'database/{id}',
  databaseReadResponseSchema: {
    type: 'object',
    properties: this.databaseInfoSchema,
  },
  // db_list
  databasesEndpoint: 'databases',
  databasesResponseSchema: {
    type: 'object',
    properties: {
      id: { type: 'integer' },
      name: { type: 'string' },
      code: { type: 'string' },
      databases: {
        type: 'array',
        items: this.databaseInfoSchema,
      },
      group_id: { type: 'integer' },
      order: { type: 'integer' },
      data_index_increment: { type: 'integer' },
    },
    additionalProperties: false,
  },
  // db_modify
  databaseModifyEndpoint: 'database/modify',
  databaseModifyResponseSchema: {
    type: 'object',
    properties: this.databaseSchemaSchema,
  },
  databaseModifyBody: {
    group_name: 'Test',
    catalog_name: 'Mother and Child',
    code: 'MCR',
    schema: {
      type: 'some object',
      properties: {
        ID: {
          type: 'some string',
          triggers: [
            {
              conditions: [
                {
                  logic: '==',
                  value: '',
                  gate: '&&',
                },
              ],
              actions: [
                {
                  type: 'set-value',
                  value: 'MCTS{indexNoByCode}',
                  field_id: 1,
                },
              ],
            },
          ],
          primaryKey: true,
          readOnly: true,
          description: 'Registration ID',
          example: 'MCTS31',
          id: 1,
        },
        Child: {
          type: ' some string',
          properties: {
            ID: {
              type: 'some string',
              description: 'Child ID',
              example: 'ID2',
              id: 13,
            },
          },
        },
      },
      incrementIndex: 30,
      required: ['ID'],
    },
  },
  // data_update_entries
  dataUpdateEntriesEndpoint:
    'data/{registryname}/{versionnumber}/update-entries',
  // data_create
  dataCreateEndpoint: 'data/{registryname}/{versionnumber}/create',
  dataCreateResponseSchema: {
    type: 'object',
    properties: { content: this.dataExampleSchema },
  },
  // data_my_personal_data_usage
  dataMyPersonalDataUsageEndpoint: 'data/MyPersonalDataUsage/1.0',
  dataMyPersonalDataUsageResponseSchema: {
    type: 'array',
    properties: {
      type: 'object',
      properties: {
        ID: { type: 'string' },
        ReaderID: { type: 'string' },
        ReaderInitials: { type: 'string' },
        ReaderInstitutionID: { type: 'string' },
        ReaderInstitutionName: { type: 'string' },
        ReaderApplicationName: { type: 'string' },
        SearchDateTime: { type: 'string', format: 'date-time' },
        Refrences: {
          type: 'array',
          items: {
            properties: {
              ReferenceID: { type: 'string' },
            },
          },
        },
      },
      additionalProperties: false,
    },
  },
  // data_list
  dataListReadEndpoint: 'data/{registryname}/{versionnumber}',
  dataListResponseSchema: {
    type: 'object',
    properties: {
      count: { type: 'number' },
      next: { type: 'string' },
      previous: { type: ['string', 'null'] },
      results: {
        type: 'array',
        items: this.dataExampleSchema,
      },
    },
    required: ['count', 'results'],
  },
  // data_exist
  dataExistReadEndpoint: 'data/{registryname}/{versionnumber}/exists',
  dataExistResponseSchema: {
    type: 'object',
    properties: {
      answer: {
        type: 'object',
        properties: {
          status: { type: 'boolean' },
          message: { type: 'string' },
        },
        required: ['status', 'message'],
      },
    },
    required: ['answer'],
  },
  // data_update
  dataUpdateReadEndpoint: 'data/{registryname}/{versionnumber}/update',
  dataUpdateResponseSchema: {
    type: 'object',
    properties: {
      query: {
        type: 'object',
        properties: {
          content: this.dataExampleSchema,
        },
        required: ['content'],
      },
      write: {
        type: 'object',
        properties: {
          content: this.dataExampleSchema,
        },
        required: ['content'],
      },
    },
    required: ['query', 'write'],
  },
  // data_update_or_create
  dataUpdateOrCreateEndpoint:
    'data/{registryname}/{versionnumber}/update-or-create',
  dataUpdateOrCreateResponseSchema: {
    type: 'object',
    properties: {
      content: this.dataExampleSchema,
    },
    required: ['content'],
  },
  // data_read_value
  dataReadValueEndpoint:
    'data/{registryname}/{versionnumber}/{uuid}/read-value/{field}.{ext}',
  dataReadValueResponseSchema: { type: 'string' },
  // data_read
  dataReadEndpoint: 'data/{registryname}/{versionnumber}/read',
  dataReadResponseSchema: {
    type: 'object',
    properties: {
      content: this.dataExampleSchema,
    },
    required: ['content'],
  },
  dataRead404ResponseSchema: {
    type: 'object',
    properties: {
      detail: {
        type: 'string',
        enum: ['no record found'],
      },
    },
  },
  // data_delete
  dataDeleteEndpoint: 'data/{registryname}/{versionnumber}/{id}/delete',
  // shares
  databaseSchemaSchema: {
    type: 'object',
    properties: {
      type: { type: 'string' },
      properties: {
        type: 'object',
        properties: {
          ID: {
            type: 'object',
            properties: {
              type: 'string',
              triggers: {
                type: 'array',
                items: {
                  type: 'object',
                  properties: {
                    conditions: {
                      type: 'array',
                      properties: {
                        logic: { type: 'string' },
                        value: { type: 'string' },
                        gate: { type: 'string' },
                      },
                      additionalProperties: false,
                    },
                    actions: {
                      type: 'array',
                      items: {
                        type: 'object',
                        properties: {
                          type: { type: 'string' },
                          value: { type: 'string' },
                          field_id: { type: 'integer' },
                        },
                        additionalProperties: false,
                      },
                    },
                  },
                  additionalProperties: false,
                },
              },
              primaryKey: { type: 'boolean' },
              readOnly: { type: 'boolean' },
              description: { type: 'string' },
              example: { type: 'string' },
              id: { type: 'integer' },
            },
            additionalProperties: false,
          },
          Child: {
            type: 'object',
            properties: {
              type: {
                type: 'string',
                properties: {
                  type: 'object',
                  properties: {
                    ID: {
                      type: 'object',
                      properties: {
                        type: { type: 'string' },
                        description: { type: 'string' },
                        example: { type: 'string' },
                        id: { type: 'integer' },
                      },
                    },
                  },
                },
              },
            },
          },
        },
        additionalProperties: false,
      },
      incrementIndex: { type: 'integer' },
      required: ['ID'],
      additionalProperties: false,
    },
  },
  databaseInfoSchema: {
    type: 'object',
    properties: {
      id: { type: 'integer' },
      version: { type: 'string' },
      name: { type: 'string' },
      description: { type: 'string' },
      institution: { type: 'string' },
      number_format: { type: 'string' },
      schema: this.databaseSchemaSchema,
      schema_tags: {
        type: 'array',
        items: {
          type: 'object',
          properties: {
            name: { type: 'string' },
            path: { type: 'string' },
            is_fulltext: { type: 'boolean' },
          },
          additionalProperties: false,
        },
      },
      schema_flags: {
        type: 'array',
        items: {
          type: 'object',
          properties: {
            name: { type: 'string' },
            path: { type: 'string' },
          },
        },
      },
      fields_uniques: {
        type: 'array',
        items: {
          type: 'array',
          items: {
            type: 'string',
          },
        },
      },
      is_draft: { type: 'boolean' },
      is_disabled: { type: 'boolean' },
      is_archived: { type: 'boolean' },
      modified_at: { type: 'string' },
      by_user_name: { type: 'string' },
      by_user_auth_id: { type: 'integer' },
      by_on_behalf_of_user_auth_id: { type: 'integer' },
      by_on_behalf_of_user_name: { type: 'string' },
      generic_services: {
        type: 'array',
        items: {
          type: 'object',
          properties: {
            service_id: { type: 'integer' },
            name: { type: 'string' },
            is_visible: { type: 'boolean' },
            used_count: { type: 'integer' },
          },
          additionalProperties: false,
        },
      },
      data_index_increment: { type: 'integer' },
      has_logo: { type: 'boolean' },
    },
  },
  dataExampleSchema: {
    type: 'object',
    properties: {
      ID: { type: 'string' },
      FirstName: { type: 'string' },
      LastName: { type: 'string' },
      BirthCertificateID: { type: 'string' },
    },
    required: ['ID', 'FirstName', 'LastName', 'BirthCertificateID'],
  },
  replaceKeyWithValueFromJson
};