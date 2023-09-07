import hashlib


def valid_proof(transactions, last_hash, proof):
    guess = (str(transactions) + str(last_hash) + str(proof)).encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    print(guess_hash)

    return guess_hash[0:2]


transactions = ["dsfadf", "dsfadf", "dsfadf", "dsfadf", "dsfadf"]
proof = ["dsfaddf", "dsfadf", "dsfadf", "dsfadf", "dsfadf"]
last_hash = "123dfsaj4o35j34o5j34o2j34o1ij53"

print(valid_proof(transactions, last_hash, proof))
