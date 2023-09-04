MINING_REWARD = 10

genesis_block = {
    "previous_hash": "",
    "index": 0,
    "transactions": [],
}

blockchain = [genesis_block]
open_transactions = []
owner = "Max"
participants = {owner}


def hash_block(block):
    return "-".join([str(block[key]) for key in block])


def add_transaction(recipient, sender=owner, amount=1.0):
    transaction = {"sender": sender, "recipient": recipient, "amount": amount}

    if verify_transaction(transaction):
        open_transactions.append(transaction)
        participants.add(sender)
        participants.add(recipient)

        return True

    return False


def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)

    reward_transaction = {
        "sender": "MINING",
        "recipient": owner,
        "amount": MINING_REWARD,
    }

    open_transactions.append(reward_transaction)

    block = {
        "previous_hash": hashed_block,
        "index": len(blockchain),
        "transactions": open_transactions,
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
        elif block["previous_hash"] != hash_block(blockchain[index - 1]):
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


while True:
    print("Please choose")
    print("1: Add a new transaction")
    print("2: Mine a new block")
    print("3: Output the blockchain blocks")
    print("4: Show participants")
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
    elif user_choice == "3":
        print_blockchain_elements()
    elif user_choice == "4":
        print(participants)
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
    print("Balance is " + str(get_balance("Max")))

    if not verify_chain():
        print("The Chain is invalid!")
        break


print("Done!")
