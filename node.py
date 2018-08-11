from verification import Verification

class Node:

    def __init__(self):
        self.blockchain = []
    
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
        for block in self.blockchain:
            print(block)
        else:
            print("-" * 30)
    
    def listen_for_input(self):
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
            user_choice = self.get_user_choice()
            if user_choice == "1":
                tx_data = self.get_transaction_value()
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
                self.print_blockchain_blocks()
            elif user_choice == "4":
                verifier = Verification()
                if verifier.verify_transactions(open_transactions, get_balances):
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

            verifier = Verification()
            if not verifier.verify_chain(blockchain):
                # print_blockchain_blocks()
                print("Invalid Blockchain!")
                # Break out of the loop
                break

            print("Balance of {}: {:6.2f}".format(owner,get_balances(owner)))
        else:
            print("User Left!")
        print ("Done!")