# Initializing out empty blockchain List[]
MINING_REWARD = 10

genisis_block = {
    "previous_hash": "",
    "index": 0,
    "transactions": []
}
blockchain = [genisis_block]
open_transactions = []
owner = "Hari"
participants = set()

def hash_block(block):
    # list comprehensions [element for element in list]
    return "-".join([str(block[key]) for key in block])

def get_balances(participant):
    tx_sender = [[tx['amount'] for tx in block['transactions'] if tx['sender'] == participant] for block in blockchain]
    open_tx_sender = [tx["amount"] for tx in open_transactions if tx['sender'] == participant]
    tx_sender.append(open_tx_sender)
    amount_sent = 0
    for tx in tx_sender:
        if len(tx) > 0:
            amount_sent += tx[0]
    tx_recipient = [[tx['amount'] for tx in block['transactions'] if tx['recipient'] == participant] for block in blockchain]
    amount_recive = 0
    for tx in tx_recipient:
        if len(tx) > 0:
            amount_recive += tx[0]
    return amount_recive - amount_sent

def get_last_blockchain_value():
    """ Returns the last value of the current blockchain """
    if len(blockchain) < 1:
        return None
    return blockchain[-1]

def verify_transaction(transaction):
    sender_balance = get_balances(transaction['sender'])
    return sender_balance >= transaction['amount']

# This function accepts two arguments
# One required one transamount and other one last_transaction is optional
def add_transaction(recipient, sender=owner, amount=1.0,):
    """ Adding transaction to our Blockchain
        
        Params:
            :sender: The sender of the coins.
            :recipient: The recipient of the coins
            :amount: The amount of coins sent with the transaction (default [1]).
    """
    transaction = {
        "sender": sender,
        "recipient": recipient,
        "amount": amount
    }
    if verify_transaction(transaction):
        open_transactions.append(transaction)
        participants.add(sender)
        participants.add(recipient)
        return True
    return False

def mine_block():
    last_block = blockchain[-1]
    reward_transaction = {
        "sender": "MINNER",
        "recipient": owner,
        "amount": MINING_REWARD
    }
    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)
    hashed_block = hash_block(last_block)
    block = {
        "previous_hash": hashed_block,
        "index": len(blockchain),
        "transactions": copied_transactions
    }
    blockchain.append(block)
    return True

def get_transaction_value():
    # Get the user input and transform it float and store it
    tx_recipient = input("Enter the recipient of the transaction: ")
    tx_amount = float(input("Your transaction amount: "))
    return (tx_recipient, tx_amount)

def get_user_choice():
    user_choice = input("Your choice: ")
    return user_choice

# This will output the blockchain blocks in loop
def print_blockchain_blocks():
    for block in blockchain:
        print(block)
    else:
        print("-" * 30)

def verify_chain():
    """ Verify the current blockchain and returns True if it's valid False if not"""
    for (index, block) in enumerate(blockchain):
        if index == 0:
            continue
        if block['previous_hash'] != hash_block(blockchain[index - 1]):
            return False
    return True

waiting_for_input = True            

# Adding while loop for asking user input
while waiting_for_input:
    print("Please enter your choice")
    print("1: Add a new transaction value")
    print("2: Mine Block")
    print("3: Output the blockchain blocks")
    print("4: List all senders/recipients")
    print("m: Manipulate the blockchain")
    print("q: Quit")
    user_choice = get_user_choice()
    if user_choice == "1":
        tx_data = get_transaction_value()
        recipient, amount = tx_data
        if add_transaction(recipient, amount=amount):
            print("Transaction success!")
        else:
            print("Transaction Failed!")
        print(open_transactions)
    elif user_choice == "2":
        if mine_block():
            open_transactions = []
    elif user_choice == "3":
        print_blockchain_blocks()
    elif user_choice == "4":
        print(participants)
    elif user_choice == "m":
        if len(blockchain) >= 1:
            blockchain[0] = {
                "previous_hash": "",
                "index": 0,
                "transactions": [{
                    "sender" : "Chiris",
                    "recipient": "Max",
                    "amount" : 200.00
                }]
            }
    elif user_choice == "q":
        waiting_for_input = False
    else:
        print("Input is invalid, please pick a value from a list.")

    if not verify_chain():
        print_blockchain_blocks()
        print("Invalid Blockchain!")
        break

    print(get_balances(owner))
else:
    print("User Left!")
print ("Done!")