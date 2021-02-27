class Layer:
    def __init__(self):
        self.depth = 0.0
        self.geometry_array = []
        self.name = ""

    def set_name(self, name):
        self.name = name
    def get_name(self):
        return self.name

    def set_depth(self, value):
        self.depth = value
    def get_depth(self):
        return self.depth

    def set_geometry_array(self, geometry_array):
        self.geometry_array = geometry_array
    def add_geometry(self, geometry):
        self.geometry_array.append(vertex)
    def get_pattern(self):
        return self.geometry_array