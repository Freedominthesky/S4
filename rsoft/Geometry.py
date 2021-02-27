class Geometry:
    def __init__(self):
        # the parameter provided by ini file.
        self.begin_coordinate = [0, 0, 0]
        self.end_coordinate = [0, 0, 0]
        self.scaling_size = 1
        self.polygon_array = []
        self.material_name = ""
        # the parameter required by lua file.
        self.center = [0, 0]

    def set_begin_coordinate(self, coordinate):
        self.begin_coordinate = coordinate
    def get_begin_coordinate(self):
        return self.begin_coordinate

    def set_end_coordinate(self, coordinate):
        self.end_coordinate = coordinate
    def get_end_coordinate(self):
        return self.end_coordinate

    def set_scaling_size(self, value):
        self.scaling_size = value
    def get_scaling_size(self):
        return self.scaling_size
    
    def set_polygon_array(self, vertexes):
        self.polygon_array = vertexes
    def add_polygon_vertex(self, vertex):
        self.polygon_array.append(vertex)
    def get_polygon_array(self):
        return self.polygon_array

    def set_material_name(self, name):
        self.material_name = name
    def get_material_name(self):
        return self.material_name

    def set_center(self, vertex):
        self.center = vertex
    def get_center(self):
        return self.center