import secrets

class SimpleORAM:
    def __init__(self, security_param_bits, num_blocks):
        self.sk, self.K, self.DB = self.init(security_param_bits, num_blocks)

    def init(self, l_bits, N):
        # Step 1: Generate secret key sk (ℓ-bit random bytes)
        sk = secrets.token_bytes(l_bits // 8)

        # Step 2: Generate a key K for a pseudorandom function (PRF)
        K = secrets.token_bytes(l_bits // 8)

        # Step 3: Initialize the database DB
        DB = [None for _ in range(N)]

        return sk, K, DB
