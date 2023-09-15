from blockchain import Blockchain
from uuid import uuid4
from utility.verification import Verification
from wallet import Wallet


class Node:
    def __init__(self) -> None:
        self.wallet = Wallet()
        self.wallet.create_keys()
        self.blockchain = Blockchain(self.wallet.public_key)

    def listen_for_input(self):
        while True:
            if self.blockchain:
                print(
                    "Balance of {} is {:.2f}".format(
                        self.wallet.public_key, self.blockchain.get_balance()
                    )
                )
            print("Please choose")
            print("1: Add a new transaction")
            print("2: Mine a new block")
            print("3: Show blockchain elements")
            print("4: Verify transactions")
            print("5: Create wallet")
            print("6: Load wallet keys")
            print("7: Save wallet keys")
            print("q: Quit")

            user_choice = self.get_user_choise()

            if user_choice == "1":
                recipient, amount = self.get_transaction_value()
                signature = self.wallet.sign_transaction(
                    self.wallet.public_key, recipient, amount
                )

                if self.blockchain.add_transaction(
                    recipient, self.wallet.public_key, signature, amount
                ):
                    print("Transaction added!")
                else:
                    print("Transaction FAILED!")
            elif user_choice == "2":
                if not self.blockchain.mine_block():
                    print("Mine block failed. Got no wallet?")
            elif user_choice == "3":
                self.print_blockchain_elements()
            elif user_choice == "4":
                if Verification.verify_transactions(
                    self.blockchain.get_open_transactions(), self.blockchain.get_balance
                ):
                    print("All transactions are valid")
                else:
                    print("There are invalid transactions")
            elif user_choice == "5":
                self.wallet.create_keys()
                self.blockchain = Blockchain(self.wallet.public_key)
            elif user_choice == "6":
                self.wallet.load_keys()
                self.blockchain = Blockchain(self.wallet.public_key)
            elif user_choice == "7":
                self.wallet.save_keys()
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


if __name__ == "__main__":
    node = Node()
    node.listen_for_input()
