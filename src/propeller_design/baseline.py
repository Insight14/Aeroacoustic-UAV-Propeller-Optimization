"""
Standard baseline UAV propeller designs for comparison
"""

from typing import Dict


class BaselinePropeller:
    """
    Provides standard baseline propeller configurations
    for comparison with bio-inspired designs
    """
    
    @staticmethod
    def get_standard_2_blade() -> Dict:
        """
        Standard 2-blade commercial UAV propeller (e.g., DJI-style)
        Typical 10-inch (0.254m) diameter propeller
        
        Returns:
            Dictionary with baseline geometry and parameters
        """
        return {
            'name': 'Standard 2-Blade Commercial',
            'num_blades': 2,
            'diameter_m': 0.254,
            'radius_m': 0.127,
            'chord_root': 0.035,
            'chord_tip': 0.015,
            'chord_length': 0.025,  # Average
            'blade_thickness': 0.005,
            'pitch_angle': 10.0,  # degrees
            'twist_distribution': 'linear',
            'angle_of_attack': 5.0,  # degrees
            'cl_max': 1.2,
            'cl_slope': 2 * 3.14159,
            'drag_coefficient': 0.02,
            'stall_angle_deg': 12.0,
            'material_properties': {
                'density': 1200,  # kg/m^3 (carbon fiber composite)
                'youngs_modulus': 70e9,  # Pa
                'yield_strength': 600e6  # Pa
            },
            'design_type': 'baseline'
        }
    
    @staticmethod
    def get_standard_3_blade() -> Dict:
        """
        Standard 3-blade commercial UAV propeller
        
        Returns:
            Dictionary with baseline geometry and parameters
        """
        baseline = BaselinePropeller.get_standard_2_blade()
        baseline['name'] = 'Standard 3-Blade Commercial'
        baseline['num_blades'] = 3
        baseline['chord_root'] = 0.030
        baseline['chord_tip'] = 0.012
        baseline['chord_length'] = 0.021
        return baseline
    
    @staticmethod
    def get_standard_4_blade() -> Dict:
        """
        Standard 4-blade commercial UAV propeller
        
        Returns:
            Dictionary with baseline geometry and parameters
        """
        baseline = BaselinePropeller.get_standard_2_blade()
        baseline['name'] = 'Standard 4-Blade Commercial'
        baseline['num_blades'] = 4
        baseline['chord_root'] = 0.028
        baseline['chord_tip'] = 0.010
        baseline['chord_length'] = 0.019
        return baseline
    
    @staticmethod
    def get_typical_operating_conditions() -> Dict:
        """
        Typical operating conditions for UAV propellers
        
        Returns:
            Dictionary with standard operating parameters
        """
        return {
            'rpm': 5000,
            'velocity': 10.0,  # m/s forward flight
            'angle_of_attack': 5.0,  # degrees
            'air_density': 1.225,  # kg/m^3
            'temperature': 20.0,  # Celsius
            'altitude_m': 0,  # Sea level
            'reynolds_number': 200000,
            'mach_number': 0.029,  # Low speed
            'frequency_hz': 1000  # Typical noise frequency of interest
        }
    
    @staticmethod
    def calculate_baseline_performance(
        propeller_geometry: Dict,
        operating_conditions: Dict
    ) -> Dict:
        """
        Calculate baseline performance metrics
        
        This is a simplified calculation for reference
        For detailed analysis, use the aeroacoustics modules
        
        Args:
            propeller_geometry: Propeller geometry
            operating_conditions: Operating conditions
            
        Returns:
            Dictionary with baseline performance estimates
        """
        import numpy as np
        
        rpm = operating_conditions.get('rpm', 5000)
        velocity = operating_conditions.get('velocity', 10.0)
        radius = propeller_geometry.get('radius_m', 0.127)
        num_blades = propeller_geometry.get('num_blades', 2)
        
        # Simplified thrust estimate (N)
        omega = rpm * 2 * np.pi / 60.0
        tip_speed = omega * radius
        thrust_estimate = 0.5 * 1.225 * tip_speed**2 * 0.05 * num_blades
        
        # Simplified power estimate (W)
        power_estimate = thrust_estimate * velocity + 0.1 * omega**2
        
        # Simplified noise estimate (dB)
        # Empirical approximation for commercial propellers
        noise_estimate = 50 + 20 * np.log10(tip_speed) + 10 * np.log10(num_blades)
        
        # Noise-to-thrust ratio
        ntr_estimate = noise_estimate / thrust_estimate if thrust_estimate > 0 else 0
        
        return {
            'thrust_N': thrust_estimate,
            'power_W': power_estimate,
            'noise_spl_db': noise_estimate,
            'ntr_dB_per_N': ntr_estimate,
            'tip_speed_m_s': tip_speed,
            'efficiency': 0.65  # Typical for commercial props
        }
