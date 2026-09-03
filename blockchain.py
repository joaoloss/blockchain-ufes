import hashlib
import json
from time import time

DIFFICULTY = 4

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        
        # Create the genesis block
        self.new_block(previous_hash='1', proof=100)

    def new_block(self, proof, previous_hash=None):
        """
        Create a new Block in the Blockchain
        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of previous Block
        :return: <dict> New Block
        """
        sha_current_transactions = self.hash(self.current_transactions)
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
            'sha_current_transactions': sha_current_transactions,
            'transactions': self.current_transactions,
        }

        # Reinicia a lista de transações atuais
        self.current_transactions = []

        self.chain.append(block)
        return block
    
    def new_transaction(self, sender, recipient, amount):
        """
        Create a new transaction to go into the next mined Block
        :param sender: <str> Address of the Sender
        :param recipient: <str> Address of the Recipient
        :param amount: <int> Amount
        """
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
    
    @staticmethod
    def hash(stuff):
        """
        Create a SHA-256 hash of the given object
        :param stuff: anything serializable
        :return: <str> SHA-256 hash hexdigest
        """
        block_string = json.dumps(stuff, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
    
    def proof_of_work(self, last_proof, sha_current_transactions):
        """
                Simple Proof of Work algorithm:
                - Find a number p' such that hash(last_proof, sha_current_transactions, p') contains
                    DIFFICULTY leading zeroes
                - last_proof is the previous proof, and p' is the new proof
                :param last_proof: <int>
                :param sha_current_transactions: <str>
                :return: <int>
        """
        proof = 0
        while self.valid_proof(last_proof, sha_current_transactions, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, sha_current_transactions, proof):
        """
        Validate the Proof: does hash(last_proof, sha_current_transactions, proof)
        contain DIFFICULTY leading zeroes?
        :param last_proof: <int> Previous proof
        :param sha_current_transactions: <str> Hash of the current transactions
        :param proof: <int> Current proof
        :return: <bool> True if correct, False otherwise
        """
        guess = f'{last_proof}{sha_current_transactions}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:DIFFICULTY] == "0" * DIFFICULTY
    
    @property
    def last_block(self):
        return self.chain[-1]


    def valid_chain(self, chain):
        """
        Determine if a given blockchain is valid

        :param chain: <list> A blockchain
        :return: <bool> True if valid, False if not
        """
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n-----------\n")
            # Check that the hash of the block is correct
            if block['previous_hash'] != self.hash(last_block):
                print("Previous hash is not correct")
                return False

            # Check that the Proof of Work is correct
            if not self.valid_proof(last_block['proof'], block['sha_current_transactions'], block['proof']):
                print("Proof of work is not correct")
                return False

            last_block = block
            current_index += 1

        return True

    def mine(self):
        # We must receive a reward for finding the proof.
        # For now, we're not in a network, so the only beneficiary is this node.
        # The sender is "0" to signify that this node has mined a new coin.
        self.new_transaction(
            sender="0",
            # write your name here, instead of nakamoto
            recipient="joaoloss",
            amount=1,
        )
        sha_current_transactions = self.hash(self.current_transactions)

        last_block = self.last_block
        proof = self.proof_of_work(last_block["proof"], sha_current_transactions)

        # Mine the new block by adding it to the chain
        previous_hash = self.hash(last_block)
        self.new_block(proof, previous_hash)

    




