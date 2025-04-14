from block import *
from transaction import *
import threading
import os


class Blockchain:

    def __init__(self):
        self.chain = []
        self.load_chain()
        self.pending_blocks = []
        self.difficulty = 4 # initial difficulty.
        self.create_genesis_block()

    def create_genesis_block(self):
        if len(self.chain) == 0:
            genesis_block = Block(0, "0", self.difficulty)
            self.add_block_to_pending(genesis_block)

    def add_block_to_pending(self, block: Block):
        if len(self.pending_blocks) == 0:
            self.pending_blocks.append(block)
            def monitor_block():
                while True:
                    if block.nonce != 0 and block.hash != "0":
                        print(f"Bloco {block.index} minerado! Adicionando à blockchain...")
                        self.add_block_to_chain()
                        self.pending_blocks.remove(block)
                        break

            threading.Thread(target=monitor_block).start()
        else:
            print(f"\033[;31mO bloco {self.pending_blocks[0].index} ainda não foi minerado!\033[m")

    def add_block_to_chain(self):
        if self.pending_blocks and self.pending_blocks[0].nonce != 0:
            self.chain.append(self.pending_blocks[0].block_to_dict())
            self.save_chain()
        else:
            print(f"O bloco {self.pending_blocks[0].index} ainda não está minerado!")

    def get_index(self):
        return len(self.chain)

    def get_previous_hash(self):
        if self.chain:
            return self.chain[-1]["hash"]
        return "0"

    def save_chain(self):
        with open('blockchain.json', 'w', encoding='utf-8') as blockchain_file:
            json.dump(self.chain, blockchain_file, ensure_ascii=False, indent=4)

    def load_chain(self):
        if os.path.exists('blockchain.json'):
            with open('blockchain.json', 'r', encoding='utf-8') as blockchain_file:
                self.chain = json.load(blockchain_file)
        else:
            self.save_chain()

    def validate_block(self, block, previous_block=None):
        if not previous_block:
            if block["previous_hash"] != "0":
                return False
            block_data = {
                "index": block["index"],
                "transactions": block["transactions"],
                "timestamp": block["timestamp"],
                "difficulty": block["difficulty"],
                "nonce": block["nonce"],
                "previous_hash": block["previous_hash"]
            }
            block_string = json.dumps(block_data, sort_keys=True)
            hash_calculado = hashlib.sha256(block_string.encode()).hexdigest()
            if hash_calculado != block["hash"]:
                return False
            for transaction in block["transactions"]:
                transaction_data = {
                    "sender": transaction["sender"],
                    "receiver": transaction["receiver"],
                    "value": transaction["value"],
                    "timestamp": transaction["timestamp"],
                }
                transaction_json = json.dumps(transaction_data, sort_keys=True)
                transaction_hash_calculado = hashlib.sha256(transaction_json.encode()).hexdigest()
                if transaction["transaction_hash"] != transaction_hash_calculado:
                    return False
        else:
            if block["previous_hash"] != previous_block["hash"]:
                return False
            block_data = {
                "index": block["index"],
                "transactions": block["transactions"],
                "timestamp": block["timestamp"],
                "difficulty": block["difficulty"],
                "nonce": block["nonce"],
                "previous_hash": block["previous_hash"]
            }
            block_string = json.dumps(block_data, sort_keys=True)
            hash_calculado = hashlib.sha256(block_string.encode()).hexdigest()
            if hash_calculado != block["hash"]:
                return False
            for transaction in block["transactions"]:
                transaction_data = {
                    "sender": transaction["sender"],
                    "receiver": transaction["receiver"],
                    "value": transaction["value"],
                    "timestamp": transaction["timestamp"],
                }
                transaction_json = json.dumps(transaction_data, sort_keys=True)
                transaction_hash_calculado = hashlib.sha256(transaction_json.encode()).hexdigest()
                if transaction["transaction_hash"] != transaction_hash_calculado:
                    return False
        return True

    def chain_is_valid(self):
        for i in range(0, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if i == 0:
                if not self.validate_block(current_block):
                    return False
            else:
                if not self.validate_block(current_block, previous_block):
                    return False
        return True

    def adjust_difficulty(self):
        if len(self.chain) > 0 and len(self.chain) % 10 == 0:
            new_difficulty = len(self.chain) // 10 # ajusta a dificuldade a cada 10 blocos.
            if new_difficulty >= 4:
                self.difficulty = new_difficulty

    def print_chain(self):
        for block in self.chain:
            print('-' * 80)
            print(f'Index: {block["index"]}')
            print(f'Transactions: {block["transactions"]}')
            print(f'Timestamp: {block["timestamp"]}')
            print(f'Difficulty: {block["difficulty"]}')
            print(f'Nonce: {block["nonce"]}')
            print(f'Previous_hash: {block["previous_hash"]}')
            print(f'Hash: {block["hash"]}')
            print('-' * 80)
            print('⛓️'.center(80))
            print('⛓️'.center(80))
        if self.pending_blocks:
            print('\033[;33m-\033[m' * 80)
            print('\033[;33mActual Pending Block: \033[m')
            print('\033[;33m-\033[m' * 80)
            print(f'\033[;33mIndex: {self.pending_blocks[0].index}\033[m')
            print(f'\033[;33mTransactions: {self.pending_blocks[0].transactions}\033[m')
            print(f'\033[;33mTimestamp: {self.pending_blocks[0].timestamp}\033[m')
            print(f'\033[;33mDifficulty: {self.pending_blocks[0].difficulty}\033[m')
            print(f'\033[;33mNonce: {self.pending_blocks[0].nonce}\033[m')
            print(f'\033[;33mPrevious_hash: {self.pending_blocks[0].previous_hash}\033[m')
            print(f'\033[;33mHash: {self.pending_blocks[0].hash}\033[m')
            print('\033[;33m-\033[m' * 80)
