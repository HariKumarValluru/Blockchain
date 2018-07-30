# Initializing out empty blockchain List[]
genisis_block = {
    "previous_hash": "",
    "index": 0,
    "transactions": []
}
blockchain = []
open_transactions = []
owner = "Hari"

def get_last_blockchain_value():
    """ Returns the last value of the current blockchain """
    if len(blockchain) < 1:
        return None
    return blockchain[-1]

# This function accepts two arguments
# One required one transamount and other one last_transaction is optional
def add_transaction(recipient, sender=owner, amount=1.0,):
    """ Adding transaction to our Blockchain
        
        Params:
            :sender: The sender of the coins.
            :recipient: The recipent of the coins
            :amount: The amount of coins sent with the transaction (default [1]).
    """
    transaction = {
        "sender":sender,
        "recipient":recipient,
        "amount":amount
    }
    open_transactions.append(transaction)

def mine_block():
    last_block = blockchain[-1]
    block = {
        "previous_hash": "XYZ",
        "index": len(blockchain),
        "transactions": open_transactions
    }
    blockchain.append(block)

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
    is_valid = True
    for block_index in range(len(blockchain)):
        if block_index == 0:
            continue
        elif blockchain[block_index][0] == blockchain[block_index - 1]:
            is_valid = True
        else:
            is_valid = False
    return is_valid

waiting_for_input = True            

# Adding while loop for asking user input
while waiting_for_input:
    print("Please enter your choice")
    print("1: Add a new transaction value")
    print("2: Output the blockchain blocks")
    print("m: Manipulate the blockchain")
    print("q: Quit")
    user_choice = get_user_choice()
    if user_choice == "1":
        tx_data = get_transaction_value()
        recipient, amount = tx_data
        add_transaction(recipient, amount=amount)
        print(open_transactions)
    elif user_choice == "2":
        print_blockchain_blocks()
    elif user_choice == "m":
        if len(blockchain) >= 1:
            blockchain[0] = [2]
    elif user_choice == "q":
        waiting_for_input = False
    else:
        print("Input is invalid, please pick a value from a list.")

    if not verify_chain():
        print_blockchain_blocks()
        print("Invalid Blockchain!")
        break
else:
    print("User Left!")
print ("Done!")