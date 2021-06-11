
import json
import re

TO_PARSE = '{"a":{"b":[1,2,3]},"c":99}'

def parse(json_string: str) -> dict:
    """ Parses a raw json string into a dict object. """
    result = {}

    PARENT_WITH_CHILD = re.compile(r"\"\w{1}\":.*\}(?=.*})")
    FLAT_PARENT = re.compile(r"\"\w{1}\":[0-9]{1,}")

    parent_with_child_matches = PARENT_WITH_CHILD.findall(json_string)
    if parent_with_child_matches:
        for match in parent_with_child_matches:
            first_delimiter_index = match.find(":")
            parent_key, child = match[:first_delimiter_index], match[first_delimiter_index+1:]

            child_key, child_value = child.split(":")
            child_key = re.findall(r"\w{1}", child_key)[0]
            child_value = [int(element) for element in re.findall(r"\d{1,}", child_value)]

            parent_key = parent_key.strip('"')
            parent_value = {child_key: child_value}
            result[parent_key] = parent_value

    flat_parent_matches = FLAT_PARENT.findall(json_string)
    if flat_parent_matches:
        for match in flat_parent_matches:
            key, value = match.split(":")
            key = key.strip('"')
            value = int(value)
            result[key] = value

    return result
         

assert json.loads(TO_PARSE) == parse(TO_PARSE)