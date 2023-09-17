from flask import Flask
from flask_cors import CORS
from blockchain import Blockchain
from wallet import Wallet
from flask import jsonify
import json

app = Flask(__name__)
CORS(app)

wallet = Wallet()
# wallet.create_keys()
blockchain = Blockchain(wallet.public_key)


@app.route("/", methods=["GET"])
def get_ui():
    return "This works!"


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

        result = (
            json.dumps(
                {
                    "message": "Block added successfully",
                    "block": dict_block,
                    "wallet_set_up": wallet.public_key != None,
                }
            ),
            200,
        )
    else:
        result = (
            json.dumps(
                {
                    "message": "Adding a block failed",
                    "block": None,
                    "wallet_set_up": wallet.public_key != None,
                }
            ),
            500,
        )

    return result


@app.route("/mine", methods=["POST"])
def api_mine():
    return mine()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
