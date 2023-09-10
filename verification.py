import hash_util


class Verification:
    def verify_transaction(self, transaction, get_balance):
        sender_balance = get_balance(transaction.sender)

        return sender_balance >= transaction.amount

    def verify_transactions(self, open_transactions, get_balance):
        return all(
            [self.verify_transaction(tx, get_balance) for tx in open_transactions]
        )

    def verify_chain(self, blockchain):
        for index, block in enumerate(blockchain):
            if index == 0:
                continue
            elif block.previous_hash != hash_util.hash_block(blockchain[index - 1]):
                return False
            elif not self.valid_proof(
                block.transactions[:-1], block.previous_hash, block.proof
            ):
                return False

        return True

    def valid_proof(self, transactions, last_hash, proof):
        transactions_str = str([tx.to_ordered_dict() for tx in transactions])
        guess = (transactions_str + str(last_hash) + str(proof)).encode()
        guess_hash = hash_util.hash_string_256(guess)

        return guess_hash[0:2] == "00"
