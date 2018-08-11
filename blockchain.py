from functools import reduce
import hashlib
import json
import pickle

# Import two functions from our hash_util.py file. Omit the ".py" in the import
from hash_util import hash_block
from block import Block
from transaction import Transaction
from verification import Verification
# The reward we give to miners (for creating a new block)
MINING_REWARD = 10

class Blockchain:
    def __init__(self, hosting_node_id):
        # Our starting block for the blockchain
        self.genesis_block = Block(0, "", [], 100, 0)
        # Initializing our (empty) blockchain list
        self.chain = [self.genesis_block]
        # Unhandled transactions
        self.open_transactions = []
        self.load_data()
        self.hosting_node = hosting_node_id
# # We are the owner of this blockchain node, hence this is our identifier (e.g. for sending coins)
# owner = "Hari"
# Registered participants: Ourself + other people sending/ receiving coins
# participants = {owner}

    def load_data(self):
        """Initialize blockchain + open transactions data from a file."""
        try:
            with open("blockchain.txt", mode="r") as f:
                # file_content = pickle.loads(f.read())
                file_content = f.readlines()
                # blockchain = file_content['chain']
                # open_transactions = file_content['ot']
                self.chain = json.loads(file_content[0][:-1])
                # We need to convert  the loaded data because Transactions should use OrderedDict
                self.chain = [
                    Block(block['index'], block['previous_hash'],
                        [ 
                            Transaction(tx['sender'], tx['recipient'], tx['amount']) for tx in block['transactions']
                        ], 
                        block['proof'], block['timestamp']
                    )
                    for block in self.chain
                ]
                self.open_transactions = json.loads(file_content[1])
                # We need to convert  the loaded data because Transactions should use OrderedDict
                self.open_transactions = [
                    Transaction(tx['sender'], tx['recipient'], tx['amount'])
                    for tx in self.open_transactions
                ]
                # print(file_content)
        except (IOError, IndexError):
            print("Handled Exception")
        finally:
            print("Cleanup!!")

    def save_data(self):
        """Save blockchain + open transactions snapshot to a file."""
        try:
            with open("blockchain.txt", mode="w") as f:
                savable_chain = [block.__dict__ for block in [Block(block_el.index, block_el.previous_hash, [tx.__dict__ for tx in block_el.transactions] ,block_el.proof, block_el.timestamp) for block_el in self.chain]]
                f.write(json.dumps(savable_chain))
                f.write("\n")
                savable_tx = [tx.__dict__ for tx in self.open_transactions]
                f.write(json.dumps(savable_tx))
                # save_data = {
                #     'chain': blockchain,
                #     'ot': open_transactions
                # }
                # f.write(pickle.dumps(save_data))
        except IOError:
            print("Saving Failed!")

    def proof_of_work(self):
        """Generate a proof of work for the open transactions, the hash of the previous block and a random number (which is guessed until it fits)."""
        last_block = self.chain[-1]
        last_hash = hash_block(last_block)
        proof = 0
        # Try different PoW numbers and return the first valid one
        verifier = Verification()
        while not verifier.valid_prof(self.open_transactions, last_hash, proof):
            proof += 1
        return proof

    def get_balances(self):
        """Calculate and return the balance for a participant.
        """
        participant = self.hosting_node
        # Fetch a list of all sent coin amounts for the given person (empty lists are returned if the person was NOT the sender)
        # This fetches sent amounts of transactions that were already included in blocks of the blockchain
        tx_sender = [[tx.amount for tx in block.transactions 
                        if tx.sender == participant] for block in self.chain]
        # Fetch a list of all sent coin amounts for the given person (empty lists are returned if the person was NOT the sender)
        # This fetches sent amounts of open transactions (to avoid double spending)
        open_tx_sender = [tx.amount for tx in self.open_transactions if tx.sender == participant]
        tx_sender.append(open_tx_sender)
        amount_sent = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) 
                            if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0)
        # This fetches received coin amounts of transactions that were already included in blocks of the blockchain
        # We ignore open transactions here because you shouldn't be able to spend coins before the transaction was confirmed + included in a block
        tx_recipient = [[tx.amount for tx in block.transactions 
                            if tx.recipient == participant] for block in self.chain]
        amount_recive = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) 
                            if len(tx_amt) > 0 else tx_sum + 0, tx_recipient, 0)
        # Return the total balance
        return amount_recive - amount_sent

    def get_last_blockchain_value(self):
        """ Returns the last value of the current blockchain """
        if len(self.chain) < 1:
            return None
        return self.chain[-1]

    # This function accepts two arguments.
    # One required one (transaction_amount) and one optional one (last_transaction)
    # The optional one is optional because it has a default value => [1]

    def add_transaction(self, recipient, sender, amount=1.0,):
        """ Adding transaction to our Blockchain
            
            Params:
                :sender: The sender of the coins.
                :recipient: The recipient of the coins
                :amount: The amount of coins sent with the transaction (default [1]).
        """
        # transaction = {
        #     "sender": sender,
        #     "recipient": recipient,
        #     "amount": amount
        # }
        transaction = Transaction(sender, recipient, amount)
        verifier = Verification()
        if verifier.verify_transaction(transaction, self.get_balances):
            self.open_transactions.append(transaction)
            self.save_data()
            return True
        return False
 
    def mine_block(self):
        """Create a new block and add open transactions to it."""
        # Fetch the currently last block of the blockchain
        last_block = self.chain[-1]
        # Hash the last block (=> to be able to compare it to the stored hash value)
        hashed_block = hash_block(last_block)
        proof = self.proof_of_work()
        # Miners should be rewarded, so let's create a reward transaction
        # reward_transaction = {
        #     "sender": "MINNER",
        #     "recipient": owner,
        #     "amount": MINING_REWARD
        # }
        reward_transaction = Transaction("MINNER", self.hosting_node, MINING_REWARD)
        # Copy transaction instead of manipulating the original open_transactions list
        # This ensures that if for some reason the mining should fail, we don't have the reward transaction stored in the open transactions
        copied_transactions = self.open_transactions[:]
        copied_transactions.append(reward_transaction)
        block = Block(len(self.chain), hashed_block, copied_transactions, proof)
        self.chain.append(block)
        self.open_transactions = []
        self.save_data()
        return True