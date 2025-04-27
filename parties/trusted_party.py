from services.ORAM import SimpleORAM


class TrustedParty:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TrustedParty, cls).__new__(cls)
            # Initialize any variables you want only once
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if not self._initialized:
            security_param_bits = 128
            num_blocks = 16
            self.DB = SimpleORAM(security_param_bits, num_blocks)

            self._sk = self.DB.sk
            self._K = self.DB.K
            self._pk_T = "⊥"
            self._sk_RS = None
            self._pk_RS = None
            self._sk_T = None

            self._initialized = True


    @property
    def sk(self):
        return self._sk

    @sk.setter
    def sk(self, value):
        self._sk = value

    @property
    def K(self):
        return self._K

    @K.setter
    def K(self, value):
        self._K = value

    @property
    def sk_RS(self):
        return self._sk_RS

    @sk_RS.setter
    def sk_RS(self, value):
        self._sk_RS = value

    @property
    def pk_RS(self):
        return self._pk_RS

    @pk_RS.setter
    def pk_RS(self, value):
        self._pk_RS = value

    @property
    def sk_T(self):
        return self._sk_T

    @sk_T.setter
    def sk_T(self, value):
        self._sk_T = value

    @property
    def pk_T(self):
        return self._pk_T

    @pk_T.setter
    def pk_T(self, value):
        self._pk_T = value

    def add_card(self, id_H, budget, ctr):
        if id_H:
            # TODO: we need to check wheter the id is in the range of the DB
            self.DB.write(id_H, budget, ctr)
        else:
            id_H = 0
            while self.DB.read(id_H) != None:
                id_H += 1    
            self.DB.write(id_H, budget, ctr)

    def get_DB_view(self):
        return self.DB.get_DB_view()





def get_trusted_party():
    return TrustedParty()