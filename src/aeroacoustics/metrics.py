"""
Aeroacoustic metrics for evaluating propeller performance
"""

import numpy as np
from typing import Dict, Optional


class AeroacousticMetrics:
    """
    Calculate key aeroacoustic performance metrics
    Primary focus: Noise-to-Thrust Ratio (NTR)
    """
    
    def __init__(self):
        """Initialize metrics calculator"""
        pass
    
    def calculate_noise_to_thrust_ratio(
        self,
        noise_spl_db: float,
        thrust_N: float,
        reference_thrust: float = 1.0
    ) -> float:
        """
        Calculate Noise-to-Thrust Ratio (NTR)
        
        Lower NTR is better (less noise per unit thrust)
        
        Args:
            noise_spl_db: Total noise SPL in dB
            thrust_N: Thrust force in Newtons
            reference_thrust: Reference thrust for normalization (N)
            
        Returns:
            Noise-to-thrust ratio (dB/N)
        """
        if thrust_N <= 0:
            return float('inf')
        
        # Normalize thrust
        normalized_thrust = thrust_N / reference_thrust
        
        # NTR = SPL / Thrust
        ntr = noise_spl_db / normalized_thrust
        
        return ntr
    
    def calculate_acoustic_efficiency(
        self,
        noise_spl_db: float,
        thrust_N: float,
        power_W: float
    ) -> float:
        """
        Calculate acoustic efficiency metric
        
        Combines both thrust efficiency and noise generation
        Higher is better
        
        Args:
            noise_spl_db: Total noise SPL in dB
            thrust_N: Thrust force in Newtons
            power_W: Power consumption in Watts
            
        Returns:
            Acoustic efficiency (dimensionless)
        """
        if noise_spl_db <= 0 or power_W <= 0:
            return 0.0
        
        # Thrust per unit power
        thrust_efficiency = thrust_N / power_W
        
        # Inverse of noise (less noise is better)
        noise_penalty = 100.0 / noise_spl_db
        
        # Combined metric
        acoustic_eff = thrust_efficiency * noise_penalty * 1000  # Scaling factor
        
        return acoustic_eff
    
    def calculate_noise_reduction_percentage(
        self,
        baseline_ntr: float,
        modified_ntr: float
    ) -> float:
        """
        Calculate percentage noise reduction compared to baseline
        
        Args:
            baseline_ntr: Baseline noise-to-thrust ratio
            modified_ntr: Modified design noise-to-thrust ratio
            
        Returns:
            Percentage reduction (positive means improvement)
        """
        if baseline_ntr <= 0:
            return 0.0
        
        reduction = ((baseline_ntr - modified_ntr) / baseline_ntr) * 100.0
        
        return reduction
    
    def evaluate_design_performance(
        self,
        noise_results: Dict,
        thrust_results: Dict,
        baseline_ntr: Optional[float] = None
    ) -> Dict[str, float]:
        """
        Comprehensive evaluation of propeller design
        
        Args:
            noise_results: Dictionary from NoiseAnalyzer
            thrust_results: Dictionary from ThrustCalculator
            baseline_ntr: Optional baseline NTR for comparison
            
        Returns:
            Dictionary with all performance metrics
        """
        total_noise = noise_results.get('total_spl_db', 0)
        thrust = thrust_results.get('thrust_N', 0)
        power = thrust_results.get('power_W', 1)
        efficiency = thrust_results.get('efficiency', 0)
        
        # Calculate NTR
        ntr = self.calculate_noise_to_thrust_ratio(total_noise, thrust)
        
        # Calculate acoustic efficiency
        acoustic_eff = self.calculate_acoustic_efficiency(
            total_noise, thrust, power
        )
        
        results = {
            'noise_to_thrust_ratio_dB_per_N': ntr,
            'acoustic_efficiency': acoustic_eff,
            'total_noise_spl_db': total_noise,
            'thrust_N': thrust,
            'power_W': power,
            'propulsive_efficiency': efficiency,
            'broadband_noise_db': noise_results.get('broadband_spl_db', 0),
            'tonal_noise_db': noise_results.get('tonal_spl_db', 0),
            'vortex_noise_db': noise_results.get('vortex_spl_db', 0)
        }
        
        # Add comparison to baseline if provided
        if baseline_ntr is not None:
            reduction = self.calculate_noise_reduction_percentage(
                baseline_ntr, ntr
            )
            results['noise_reduction_percentage'] = reduction
            results['meets_15_percent_target'] = reduction >= 15.0
        
        return results
    
    def calculate_weighted_noise_metric(
        self,
        noise_spectrum: Dict[str, float],
        frequency_weights: Optional[Dict[str, float]] = None
    ) -> float:
        """
        Calculate frequency-weighted noise metric
        Accounts for human perception of different frequencies
        
        Args:
            noise_spectrum: Dictionary with frequency: SPL pairs
            frequency_weights: Optional custom frequency weighting
            
        Returns:
            Weighted noise level (dB)
        """
        if not noise_spectrum:
            return 0.0
        
        # A-weighting approximation for human hearing
        if frequency_weights is None:
            frequency_weights = {}
        
        # Convert SPL values to pressure, apply weights, sum
        total_weighted_pressure_sq = 0.0
        p_ref = 2e-5  # Reference pressure
        
        for freq_key, spl in noise_spectrum.items():
            # Extract frequency if available
            if 'frequency_hz' in freq_key:
                continue  # Skip frequency entries, only process SPL
            
            # Get weight (default 1.0)
            weight = frequency_weights.get(freq_key, 1.0)
            
            # Convert to pressure
            pressure = p_ref * 10 ** (spl / 20.0)
            
            # Add weighted pressure squared
            total_weighted_pressure_sq += (weight * pressure) ** 2
        
        # Convert back to dB
        if total_weighted_pressure_sq > 0:
            total_pressure = np.sqrt(total_weighted_pressure_sq)
            weighted_spl = 20 * np.log10(total_pressure / p_ref)
        else:
            weighted_spl = 0.0
        
        return weighted_spl
