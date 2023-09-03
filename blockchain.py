blockchain = []
open_transactions = []
owner = "Max"


def add_transaction(recipient, sender=owner, amount=1.0):
    transaction = {"sender": sender, "recipient": recipient, "amount": amount}

    open_transactions.append(transaction)


def mine_block():
    pass


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
    for index in range(len(blockchain)):
        if index == 0:
            continue
        elif blockchain[index][0] != blockchain[index - 1]:
            return False
        index += 1

    return True


while True:
    print("Please choose")
    print("1: Add a new transaction")
    print("2: Output the blockchain blocks")
    print("h: Manipulate the chain")
    print("q: Quit")

    user_choice = get_user_choise()

    if user_choice == "1":
        tx_data = get_transaction_value()
        recipient, amount = tx_data

        add_transaction(recipient, amount=amount)
        print(open_transactions)
    elif user_choice == "2":
        print_blockchain_elements()
    elif user_choice == "q":
        break
    elif user_choice == "h":
        if len(blockchain) >= 1:
            blockchain[0] = [666]
    else:
        print("Input was invalid")

    print("Choice registered")

    if not verify_chain():
        print("The Chain is invalid!")
        break


print("Done!")
