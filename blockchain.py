from utility.verification import Verification
from wallet import Wallet

from transaction import Transaction
from block import Block
from utility import hash_util
import json
import os
import requests

MINING_REWARD = 10


class Blockchain:
    def __init__(self, public_key, node_id) -> None:
        self.__chain = [Block(0, "", [], 100, 0)]
        self.__open_transactions = []
        self.__peer_nodes = set()
        self.__peer_nodes.add("localhost:4001")
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
                    transactions.append(Transaction(transaction_invalid))

                self.__chain.append(
                    Block(
                        block_invalid["index"],
                        block_invalid["previous_hash"],
                        transactions,
                        block_invalid["proof"],
                    )
                )

            open_transactions_invalid = json.loads(file_content[1][:-1])
            self.__open_transactions = []

            for transaction_invalid in open_transactions_invalid:
                self.__open_transactions.append(Transaction(transaction_invalid))

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

    def get_balance(self, sender=None):
        if sender == None:
            if self.public_key == None:
                return None

            participant = self.public_key
        else:
            participant = sender

        amount_sent = 0
        amount_received = 0

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

    def add_block(self, block):
        transactions = [Transaction(tx) for tx in block["transactions"]]
        proof_is_valid = Verification.valid_proof(
            transactions[:-1], block["previous_hash"], block["proof"]
        )

        hashes_match = hash_util.hash_block(self.__chain[-1]) == block["previous_hash"]

        if not proof_is_valid or not hashes_match:
            return False

        self.__chain.append(
            Block(
                block["index"],
                block["previous_hash"],
                transactions,
                block["proof"],
                block["time"],
            )
        )

        self.save_data()

        return True

    def add_transaction(
        self, recipient, sender, signature, amount=1.0, is_receiving_broadcast=False
    ):
        # if self.public_key == None:
        #     return "No public key"

        transaction = Transaction(
            {
                "sender": sender,
                "recipient": recipient,
                "signature": signature,
                "amount": amount,
            }
        )

        if is_receiving_broadcast:
            verification_result = Verification.verify_transaction(transaction)
        else:
            verification_result = Verification.verify_transaction(
                transaction, self.get_balance
            )

        if verification_result:
            self.__open_transactions.append(transaction)
            self.save_data()

            if not is_receiving_broadcast:
                for node in self.__peer_nodes:
                    try:
                        response = requests.post(
                            "http://{}/broadcast-transaction".format(node),
                            json={
                                "sender": sender,
                                "recipient": recipient,
                                "amount": amount,
                                "signature": signature,
                            },
                        )

                        if response.status_code == 400 or response.status_code == 500:
                            return (
                                "Transaction decline with status "
                                + str(response.status_code)
                                + " and error message: "
                                + response.text
                            )
                    except requests.exceptions.ConnectionError:
                        continue
            return None

        return "Transaction verification failed"

    def mine_block(self):
        if self.public_key == None:
            return "Public key is empty"

        last_block = self.__chain[-1]
        hashed_block = hash_util.hash_block(last_block)
        proof = self.proof_of_work()

        copied_transactions = self.__open_transactions[:]

        for tx in copied_transactions:
            if not Wallet.verify_transaction(tx):
                return "There is an invalid transaction: " + tx

        copied_transactions.append(
            Transaction(
                {
                    "sender": "MINING",
                    "recipient": self.public_key,
                    "signature": "",
                    "amount": MINING_REWARD,
                }
            )
        )

        block = Block(len(self.__chain), hashed_block, copied_transactions, proof)

        self.__chain.append(block)
        self.__open_transactions = []
        self.save_data()

        for node in self.__peer_nodes:
            url = "http://{}/broadcast-block".format(node)
            converted_block = block.__dict__.copy()
            converted_block["transactions"] = [
                tx.__dict__.copy() for tx in converted_block["transactions"]
            ]

            try:
                response = requests.post(url, json={"block": converted_block})

                if response.status_code == 400 or response.status_code == 500:
                    print("Block declined, needs resolving")
            except requests.exceptions.ConnectionError:
                continue

        return block

    def add_peer_node(self, node):
        self.__peer_nodes.add(node)
        self.save_data()

    def remove_peer_node(self, node):
        self.__peer_nodes.discard(node)
        self.save_data()

    def get_peer_nodes(self):
        return list(self.__peer_nodes)
