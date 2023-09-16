from flask import Flask
from flask_cors import CORS
from blockchain import Blockchain
from wallet import Wallet
from flask import jsonify

app = Flask(__name__)
wallet = Wallet()
CORS(app)

wallet = Wallet()
blockchain = Blockchain(wallet)


@app.route("/", methods=["GET"])
def get_ui():
    return "This works!"


@app.route("/chain", methods=["GET"])
def get_chain():
    dict_chain = [block.__dict__.copy() for block in blockchain.get_chain()]

    for dict_block in dict_chain:
        dict_block["transactions"] = [
            tx.__dict__.copy() for tx in dict_block["transactions"]
        ]

    return jsonify(dict_block), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
