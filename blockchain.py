from utility.verification import Verification
from wallet import Wallet

from transaction import Transaction
from block import Block
from utility import hash_util
import json
import os

MINING_REWARD = 10


class Blockchain:
    def __init__(self, public_key, node_id) -> None:
        self.__chain = [Block(0, "", [], 100, 0)]
        self.__open_transactions = []
        self.__peer_nodes = set()
        self.public_key = public_key
        self.node_id = node_id
        self.load_data()

    def get_chain(self):
        return self.__chain[:]

    def get_open_transactions(self):
        return self.__open_transactions[:]

    def load_data(self):
        if not os.path.isfile("blockchain-{}.txt".format(self.node_id)):
            return False

        with open("blockchain-{}.txt".format(self.node_id), mode="r") as f:
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

            open_transactions_invalid = json.loads(file_content[1][:-1])
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

            peer_nodes = json.loads(file_content[2])
            self.__peer_nodes = set(peer_nodes)

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
            with open("blockchain-{}.txt".format(self.node_id), mode="w") as f:
                f.write(json.dumps(blockchain_dict))
                f.write("\n")
                f.write(json.dumps(open_transactions_dict))
                f.write("\n")
                f.write(json.dumps(list(self.__peer_nodes)))
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
        if self.public_key == None:
            return None

        amount_sent = 0
        amount_received = 0
        participant = self.public_key

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
        if self.public_key == None:
            return "No public key"

        transaction = Transaction(sender, recipient, signature, amount)

        if Verification.verify_transaction(transaction, self.get_balance):
            self.__open_transactions.append(transaction)
            self.save_data()

            return None

        return "Transaction verification failed, balance is " + str(self.get_balance())

    def mine_block(self):
        if self.public_key == None:
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
            Transaction("MINING", self.public_key, "", MINING_REWARD)
        )

        block = Block(len(self.__chain), hashed_block, copied_transactions, proof)

        self.__chain.append(block)
        self.__open_transactions = []
        self.save_data()

        return block

    def add_peer_node(self, node):
        self.__peer_nodes.add(node)
        self.save_data()

    def remove_peer_node(self, node):
        self.__peer_nodes.discard(node)
        self.save_data()

    def get_peer_nodes(self):
        return list(self.__peer_nodes)
