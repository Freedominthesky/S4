class Material:
    def __init__(self):
        '''
        name: the name of current material
        epsilon: the dialetric of current material
        n: the reflactive index of current material
        '''
        self.name = ""
        self.epsilon = 1.0
        self.n = 1.0
        self.k = 0.0

    def set_epsilon(self, value):
        self.epsilon = value
    def get_epsilon(self):
        return self.epsilon

    def set_n(self, value):
        self.n = value
    def get_n(self):
        return self.n
    
    def set_k(self, value):
        self.k = value
    def get_k(self):
        return self.k

    def set_name(self, name):
        self.name = name
    def get_name(self):
        return self.name