from blockchain import Blockchain
from uuid import uuid4
from verification import Verification


class Node:
    def __init__(self) -> None:
        # self.id = str(uuid4())
        self.id = "Max"
        self.blockchain = Blockchain(self.id)

    def listen_for_input(self):
        while True:
            print(
                "Balance of {} is {:.2f}".format(self.id, self.blockchain.get_balance())
            )
            print("Please choose")
            print("1: Add a new transaction")
            print("2: Mine a new block")
            print("3: Show participants")
            print("4: Verify transactions")
            print("q: Quit")

            user_choice = self.get_user_choise()

            if user_choice == "1":
                recipient, amount = self.get_transaction_value()

                if self.blockchain.add_transaction(recipient, self.id, amount=amount):
                    print("Transaction completed!")
                else:
                    print("Transaction FAILED!")
            elif user_choice == "2":
                self.blockchain.mine_block()
            elif user_choice == "3":
                self.print_blockchain_elements()
            elif user_choice == "4":
                if Verification.verify_transactions(
                    self.blockchain.get_open_transactions(), self.blockchain.get_balance
                ):
                    print("All transactions are valid")
                else:
                    print("There are invalid transactions")
            elif user_choice == "q":
                break
            else:
                print("Input was invalid")

            print("Choice registered")

            if not Verification.verify_chain(self.blockchain):
                print("The Chain is invalid!")
                break

    def get_transaction_value(self):
        tx_recipient = input("Enter the recipient: ")
        tx_amount = float(input("Enter the amount: "))

        return (tx_recipient, tx_amount)

    def get_user_choise(self):
        return input("Your choice: ")

    def print_blockchain_elements(self):
        for block in self.blockchain.get_chain():
            print("Outputing Block")
            print(block)
        else:
            print("-" * 20)


node = Node()
node.listen_for_input()
