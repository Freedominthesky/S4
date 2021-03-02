# Function: This program translates the given ini file into lua script supported by S4.
# Author: Yang Yang(yyang16@126.com)
# Update Date: 2021年2月23日
import os
import re
import sys
import math
import Material
import Geometry
import Layer  
import Optic      


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


class S4:
    def __init__(self):
        self.optic = Optic.Optic()
        self.optical_grating = OpticalGrating()
        self.lattice_vector = [[1, 0], [0, 1]]
        self.fourier_series_num = 10
        self.background_index = 1.0
        self.depth_array = [0]
    
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

    def set_depth_array(self, depth_array):
        self.depth_array.extend(depth_array)
        self.depth_array.append(0)
    def get_depth_array(self):
        return self.depth_array


def extract_data_from(input_ini_file):
    input_file = open(input_ini_file, 'r')
    temp_file = open("temp_file.txt", 'w')
    line = input_file.readline()
    while line:
        if(line.count('\n') == len(line)):
            pass
        else:
            i = 0
            while i < len(line):
                if line[i] != ' ':
                    i = i + 1
                else:
                    break
            temp_file.write(line[ : i] + '\n')        
        line = input_file.readline()
    input_file.close()
    temp_file.close()
    S4_Object = S4()
    read_mode = 0
    file = open("temp_file.txt", 'r')
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
            temp_material = Material.Material()
            S4_Object.optical_grating.add_material(temp_material)
            read_mode = 2
        elif re.match(r'\[GEOMETRY', line):
            geometry_num = geometry_num + 1
            temp_geometry = Geometry.Geometry()
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
                    S4_Object.set_depth_array([float(elem) for elem in re.findall(r'\d+.?\d*', line)])
                #elif re.match(r'slice_num', line):
                #    S4_Object.optical_grating.set_layer_num(float(re.findall(r'\d+.?\d*', line)[0] + 2))
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
                        vertex_array = [[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]]
                    else:
                        poly_file_name = (line[10:])[:-1]
                        poly_file = open(poly_file_name, 'r')
                        line_poly = poly_file.readline()
                        while line_poly:
                            vertex = [float(re.findall(r'\d+.?\d*', line)[0]), float(re.findall(r'\d+.?\d*', line)[1])]
                            line_poly = poly_file.readline()
                            vertex_array.append(vertex)
                    S4_Object.optical_grating.geometry_array[geometry_num].set_polygon_array(vertex_array)
                elif re.match(r'begin_x', line):
                    x = float(re.findall(r'\d+.?\d*', line)[0])
                    line = file.readline()
                    while line.count('\n') == len(line):
                        line = file.readline()
                    y = float(re.findall(r'\d+.?\d*', line)[0])
                    line = file.readline()
                    while line.count('\n') == len(line):
                        line = file.readline()
                    #z = float(re.findall(r'\d+.?\d*', line)[0])
                    S4_Object.optical_grating.geometry_array[geometry_num].set_begin_coordinate([x, y])
                elif re.match(r'end_x', line):
                    print("x: ", line)
                    x = float(re.findall(r'\d+.?\d*', line)[0])
                    line = file.readline()
                    while line.count('\n') == len(line):
                        line = file.readline()
                    print("y: ", line)
                    y = float(re.findall(r'\d+.?\d*', line)[0])
                    line = file.readline()
                    while line.count('\n') == len(line):
                        line = file.readline()
                    print("z: ", line)
                    #z = float(re.findall(r'\d+.?\d*', line)[0])
                    S4_Object.optical_grating.geometry_array[geometry_num].set_end_coordinate([x, y])
                elif re.match(r'mat_name=', line):
                    material_name = (line[9:])[:-1]
                    S4_Object.optical_grating.geometry_array[geometry_num].set_material_name(material_name)
                elif re.match(r'end_scaling', line):
                    value = float(re.findall(r'\d+.?\d*', line)[0])
                    S4_Object.optical_grating.geometry_array[geometry_num].set_scaling_size(value)    

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
    file.write("S:SetLattice({" + str((S4_Object.get_lattice_vector())[0][0]) + ',' + "0},{0,"\
            +str((S4_Object.get_lattice_vector())[1][1]) + "})")
    file.write('\n\n')

    #set the spanning number of fourier series
    file.write("S:SetNumG(" + str(S4_Object.get_fourier_series_num()) + ")")
    file.write('\n\n')

    #set the material
    for i in range(len(S4_Object.optical_grating.get_material_array())):
        file.write("S:AddMaterial(" + '"' + (S4_Object.optical_grating.get_material_array())[i].get_name() + '", {' \
            +str((S4_Object.optical_grating.get_material_array())[i].get_n() ** 2) + ", 0})")
        file.write('\n')
    file.write('\n')

    #set the structure of optical grating
    file.write('\n')
    #add the top layer
    file.write("S:AddLayer('AirAbove', 0 , 'air')\n")
    #add the grating layer
    file.write("S:AddLayer('Grating', " + str((S4_Object.get_depth_array())[1]) + ', \'air\')\n')

    #S:SetLayerPatternPolygon('Slab',     -- which layer to alter
    #                     'Vacuum',   -- material in polygon
	#                     {0.2,0},    -- center
	#                     0,          -- tilt angle (degrees)
	#                     {0.3, 0.2,  -- vertices
	#                      0.3, 0.3,
	#                     -0.3, 0.3,
	#                     -0.3,-0.3,
	#                      0.3,-0.3,
	#                      0.3,-0.2,
	#                     -0.2,-0.2,
	#                     -0.2, 0.2})
    for element in S4_Object.optical_grating.get_geometry_array():
        file.write("S:SetLayerPatternPolygon('Grating',    -- which layer to alter\n")
        file.write("'" + element.get_material_name() + "',    -- material in polygon\n")
        file.write("{" + str((element.get_center())[0]) +',' + str((element.get_center())[1]) + "},  -- center\n")
        file.write("0,    -- tilt angle (degrees)\n{")
        i = 0
        for elem in element.get_polygon_array():
            i = i + 1
            file.write(str(elem[0]) + ',')
            if i != len(element.get_polygon_array()):
                file.write(str(elem[1]) + ',')
            else:
                file.write(str(elem[1]) + '})\n')

    #add the bottom layer
    file.write("S:AddLayerCopy('AirBelow', 0, 'AirAbove')\n")

    #simulation
    file.write("S:SetFrequency(" + str(S4_Object.optic.get_free_space_wavelength()) + ")")
    file.write("Simulation:SetExcitationPlanewave(" \
        + "{" + str(S4_Object.optic.get_phi())  + ',' + str(S4_Object.optic.get_theta()) + '},' \
        + "{" + str(S4_Object.optic.get_s_amp()) + ',' + str(S4_Object.optic.get_s_phase()) + '},' \
        + "{" + str(S4_Object.optic.get_p_amp()) + ',' + str(S4_Object.optic.get_p_phase()) + '})' )
    file.close()


def ini2lua(input_file_name):
    '''
    This is the main body of interface transfer function.
    '''
    S4_Object = extract_data_from(input_file_name)
    write_script_to(S4_Object, "temp.lua")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Illegal Number of Arguments! The legal command is 'python ini_simulation.py filename.ini'")
    elif sys.argv[1][-4:] != ".ini":
        print("Illegal type of Arguments! filename.ini is required!")
        print(sys.argv[1][-4:])
    else:
        lua_file = ini2lua(sys.argv[1])
        os.system("../build/S4 temp.lua")
        #os.system("rm temp.lua")

