from flask import Flask, jsonify
import datetime

import jsonpickle

from blockchain import Blockchain
# 2. mining blockchain
# because python do not have singleton, we put all mining logic in blockchain module
# just regard the whole module as a singleton
app = Flask(__name__)
block_chain = Blockchain()


# mine a new block
@app.route("/mine_block", methods=['GET'])
def mine_block():
    data = {'timestamp': datetime.datetime.now()}
    block = block_chain.create_block(data=data)
    response = {'message': 'Congratulations, you have just mined a block!',
                'block index': block.block_index,
                'data': block.data,
                'nounce': block.nounce,
                'previous hash': block.prev_hash}
    print(response)
    return jsonify(response), 200


# get the full blockchain
@app.route("/get_chain", methods=['GET'])
def get_chain():
    # response = {'chain': block_chain.chain,
    #             'length': len(block_chain.chain)}
    response = {'chain': jsonpickle.encode(block_chain.chain, unpicklable=False),
                'length': len(block_chain.chain)}
    print(response)
    return jsonify(response), 200


# to see whether the blockchain is valid
@app.route("/validate", method=['GET'])
def validate():
    is_valid = block_chain.is_chain_valid()
    response = {}

    if is_valid:
        response = {'message': 'All good. The blockchain is valid.'}
    else:
        response = {'message': 'Problem! The blockchain is not valid.'}

    return jsonify(response), 200


# run the app
app.run(host='localhost', port='5000')