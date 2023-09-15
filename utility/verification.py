from utility.hash_util import hash_string_256, hash_block


class Verification:
    @staticmethod
    def verify_transaction(transaction, get_balance):
        sender_balance = get_balance()

        return sender_balance >= transaction.amount

    @staticmethod
    def verify_transactions(open_transactions, get_balance):
        return all(
            [
                Verification.verify_transaction(tx, get_balance)
                for tx in open_transactions
            ]
        )

    @classmethod
    def verify_chain(cls, blockchain):
        for index, block in enumerate(blockchain.get_chain()):
            if index == 0:
                continue
            elif block.previous_hash != hash_block(blockchain.get_chain()[index - 1]):
                return False
            elif not cls.valid_proof(
                block.transactions[:-1], block.previous_hash, block.proof
            ):
                return False

        return True

    @staticmethod
    def valid_proof(transactions, last_hash, proof):
        transactions_str = str([tx.to_ordered_dict() for tx in transactions])
        guess = (transactions_str + str(last_hash) + str(proof)).encode()
        guess_hash = hash_string_256(guess)

        return guess_hash[0:2] == "00"