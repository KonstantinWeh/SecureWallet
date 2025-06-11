from parties.trusted_party import get_trusted_party


class SmartCard:
    def __init__(self, st):
        # st = (pkRS, skT, pkT, K)
        self.pkRS, self.skT, self.pkT, self.K = st
        self.idH = None 
        self.skRS = None
        self.counter = None


    def receive_skRS_and_verify(self, skRS, verify_signature_func):
        # Step 4: Receive RS's secret key and verify it against known pkRS
        if verify_signature_func(skRS, self.pkRS):
            self.skRS = skRS
            return True
        else:
            return False

    def initialize_counter_and_store(self, ORAM_Write, DB):
        # Step 6: Initialize counter and write budget to ORAM (secure storage)
        try:
            self.counter = 0
            ORAM_Write(DB, self.idH, { 'budget': self.budget, 'counter': self.counter })
            return True
        except Exception as e:
            print(f"Storage error: {e}")
            return False

    def output_state(self):
        # Step 7: Output final state
        if self.skRS and self.idH is not None:
            return (self.skRS, self.pkRS, self.skT, self.pkT, self.K, self.idH)
        else:
            return None
        
    def update_balance(self, id_H, budget, ctr):
        trusted_party = get_trusted_party()
        trusted_party.update_balance(id_H, budget, ctr)
