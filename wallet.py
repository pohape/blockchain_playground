from Crypto.PublicKey import RSA
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
