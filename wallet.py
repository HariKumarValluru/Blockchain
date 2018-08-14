from Cryptodome.PublicKey import RSA
import Cryptodome.Random

class Wallet:
    def __init__(self):
        pass
    def generate_keys(self):
        RSA.generate