# Paste your version of blockchain.py from the client_mining_p
# folder here
# Paste your version of blockchain.py from the basic_block_gp
# folder here

import hashlib
import json
from time import time
from uuid import uuid4

from flask import Flask, jsonify, request

DIFFICULTY = 3

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # Create the genesis block
        self.new_block(previous_hash="==============", proof=100)

    def new_block(self, proof, previous_hash=None):
        
        block = {
            # TODO
            'index' : len(self.chain) + 1,
            'timestamp' : time(),
            'transactions' : self.current_transactions,
            'proof' : proof, 
            'previous_hash': previous_hash or self.hash(self.chain[-1])
        }
        # Reset the current list of transactions
        self.current_transactions = []
        # Append the chain to the block
        self.chain.append(block)
        # Return the new block
        return block

    def hash(self, block):
        

        # TODO: Create the block_string
        block_string = json.dumps(block, sort_keys=True).encode()
        # TODO: Hash this string using sha256
        hash = hashlib.sha256(block_string).hexdigest()

        # By itself, the sha256 function returns the hash in a raw string
        # that will likely include escaped characters.
        # This can be hard to read, but .hexdigest() converts the
        # hash to a string of hexadecimal characters, which is
        # easier to work with and understand

        # TODO: Return the hashed block string in hexadecimal format
        return hash

    @property
    def last_block(self):
        return self.chain[-1]

    # def proof_of_work(self, block):
        
    #     block_string = json.dumps(self.last_block, sort_keys=True)
    #     proof = 0
    #     while self.valid_proof(block_string, proof) is False:
    #         proof +=1

    #     return proof
        
        # return proof

    @staticmethod
    def valid_proof(block_string, proof):
              
        # return True or False
        guess = f'{block_string}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()

        return guess_hash[:DIFFICULTY] == '0' * DIFFICULTY

    def new_transaction(self, sender, recipient, amount):
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })
# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()

@app.route('/transactions/new', methods=['POST'])
def post_new_transaction():
    #handle non-json response
    try:
        values = request.get_json()
    except ValueError:
        print("Error:  Non-json response")
        print("Response returned:")
        print(request)
        return "Error"

    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        response = {'message': "Missing Values"}
        return jsonify(response), 400

    blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    message ={
        'block_index': blockchain.last_block['index'],
        'block': blockchain.last_block
    }

    return jsonify(message), 200

@app.route('/mine', methods=['POST'])
def mine():
    #Handle vlaues
    try:
        values = request.get_json()
    except ValueError:
        print("Error:  Non-json response")
        print("Response returned:")
        print(request)
        return "Error"
    required = ['proof', 'id']
    if not all(k in values for k in required):
        response = {'message': "Missing Values"}
        return jsonify(response), 400
            
    submitted_proof = values['proof']

    #Determine if proof is valid
    last_block = blockchain.last_block
    last_block_sting = json.dumps(last_block, sort_keys=True)
    if blockchain.valid_proof(last_block_sting, submitted_proof):

    # Run the proof of work algorithm to get the next proof
    # proof = blockchain.proof_of_work(blockchain.last_block)
    # Forge the new Block by adding it to the chain with the proof
        previous_hash = blockchain.hash(blockchain.last_block)
        new_block = blockchain.new_block(submitted_proof, previous_hash)
        # blockchain.new_block(proof, )
        blockchain.new_transaction("0", values['id'], 1)

        response = {
            # TODO: Send a JSON response with the new block
            'message': "New Block Forged",
            'block': new_block
        }

        return jsonify(response), 200
    else:
        response = {
            'message': "Proof invalid or already submited"
        }
        return jsonify(response), 200

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        # TODO: Return the chain and its current length
        'length': len(blockchain.chain),
        'chain': blockchain.chain
    }
    return jsonify(response), 200


@app.route('/last_block', methods=['GET'])
def return_last_block():
    response = {
        'last_block': blockchain.last_block
    }
    return jsonify(response), 200

# Run the program on port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
