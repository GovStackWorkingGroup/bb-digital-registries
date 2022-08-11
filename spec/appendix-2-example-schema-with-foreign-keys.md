# Appendix 2- Example Schema with Foreign Keys

```
{
    "id": 185,
    "version": "1.0",
    "name": null,
    "description": null,
    "institution": null,
    "number_format": "{code}{indexNoByCode}",
    "schema": {
        "type": "object",
        "properties": {
            "ID": {
                "type": "string",
                "triggers": [{
                    "conditions": [{
                        "logic": "==",
                        "value": "",
                        "gate": "&&"
                    }],
                    "actions": [{
                            "type": "set-value",
                            "value": "{code}{indexNoByCode}",
                            "field_id": 1
                        },
                        {
                            "type": "upper-case",
                            "field_id": 1
                        }
                    ]
                }],
                "primaryKey": true,
                "readOnly": true,
                "$id": 1
            },
            "Client ID": {
                "type": "string",
                "$id": 5
            },
            "Client first name": {
                "type": "string",
                "$id": 6
            },
            "Client last name": {
                "type": "string",
                "$id": 7
            },
            "Client date of birth": {
                "type": "string",
                "format": "date",
                "$id": 8
            },
            "Prescriptions": {
                "type": "string",
                "foreignKeys": [{
                    "databaseKey": "54",
                    "values": [{
                        "fieldKey": "6"
                    }]
                }],
                "$id": 3
            }
        },
        "$incrementIndex": 13,
        "required": [
            "ID"
        ]
    }
```

![Linking databases with foreign keys.](<.gitbook/assets/image6 (1) (1).png>)
