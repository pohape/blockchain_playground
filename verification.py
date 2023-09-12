import hash_util


class Verification:
    @staticmethod
    def verify_transaction(transaction, get_balance):
        sender_balance = get_balance()

        return sender_balance >= transaction.amount

    def verify_transactions(cls, open_transactions, get_balance):
        return all(
            [cls.verify_transaction(tx, get_balance) for tx in open_transactions]
        )

    @classmethod
    def verify_chain(cls, blockchain):
        for index, block in enumerate(blockchain.chain):
            if index == 0:
                continue
            elif block.previous_hash != hash_util.hash_block(
                blockchain.chain[index - 1]
            ):
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
        guess_hash = hash_util.hash_string_256(guess)

        return guess_hash[0:2] == "00"
