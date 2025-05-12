import secrets
import hashlib

# Helper: generate a random prime (very basic for demonstration)
from sympy import nextprime

def generate_prime(bits):
    random_num = secrets.randbits(bits)
    prime = nextprime(random_num)
    return prime

def hash_to_group(val, q):
    hash_val = hashlib.sha256(val).digest()
    num = int.from_bytes(hash_val, 'big')
    return num % q

class PedersenCommitment:
    def __init__(self, security_param_bits):
        self.params = self.gen(security_param_bits)

    def get_mod_q(self):
        return self.params[1]

    def gen(self, l_bits):
        # Step 1: Generate a prime q
        q = generate_prime(l_bits)

        # Step 2: Define group G implicitly (we use Z_q^*)
        G = f"Z_{q}^*" 

        # Step 3: Choose generators g, h
        g_seed = secrets.token_bytes(32)
        h_seed = secrets.token_bytes(32)
        g = hash_to_group(g_seed, q)
        h = hash_to_group(h_seed, q)

        # Ensure g and h are not 0
        while g == 0:
            g_seed = secrets.token_bytes(32)
            g = hash_to_group(g_seed, q)
        while h == 0:
            h_seed = secrets.token_bytes(32)
            h = hash_to_group(h_seed, q)

        return (G, q, g, h)

    def commit(self, m, r=None):
        _, q, g, h = self.params
        if r is None:
            r = secrets.randbelow(q)

        # Commitment: com = g^m * h^r mod q

        if isinstance(m, bytes):
            m = int.from_bytes(m, byteorder='big')

        if isinstance(r, bytes):
            r = int.from_bytes(r, byteorder='big')

        com = (pow(g, m, q) * pow(h, r, q)) % q
        return com, r

