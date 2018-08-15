from uuid import uuid4
from blockchain import Blockchain
from utility.verification import Verification
from wallet import Wallet

class Node:
    """The node which runs the local blockchain instance.
    
    Attributes:
        :id: The id of the node.
        :blockchain: The blockchain which is run by this node.
    """
    def __init__(self):
        # self.id = "Hari"
        self.wallet = Wallet()
        self.wallet.create_keys()
        self.blockchain = Blockchain(self.wallet.public_key)
    
    def get_transaction_value(self):
        """ Returns the input of the user (a new transaction amount) as a float. """
        # Get the user input, transform it from a string to a float and store it in user_input
        tx_recipient = input("Enter the recipient of the transaction: ")
        tx_amount = float(input("Your transaction amount: "))
        return (tx_recipient, tx_amount)

    def get_user_choice(self):
        """Prompts the user for its choice and return it."""
        user_choice = input("Your choice: ")
        return user_choice

    # This will output the blockchain blocks in loop
    def print_blockchain_blocks(self):
        """ Output all blocks of the blockchain. """
        # Output the blockchain list to the console
        for block in self.blockchain.get_chain():
            print(block)
        else:
            print("-" * 30)
    
    def listen_for_input(self):
        """Starts the node and waits for user input."""
        waiting_for_input = True
        # A while loop for the user input interface
        # It's a loop that exits once waiting_for_input becomes False or when break is called
        while waiting_for_input:
            print("Please enter your choice")
            print("1: Add a new transaction value")
            print("2: Mine Block")
            print("3: Output the blockchain blocks")
            print("4: Check transaction validity")
            print("5: Create Wallet")
            print("6: Load Wallet")
            print("7: Save keys")
            print("q: Quit")
            user_choice = self.get_user_choice()
            if user_choice == "1":
                tx_data = self.get_transaction_value()
                recipient, amount = tx_data
                # Add the transaction amount to the blockchain
                if self.blockchain.add_transaction(recipient, self.wallet.public_key, amount=amount):
                    print('Added transaction!')
                else:
                    print('Transaction failed!')
                print(self.blockchain.get_open_transactions())
            elif user_choice == "2":
                if not self.blockchain.mine_block():
                    print("Mining Failed. Got no Wallet?")
            elif user_choice == "3":
                self.print_blockchain_blocks()
            elif user_choice == "4":
                # verifier = Verification()
                if Verification.verify_transactions(self.blockchain.get_open_transactions(), self.blockchain.get_balances):
                    print("All transactions are valid!")
                else:
                    print("There are some transactions failed!")
            elif user_choice == "5":
                self.wallet.create_keys()
                self.blockchain = Blockchain(self.wallet.public_key)
            elif user_choice == "6":
                self.wallet.load_keys()
                self.blockchain = Blockchain(self.wallet.public_key)
            elif user_choice == "7":
                self.wallet.save_keys()
            elif user_choice == "q":
                # This will lead to the loop to exist because it's running condition becomes False
                waiting_for_input = False
            else:
                print("Input is invalid, please pick a value from a list.")

            # verifier = Verification()
            if not Verification.verify_chain(self.blockchain.get_chain()):
                self.print_blockchain_blocks()
                print("Invalid Blockchain!")
                # Break out of the loop
                break

            print("Balance of {}: {:6.2f}".format(self.wallet.public_key, self.blockchain.get_balances()))
        else:
            print("User Left!")
        print ("Done!")

if __name__ == '__main__':
    node = Node()
    node.listen_for_input()