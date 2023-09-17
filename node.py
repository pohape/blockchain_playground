from flask import Flask
from flask_cors import CORS
from blockchain import Blockchain
from wallet import Wallet
from flask import jsonify
import json

app = Flask(__name__)
CORS(app)

wallet = Wallet()
blockchain = Blockchain(wallet.public_key)


@app.route("/", methods=["GET"])
def get_ui():
    return "This works!"


@app.route("/wallet", methods=["POST"])
def create_keys():
    wallet.create_keys()

    if wallet.save_keys():
        global blockchain
        blockchain = Blockchain(wallet.public_key)

        return (
            jsonify(
                {
                    "message": "OK",
                    "public_key": wallet.public_key,
                    "private_key": wallet.private_key,
                }
            ),
            201,
        )
    else:
        return (
            jsonify(
                {
                    "message": "Saving the keys failed",
                    "public_key": None,
                    "private_key": None,
                }
            ),
            500,
        )


@app.route("/wallet", methods=["GET"])
def load_keys():
    if wallet.load_keys():
        global blockchain
        blockchain = Blockchain(wallet.public_key)

        return (
            jsonify(
                {
                    "message": "OK",
                    "public_key": wallet.public_key,
                    "private_key": wallet.private_key,
                }
            ),
            201,
        )
    else:
        return (
            jsonify(
                {
                    "message": "Loading the keys failed",
                    "public_key": None,
                    "private_key": None,
                }
            ),
            500,
        )


@app.route("/chain", methods=["GET"])
def api_get_chain():
    dict_chain = [block.__dict__.copy() for block in blockchain.get_chain()]

    for dict_block in dict_chain:
        dict_block["transactions"] = [
            tx.__dict__.copy() for tx in dict_block["transactions"]
        ]

    return jsonify(dict_block), 200


def mine():
    block = blockchain.mine_block()

    if block:
        dict_block = block.__dict__.copy()
        dict_block["transactions"] = [
            tx.__dict__.copy() for tx in dict_block["transactions"]
        ]

        return {
            "message": "Block added successfully",
            "block": dict_block,
            "wallet_set_up": wallet.public_key != None,
        }
    else:
        return {
            "message": "Adding a block failed",
            "block": None,
            "wallet_set_up": wallet.public_key != None,
        }


@app.route("/mine", methods=["POST"])
def api_mine():
    dictionary = mine()

    if dictionary["block"] == None:
        http_code = 500
    else:
        http_code = 200

    return jsonify(dictionary), http_code


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
