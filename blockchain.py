# blockchain = [[1]]

# def add_value():
#     blockchain.append([blockchain[-1],23])
#     print(blockchain)

# add_value()
# add_value()
# add_value()

# blockchain = [[1]]

# def add_value(transaction_amount):
#     blockchain.append([blockchain[-1], transaction_amount])
#     print(blockchain)

# add_value(2)

# add_value(16.8)

# add_value(5.9)

# blockchain = [[1]]

# def get_last_blockchain_value():
#     return blockchain[-1]

# def add_value(transaction_amount):
#     blockchain.append([get_last_blockchain_value(),transaction_amount])

# add_value(5)
# add_value(47.4)

# print(blockchain)

# blockchain = []

# def get_last_blockchain_value():
#     return blockchain[-1]

# def add_value(transaction_amount, last_tranaction=[[1]]):
#     blockchain.append([last_tranaction,transaction_amount])

# add_value(4)
# add_value(4,get_last_blockchain_value())

# print(blockchain)


# blockchain = []

# def get_last_blockchain_value():
#     return blockchain[-1]

# def add_value(transaction_amount, last_transaction=[[1]]):
#     blockchain.append([last_transaction,transaction_amount])

# add_value(55)
# add_value(last_transaction=get_last_blockchain_value(),transaction_amount=411)

# print(blockchain)

# Initializing out empty blockchain List[]
blockchain = []

def get_last_blockchain_value():
    """ Returns the last value of the current blockchain """
    if len(blockchain) < 1:
        return None
    return blockchain[-1]

# This function accepts two arguments
# One required one transamount and other one last_transaction is optional
def add_transaction(transaction_amount, last_transaction=[1]):
    """ Adding transaction to our Blockchain
        
        Arguments:
            :transaction_amount: The amount should be added.
            :last_transaction: The last blockchain value (default [1]).

    """
    if last_transaction == None:
        last_transaction = [1]
    blockchain.append([last_transaction,transaction_amount])

def get_transaction_value():
    # Get the user input and transform it float and store it
    return float(input("Your transaction amount: "))

def get_user_choice():
    user_choice = input("Your choice: ")
    return user_choice

# Get the first tranaction value and add it to the blockchain
# tx_amount = get_transaction_value()
# add_value(tx_amount)

# Get the second tranaction value and add it to the blockchain
# tx_amount = get_transaction_value()
# add_value(last_transaction=get_last_blockchain_value(),transaction_amount=tx_amount)

# This will output the blockchain blocks in loop
def print_blockchain_blocks():
    for block in blockchain:
        print(block)

def verify_chain():
    block_index = 0
    is_valid = True
    for block in blockchain:
        if block_index == 0:
            block_index += 1
            continue
        elif block[0] == blockchain[block_index - 1]:
            is_valid = True
        else:
            is_valid = False
            break
        block_index += 1
    return is_valid
            

# Adding while loop for asking user input
while True:
    print("Please enter your choice")
    print("1: Add a new transaction value")
    print("2: Output the blockchain blocks")
    print("m: Manipulate the blockchain")
    print("q: Quit")
    user_choice = get_user_choice()
    if user_choice == "1":
        tx_amount = get_transaction_value()
        add_transaction(tx_amount, get_last_blockchain_value())
    elif user_choice == "2":
        # Output the blockchain value to console
        # print(blockchain)
        print_blockchain_blocks()
    elif user_choice == "m":
        if len(blockchain) >= 1:
            blockchain[0] = [2]
    elif user_choice == "q" :
        break

    else:
        print("Input is invalid, please pick a value from a list.")

    if not verify_chain():
        print("Invalid Blockchain!")
        break

print ("Done!")