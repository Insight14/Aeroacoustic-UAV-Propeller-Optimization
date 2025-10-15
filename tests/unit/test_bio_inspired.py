"""
Unit tests for bio-inspired design modules
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from bio_inspired import OwlWingSerrations, HumpbackWhaleTubercles, DragonflyCorrugations
from bio_inspired import BioInspiredDesignFactory


class TestOwlSerrations(unittest.TestCase):
    """Test cases for owl wing serrations"""
    
    def setUp(self):
        self.owl = OwlWingSerrations()
    
    def test_geometry_calculation(self):
        """Test serration geometry calculation"""
        params = self.owl.calculate_serration_geometry(
            chord_length=0.05
        )
        self.assertIn('depth_m', params)
        self.assertIn('wavelength_m', params)
        self.assertGreater(params['depth_m'], 0)
    
    def test_noise_reduction_estimate(self):
        """Test noise reduction estimation"""
        params = self.owl.calculate_serration_geometry(0.05)
        reduction = self.owl.estimate_noise_reduction(
            baseline_noise_db=80.0,
            serration_params=params,
            frequency_hz=1000,
            flow_velocity=10.0
        )
        self.assertIn('noise_reduction_db', reduction)
        self.assertGreater(reduction['noise_reduction_db'], 0)
    
    def test_apply_to_blade(self):
        """Test applying serrations to blade"""
        base_geometry = {
            'chord_length': 0.05,
            'drag_coefficient': 0.02
        }
        modified = self.owl.apply_to_blade_design(base_geometry)
        self.assertIn('trailing_edge_serrations', modified)


class TestHumpbackTubercles(unittest.TestCase):
    """Test cases for humpback whale tubercles"""
    
    def setUp(self):
        self.humpback = HumpbackWhaleTubercles()
    
    def test_geometry_calculation(self):
        """Test tubercle geometry calculation"""
        params = self.humpback.calculate_tubercle_geometry(
            blade_span=0.127
        )
        self.assertIn('num_tubercles', params)
        self.assertGreater(params['num_tubercles'], 0)
    
    def test_noise_reduction_estimate(self):
        """Test noise reduction estimation"""
        params = self.humpback.calculate_tubercle_geometry(0.127)
        operating_conditions = {'angle_of_attack': 5.0}
        
        reduction = self.humpback.estimate_noise_reduction(
            baseline_noise_db=80.0,
            tubercle_params=params,
            operating_conditions=operating_conditions
        )
        self.assertIn('noise_reduction_db', reduction)
    
    def test_apply_to_blade(self):
        """Test applying tubercles to blade"""
        base_geometry = {
            'radius': 0.127,
            'cl_max': 1.2
        }
        modified = self.humpback.apply_to_blade_design(base_geometry)
        self.assertIn('leading_edge_tubercles', modified)


class TestDragonflyCorrugations(unittest.TestCase):
    """Test cases for dragonfly corrugations"""
    
    def setUp(self):
        self.dragonfly = DragonflyCorrugations()
    
    def test_geometry_calculation(self):
        """Test corrugation geometry calculation"""
        params = self.dragonfly.calculate_corrugation_geometry(
            chord_length=0.05
        )
        self.assertIn('depth_m', params)
        self.assertIn('num_corrugations', params)
    
    def test_noise_reduction_estimate(self):
        """Test noise reduction estimation"""
        params = self.dragonfly.calculate_corrugation_geometry(0.05)
        
        reduction = self.dragonfly.estimate_noise_reduction(
            baseline_noise_db=80.0,
            corrugation_params=params,
            reynolds_number=200000,
            flow_velocity=10.0
        )
        self.assertIn('noise_reduction_db', reduction)
    
    def test_structural_benefits(self):
        """Test structural benefits calculation"""
        params = self.dragonfly.calculate_corrugation_geometry(0.05)
        benefits = self.dragonfly.estimate_structural_benefits(
            params,
            blade_material={}
        )
        self.assertIn('stiffness_increase_percentage', benefits)


class TestBioInspiredFactory(unittest.TestCase):
    """Test cases for bio-inspired design factory"""
    
    def setUp(self):
        self.factory = BioInspiredDesignFactory()
    
    def test_create_single_feature(self):
        """Test creating design with single feature"""
        base_geometry = {'chord_length': 0.05, 'radius': 0.127}
        modified = self.factory.create_design(
            base_geometry,
            features=['owl_serrations']
        )
        self.assertIn('trailing_edge_serrations', modified)
    
    def test_create_multiple_features(self):
        """Test creating design with multiple features"""
        base_geometry = {'chord_length': 0.05, 'radius': 0.127}
        modified = self.factory.create_design(
            base_geometry,
            features=['owl_serrations', 'humpback_tubercles']
        )
        self.assertIn('bio_inspired_features', modified)
        self.assertEqual(len(modified['bio_inspired_features']), 2)
    
    def test_generate_variants(self):
        """Test generating design variants"""
        base_geometry = {'chord_length': 0.05, 'radius': 0.127}
        variants = self.factory.generate_design_variants(
            base_geometry,
            num_variants=3
        )
        self.assertEqual(len(variants), 3)
        self.assertEqual(variants[0]['name'], 'Baseline')


if __name__ == '__main__':
    unittest.main()
