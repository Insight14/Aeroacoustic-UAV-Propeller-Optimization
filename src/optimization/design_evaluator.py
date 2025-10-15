"""
Design evaluator for comprehensive propeller performance assessment
"""

from typing import Dict
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from aeroacoustics import NoiseAnalyzer, ThrustCalculator, AeroacousticMetrics
from bio_inspired import BioInspiredDesignFactory


class DesignEvaluator:
    """
    Comprehensive evaluator for propeller designs
    Combines aeroacoustic analysis with bio-inspired features
    """
    
    def __init__(self):
        """Initialize design evaluator"""
        self.noise_analyzer = NoiseAnalyzer()
        self.thrust_calculator = ThrustCalculator()
        self.metrics_calculator = AeroacousticMetrics()
        self.bio_factory = BioInspiredDesignFactory()
        
    def evaluate_design(
        self,
        propeller_geometry: Dict,
        operating_conditions: Dict,
        baseline_ntr: float = None
    ) -> Dict:
        """
        Comprehensive evaluation of a propeller design
        
        Args:
            propeller_geometry: Propeller geometry parameters
            operating_conditions: Operating conditions
            baseline_ntr: Optional baseline NTR for comparison
            
        Returns:
            Complete evaluation results
        """
        # Calculate noise
        noise_results = self.noise_analyzer.calculate_total_noise(
            propeller_geometry,
            operating_conditions,
            distance=1.0
        )
        
        # Calculate thrust and performance
        rpm = operating_conditions.get('rpm', 5000)
        blade_params = {
            'radius': propeller_geometry.get('radius_m', 0.127),
            'chord_root': propeller_geometry.get('chord_root', 0.03),
            'chord_tip': propeller_geometry.get('chord_tip', 0.015),
            'pitch_angle': propeller_geometry.get('pitch_angle', 10.0),
            'cl_slope': propeller_geometry.get('cl_slope', 2 * 3.14159)
        }
        num_blades = propeller_geometry.get('num_blades', 2)
        
        thrust_results = self.thrust_calculator.calculate_thrust_blade_element(
            rpm, blade_params, num_blades
        )
        
        # Calculate aeroacoustic metrics
        performance_metrics = self.metrics_calculator.evaluate_design_performance(
            noise_results,
            thrust_results,
            baseline_ntr
        )
        
        # Combine all results
        evaluation = {
            'noise_analysis': noise_results,
            'thrust_analysis': thrust_results,
            'performance_metrics': performance_metrics,
            'propeller_geometry': propeller_geometry,
            'operating_conditions': operating_conditions
        }
        
        return evaluation
    
    def evaluate_bio_inspired_design(
        self,
        base_geometry: Dict,
        features: list,
        operating_conditions: Dict,
        baseline_ntr: float = None
    ) -> Dict:
        """
        Evaluate a bio-inspired propeller design
        
        Args:
            base_geometry: Base propeller geometry
            features: List of bio-inspired features to apply
            operating_conditions: Operating conditions
            baseline_ntr: Optional baseline NTR for comparison
            
        Returns:
            Complete evaluation with bio-inspired modifications
        """
        # Create design with bio-inspired features
        modified_geometry = self.bio_factory.create_design(
            base_geometry,
            features
        )
        
        # Evaluate the modified design (baseline noise calculation)
        evaluation = self.evaluate_design(
            modified_geometry,
            operating_conditions,
            baseline_ntr
        )
        
        # Apply bio-inspired noise reductions
        if features:
            baseline_noise = evaluation['noise_analysis']['total_spl_db']
            
            # Extract feature parameters from modified geometry
            feature_params = {}
            if 'owl_serrations' in features:
                feature_params['owl_serrations'] = modified_geometry.get('trailing_edge_serrations', {})
            if 'humpback_tubercles' in features:
                feature_params['humpback_tubercles'] = modified_geometry.get('leading_edge_tubercles', {})
            if 'dragonfly_corrugations' in features:
                feature_params['dragonfly_corrugations'] = modified_geometry.get('surface_corrugations', {})
            
            # Calculate combined noise reduction
            reduction_results = self.bio_factory.estimate_combined_noise_reduction(
                baseline_noise,
                features,
                feature_params,
                operating_conditions
            )
            
            # Update noise analysis with reduced noise
            reduced_noise = reduction_results['final_noise_db']
            noise_reduction_db = reduction_results['total_reduction_db']
            
            # Update all noise metrics
            evaluation['noise_analysis']['total_spl_db'] = reduced_noise
            evaluation['noise_analysis']['noise_reduction_db'] = noise_reduction_db
            evaluation['noise_analysis']['bio_inspired_reduction'] = reduction_results
            
            # Recalculate performance metrics with reduced noise
            thrust_results = evaluation['thrust_analysis']
            performance_metrics = self.metrics_calculator.evaluate_design_performance(
                evaluation['noise_analysis'],
                thrust_results,
                baseline_ntr
            )
            evaluation['performance_metrics'] = performance_metrics
        
        # Add bio-inspired specific information
        evaluation['bio_inspired_features'] = features
        evaluation['modified_geometry'] = modified_geometry
        
        return evaluation
    
    def compare_designs(
        self,
        designs: list,
        operating_conditions: Dict
    ) -> Dict:
        """
        Compare multiple propeller designs
        
        Args:
            designs: List of propeller geometry dictionaries
            operating_conditions: Operating conditions
            
        Returns:
            Comparison results
        """
        results = []
        
        for i, design in enumerate(designs):
            name = design.get('name', f'Design {i+1}')
            evaluation = self.evaluate_design(design, operating_conditions)
            
            results.append({
                'name': name,
                'evaluation': evaluation,
                'ntr': evaluation['performance_metrics']['noise_to_thrust_ratio_dB_per_N'],
                'noise_db': evaluation['performance_metrics']['total_noise_spl_db'],
                'thrust_N': evaluation['performance_metrics']['thrust_N']
            })
        
        # Sort by NTR (lower is better)
        results.sort(key=lambda x: x['ntr'])
        
        # Find best design
        best_design = results[0]
        
        comparison = {
            'designs': results,
            'best_design': best_design,
            'num_designs': len(designs)
        }
        
        return comparison
