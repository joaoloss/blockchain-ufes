import hashlib
import json
from time import time

DIFFICULTY = 4

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        
        # Criar o bloco gênesis
        self.new_block(previous_hash='1', proof=100)

    def new_block(self, proof, previous_hash=None):
        """
        Cria um novo bloco na Blockchain
        :param proof: <int> A prova fornecida pelo PoW
        :param previous_hash: (Opcional) <str> Hash do bloco anterior
        :return: <dict> Novo bloco
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
        Cria uma nova transação para ir para o próximo bloco minerado
        :param sender: <str> Endereço do remetente
        :param recipient: <str> Endereço do destinatário
        :param amount: <int> Quantidade
        """
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
    
    @staticmethod
    def hash(stuff):
        """
        Cria um hash SHA-256 de um bloco
        :param stuff: anything
        :return: <str> Hash do bloco
        """
        block_string = json.dumps(stuff, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
    
    def proof_of_work(self, last_proof, sha_current_transactions):
        """
        Algoritmo de prova de trabalho:
        - Encontre um número p' tal que hash(last_proof, sha_current_transactions, p') contenha 4 zeros à esquerda
        - p é a prova do bloco anterior , e p' é a nova prova
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
        Valida a prova: verifica se hash(last_proof, proof) contém 4 zeros à esquerda
        :param last_proof: <int> Prova anterior
        :param sha_current_transactions: <str> Hash das transações atuais
        :param proof: <int> Prova atual
        :return: <bool> TRUE se correto, FALSE se não
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
        # Devemos receber uma recompensa por encontrar a prova.
        # Por enquanto, não estamos em rede, então o único beneficiário é ELE
        # O remetente é "0" para significar que este nó minerou uma nova moeda.
        self.new_transaction(
            sender="0",
            # escreva aqui seu nome, ao invés de nakamoto
            recipient="joaoloss",
            amount=1,
        )
        sha_current_transactions = self.hash(self.current_transactions)

        last_block = self.last_block
        proof = self.proof_of_work(last_block["proof"], sha_current_transactions)

        # Minera o novo bloco adicionando-o à cadeia
        previous_hash = self.hash(last_block)
        self.new_block(proof, previous_hash)

    




