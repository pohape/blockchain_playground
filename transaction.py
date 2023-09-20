from collections import OrderedDict
from utility.printable import Printable


class Transaction(Printable):
    def __init__(self, transactionArray):
        self.sender = transactionArray["sender"]
        self.recipient = transactionArray["recipient"]
        self.amount = transactionArray["amount"]
        self.signature = transactionArray["signature"]

    def to_ordered_dict(self):
        return OrderedDict(
            [
                ("sender", self.sender),
                ("recipient", self.recipient),
                ("amount", self.amount),
                ("signature", self.signature),
            ]
        )
