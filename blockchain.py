blockchain = []


def add_transaction(transaction_amount, last_transaction=[1]):
    if last_transaction == None:
        last_transaction = [1]

    blockchain.append([last_transaction, transaction_amount])
    print(blockchain)


def get_transaction_value():
    return float(input("Your transaction amount please:"))


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
    index = 0

    for block in blockchain:
        if index >= 1:
            # print()
            # print("Check start for index " + str(index))
            # print(block[0])
            # print(blockchain[index - 1])
            # print("Check end")
            # print()

            if block[0] != blockchain[index - 1]:
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
        tx_amount = get_transaction_value()
        add_transaction(tx_amount, get_last_blockchain_value())
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
