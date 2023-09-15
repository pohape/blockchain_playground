from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
import binascii


class Wallet:
    def __init__(self):
        self.private_key = None
        self.public_key = None

    def create_keys(self):
        self.private_key, self.public_key = self.generate_keys()

    def load_keys(self):
        try:
            with open("wallet.txt", mode="r") as f:
                keys = f.readlines()
                self.public_key = keys[0][:-1]
                self.private_key = keys[1]
        except (IOError, IndexError):
            print("Wallet loading failed!")
            quit()

    def save_keys(self):
        if not self.private_key or not self.public_key:
            return False

        try:
            with open("wallet.txt", mode="w") as f:
                f.write(self.public_key)
                f.write("\n")
                f.write(self.private_key)
        except (IOError, IndexError):
            print("Wallet saving failed!")
            quit()

    def generate_keys(self):
        private_key = RSA.generate(1024)
        public_key = private_key.publickey()

        private_key_str = binascii.hexlify(private_key.exportKey(format="DER")).decode(
            "ascii"
        )

        public_key_str = binascii.hexlify(public_key.exportKey(format="DER")).decode(
            "ascii"
        )

        return private_key_str, public_key_str

    def sign_transaction(self, sender, recipient, amount):
        rsa_private_key = RSA.import_key(binascii.unhexlify(self.private_key))
        pkcs = PKCS1_v1_5.new(rsa_private_key)

        str_to_hash = str(sender) + str(recipient) + str(amount)
        hash_ = SHA256.new(str_to_hash.encode("utf8"))
        signature = pkcs.sign(hash_)

        return binascii.hexlify(signature).decode("ascii")

    def verify_transaction(transaction):
        if transaction.sender == "MINING":
            return True

        rsa_public_key = RSA.import_key(binascii.unhexlify(transaction.sender))
        pkcs = PKCS1_v1_5.new(rsa_public_key)

        str_to_hash = (
            str(transaction.sender)
            + str(transaction.recipient)
            + str(transaction.amount)
        )
        hash_ = SHA256.new(str_to_hash.encode("utf8"))

        return pkcs.verify(hash_, binascii.unhexlify(transaction.signature))
