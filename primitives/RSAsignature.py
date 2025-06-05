import secrets
import hashlib
from sympy import nextprime, gcd, isprime
from primitives.encoding import ensure_bytes


def generate_safe_prime_pair(bits):
    # compute safe primes as pointed out
    while True:
        # Generate random odd q in [2^(bits-1), 2^bits)
        q = secrets.randbits(bits - 1) | 1  # ensure q is odd
        q |= (1 << (bits - 2))  # ensure q has (bits - 1) bits (i.e. MSB = 1)

        if not isprime(q):
            continue

        p = 2 * q + 1
        if isprime(p):
            return p, q


class RSASignature:
    # 256 bits as a trade off between realistic choice and speed
    def __init__(self, key_size_bits=256):
        self.key_size_bits = key_size_bits

        self._sk, self._pk = self.keygen()

    def keygen(self):
        # Comment 3 - repeat if e is not co prime with phi
        while True:
            # Comment 3 - changed prime generation
            # Generate two large safe primes p and q
            p, q = generate_safe_prime_pair(self.key_size_bits)
            n = p * q
            phi = (p - 1) * (q - 1)

            # public exponent e
            e = 65537

            # ensure e is coprime with phi
            if gcd(e, phi) != 1:
                continue  # retry with new primes

            # private exponent d
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
