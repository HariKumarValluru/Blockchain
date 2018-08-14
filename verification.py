from hash_util import hash_string_256, hash_block

class Verification:
    @staticmethod
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
    
    @classmethod
    def verify_chain(cls, blockchain):
        """ Verify the current blockchain and returns True if it's valid False if not"""
        for (index, block) in enumerate(blockchain):
            if index == 0:
                continue
            if block.previous_hash != hash_block(blockchain[index - 1]):
                return False
            if not cls.valid_prof(block.transactions[:-1], block.previous_hash, block.proof):
                print("Proof of Work is invalid!")
                return False
        return True

    @classmethod
    def verify_transactions(cls, open_transactions, get_balances):
        """Verifies all open transactions."""
        return all([cls.verify_transaction(tx, get_balances) for tx in open_transactions])
    
    @staticmethod
    def verify_transaction(transaction, get_balances):
        """Verify a transaction by checking whether the sender has sufficient coins.

        Arguments:
            :transaction: The transaction that should be verified.
        """
        sender_balance = get_balances()
        return sender_balance >= transaction.amount