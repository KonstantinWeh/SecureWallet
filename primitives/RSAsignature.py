import secrets
import hashlib
from sympy import nextprime, gcd
from services.encoding import ensure_bytes

class RSASignature:
    def __init__(self, key_size_bits=512):
        self.key_size_bits = key_size_bits

        self._sk, self._pk = self.keygen()

    def keygen(self):
        # Step 1: Generate two large primes p and q
        p = nextprime(secrets.randbits(self.key_size_bits // 2))
        q = nextprime(secrets.randbits(self.key_size_bits // 2))

        n = p * q
        phi = (p - 1) * (q - 1)

        # Step 2: Choose public exponent e
        e = 65537

        # Step 3: Compute private exponent d
        d = pow(e, -1, phi)

        sk = (d, n)
        pk = (e, n)
        return sk, pk


    @property
    def sk(self):
        return self._sk
    
    @property
    def pk(self):
        return self._pk
    
    def hash_message(self, message: bytes):
        digest = hashlib.sha256(message).digest()
        return int.from_bytes(digest, 'big')

    def sign(self, sk, message: bytes):
        d, n = sk
        h = self.hash_message(message)
        signature = pow(h, d, n)
        return signature

    def verify(self, pk, message: bytes, signature):
        e, n = pk

        h = self.hash_message(message)

        if isinstance(signature, bytes):
            signature = int.from_bytes(signature, byteorder='big')

        sig_check = pow(signature, e, n)

        return sig_check == h
