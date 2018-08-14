from Cryptodome.PublicKey import RSA
import Cryptodome.Random
import binascii

class Wallet:
    def __init__(self):
        private_key, public_key = self.generate_keys()
        self.private_key = private_key
        self.public_key = public_key
        
    def generate_keys(self):
        private_key = RSA.generate(1024, Cryptodome.Random.new().read)
        public_key = private_key.publickey()
        return (binascii.hexlify(private_key.export_key(format='DER')).decode('ascii'), binascii.hexlify(public_key.export_key(format='DER')).decode('ascii'))