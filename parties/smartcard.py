from parties.trusted_party import get_trusted_party


class SmartCard:
    def __init__(self, st):
        # st = (pkRS, skT, pkT, K)
        self.pkRS, self.skT, self.pkT, self.K = st
        self.idH = None 
        self.skRS = None
        self.counter = None

      
    def update_balance(self, id_H, budget, ctr):
        trusted_party = get_trusted_party()
        trusted_party.update_balance(id_H, budget, ctr)
