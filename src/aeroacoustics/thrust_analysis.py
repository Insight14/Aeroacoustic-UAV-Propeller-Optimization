"""
Thrust calculation module for UAV propellers
"""

import numpy as np
from typing import Dict, Optional


class ThrustCalculator:
    """
    Calculates thrust and aerodynamic forces for UAV propellers
    """
    
    def __init__(self, air_density: float = 1.225):
        """
        Initialize thrust calculator
        
        Args:
            air_density: Air density (kg/m^3), default at sea level
        """
        self.air_density = air_density
        
    def calculate_thrust_momentum_theory(
        self,
        rpm: float,
        diameter: float,
        power: float
    ) -> float:
        """
        Calculate thrust using momentum theory
        
        Args:
            rpm: Propeller rotation speed (rev/min)
            diameter: Propeller diameter (m)
            power: Power input (W)
            
        Returns:
            Thrust force (N)
        """
        # Convert RPM to rad/s
        omega = rpm * 2 * np.pi / 60.0
        
        # Propeller disk area
        area = np.pi * (diameter / 2.0) ** 2
        
        # Simplified thrust calculation from momentum theory
        # T = sqrt(2 * rho * A * P)
        thrust = np.sqrt(2 * self.air_density * area * power)
        
        return thrust
    
    def calculate_thrust_blade_element(
        self,
        rpm: float,
        blade_params: Dict,
        num_blades: int,
        num_elements: int = 20
    ) -> Dict[str, float]:
        """
        Calculate thrust using blade element theory
        
        Args:
            rpm: Propeller rotation speed (rev/min)
            blade_params: Dictionary with blade geometry parameters
            num_blades: Number of blades
            num_elements: Number of blade elements for integration
            
        Returns:
            Dictionary with thrust and other aerodynamic forces
        """
        # Convert RPM to rad/s
        omega = rpm * 2 * np.pi / 60.0
        
        # Extract blade parameters
        radius = blade_params.get('radius', 0.127)
        chord_root = blade_params.get('chord_root', 0.03)
        chord_tip = blade_params.get('chord_tip', 0.015)
        pitch_angle = blade_params.get('pitch_angle', 10.0) * np.pi / 180.0
        cl_slope = blade_params.get('cl_slope', 2 * np.pi)  # Lift coefficient slope
        
        # Blade element integration
        r_elements = np.linspace(0.2 * radius, radius, num_elements)
        dr = r_elements[1] - r_elements[0]
        
        total_thrust = 0.0
        total_torque = 0.0
        
        for r in r_elements:
            # Local chord length (linear taper)
            chord = chord_root + (chord_tip - chord_root) * (r / radius)
            
            # Local velocity
            u_rot = omega * r
            
            # Simplified angle of attack (neglecting induced velocity)
            alpha = pitch_angle
            
            # Lift coefficient
            cl = cl_slope * alpha
            
            # Local thrust contribution
            dT = 0.5 * self.air_density * u_rot**2 * chord * cl * dr * num_blades
            
            # Local torque contribution (simplified)
            cd = 0.01 + 0.05 * alpha**2  # Simple drag model
            dQ = 0.5 * self.air_density * u_rot**2 * chord * cd * r * dr * num_blades
            
            total_thrust += dT
            total_torque += dQ
        
        # Calculate power
        power = total_torque * omega
        
        # Calculate efficiency
        if power > 0:
            # Ideal power for the thrust produced
            v_induced = np.sqrt(total_thrust / (2 * self.air_density * np.pi * radius**2))
            ideal_power = total_thrust * v_induced
            efficiency = ideal_power / power
        else:
            efficiency = 0.0
        
        return {
            'thrust_N': total_thrust,
            'torque_Nm': total_torque,
            'power_W': power,
            'efficiency': min(efficiency, 1.0)
        }
    
    def calculate_figure_of_merit(
        self,
        thrust: float,
        power: float,
        radius: float
    ) -> float:
        """
        Calculate figure of merit for hovering propeller
        
        Args:
            thrust: Thrust force (N)
            power: Power input (W)
            radius: Propeller radius (m)
            
        Returns:
            Figure of merit (dimensionless)
        """
        if power <= 0:
            return 0.0
        
        # Ideal power in hover
        disk_area = np.pi * radius**2
        v_induced_ideal = np.sqrt(thrust / (2 * self.air_density * disk_area))
        ideal_power = thrust * v_induced_ideal
        
        # Figure of merit
        fm = ideal_power / power
        
        return min(fm, 1.0)
    
    def calculate_advance_ratio(
        self,
        forward_velocity: float,
        rpm: float,
        diameter: float
    ) -> float:
        """
        Calculate advance ratio J = V / (n * D)
        
        Args:
            forward_velocity: Forward flight velocity (m/s)
            rpm: Propeller rotation speed (rev/min)
            diameter: Propeller diameter (m)
            
        Returns:
            Advance ratio (dimensionless)
        """
        n = rpm / 60.0  # Rev/s
        
        if n * diameter == 0:
            return 0.0
        
        J = forward_velocity / (n * diameter)
        
        return J
    
    def calculate_thrust_coefficient(
        self,
        thrust: float,
        rpm: float,
        diameter: float
    ) -> float:
        """
        Calculate thrust coefficient CT = T / (rho * n^2 * D^4)
        
        Args:
            thrust: Thrust force (N)
            rpm: Propeller rotation speed (rev/min)
            diameter: Propeller diameter (m)
            
        Returns:
            Thrust coefficient (dimensionless)
        """
        n = rpm / 60.0  # Rev/s
        
        denominator = self.air_density * n**2 * diameter**4
        
        if denominator == 0:
            return 0.0
        
        CT = thrust / denominator
        
        return CT
