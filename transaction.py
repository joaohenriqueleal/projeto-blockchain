import hashlib
import time
import json


class Transaction:

    def __init__(self, sender, receiver, value):
        self.sender = sender
        self.receiver = receiver
        self.value = value
        self.timestamp = time.time_ns()
        self.transaction_hash = self.calculate_hash()

    def calculate_hash(self):
        transaction_data = {
            "sender": self.sender,
            "receiver": self.receiver,
            "value": self.value,
            "timestamp": self.timestamp,
        }
        transaction_json = json.dumps(transaction_data, sort_keys=True)
        return hashlib.sha256(transaction_json.encode()).hexdigest()

    def transaction_to_dict(self):
        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "value": self.value,
            "timestamp": self.timestamp,
            "transaction_hash": self.transaction_hash
        }
