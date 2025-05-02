from services.RSDSA import RSASignature
from services.pedersen_commitment import PedersenCommitment
from services.encoding import ensure_bytes


class Vendor:
    def __init__(self):
        self.pkRS = None
        self.local_storage = []  # local in-memory storage for accepted proofs
        self.DB = {}             # simulate a database (e.g., items, balances, etc.)
        self.epsilon = b""       # ε is assumed to be empty in this context

    def set_pk(self, pk):
        self.pkRS = pk


    def get_proofs(self):
        return self.local_storage


    def verify_signature(self, signature, message):
        signature = ensure_bytes(signature)
        RSDSA = RSASignature()
        valid = RSDSA.verify(self.pkRS, message, signature)
        return valid

    def verify(self, proof, price, reclaim_period, commitment_scheme):
        """
        proof: tuple (σ, τ, Com, r)
        price: value expected in the commitment
        commitment_scheme: params published by trusted party
        """
        try:

            signature, tag, commitment, com_r = proof

            
            # Ensure all inputs are bytes
            tag = ensure_bytes(tag)
            commitment = ensure_bytes(commitment)
            signature = ensure_bytes(signature)
            reclaim_period = ensure_bytes(reclaim_period)
            
            # Construct message τ || ε || Com
            message = tag + reclaim_period + commitment


            # Verify digital signature
            RSDSA = RSASignature()
            is_valid = RSDSA.verify(self.pkRS, message, signature)

            # Verify commitment
            expected_commitment = ensure_bytes(commitment_scheme.commit(int(price), com_r)[0])

            if not is_valid or commitment != expected_commitment:
                print("Verification failed.")
                return None  # return ⊥

            # If everything passes, store (π, DB)
            db_entry = ((signature, tag, commitment, com_r), int(price), int(reclaim_period))
            self.local_storage.append(db_entry)
            return proof

        except Exception as e:
            print(f"Error during verification: {e}")
            return None
