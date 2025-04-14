from transaction import *
import time
import hashlib
import json


class Block:

    def __init__(self, index, previous_hash, difficulty):
        self.index = index
        self.transactions = []
        self.timestamp = time.time_ns()
        self.difficulty = difficulty
        self.nonce = 0
        self.previous_hash = previous_hash
        self.hash = "0"

    def calculate_hash(self):
        block_data = {
            "index": self.index,
            "transactions": self.transactions,
            "timestamp": self.timestamp,
            "difficulty": self.difficulty,
            "nonce": self.nonce,
            "previous_hash": self.previous_hash
        }
        block_string = json.dumps(block_data, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self):
        prefix = "0" * self.difficulty
        while True:
            hash_attempt = self.calculate_hash()
            if hash_attempt.startswith(prefix):
                self.hash = hash_attempt
                break
            else:
                self.nonce += 1

    def block_to_dict(self):
        return {
            "index": self.index,
            "transactions": self.transactions,
            "timestamp": self.timestamp,
            "difficulty": self.difficulty,
            "nonce": self.nonce,
            "previous_hash": self.previous_hash,
            "hash": self.hash
        }

    def add_transaction(self, transaction: Transaction):
        self.transactions.append(transaction.transaction_to_dict())

    def print_block(self):
        print('-' * 80)
        print(f'Index: {self.index}')
        print(f'Transactions: {self.transactions}')
        print(f'Timestamp: {self.timestamp}')
        print(f'Difficulty: {self.difficulty}')
        print(f'Nonce: {self.nonce}')
        print(f'Previous_hash: {self.previous_hash}')
        print(f'Hash: {self.hash}')
        print('-' * 80)
