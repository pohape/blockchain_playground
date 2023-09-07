import hashlib
import json


def hash_string_256(string):
    return hashlib.sha256(string).hexdigest()


def json_dump(data):
    return json.dumps(data, sort_keys=True).encode()


def hash_block(block):
    return hash_string_256(json_dump(block))
