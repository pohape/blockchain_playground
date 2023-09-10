import hashlib
import json


def hash_string_256(string):
    return hashlib.sha256(string).hexdigest()


def transactions_dict(transactions):
    transactions_dict = []

    for transaction in transactions:
        transactions_dict.append(transaction.__dict__.copy())

    return transactions_dict


def json_dump_block(block):
    block_dict = block.__dict__.copy()
    block_dict["transactions"] = [tx.to_ordered_dict() for tx in block.transactions]
    block_dict["time"] = None

    return json_dump(block_dict)


def json_dump(data):
    return json.dumps(data, sort_keys=True).encode()


def hash_block(block):
    return hash_string_256(json_dump_block(block))
