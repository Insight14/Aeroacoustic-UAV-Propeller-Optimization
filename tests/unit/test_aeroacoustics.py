"""
Unit tests for aeroacoustic analysis modules
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from aeroacoustics import NoiseAnalyzer, ThrustCalculator, AeroacousticMetrics


class TestNoiseAnalyzer(unittest.TestCase):
    """Test cases for NoiseAnalyzer"""
    
    def setUp(self):
        self.analyzer = NoiseAnalyzer()
        
    def test_spl_calculation(self):
        """Test SPL calculation"""
        spl = self.analyzer.calculate_spl(pressure=0.02, distance=1.0)
        self.assertGreater(spl, 0)
        self.assertIsInstance(spl, float)
    
    def test_broadband_noise(self):
        """Test broadband noise calculation"""
        noise = self.analyzer.calculate_broadband_noise(
            velocity=10.0,
            chord_length=0.05,
            blade_thickness=0.005,
            angle_of_attack=5.0
        )
        self.assertGreater(noise, 0)
        self.assertLess(noise, 200)  # Reasonable range
    
    def test_tonal_noise(self):
        """Test tonal noise calculation"""
        results = self.analyzer.calculate_tonal_noise(
            rpm=5000,
            num_blades=2,
            tip_speed=50.0
        )
        self.assertIn('BPF_harmonic_1', results)
        self.assertGreater(results['BPF_harmonic_1'], 0)
    
    def test_total_noise(self):
        """Test total noise calculation"""
        propeller_params = {
            'chord_length': 0.05,
            'blade_thickness': 0.005,
            'num_blades': 2,
            'radius': 0.127,
            'angle_of_attack': 5.0
        }
        operating_conditions = {
            'rpm': 5000,
            'velocity': 10.0
        }
        
        results = self.analyzer.calculate_total_noise(
            propeller_params,
            operating_conditions
        )
        
        self.assertIn('total_spl_db', results)
        self.assertGreater(results['total_spl_db'], 0)


class TestThrustCalculator(unittest.TestCase):
    """Test cases for ThrustCalculator"""
    
    def setUp(self):
        self.calculator = ThrustCalculator()
    
    def test_momentum_theory(self):
        """Test momentum theory thrust calculation"""
        thrust = self.calculator.calculate_thrust_momentum_theory(
            rpm=5000,
            diameter=0.254,
            power=100
        )
        self.assertGreater(thrust, 0)
        self.assertLess(thrust, 100)  # Reasonable range
    
    def test_blade_element_theory(self):
        """Test blade element theory calculation"""
        blade_params = {
            'radius': 0.127,
            'chord_root': 0.03,
            'chord_tip': 0.015,
            'pitch_angle': 10.0
        }
        
        results = self.calculator.calculate_thrust_blade_element(
            rpm=5000,
            blade_params=blade_params,
            num_blades=2
        )
        
        self.assertIn('thrust_N', results)
        self.assertIn('power_W', results)
        self.assertGreater(results['thrust_N'], 0)
    
    def test_figure_of_merit(self):
        """Test figure of merit calculation"""
        fm = self.calculator.calculate_figure_of_merit(
            thrust=5.0,
            power=100.0,
            radius=0.127
        )
        self.assertGreater(fm, 0)
        self.assertLessEqual(fm, 1.0)


class TestAeroacousticMetrics(unittest.TestCase):
    """Test cases for AeroacousticMetrics"""
    
    def setUp(self):
        self.metrics = AeroacousticMetrics()
    
    def test_ntr_calculation(self):
        """Test noise-to-thrust ratio calculation"""
        ntr = self.metrics.calculate_noise_to_thrust_ratio(
            noise_spl_db=80.0,
            thrust_N=5.0
        )
        self.assertGreater(ntr, 0)
        self.assertEqual(ntr, 80.0 / 5.0)
    
    def test_noise_reduction_percentage(self):
        """Test noise reduction percentage calculation"""
        reduction = self.metrics.calculate_noise_reduction_percentage(
            baseline_ntr=20.0,
            modified_ntr=17.0
        )
        self.assertEqual(reduction, 15.0)  # (20-17)/20 * 100 = 15%
    
    def test_design_evaluation(self):
        """Test comprehensive design evaluation"""
        noise_results = {
            'total_spl_db': 80.0,
            'broadband_spl_db': 70.0,
            'tonal_spl_db': 75.0,
            'vortex_spl_db': 65.0
        }
        thrust_results = {
            'thrust_N': 5.0,
            'power_W': 100.0,
            'efficiency': 0.65
        }
        
        results = self.metrics.evaluate_design_performance(
            noise_results,
            thrust_results,
            baseline_ntr=20.0
        )
        
        self.assertIn('noise_to_thrust_ratio_dB_per_N', results)
        self.assertIn('meets_15_percent_target', results)


if __name__ == '__main__':
    unittest.main()
