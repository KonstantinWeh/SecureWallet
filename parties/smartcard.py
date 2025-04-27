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


# Example Usage
if __name__ == "__main__":
    # Simulate initial smart card state
    initial_state = ("pkRS_example", "skT_example", "pkT_example", "K_example")

    # Simulated database
    DB = {}

    # RS side: allocate budget, generate household id
    allocated_budget = 1000
    next_household_id = "H12345"
    secret_skRS = "secret_skRS_example"

    # Create smart card with initial state
    sc = SmartCard(initial_state)

    # Step-by-step protocol
    sc.receive_household_id(next_household_id)
    if sc.receive_skRS_and_verify(secret_skRS, verify_signature_func):
        sc.receive_budget(allocated_budget)
        if sc.initialize_counter_and_store(ORAM_Write, DB):
            final_state = sc.output_state()
            print("Registration successful. Final smart card state:")
            print(final_state)
            print("Database contents:")
            print(DB)
        else:
            print("Failed during ORAM write.")
    else:
        print("Verification of skRS failed.")
