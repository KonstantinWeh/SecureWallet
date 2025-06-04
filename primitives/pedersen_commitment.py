import secrets
import hashlib

# Helper: generate a random prime (very basic for demonstration)
from sympy import isprime, nextprime

       
def generate_safe_prime_pair(bits):
    # Comment 1 - safe primes: Generate a random prime q with (bits - 1) bits

    while True:
        q = nextprime(secrets.randbits(bits - 1))
        p = 2 * q + 1
        if isprime(p):
            return p, q

def hash_to_group(val, q):
    hash_val = hashlib.sha256(val).digest()
    num = int.from_bytes(hash_val, 'big')
    return num % q

def find_generator(p, q):
    # Comment 2 - Find a generator of the subgroup G of order q in Z_p^*
    while True:
        h = secrets.randbelow(p - 3) + 2  # in [2, p-2]
        g = pow(h, (p - 1) // q, p)
        if g != 1:
            return g
        
class PedersenCommitment:
    def __init__(self, security_param_bits):
        self.params = self.gen(security_param_bits)

    def get_mod_q(self):
        return self.params[1]

    def gen(self, l_bits):
        # Comment 2 - “g” and “h” you choose need to be generators of that subgroup
        # Step 1: Generate primes p = 2q + 1
        p, q = generate_safe_prime_pair(l_bits)

        # Step 2: Subgroup G is implicitly the order-q subgroup of Z_p^*
        G = f"Subgroup of Z_{p}^* of order {q}"

        # Step 3: Choose independent generators g, h of G
        g = find_generator(p, q)
        while True:
            h = find_generator(p, q)
            if h != g:
                break

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

