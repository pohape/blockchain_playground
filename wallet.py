from Crypto.PublicKey import RSA
import Crypto.Random
import binascii


class Wallet:
    def __init__(self):
        self.private_key = None
        self.public_key = None

    def create_keys(self):
        self.private_key, self.public_key = self.generate_keys()

    def load_keys(self):
        pass

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
