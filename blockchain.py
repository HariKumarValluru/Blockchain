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
    return blockchain[-1]

# This function accepts two arguments
# One required one transamount and other one last_transaction is optional
def add_value(transaction_amount, last_transaction=[[1]]):
    """ Adding transaction to our Blockchain
        
        Arguments:
            :transaction_amount: The amount should be added.
            :last_transaction: The last blockchain value (default [1]).

    """
    blockchain.append([last_transaction,transaction_amount])

def get_user_input():
    # Get the user input and transform it float and store it
    return float(input("Your transaction amount: "))

# Get the first tranaction value and add it to the blockchain
tx_amount = get_user_input()
add_value(tx_amount)

# Get the second tranaction value and add it to the blockchain
# tx_amount = get_user_input()
# add_value(last_transaction=get_last_blockchain_value(),transaction_amount=tx_amount)

# Adding while loop for asking user input
while True:
    tx_amount = get_user_input()
    add_value(last_transaction=get_last_blockchain_value(),transaction_amount=tx_amount)

    # Output the blockchain value to console
    # print(blockchain)

    # Outputting the blockchain using for loop
    for block in blockchain:
        print("Outputing the Block")
        print(block)

print ("Done!")