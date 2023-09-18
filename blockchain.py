from utility.verification import Verification
from wallet import Wallet

from transaction import Transaction
from block import Block
from utility import hash_util
import json
import os

MINING_REWARD = 10


class Blockchain:
    def __init__(self, hosting_node_id) -> None:
        self.__chain = [Block(0, "", [], 100, 0)]
        self.__open_transactions = []
        self.load_data()
        self.hosting_node = hosting_node_id

    def get_chain(self):
        return self.__chain[:]

    def get_open_transactions(self):
        return self.__open_transactions[:]

    def load_data(self):
        if not os.path.isfile("blockchain.txt"):
            return False

        with open("blockchain.txt", mode="r") as f:
            file_content = f.readlines()

            blockchain_invalid = json.loads(file_content[0][:-1])
            self.__chain = []

            for block_invalid in blockchain_invalid:
                transactions = []

                for transaction_invalid in block_invalid["transactions"]:
                    transactions.append(
                        Transaction(
                            transaction_invalid["sender"],
                            transaction_invalid["recipient"],
                            transaction_invalid["signature"],
                            transaction_invalid["amount"],
                        )
                    )

                self.__chain.append(
                    Block(
                        block_invalid["index"],
                        block_invalid["previous_hash"],
                        transactions,
                        block_invalid["proof"]
                        # block_invalid['timestamp']
                    )
                )

            open_transactions_invalid = json.loads(file_content[1])
            self.__open_transactions = []

            for transaction_invalid in open_transactions_invalid:
                self.__open_transactions.append(
                    Transaction(
                        transaction_invalid["sender"],
                        transaction_invalid["recipient"],
                        transaction_invalid["signature"],
                        transaction_invalid["amount"],
                    ),
                )

            return True

    def save_data(self):
        blockchain_dict = []
        open_transactions_dict = []

        for block in self.__chain:
            transactions_dict = []

            for transaction in block.transactions:
                transactions_dict.append(transaction.__dict__.copy())

            block_dict = block.__dict__.copy()
            block_dict["transactions"] = transactions_dict

            blockchain_dict.append(block_dict)

        for transaction in self.__open_transactions:
            open_transactions_dict.append(transaction.__dict__.copy())

        try:
            with open("blockchain.txt", mode="w") as f:
                f.write(json.dumps(blockchain_dict))
                f.write("\n")
                f.write(json.dumps(open_transactions_dict))
        except IOError:
            print("Saving failed!")
            quit()

    def proof_of_work(self):
        last_block = self.__chain[-1]
        last_hash = hash_util.hash_block(last_block)
        proof = 0

        while not Verification.valid_proof(self.__open_transactions, last_hash, proof):
            proof += 1

        return proof

    def get_balance(self):
        if self.hosting_node == None:
            return None

        amount_sent = 0
        amount_received = 0
        participant = self.hosting_node

        for block in self.__chain:
            for transaction in block.transactions:
                if transaction.sender == participant:
                    amount_sent += transaction.amount
                elif transaction.recipient == participant:
                    amount_received += transaction.amount

        for transaction in self.__open_transactions:
            if transaction.sender == participant:
                amount_sent += transaction.amount

        return amount_received - amount_sent

    def get_last_blockchain_value(self):
        if len(self.__chain) < 1:
            return None

        return self.__chain[-1]

    def add_transaction(self, recipient, sender, signature, amount=1.0):
        if self.hosting_node == None:
            return "No hosting node"

        transaction = Transaction(sender, recipient, signature, amount)

        if Verification.verify_transaction(transaction, self.get_balance):
            self.__open_transactions.append(transaction)
            self.save_data()

            return None

        return "Transaction verification failed, balance is " + str(self.get_balance())

    def mine_block(self):
        if self.hosting_node == None:
            return None

        last_block = self.__chain[-1]
        hashed_block = hash_util.hash_block(last_block)
        proof = self.proof_of_work()

        copied_transactions = self.__open_transactions[:]

        for tx in copied_transactions:
            if not Wallet.verify_transaction(tx):
                # print("There is an invalid transaction: " + tx)

                return None

        copied_transactions.append(
            Transaction("MINING", self.hosting_node, "", MINING_REWARD)
        )

        block = Block(len(self.__chain), hashed_block, copied_transactions, proof)

        self.__chain.append(block)
        self.__open_transactions = []
        self.save_data()

        return block
