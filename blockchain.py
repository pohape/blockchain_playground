from verification import Verification
from node import Node
from transaction import Transaction
from block import Block
import hash_util
import json
import os

MINING_REWARD = 10


class Blockchain:
    def __init__(self) -> None:
        self.chain = [Block(0, "", [], 100, 0)]
        self.open_transactions = []
        self.load_data()

    def load_data(self):
        if not os.path.isfile("blockchain.txt"):
            return False

        with open("blockchain.txt", mode="r") as f:
            file_content = f.readlines()

            blockchain_invalid = json.loads(file_content[0][:-1])
            self.chain = []

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

                self.chain.append(
                    Block(
                        block_invalid["index"],
                        block_invalid["previous_hash"],
                        transactions,
                        block_invalid["proof"]
                        # block_invalid['timestamp']
                    )
                )

            open_transactions_invalid = json.loads(file_content[1])
            self.open_transactions = []

            for transaction_invalid in open_transactions_invalid:
                self.open_transactions.append(
                    Transaction(
                        transaction_invalid["sender"],
                        transaction_invalid["recipient"],
                        transaction_invalid["amount"],
                    ),
                )

            return True

    def save_data(self):
        blockchain_dict = []
        open_transactions_dict = []

        for block in self.chain:
            transactions_dict = []

            for transaction in block.transactions:
                transactions_dict.append(transaction.__dict__.copy())

            block_dict = block.__dict__.copy()
            block_dict["transactions"] = transactions_dict

            blockchain_dict.append(block_dict)

        for transaction in self.open_transactions:
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
        last_block = self.chain[-1]
        last_hash = hash_util.hash_block(last_block)
        proof = 0

        while not verification.valid_proof(self.open_transactions, last_hash, proof):
            proof += 1

        return proof

    def get_balance(self, participant):
        amount_sent = 0
        amount_received = 0

        for block in self.chain:
            for transaction in block.transactions:
                if transaction.sender == participant:
                    amount_sent += transaction.amount
                elif transaction.recipient == participant:
                    amount_received += transaction.amount

        for transaction in self.open_transactions:
            if transaction.sender == participant:
                amount_sent += transaction.amount

        return amount_received - amount_sent

    def get_last_blockchain_value(self):
        if len(self.chain) < 1:
            return None

        return self.chain[-1]

    def add_transaction(self, recipient, sender, amount=1.0):
        transaction = Transaction(sender, recipient, amount)

        if verification.verify_transaction(transaction, self.get_balance):
            self.open_transactions.append(transaction)
            self.save_data()

            return True

        return False

    def mine_block(self, node):
        last_block = self.chain[-1]
        hashed_block = hash_util.hash_block(last_block)
        proof = self.proof_of_work()

        copied_transactions = self.open_transactions[:]
        copied_transactions.append(Transaction("MINING", node, MINING_REWARD))

        block = Block(len(self.chain), hashed_block, copied_transactions, proof)
        self.chain.append(block)

        return True


verification = Verification()
node = Node()


node.listen_for_input()
