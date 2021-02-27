# Function: This program translates the given ini file into lua script supported by S4.
# Author: Yang Yang(yyang16@126.com)
# Update Date: 2021年2月23日
import os
import re
import sys

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

    def set_epsilon(self, value):
        self.epsilon = value
    def get_epsilon(self):
        return self.epsilon

    def set_n(self, value):
        self.n = value
    def get_n(self):
        return self.n

    def set_name(self, name):
        self.name = name
    def get_name(self):
        return self.name

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

class OpticalGrating:
    def __init__(self):
        '''
        layer_array: 
        material_array: 
        dimension:
        '''
        self.layer_array = []
        self.material_array = []
        self.geometry_array = []
        self.dimension = 3

    def set_layer_array(self, layer_array):
        self.layer_array = layer_array
    def add_layer(self, layer):
        self.layer_array.append(layer)
    def get_layer_array(self, layer_array):
        return self.layer_array

    def set_material_array(self, material_array):
        self.material_array = material_array
    def add_material(self, material):
        self.material_array.append(material)
    def get_material_array(self):
        return self.material_array
    
    def set_geometry_array(self, geometry_array):
        self.geometry_array = geometry_array
    def add_geometry(self, geometry):
        self.geometry_array.append(geometry)
    def get_geometry_array(self):
        return self.geometry_array

    def set_dimension(self, value):
        self.dimension = value
    def get_dimension(self):
        return self.dimension


class Optic:
    def __init__(self):
        '''
            (number) Angles in degrees. 
            phi and theta give the spherical coordinate angles of the planewave k-vector. 
            For zero angles, the k-vector is assumed to be (0, 0, kz), 
            while the electric field is assumed to be (E0, 0, 0), and the magnetic field is in (0, H0, 0). 
            The angle phi specifies first the angle by which the E,H,k frame should be rotated (CW) about the y-axis,
            and the angle theta specifies next the angle by which the E,H,k frame should be rotated (CCW) about the z-axis. 
            Note the different directions of rotations for each angle
        '''
        #optic parameter in ini file
        self.free_space_wavelength = 0.0
        self.incidence_angle = 0.0
        self.azimuth_angle = 0.0
        self.polarization_angle = 0.0
        self.polarization_phase_diff = 0.0
        #optic parameter in lua file
        self.phi = 0
        self.theta = 0
        self.s_amp = 1
        self.s_phase = 0
        self.p_amp = 1
        self.p_phase = 0
    
    def set_free_space_wavelength(self, value):
        self.free_space_wavelength = value
    def get_free_space_wavelength(self):
        return self.free_space_wavelength
    
    def set_incidence_angle(self, value):
        self.incidence_angle = value
        self.theta = value
    def get_incidence_angle(self):
        return self.incidence_angle
    def get_theta(self):
        return self.theta

    def set_azimuth_angle(self, value):
        self.azimuth_angle = value
        self.phi = 90 - value
    def get_azimuth_angle(self):
        return self.azimuth_angle
    def get_phi(self):
        return self.phi
    
    def set_polarization_angle(self, value):
        self.polarization_angle = value
        self.p_amp = 10 * math.cos(math.radians(value))
        self.s_amp = 10 * math.sin(math.radians(value))
    def get_polarization_angle(self):
        return self.polarization_angle
    def get_p_amp(self):
        return self.p_amp
    def get_s_amp(self):
        return self.s_amp

    def set_polarization_phase_diff(self, value):
        self.polarization_phase_diff = value
        self.p_phase = 0
        self.s_phase = self.p_phase + value
    def get_polarization_phase_diff(self):
        return self.polarization_phase_diff
    def get_s_phase(self):
        return self.s_phase
    def get_p_phase(self):
        return self.p_phase


class S4:
    def __init__(self):
        self.optic = Optic()
        self.optical_grating = OpticalGrating()
        self.lattice_vector = [[1, 0], [0, 1]]
        self.fourier_series_num = 10
        self.background_index = 1.0
    
    def set_optic(self, optic):
        self.optic = optic
    def get_optic(self):
        return self.optic 

    def set_material(self, material):
        self.material = material
    def get_material(self):
        return self.material
 
    def set_optical_grating(self, optical_grating):
        self.optical_grating = optical_grating
    def get_optical_grating(self):
        return self.optical_grating

    def set_fourier_series_num(self, value):
        self.fourier_series_num = value
    def get_fourier_series_num(self):
        return self.fourier_series_num

    def set_lattice_vector(self, lattice_vector):
        self.lattice_vector = lattice_vector
    def get_lattice_vector(self):
        return self.lattice_vector
    
    def set_background_index(self, value):
        self.background_index = value
    def get_background_index(self):
        return self.get_background_index()


def extract_data_from(input_ini_file):
    S4_Object = S4()
    read_mode = 0
    file = open(input_ini_file, 'r', encoding = 'utf-8')
    line = file.readline()
    material_num = -1
    geometry_num = -1
    while line:
        if line.count('\n') == len(line):
            line = file.readline()
            continue
        elif re.match(r'\[GENERAL\]', line):
            read_mode = 0
        elif re.match(r'\[OPTICAL\]', line):
            read_mode = 1
        elif re.match(r'\[MATERIAL', line):
            material_num = material_num + 1
            temp_material = Material()
            S4_Object.optical_grating.add_material(temp_material)
            read_mode = 2
        elif re.match(r'\[GEOMETRY', line):
            geometry_num = geometry_num + 1
            temp_geometry = Geometry()
            S4_Object.optical_grating.add_geometry(temp_geometry)
            read_mode = 3
        else:
            if read_mode == 0:
                lattice_vector = [[1, 0], [0, 1]]
                height_min = -1.0
                height_max = 1.0
                if re.match(r'dimension', line):
                    temp = int(re.findall(r'\d+.?\d*', line)[0])
                    print("temp: ", temp)
                    S4_Object.optical_grating.set_dimension(temp)
                    
                elif re.match(r'background_index', line):
                    S4_Object.set_background_index(float(re.findall(r'\d+.?\d*', line)[0]))
                elif re.match(r'pitch_x', line):
                    lattice_vector[0][0] = float(re.findall(r'\d+.?\d*', line)[0])
                    line = file.readline()
                    if re.match(r'pitch_y', line):
                        lattice_vector[1][1] = float(re.findall(r'\d+.?\d*', line)[0])
                    S4_Object.set_lattice_vector(lattice_vector)   
                elif re.match(r'domain_max', line):
                    height_max = float(re.findall(r'\d+.?\d*', line)[0])
                    line = file.readline()
                    if re.match(r'domain_min', line):
                        height_min = float(re.findall(r'\d+.?\d*', line)[0])
                        #S4_Object.set_height(height_max - height_min)
                elif re.match(r'rcwa_harmonics', line):
                    fourier_series_num = float(re.findall(r'\d+.?\d*', line)[0])
                    line = file.readline()
                    if re.match(r'rcwa_harmonics', line):
                        if float(re.findall(r'\d+.?\d*', line)[0]) > fourier_series_num:
                            fourier_series_num = float(re.findall(r'\d+.?\d*', line)[0])
                    S4_Object.set_fourier_series_num(fourier_series_num)
                elif re.match(r'depth', line):
                    S4_Object.set_depth_array([float(re.findall(r'\d+.?\d*', line)[0])])
                elif re.match(r'slice_num', line):
                    S4_Object.optical_grating.set_layer_num(float(re.findall(r'\d+.?\d*', line)[0] + 2))
                else:
                    pass

            elif read_mode == 1:
                if re.match(r'free_space_wavelength', line):
                    S4_Object.optic.set_free_space_wavelength(float(re.findall(r'\d+.?\d*', line)[0]))
                elif re.match(r'incidence_angle', line):
                    S4_Object.optic.set_incidence_angle(float(re.findall(r'\d+.?\d*', line)[0]))
                elif re.match(r'azimuth_angle', line):
                    S4_Object.optic.set_azimuth_angle(float(re.findall(r'\d+.?\d*', line)[0]))
                elif re.match(r'polarization_angle', line):
                    S4_Object.optic.set_polarization_angle(float(re.findall(r'\d+.?\d*', line)[0]))
                elif re.match(r'polarization_phase_diff', line):
                    S4_Object.optic.set_polarization_phase_diff(float(re.findall(r'\d+.?\d*', line)[0]))

            elif read_mode == 2:
                if re.match(r'name=', line):
                    S4_Object.optical_grating.material_array[material_num].set_name(line[5:len(line) - 1])
                elif re.match(r'n=', line):
                    S4_Object.optical_grating.material_array[material_num].set_n(float(re.findall(r'\d+.?\d*', line)[0]))
                elif re.match(r'k=', line):
                    S4_Object.optical_grating.material_array[material_num].set_k(float(re.findall(r'\d+.?\d*', line)[0]))

            elif read_mode == 3:
                if re.match(r'poly_file=', line):
                    vertex_array = []
                    if(line[10] == '\n'):
                        pass
                    else:
                        poly_file_name = (line[10:])[:-1]
                        poly_file = open(poly_file, 'r')
                        line_poly = poly_file.readline()
                        while line_poly:
                            vertex = [float(re.findall(r'\d+.?\d*', line)[0]), float(re.findall(r'\d+.?\d*', line)[1])]
                            line_poly = poly_file.readline()
                            vertex_array.append(vertex)
                    S4_Object.optical_grating.geometry_array[geometry_num].set_polygon_array(vertex_array)

                elif re.match(r'mat_name=', line):
                    material_name = (line[9:])[:-1]
                    S4_Object.optical_grating.geometry_array[geometry_num].set_material_name(material_name)
                else:
                    pass

            else:
                pass
        line = file.readline()
    file.close()
    return S4_Object


def write_script_to(S4_Object, output_lua_file):
    file = open(output_lua_file, 'w')
    #set S4 simulation object
    file.write("S = S4.NewSimulation()\n\n")
    #set lattice vector
    file.write("S:SetLattice({" + str((S4_Object.optical_grating.get_lattice_vector())[0][0]) + ',' + "0},{0,"\
            +str((S4_Object.optical_grating.get_lattice_vector())[1][1]) + "})")
    file.write('\n\n')
    #set the spanning number of fourier series
    file.write("S:SetNumG(" + str(S4_Object.get_fourier_series_num()) + ")")
    file.write('\n\n')
    #set the material
    for i in range(len(S4_Object.optical_grating.get_material_array())):
        file.write("S:AddMaterial(" + (S4_Object.optical_grating.get_material_array())[i].get_name() + '", {' \
            +str((S4_Object.optical_grating.get_material_array())[i].get_n() ** 2) + ", 0})")
        file.write('\n')
    file.write('\n')
    #set the structure of optical grating

    file.write('\n')
    #simulation
    file.write("Simulation:SetExcitationPlanewave(" \
        + "{" + str(S4_Object.optic.get_phi())  + ',' + str(S4_Object.optic.get_theta()) + '}' \
        + "{" + str(S4_Object.optic.get_s_amp()) + ',' + str(S4_Object.optic.get_s_phase()) + '}' \
        + "{" + str(S4_Object.optic.get_p_amp()) + ',' + str(S4_Object.optic.get_p_phase()) + '})' )
    file.close()



def ini2lua(input_file_name):
    '''
    This is the main body of interface transfer function.
    '''
    S4_Object = extract_data_from(input_file_name)
    write_script_to(S4_Object, "temp.lua")
    return output_file_name

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Illegal Number of Arguments! The legal command is 'python ini_simulation.py filename.ini'")
    elif sys.argv[1][-4:] != ".ini":
        print("Illegal type of Arguments! filename.ini is required!")
        print(sys.argv[1][-4:])
    else:
        lua_file = ini2lua(sys.argv[1])
        os.system("./S4 temp.lua")
        #os.system("rm temp.lua")

