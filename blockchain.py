from functools import reduce
import hashlib
import json
import pickle

# Import two functions from our hash_util.py file. Omit the ".py" in the import
from hash_util import hash_string_256, hash_block
from block import Block
from transaction import Transaction

# The reward we give to miners (for creating a new block)
MINING_REWARD = 10

# Initializing our (empty) blockchain list
blockchain = []
# Unhandled transactions
open_transactions = []
# We are the owner of this blockchain node, hence this is our identifier (e.g. for sending coins)
owner = "Hari"
# Registered participants: Ourself + other people sending/ receiving coins
participants = {owner}

def load_data():
    global blockchain
    global open_transactions
    """Initialize blockchain + open transactions data from a file."""
    try:
        with open("blockchain.txt", mode="r") as f:
            # file_content = pickle.loads(f.read())
            file_content = f.readlines()
            # blockchain = file_content['chain']
            # open_transactions = file_content['ot']
            blockchain = json.loads(file_content[0][:-1])
            # We need to convert  the loaded data because Transactions should use OrderedDict
            blockchain = [
                Block(block['index'], block['previous_hash'],
                    [ 
                        Transaction(tx['sender'], tx['recipient'], tx['amount']) for tx in block['transactions']
                    ], 
                    block['proof'], block['timestamp']
                )
                for block in blockchain
            ]
            open_transactions = json.loads(file_content[1])
            # We need to convert  the loaded data because Transactions should use OrderedDict
            open_transactions = [
                Transaction(tx['sender'], tx['recipient'], tx['amount'])
                for tx in open_transactions
            ]
            # print(file_content)
    except (IOError, IndexError):
        # Our starting block for the blockchain
        genesis_block = Block(0, "", [], 100, 0)
        # Initializing our (empty) blockchain list
        blockchain = [genesis_block]
        # Unhandled transactions
        open_transactions = []
    finally:
        print("Cleanup!!")

load_data()

def save_data():
    """Save blockchain + open transactions snapshot to a file."""
    try:
        with open("blockchain.txt", mode="w") as f:
            savable_chain = [block.__dict__ for block in [Block(block_el.index, block_el.previous_hash, [tx.__dict__ for tx in block_el.transactions] ,block_el.proof, block_el.timestamp) for block_el in blockchain]]
            f.write(json.dumps(savable_chain))
            f.write("\n")
            savable_tx = [tx.__dict__ for tx in open_transactions]
            f.write(json.dumps(savable_tx))
            # save_data = {
            #     'chain': blockchain,
            #     'ot': open_transactions
            # }
            # f.write(pickle.dumps(save_data))
    except IOError:
        print("Saving Failed!")
    

def valid_prof(transactions, previous_hash, proof):
    """Validate a proof of work number and see if it solves the puzzle algorithm (two leading 0s)

    Arguments:
        :transactions: The transactions of the block for which the proof is created.
        :previous_hash: The previous block's hash which will be stored in the current block.
        :proof: The proof number we're testing.
    """
    # Create a string with all the hash inputs
    guess = (str([tx.to_ordered_dict() for tx in transactions]) + str(previous_hash) + str(proof)).encode()
    # Hash the string
    # IMPORTANT: This is NOT the same hash as will be stored in the previous_hash. It's a not a block's hash. It's only used for the proof-of-work algorithm.
    guess_hash = hash_string_256(guess)
    # Only a hash (which is based on the above inputs) which starts with two 0s is treated as valid
    # This condition is of course defined by you. You could also require 10 leading 0s - this would take significantly longer (and this allows you to control the speed at which new blocks can be added)
    return guess_hash[0:2] == "00"

def proof_of_work():
    """Generate a proof of work for the open transactions, the hash of the previous block and a random number (which is guessed until it fits)."""
    last_block = blockchain[-1]
    last_hash = hash_block(last_block)
    proof = 0
    # Try different PoW numbers and return the first valid one
    while not valid_prof(open_transactions, last_hash, proof):
        proof += 1
    return proof

def get_balances(participant):
    """Calculate and return the balance for a participant.

    Arguments:
        :participant: The person for whom to calculate the balance.
    """
    # Fetch a list of all sent coin amounts for the given person (empty lists are returned if the person was NOT the sender)
    # This fetches sent amounts of transactions that were already included in blocks of the blockchain
    tx_sender = [[tx.amount for tx in block.transactions 
                    if tx.sender == participant] for block in blockchain]
    # Fetch a list of all sent coin amounts for the given person (empty lists are returned if the person was NOT the sender)
    # This fetches sent amounts of open transactions (to avoid double spending)
    open_tx_sender = [tx.amount for tx in open_transactions if tx.sender == participant]
    tx_sender.append(open_tx_sender)
    amount_sent = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) 
                        if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0)
    # This fetches received coin amounts of transactions that were already included in blocks of the blockchain
    # We ignore open transactions here because you shouldn't be able to spend coins before the transaction was confirmed + included in a block
    tx_recipient = [[tx.amount for tx in block.transactions 
                        if tx.recipient == participant] for block in blockchain]
    amount_recive = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) 
                        if len(tx_amt) > 0 else tx_sum + 0, tx_recipient, 0)
    # Return the total balance
    return amount_recive - amount_sent

def get_last_blockchain_value():
    """ Returns the last value of the current blockchain """
    if len(blockchain) < 1:
        return None
    return blockchain[-1]

def verify_transaction(transaction):
    """Verify a transaction by checking whether the sender has sufficient coins.

    Arguments:
        :transaction: The transaction that should be verified.
    """
    sender_balance = get_balances(transaction.sender)
    return sender_balance >= transaction.amount

# This function accepts two arguments.
# One required one (transaction_amount) and one optional one (last_transaction)
# The optional one is optional because it has a default value => [1]

def add_transaction(recipient, sender=owner, amount=1.0,):
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
    if verify_transaction(transaction):
        open_transactions.append(transaction)
        save_data()
        return True
    return False

def mine_block():
    """Create a new block and add open transactions to it."""
    # Fetch the currently last block of the blockchain
    last_block = blockchain[-1]
    # Hash the last block (=> to be able to compare it to the stored hash value)
    hashed_block = hash_block(last_block)
    proof = proof_of_work()
    # Miners should be rewarded, so let's create a reward transaction
    # reward_transaction = {
    #     "sender": "MINNER",
    #     "recipient": owner,
    #     "amount": MINING_REWARD
    # }
    reward_transaction = Transaction("MINNER", owner, MINING_REWARD)
    # Copy transaction instead of manipulating the original open_transactions list
    # This ensures that if for some reason the mining should fail, we don't have the reward transaction stored in the open transactions
    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)
    block = Block(len(blockchain), hashed_block, copied_transactions, proof)
    blockchain.append(block)
    return True

def get_transaction_value():
    """ Returns the input of the user (a new transaction amount) as a float. """
    # Get the user input, transform it from a string to a float and store it in user_input
    tx_recipient = input("Enter the recipient of the transaction: ")
    tx_amount = float(input("Your transaction amount: "))
    return (tx_recipient, tx_amount)

def get_user_choice():
    """Prompts the user for its choice and return it."""
    user_choice = input("Your choice: ")
    return user_choice

# This will output the blockchain blocks in loop
def print_blockchain_blocks():
    """ Output all blocks of the blockchain. """
    # Output the blockchain list to the console
    for block in blockchain:
        print(block)
    else:
        print("-" * 30)

def verify_chain():
    """ Verify the current blockchain and returns True if it's valid False if not"""
    for (index, block) in enumerate(blockchain):
        if index == 0:
            continue
        if block.previous_hash != hash_block(blockchain[index - 1]):
            return False
        if not valid_prof(block.transactions[:-1], block.previous_hash, block.proof):
            print("Proof of Work is invalid!")
            return False
    return True

def verify_transactions():
    """Verifies all open transactions."""
    return all([verify_transaction(tx) for tx in open_transactions])

waiting_for_input = True            

# A while loop for the user input interface
# It's a loop that exits once waiting_for_input becomes False or when break is called
while waiting_for_input:
    print("Please enter your choice")
    print("1: Add a new transaction value")
    print("2: Mine Block")
    print("3: Output the blockchain blocks")
    print("4: Check transaction validity")
    # print("m: Manipulate the blockchain")
    print("q: Quit")
    user_choice = get_user_choice()
    if user_choice == "1":
        tx_data = get_transaction_value()
        recipient, amount = tx_data
        # Add the transaction amount to the blockchain
        if add_transaction(recipient, amount=amount):
            print("Transaction success!")
        else:
            print("Transaction Failed!")
        # print(open_transactions)
    elif user_choice == "2":
        if mine_block():
            open_transactions = []
            save_data()
    elif user_choice == "3":
        print_blockchain_blocks()
    elif user_choice == "4":
        if verify_transactions():
            print("All transactions are valid!")
        else:
            print("There are some transactions failed!")
    # elif user_choice == "m":
    #     # Make sure that you don't try to "hack" the blockchain if it's empty
    #     if len(blockchain) >= 1:
    #         blockchain[0] = {
    #             "previous_hash": "",
    #             "index": 0,
    #             "transactions": [{
    #                 "sender" : "Chiris",
    #                 "recipient": "Max",
    #                 "amount" : 200.00
    #             }]
    #         }
    elif user_choice == "q":
        # This will lead to the loop to exist because it's running condition becomes False
        waiting_for_input = False
    else:
        print("Input is invalid, please pick a value from a list.")

    if not verify_chain():
        # print_blockchain_blocks()
        print("Invalid Blockchain!")
        # Break out of the loop
        break

    print("Balance of {}: {:6.2f}".format(owner,get_balances(owner)))
else:
    print("User Left!")
print ("Done!")