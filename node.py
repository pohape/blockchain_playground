from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from blockchain import Blockchain
from wallet import Wallet
import json
from bs4 import BeautifulSoup
from argparse import ArgumentParser

app = Flask(__name__)
CORS(app)

wallet = Wallet()
blockchain = Blockchain(wallet.public_key)


def html_get_header_with_menu(current_page_name):
    with open("ui/header.html", mode="r") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    # find the tag <li> by ID
    tag = soup.find(id="menu_" + current_page_name)

    # create a new tag <b> with the same text as in <li>
    newtag = soup.new_tag("b")
    newtag.string = tag.get_text()

    # replace <a> inside <li> to <b>
    # so <li><a>...</a></li> turns into <li><b>...</b></li>
    tag.find("a").replace_with(newtag)

    # return prettified HTML
    return soup.prettify()


def html_get_header(current_page_name):
    return (
        html_get_header_with_menu(current_page_name)
        .replace(
            "{public_key}",
            "wallet is not initialized"
            if wallet.public_key == None
            else wallet.public_key,
        )
        .replace("{balance}", str(blockchain.get_balance()))
    )


@app.route("/", methods=["GET"])
def get_ui():
    return (
        html_get_header("open_transactions")
        + '<iframe src="/transactions" height="500" width="1000" title="Transactions"></iframe>'
    ), 200


@app.route("/chain.html", methods=["GET"])
def blockchain_html():
    return (
        html_get_header("chain")
        + '<iframe src="/chain" height="500" width="1000" title="Chain"></iframe>'
    ), 200


@app.route("/transaction.html", methods=["GET"])
def transaction_html():
    with open("ui/transaction.html", mode="r") as f:
        return (html_get_header("transaction") + f.read()), 200


@app.route("/network.html", methods=["GET"])
def network_html():
    with open("ui/network.html", mode="r") as f:
        html = html_get_header("network") + f.read()

    html += "<ol>"

    for node in blockchain.get_peer_nodes():
        html += "<li><b>" + node + "</b>"
        html += (
            "<form action='/node/"
            + node
            + "' method='POST'><input type='submit' value='Delete'></form></li>"
        )

    return html + "</ol>", 200


@app.route("/load_wallet.html", methods=["GET"])
def load_wallet_html():
    if wallet.load_keys():
        global blockchain
        blockchain = Blockchain(wallet.public_key)

    return (
        html_get_header("load_wallet")
        + '<iframe src="/wallet" height="500" width="1000" title="Load Wallet"></iframe>'
    ), 200


@app.route("/transactions", methods=["GET"])
def open_transactions():
    transactions = blockchain.get_open_transactions()
    dict_transactions = [tx.__dict__ for tx in transactions]

    return (
        Response(json.dumps(dict_transactions, indent=2), mimetype="application/json"),
        200,
    )


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
                    "funds": blockchain.get_balance(),
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
                    "funds": None,
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
            Response(
                json.dumps(
                    {
                        "message": "OK",
                        "public_key": wallet.public_key,
                        "private_key": wallet.private_key,
                        "funds": blockchain.get_balance(),
                    },
                    indent=2,
                ),
                mimetype="application/json",
            ),
            201,
        )
    else:
        return (
            Response(
                json.dumps(
                    {
                        "message": "Loading the keys failed",
                        "public_key": None,
                        "private_key": None,
                        "funds": None,
                    },
                    indent=2,
                ),
                mimetype="application/json",
            ),
            500,
        )


@app.route("/chain", methods=["GET"])
def get_chain():
    dict_chain = [block.__dict__.copy() for block in blockchain.get_chain()]

    for dict_block in dict_chain:
        dict_block["transactions"] = [
            tx.__dict__.copy() for tx in dict_block["transactions"]
        ]

    return (
        Response(json.dumps(dict_chain, indent=2), mimetype="application/json"),
        200,
    )


@app.route("/add_transaction", methods=["POST"])
def add_transaction():
    if wallet.public_key == None:
        return jsonify(response={"message": "No wallet set up"}), 400

    values = request.form.to_dict()

    if len(values) == 0:
        values = request.get_json()

    if not values:
        return jsonify({"messsage": "No data found"}), 400

    required_fileds = ["recipient", "amount"]

    if not all(field in values for field in required_fileds):
        return jsonify({"message": "Required data is missing"}), 400

    amount = float(values["amount"])
    signature = wallet.sign_transaction(wallet.public_key, values["recipient"], amount)

    error = blockchain.add_transaction(
        values["recipient"], wallet.public_key, signature, amount
    )

    if error == None:
        return (
            Response(
                json.dumps(
                    {
                        "message": "Success",
                        "transaction": {
                            "sender": wallet.public_key,
                            "recipient": values["recipient"],
                            "amount": values["amount"],
                            "signature": signature,
                        },
                        "funds": blockchain.get_balance(),
                    },
                    indent=2,
                ),
                mimetype="application/json",
            ),
            201,
        )
    else:
        return jsonify({"message": error})


@app.route("/balance", methods=["GET"])
def balance():
    balance = blockchain.get_balance()

    if balance == None:
        return (
            Response(
                json.dumps(
                    {
                        "funds": balance,
                        "message": "Failed",
                        "wallet_set_up": wallet.public_key != None,
                    },
                    indent=2,
                ),
                mimetype="application/json",
            ),
            500,
        )
    else:
        return (
            Response(
                json.dumps(
                    {
                        "funds": balance,
                        "message": "OK",
                        "wallet_set_up": wallet.public_key != None,
                    },
                    indent=2,
                ),
                mimetype="application/json",
            ),
            500,
        )


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
            "funds": blockchain.get_balance(),
            "wallet_set_up": wallet.public_key != None,
        }
    else:
        return {
            "message": "Adding a block failed",
            "block": None,
            "funds": None,
            "wallet_set_up": wallet.public_key != None,
        }


@app.route("/mine", methods=["POST"])
def api_mine():
    dictionary = mine()

    if dictionary["block"] == None:
        http_code = 500
    else:
        http_code = 200

    return (
        Response(json.dumps(dictionary, indent=2), mimetype="application/json"),
        http_code,
    )


@app.route("/node", methods=["POST"])
def add_node():
    values = request.form.to_dict()

    if len(values) == 0:
        values = request.get_json()

    if not values:
        return jsonify({"message": "No data"}), 400
    if "node" not in values:
        return jsonify({"message": "No node data found"}), 400

    blockchain.add_peer_node(values["node"])

    return jsonify({"message": "OK", "nodes": blockchain.get_peer_nodes()}), 200


@app.route("/node/<node_url>", methods=["DELETE", "POST"])
def remove_node(node_url):
    if node_url == "" or node_url == None:
        return jsonify({"message": "No data"}), 400

    blockchain.remove_peer_node(node_url)

    return jsonify({"message": "OK", "nodes": blockchain.get_peer_nodes()}), 200


@app.route("/nodes", methods=["GET"])
def get_nodes():
    return jsonify({"nodes": blockchain.get_peer_nodes()}), 200


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-p", "--port", default=5000)
    port = parser.parse_args().port

    print("Starting on a port: " + str(port))
    app.run(host="0.0.0.0", port=port)
