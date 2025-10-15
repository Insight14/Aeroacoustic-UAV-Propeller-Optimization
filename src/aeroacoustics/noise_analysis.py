"""
Noise analysis module for UAV propellers
Implements various noise prediction models including:
- Broadband noise (turbulent boundary layer)
- Tonal noise (blade passage frequency)
- Vortex shedding noise
"""

import numpy as np
from typing import Dict, Tuple, Optional


class NoiseAnalyzer:
    """
    Analyzes aeroacoustic noise generation from UAV propellers
    """
    
    def __init__(self, reference_pressure: float = 2e-5):
        """
        Initialize noise analyzer
        
        Args:
            reference_pressure: Reference pressure for SPL calculation (Pa), default 20 µPa
        """
        self.reference_pressure = reference_pressure
        
    def calculate_spl(self, pressure: float, distance: float = 1.0) -> float:
        """
        Calculate Sound Pressure Level (SPL) in dB
        
        Args:
            pressure: RMS pressure (Pa)
            distance: Distance from source (m)
            
        Returns:
            Sound pressure level in dB
        """
        if pressure <= 0:
            return 0.0
        
        # Account for spherical spreading
        adjusted_pressure = pressure / distance
        spl = 20 * np.log10(adjusted_pressure / self.reference_pressure)
        return spl
    
    def calculate_broadband_noise(
        self,
        velocity: float,
        chord_length: float,
        blade_thickness: float,
        angle_of_attack: float,
        distance: float = 1.0
    ) -> float:
        """
        Calculate broadband noise using empirical models
        
        Args:
            velocity: Flow velocity (m/s)
            chord_length: Blade chord length (m)
            blade_thickness: Blade thickness (m)
            angle_of_attack: Angle of attack (degrees)
            distance: Observer distance (m)
            
        Returns:
            Broadband noise SPL (dB)
        """
        # Simplified broadband noise model based on turbulent boundary layer
        # Uses velocity^5-6 scaling law
        velocity_term = velocity ** 5.5
        
        # Geometric scaling
        area_term = chord_length * blade_thickness
        
        # Angle of attack effect (increased turbulence at higher AoA)
        aoa_factor = 1.0 + 0.5 * np.abs(angle_of_attack) / 15.0
        
        # Reference pressure calculation
        pressure_rms = 1e-3 * velocity_term * area_term * aoa_factor / (distance ** 2)
        
        return self.calculate_spl(pressure_rms, distance)
    
    def calculate_tonal_noise(
        self,
        rpm: float,
        num_blades: int,
        tip_speed: float,
        distance: float = 1.0,
        harmonics: int = 3
    ) -> Dict[str, float]:
        """
        Calculate tonal noise at blade passage frequency and harmonics
        
        Args:
            rpm: Propeller rotation speed (rev/min)
            num_blades: Number of blades
            tip_speed: Blade tip speed (m/s)
            distance: Observer distance (m)
            harmonics: Number of harmonics to calculate
            
        Returns:
            Dictionary with BPF and harmonic SPL values
        """
        # Blade passage frequency
        bpf = (rpm / 60.0) * num_blades
        
        results = {}
        
        for h in range(1, harmonics + 1):
            # Harmonic frequency
            freq = bpf * h
            
            # Simplified tonal noise model
            # Scales with tip speed and decreases with harmonic order
            pressure_rms = 5e-3 * (tip_speed ** 4) * (num_blades / 2.0) / (h ** 1.5 * distance ** 2)
            
            spl = self.calculate_spl(pressure_rms, distance)
            results[f"BPF_harmonic_{h}"] = spl
            results[f"frequency_hz_{h}"] = freq
            
        return results
    
    def calculate_vortex_noise(
        self,
        velocity: float,
        diameter: float,
        strouhal_number: float = 0.2,
        distance: float = 1.0
    ) -> Tuple[float, float]:
        """
        Calculate vortex shedding noise
        
        Args:
            velocity: Flow velocity (m/s)
            diameter: Characteristic dimension (m)
            strouhal_number: Strouhal number (typically 0.2)
            distance: Observer distance (m)
            
        Returns:
            Tuple of (vortex frequency Hz, SPL dB)
        """
        # Vortex shedding frequency
        vortex_freq = strouhal_number * velocity / diameter
        
        # Simplified vortex noise model
        pressure_rms = 8e-4 * (velocity ** 3) * diameter / (distance ** 2)
        
        spl = self.calculate_spl(pressure_rms, distance)
        
        return vortex_freq, spl
    
    def calculate_total_noise(
        self,
        propeller_params: Dict,
        operating_conditions: Dict,
        distance: float = 1.0
    ) -> Dict[str, float]:
        """
        Calculate total noise from all sources
        
        Args:
            propeller_params: Dictionary with propeller geometry
            operating_conditions: Dictionary with operating conditions
            distance: Observer distance (m)
            
        Returns:
            Dictionary with noise analysis results
        """
        # Extract parameters
        rpm = operating_conditions.get('rpm', 5000)
        velocity = operating_conditions.get('velocity', 10.0)
        
        chord = propeller_params.get('chord_length', 0.05)
        thickness = propeller_params.get('blade_thickness', 0.005)
        num_blades = propeller_params.get('num_blades', 2)
        radius = propeller_params.get('radius', 0.127)
        aoa = propeller_params.get('angle_of_attack', 5.0)
        
        # Calculate tip speed
        tip_speed = (rpm / 60.0) * 2 * np.pi * radius
        
        # Calculate noise components
        broadband_spl = self.calculate_broadband_noise(
            velocity, chord, thickness, aoa, distance
        )
        
        tonal_results = self.calculate_tonal_noise(
            rpm, num_blades, tip_speed, distance
        )
        
        vortex_freq, vortex_spl = self.calculate_vortex_noise(
            velocity, thickness, distance=distance
        )
        
        # Total noise (energy summation)
        tonal_spl_primary = tonal_results.get('BPF_harmonic_1', 0)
        
        # Convert dB to pressure, sum, convert back
        p_broadband = self.reference_pressure * 10 ** (broadband_spl / 20.0)
        p_tonal = self.reference_pressure * 10 ** (tonal_spl_primary / 20.0)
        p_vortex = self.reference_pressure * 10 ** (vortex_spl / 20.0)
        
        p_total = np.sqrt(p_broadband**2 + p_tonal**2 + p_vortex**2)
        total_spl = 20 * np.log10(p_total / self.reference_pressure)
        
        return {
            'total_spl_db': total_spl,
            'broadband_spl_db': broadband_spl,
            'tonal_spl_db': tonal_spl_primary,
            'vortex_spl_db': vortex_spl,
            'vortex_frequency_hz': vortex_freq,
            **tonal_results
        }
