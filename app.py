import time
import json
import uuid
from flask import Flask, jsonify, request
from blockhain import BlockChain


app = Flask(__name__)
blockchain = BlockChain()
node = uuid.uuid4().hex.replace('-','')


@app.route('/transaction/new', methods=['POST'])
def post_transaction():
    values = request.get_json()

    required_fields = ['sender', 'reciever', 'amount']
    if not (all([key in values for key in required_fields])):
        return jsonify('Request missing required parameter'), 400

    next_block = blockchain.add_transaction(
        _from=values['sender'],
        _to=values['reciever'],
        _amount=values['amount']
    )
    return jsonify(f'New transaction will be added to block #{next_block}'), 201


@app.route('/chain/list', methods=['GET'])
def get_chain():
    chain = blockchain.chain
    return jsonify({
        'blockchain': chain,
        'length': len(chain)
    }), 200


@app.route('/mine', methods=['POST'])
def post_block():
    previous_block = blockchain.previous_block
    previous_proof = previous_block['proof']
    previous_hash = blockchain.hash(previous_block)

    new_proof = blockchain.get_proof_of_work(previous_proof)

    # below add_transaction ensures that this node gets rewarded for mining this block
    blockchain.add_transaction(_from='0', _to=node, _amount=1)
    mined_block = blockchain.add_block(proof=new_proof, previous_hash=previous_hash)
    return jsonify(mined_block), 200


@app.route('/node/register', methods=['POST'])
def register_nodes():
    values = request.get_json()
    nodes = values.get('nodes')

    if not nodes:
        return jsonify('Provide a valid list of nodes'), 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'num_nodes': len(nodes)
    }
    return jsonify(response), 200


@app.route('/node/resolve', methods=['POST'])
def consensus():
    is_replaced = blockchain.resolve_conflicts()
    if is_replaced:
        response = {
            'message': 'Blockchain for node has been updated',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our node is the authoritative node',
            'chain': blockchain.chain
        }
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
