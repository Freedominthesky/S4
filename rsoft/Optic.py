import math
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
        if self.p_amp < 0.0001:
            self.p_amp = 0
        self.s_amp = 10 * math.sin(math.radians(value))
        if self.s_amp < 0.0001:
            self.s_amp = 0
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