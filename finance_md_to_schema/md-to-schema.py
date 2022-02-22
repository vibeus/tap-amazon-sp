#!/usr/bin/env python
"""
Reads schema definition from raw markdown format from stdin and write json schema to stdout.

Raw markdown can be copied from Amazon SP's documentation. For example:
- Orders: https://github.com/amzn/selling-partner-api-docs/blob/main/references/orders-api/ordersV0.md

Manually extract object definition from raw markdown, see saved extracted objects in this directory.

If object contain nested object, an empty schema for the nested object will be produced. Manually fill it will actual
schema by running this tool against the nested object definition.
"""

import json
import re
import sys


def process_line(line):
    columns = line.strip("|").split("|")
    assert len(columns) == 3, f"Malformat: {line}"

    key_tokens = re.findall(r"\w+", columns[0].replace("<br>", ""))
    key = key_tokens[0]
    required = False
    if len(key_tokens) > 1 and key_tokens[1] == "required":
        required = True

    value = {}
    value["description"] = columns[1].replace("<br>", " ")
    value_type = columns[2]

# valid JSON value type: 
#       "string", "number", "object", "array", "boolean", "null" <---- with quotation marks

    if value_type.startswith("enum"):
        value["type"] = "string" if required else ["null", "string"]
    elif value_type.startswith("[Money]"):
        value["type"] = "object" if required else ["null", "object"]
        value["properties"] = {
            "CurrencyCode": {"type": ["null", "string"]},
            "Amount": {"type": ["null", "number"]},
        }
    elif value_type in ["integer", "string", "boolean"]:
        value["type"] = value_type if required else ["null", value_type]
    else:
        value["type"] = "object" if required else ["null", "object"]
        value["properties"] = {}

    return key, value


def main():
    properties = {}

    for line in sys.stdin:
        key, value = process_line(line.strip())
        properties[key] = value

    schema = dict()
    schema["type"] = "object"
    schema["properties"] = properties

    print(json.dumps(schema, indent=2))


if __name__ == "__main__":
    main()
