from collections import OrderedDict
import hash_util
import json
import os

MINING_REWARD = 10

genesis_block = {
    "previous_hash": "",
    "index": 0,
    "transactions": [],
    "proof": 100,
}

owner = "Max"
participants = {owner}


def load_data():
    if not os.path.isfile("blockchain.txt"):
        return False

    with open("blockchain.txt", mode="r") as f:
        file_content = f.readlines()
        global blockchain
        global open_transactions

        blockchain_invalid = json.loads(file_content[0][:-1])
        blockchain = []

        for block in blockchain_invalid:
            transactions = []

            for transaction in block["transactions"]:
                transactions.append(
                    OrderedDict(
                        [
                            ("sender", transaction["sender"]),
                            ("recipient", transaction["recipient"]),
                            ("amount", transaction["amount"]),
                        ]
                    )
                )

            blockchain.append(
                {
                    "previous_hash": block["previous_hash"],
                    "index": block["index"],
                    "proof": block["proof"],
                    "transactions": transactions,
                }
            )

        open_transactions_invalid = json.loads(file_content[1])
        open_transactions = []

        for transaction in open_transactions_invalid:
            open_transactions.append(
                OrderedDict(
                    [
                        ("sender", transaction["sender"]),
                        ("recipient", transaction["recipient"]),
                        ("amount", transaction["amount"]),
                    ]
                )
            )

        return True


def valid_proof(transactions, last_hash, proof):
    guess = (str(transactions) + str(last_hash) + str(proof)).encode()
    guess_hash = hash_util.hash_string_256(guess)

    return guess_hash[0:2] == "00"


def proof_of_work():
    last_block = blockchain[-1]
    last_hash = hash_util.hash_block(last_block)
    proof = 0

    while not valid_proof(open_transactions, last_hash, proof):
        proof += 1

    return proof


def add_transaction(recipient, sender=owner, amount=1.0):
    transaction = OrderedDict(
        [("sender", sender), ("recipient", recipient), ("amount", amount)]
    )

    if verify_transaction(transaction):
        open_transactions.append(transaction)
        save_data()

        participants.add(sender)
        participants.add(recipient)

        return True

    return False


def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_util.hash_block(last_block)
    proof = proof_of_work()

    reward_transaction = OrderedDict(
        [("sender", "MINING"), ("recipient", owner), ("amount", MINING_REWARD)]
    )

    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)

    block = {
        "previous_hash": hashed_block,
        "index": len(blockchain),
        "transactions": copied_transactions,
        "proof": proof,
    }

    blockchain.append(block)

    return True


def get_transaction_value():
    tx_recipient = input("Enter the recipient: ")
    tx_amount = float(input("Enter the amount: "))

    return (tx_recipient, tx_amount)


def get_user_choise():
    return input("Your choice: ")


def print_blockchain_elements():
    for block in blockchain:
        print("Outputing Block")
        print(block)


def get_last_blockchain_value():
    if len(blockchain) < 1:
        return None

    return blockchain[-1]


def verify_transaction(transaction):
    sender_balance = get_balance(transaction["sender"])

    return sender_balance >= transaction["amount"]


def verify_chain():
    for index, block in enumerate(blockchain):
        if index == 0:
            continue
        elif block["previous_hash"] != hash_util.hash_block(blockchain[index - 1]):
            return False
        elif not valid_proof(
            block["transactions"][:-1], block["previous_hash"], block["proof"]
        ):
            return False

    return True


def get_balance(participant):
    amount_sent = 0
    amount_received = 0

    for block in blockchain:
        for transaction in block["transactions"]:
            if transaction["sender"] == participant:
                amount_sent += transaction["amount"]
            elif transaction["recipient"] == participant:
                amount_received += transaction["amount"]

    for transaction in open_transactions:
        if transaction["sender"] == participant:
            amount_sent += transaction["amount"]

    return amount_received - amount_sent


def verify_transactions():
    return all([verify_transaction(tx) for tx in open_transactions])


def save_data():
    with open("blockchain.txt", mode="w") as f:
        f.write(json.dumps(blockchain))
        f.write("\n")
        f.write(json.dumps(open_transactions))


if not load_data():
    blockchain = [genesis_block]
    open_transactions = []

while True:
    print("Balance of {} is {:.2f}".format(owner, get_balance(owner)))
    print("Please choose")
    print("1: Add a new transaction")
    print("2: Mine a new block")
    print("3: Output the blockchain blocks")
    print("4: Show participants")
    print("5: Verify transactions")
    print("h: Manipulate the chain")
    print("q: Quit")

    user_choice = get_user_choise()

    if user_choice == "1":
        recipient, amount = get_transaction_value()

        if add_transaction(recipient, amount=amount):
            print("Transaction completed!")
        else:
            print("Transaction FAILED!")
    elif user_choice == "2":
        if mine_block():
            open_transactions = []
            save_data()
    elif user_choice == "3":
        print_blockchain_elements()
    elif user_choice == "4":
        print(participants)
    elif user_choice == "5":
        if verify_transactions():
            print("All transactions are valid")
        else:
            print("There are invalid transactions")
    elif user_choice == "q":
        break
    elif user_choice == "h":
        if len(blockchain) >= 1:
            blockchain[0] = {
                "previous_hash": "",
                "index": 0,
                "transactions": [{"sender": "Max", "recipient": "Chris", "amount": 1}],
            }
    else:
        print("Input was invalid")

    print("Choice registered")

    if not verify_chain():
        print("The Chain is invalid!")
        break


print("Done!")
