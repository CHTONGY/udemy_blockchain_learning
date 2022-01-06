# Module 2 - Create a Cryptocurrency

# Cryptocurrency = blockchain + transactions + consensus

# Importing the libraries
import datetime
import hashlib
import json
from flask import Flask, jsonify, request
from urllib.parse import urlparse
import requests
from uuid import uuid4

# Part 1 - Building a Blockchain


class Blockchain:

    def __init__(self):
        self.chain = []
        self.transactions = []
        self.create_block(proof=1, previous_hash='0')
        self.nodes = set()

    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash,
                 'transactions': self.transactions}
        self.transactions = []
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(
                str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(
                str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True

    # return the block index this transaction will be added into
    def add_transaction(self, sender, receiver, amount) -> int:
        self.transactions.append({
            'sender': sender,
            'receiver': receiver,
            'amount': amount
        })
        prev_block = self.get_previous_block()
        return prev_block['index'] + 1

    def add_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    # return whether replace chain
    def replace_chain(self) -> bool:
        network = self.nodes

        max_length = len(self.chain)
        longest_chain = None

        for node in network:
            response = requests.get(f'http://{node}/get_chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.is_chain_valid(chain):
                    longest_chain = chain
                    max_length = length

        if longest_chain:
            self.chain = longest_chain
            return True

        return False


# Part 2 - Mining our Blockchain

# Creating a Web App
app = Flask(__name__)

# create an address for node
node_address = str(uuid4()).replace('-', '')

# Creating a Blockchain
blockchain = Blockchain()

# Mining a new block


@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    blockchain.add_transaction(sender=node_address, receiver='BOB', amount=1)
    block = blockchain.create_block(proof, previous_hash)
    response = {'message': 'Congratulations, you just mined a block!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash'],
                'transactions': block['transactions']}
    return jsonify(response), 200

# Getting the full Blockchain


@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200

# Checking if the Blockchain is valid


@app.route('/is_valid', methods=['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message': 'All good. The Blockchain is valid.'}
    else:
        response = {
            'message': 'Houston, we have a problem. The Blockchain is not valid.'}
    return jsonify(response), 200


# add a new transaction to the blockchain
@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    req = request.get_json()
    transaction_keys = ['sender', 'receiver', 'amount']
    # check whether post json is valid
    if not all(key in req for key in transaction_keys):
        return 'Some elements of transaction are missing', 400
    
    # add into blockchain
    index = blockchain.add_transaction(sender=req['sender'], receiver=req['receiver'], amount=req['amount'])
    resp_json = {'message': f'This transaction will be added into Block {index}'}
    return jsonify(resp_json), 201


# Part3: Decentralizing blockchain

# connecting new node
@app.route('/connect_node', methods=['POST'])
def connect_node():
    req_json = request.get_json()
    nodes = req_json.get('nodes')   # use get() because it's possible that req json does not contain such key

    if not nodes:
        return 'No node', 400
    
    for node in nodes:
        blockchain.add_node(node)
    
    resp_json = {
        'message': 'All the nodes are now connected',
        'total_nodes': list(blockchain.nodes)
    }
    return jsonify(resp_json), 201

# replace chain by the longest chain
@app.route('/replace_chain', methods=['GET'])
def replace_chain():
    is_replaced = blockchain.replace_chain()
    resp_json = {}
    if is_replaced:
        resp_json = {
            'message': 'The chain on this node is replaced by the longest chain in network.',
            'new_chain': blockchain.chain
        }
    else:
        resp_json = {
            'message': 'All good. Do not need to be replaced.',
            'current_chain': blockchain.chain
        }
    
    return jsonify(resp_json), 200


# Running the app
app.run(host='127.0.0.1', port=5002)
