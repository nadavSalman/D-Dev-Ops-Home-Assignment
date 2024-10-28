import jsonschema
from jsonschema import validate
from datetime import datetime

class DataValidator:
    # JSON schema Post document
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
            "author": { "type": "string" },
            "body": { "type": "string" },
            "comments": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "author": { "type": "string" },
                        "body": { "type": "string" },
                        "email": { "type": "string", "format": "email" }
                    },
                    "required": ["author", "body", "email"]
                }
            },
            "date": { "type": "string", "format": "date-time" },
            "permalink": { "type": "string" },
            "tags": {
                "type": "array",
                "items": { "type": "string" }
            },
            "title": { "type": "string" }
        },
        "required": ["author", "body", "comments", "date", "permalink", "tags", "title"]
    }

    def __init__(self, data):
        self.data = data

    def validate(self):
        try:
            validate(instance=self.data, schema=self.schema)
            print("Validation succeeded.")
        except jsonschema.exceptions.ValidationError as err:
            print("Validation error:", err.message)

