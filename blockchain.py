from collections import OrderedDict
from block import Block
from transaction import Transaction
import hash_util
import json
import os

MINING_REWARD = 10

genesis_block = Block(0, "", [], 100, 0)
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

        for block_invalid in blockchain_invalid:
            transactions = []

            for transaction_invalid in block_invalid["transactions"]:
                transactions.append(
                    Transaction(
                        transaction_invalid["sender"],
                        transaction_invalid["recipient"],
                        transaction_invalid["amount"],
                    )
                )

            blockchain.append(
                Block(
                    block_invalid["index"],
                    block_invalid["previous_hash"],
                    transactions,
                    block_invalid["proof"]
                    # block_invalid['timestamp']
                )
            )

        open_transactions_invalid = json.loads(file_content[1])
        open_transactions = []

        for transaction_invalid in open_transactions_invalid:
            open_transactions.append(
                Transaction(
                    transaction_invalid["sender"],
                    transaction_invalid["recipient"],
                    transaction_invalid["amount"],
                ),
            )

        return True


def valid_proof(transactions, last_hash, proof):
    transactions_str = str(hash_util.transactions_dict(transactions))
    guess = (transactions_str + str(last_hash) + str(proof)).encode()
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
    transaction = Transaction(sender, recipient, amount)

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

    copied_transactions = open_transactions[:]
    copied_transactions.append(Transaction("MINING", owner, MINING_REWARD))

    block = Block(len(blockchain), hashed_block, copied_transactions, proof)
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
    sender_balance = get_balance(transaction.sender)

    return sender_balance >= transaction.amount


def verify_chain():
    for index, block in enumerate(blockchain):
        if index == 0:
            continue
        elif block.previous_hash != hash_util.hash_block(blockchain[index - 1]):
            return False
        elif not valid_proof(block.transactions[:-1], block.previous_hash, block.proof):
            return False

    return True


def get_balance(participant):
    amount_sent = 0
    amount_received = 0

    for block in blockchain:
        for transaction in block.transactions:
            if transaction.sender == participant:
                amount_sent += transaction.amount
            elif transaction.recipient == participant:
                amount_received += transaction.amount

    for transaction in open_transactions:
        if transaction.sender == participant:
            amount_sent += transaction.amount

    return amount_received - amount_sent


def verify_transactions():
    return all([verify_transaction(tx) for tx in open_transactions])


def save_data():
    blockchain_dict = []
    open_transactions_dict = []

    for block in blockchain:
        transactions_dict = []

        for transaction in block.transactions:
            transactions_dict.append(transaction.__dict__.copy())

        block_dict = block.__dict__.copy()
        block_dict["transactions"] = transactions_dict

        blockchain_dict.append(block_dict)

    for transaction in open_transactions:
        open_transactions_dict.append(transaction.__dict__.copy())

    try:
        with open("blockchain.txt", mode="w") as f:
            f.write(json.dumps(blockchain_dict))
            f.write("\n")
            f.write(json.dumps(open_transactions_dict))
    except IOError:
        print("Saving failed!")
        quit()


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
    else:
        print("Input was invalid")

    print("Choice registered")

    if not verify_chain():
        print("The Chain is invalid!")
        break


print("Done!")
