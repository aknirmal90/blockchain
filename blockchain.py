import hashlib
import urllib3
import requests


class BlockChain(object):

    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.nodes = set()

        # genesis block - aka first block premined on the blockchain
        self.add_block(proof=1, previous_hash=100)

    @property
    def previous_block(self):
        """
        returns the most recently mined block
        """
        return self.chain[-1]

    def add_transaction(self, _from, _to, _amount):
        """
        appends a new transaction to be mined in the new block
        """
        transaction = {
            'sender': _from,
            'reciever': _to,
            'amount': _amount
        }
        self.current_transactions.append(transaction)
        return len(self.chain) + 1

    def add_block(self, proof, previous_hash):
        """
        generates a block and adds it to the blockchain
        """
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash
        }
        self.current_transactions = []
        self.chain.append(block)
        return block

    def get_proof_of_work(self, previous_proof):
        """
        iteratively verify if possible integers are the required POW
        """
        candidate_proof = 0
        while not self.verify_proof_of_work(previous_proof, candidate_proof):
            candidate_proof += 1
        return candidate_proof

    def verify_proof_of_work(self, previous_proof, proof):
        """
        the POW value we want to identify is one which when hashed with the POW of the previous
        block yields a hash whose first 4 characters are `0`
        """
        return hashlib.sha256(f'{previous_proof}{proof}'.encode()).hexdigest()[:4] == '0000'

    def hash(self, block):
        """
        hashes the contents of a block
        """
        message = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(message).hexdigest().replace('-', '')

    def register_node(self, url):
        """
        adds a new node to the list of registered nodes. the node with the
        largest chain is considered to be the blockchain
        """
        new_node = urllib3.util.parse_url(url).netloc
        self.nodes.add(new_node)
        return new_node

    def is_valid_chain(self, chain):
        """
        iterates over all blocks and verifies integrity of each block by
        - checking if it has an appropriate Proof of Work value
        - checking if hash of the previous block is correct
        """
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            current_block = chain[current_index]
            if not current_block['previous_hash'] == blockchain.hash(last_block):
                return False

            if not verify_proof_of_work(last_block['proof'], current_block['proof']):
                return False

            last_block = current_block
            current_index += 1
        return True

    def resolve_conflicts(self):
        """
        allows this node to converge towards the longest chain
        """

        new_chain = None
        max_length = len(self.chain)
        for node in self.nodes:
            url = f'http://{node}/chain/list'
            response = requests.get(url)

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['blockchain']

                if max_length > length and self.is_valid_chain(chain):
                    max_length = length
                    new_chain = chain

        if new_chain:
            self.chain = new_chain
            return True
        return False
