# Function: This program translates the given ini file into lua script supported by S4.
# Author: Yang Yang(yyang16@126.com)
# Update Date: 2021年2月23日
import os
import re

class Material:
    def __init__(self):
        '''
        name: the name of current material
        pattern: 
        epsilon:
        n:
        '''
        self.name = ""
        self.pattern = []
        self.epsilon = 1.0
        self.n = 1.0

    def set_epsilon(value):
        self.epsilon = value
    def get_epsilon():
        return self.epsilon

    def set_n(value):
        self.n = value
    def get_n():
        return self.n

    def set_pattern(polygon_array):
        self.pattern = polygon_array
    def add_polygon(polygon):
        self.pattern.append(polygon)
    def get_pattern():
        return self.pattern

    def set_name(name):
        self.name = name
    def get_name():
        return self.name

class Layer:
    def __init__(self):
        self.depth = 0.0
        self.pattern = [[0, 0], [0, 1], [1, 0], [1, 1]]
        self.name = ""

    def set_name(name):
        self.name = name
    def get_name():
        return self.name

    def set_depth(value):
        self.depth = value
    def get_depth():
        return self.depth

    def set_pattern(vertexes_array):
        self.pattern = vertexes_array
    def add_vertex(vertex):
        self.pattern.append(vertex)
    def get_pattern():
        return self.pattern

class OpticalGrating:
    def __init__(self):
        '''
        layer_num: total layer of the optical grating, input layer and output layer.
        depth_array: depth of each layer, the default value of input value and output layer is 0.
        material_array: the array consists of all the materials in the system.
        '''
        self.layer_num = 3
        self.depth_array = None
        self.material_array = []
        self.dimension = 3
        self.height = 1.0

    def set_layer_num(value):
        self.layer_num = value
    def get_layer_num(value):
        return self.layer_num
    
    def set_depth_array(depth_array):
        self.depth_array = depth_array
    def get_depth_array():
        return self.depth_array

    def set_material_array(material_array):
        self.material_array = material_array
    def add_material(material):
        self.material_array.append(material)
    def get_material_array():
        return self.material_array

    def set_dimension(value):
        self.dimension = value
    def get_dimension():
        return self.dimension

    def set_height(value):
        self.height = value
    def get_height():
        return self.height


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
    
    def set_free_space_wavelength(value):
        self.free_space_wavelength = value
    def get_free_space_wavelength():
        return self.free_space_wavelength
    
    def set_incidence_angle(value):
        self.incidence_angle = value
        self.theta = value
    def get_incidence_angle():
        return self.incidence_angle
    def get_theta():
        return self.theta

    def set_azimuth_angle(value):
        self.azimuth_angle = value
        self.phi = 90 - value
    def get_azimuth_angle():
        return self.azimuth_angle
    def get_phi():
        return self.phi
    
    def set_polarization_angle(value):
        self.polarization_angle = value
        self.p_amp = 10 * math.cos(math.radians(value))
        self.s_amp = 10 * math.sin(math.radians(value))
    def get_polarization_angle():
        return self.polarization_angle
    def get_p_amp():
        return self.p_amp
    def get_s_amp():
        return self.s_amp

    def set_polarization_phase_diff(value):
        self.polarization_phase_diff = value
        self.p_phase = 0
        self.s_phase = self.p_phase + value
    def get_polarization_phase_diff():
        return self.polarization_phase_diff
    def get_s_phase():
        return self.s_phase
    def get_p_phase():
        return self.p_phase


class S4:
    def __init__(self):
        self.optic = Optic()
        self.optical_grating = OpticalGrating()
        self.lattice_vector = None
        self.fourier_series_num = 10
        self.background_index = 1.0
    
    def set_optic(optic):
        self.optic = optic
    def get_optic():
        return self.optic 

    def set_material(material):
        self.material = material
    def get_material():
        return self.material
 
    def set_optical_grating(optical_grating):
        self.optical_grating = optical_grating
    def get_optical_grating():
        return self.optical_grating

    def set_fourier_series_num(value):
        self.fourier_series_num = value
    def get_fourier_series_num():
        return self.fourier_series_num

    def set_lattice_vector(lattice_vector):
        self.lattice_vector = lattice_vector
    def get_lattice_vector():
        return self.lattice_vector
    
    def set_background_index(value):
        self.background_index = value
    def get_background_index():
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
        elif re.match(r'\[[GEOMETRY', line):
            geometry_num = geometry_num + 1
            read_mode = 3
        else:
            if read_mode == 0:
                lattice_vector = [[1.0, 0], [0, 1.0]]
                height_min = -1.0
                height_max = 1.0
                if re.match(r'dimension', line):
                    S4_Object.optical_grating.set_dimension(float(re.findall(r'\d+.?\d*', line)[0]))
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
                        S4_Object.set_height(height_max - height_min)
                elif re.match(r'rcwa_harmonics', line):
                    fourier_series_num = float(re.findall(r'\d+.?\d*', line)[0])
                    line = file.readline()
                    if re.match(r'rcwa_harmonics', line):
                        if float(re.findall(r'\d+.?\d*', line)[0]) > fourier_series_num:
                            fourier_series_num = float(re.findall(r'\d+.?\d*', line)[0])
                    S4_Object.set_fourier_series_num(fourier_series_num)
                elif re.match(r'depth', line):
                    S4_Object.set_depth_array([float(re.findall(r'\d+.?\d*', line)[0])])
                elif re.match(r'slice_num', line)
                    S4_Object.optical_grating.set_layer_num(float(re.findall(r'\d+.?\d*', line)[0] + 2)

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
    if S4_Object.optical_grating.get_dimension() == 2:
        file.write("S:SetLattice({" + str((S4_Object.optical_grating.get_lattice_vector())[0][0]) + ',' + "0})")
    elif S4_Object.optical_grating.get_dimension() == 3:
        file.write("S:SetLattice({" + str((S4_Object.optical_grating.get_lattice_vector())[0][0]) + ',' + "0},{0,"\
            str((S4_Object.optical_grating.get_lattice_vector())[1][1]) + "})")
    else:
        pass
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



def main(input_file_name, output_file_name):
    '''
    This is the main body of interface transfer function.
    '''
    S4_Object = extract_data_from(input_file_name)
    write_script_to(output_file_name)

if __name__ == '__main__':
    main()
