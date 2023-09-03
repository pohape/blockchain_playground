genesis_block = {
    "previous_hash": "",
    "index": 0,
    "transactions": [],
}

blockchain = [genesis_block]
open_transactions = []
owner = "Max"


def hash_block(block):
    return "-".join([str(block[key]) for key in block])


def add_transaction(recipient, sender=owner, amount=1.0):
    transaction = {"sender": sender, "recipient": recipient, "amount": amount}

    open_transactions.append(transaction)


def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)

    block = {
        "previous_hash": hashed_block,
        "index": len(blockchain),
        "transactions": open_transactions,
    }

    blockchain.append(block)
    # open_transactions = []


def get_transaction_value():
    tx_recepient = input("Enter the recipient: ")
    tx_amount = input("Enter the amount: ")

    return (tx_recepient, tx_amount)


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


def verify_chain():
    for index, block in enumerate(blockchain):
        print(block)
        if index == 0:
            continue
        elif block["previous_hash"] != hash_block(blockchain[index - 1]):
            return False

    return True


while True:
    print("Please choose")
    print("1: Add a new transaction")
    print("2: Mine a new block")
    print("3: Output the blockchain blocks")
    print("h: Manipulate the chain")
    print("q: Quit")

    user_choice = get_user_choise()

    if user_choice == "1":
        tx_data = get_transaction_value()
        recipient, amount = tx_data

        add_transaction(recipient, amount=amount)
        print(open_transactions)
    elif user_choice == "2":
        mine_block()
    elif user_choice == "3":
        print_blockchain_elements()
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
