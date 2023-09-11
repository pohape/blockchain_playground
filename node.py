from blockchain import Blockchain


class Node:
    def __init__(self) -> None:
        self.blockchain = []

    def listen_for_input(self):
        while True:
            print("Balance of {} is {:.2f}".format(owner, get_balance(owner)))
            print("Please choose")
            print("1: Add a new transaction")
            print("2: Mine a new block")
            print("3: Show participants")
            print("4: Verify transactions")
            print("q: Quit")

            user_choice = self.get_user_choise()

            if user_choice == "1":
                recipient, amount = node.get_transaction_value()

                if add_transaction(recipient, amount=amount):
                    print("Transaction completed!")
                else:
                    print("Transaction FAILED!")
            elif user_choice == "2":
                if mine_block():
                    open_transactions = []
                    save_data()
            elif user_choice == "3":
                self.print_blockchain_elements()
            elif user_choice == "4":
                if verification.verify_transactions(open_transactions, get_balance):
                    print("All transactions are valid")
                else:
                    print("There are invalid transactions")
            elif user_choice == "q":
                break
            else:
                print("Input was invalid")

            print("Choice registered")

            if not verification.verify_chain(self.blockchain):
                print("The Chain is invalid!")
                break

    print("Done!")

    def get_transaction_value(self):
        tx_recipient = input("Enter the recipient: ")
        tx_amount = float(input("Enter the amount: "))

        return (tx_recipient, tx_amount)

    def get_user_choise(self):
        return input("Your choice: ")

    def print_blockchain_elements(self):
        for block in self.blockchain:
            print("Outputing Block")
            print(block)
