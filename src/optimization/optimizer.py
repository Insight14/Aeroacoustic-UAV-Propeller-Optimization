"""
Propeller optimizer for finding optimal bio-inspired designs
"""

import numpy as np
from typing import Dict, List, Callable, Optional
from .design_evaluator import DesignEvaluator


class PropellerOptimizer:
    """
    Optimization framework for bio-inspired propeller designs
    """
    
    def __init__(self):
        """Initialize optimizer"""
        self.evaluator = DesignEvaluator()
        self.history = []
        
    def optimize_bio_inspired_parameters(
        self,
        base_geometry: Dict,
        features: List[str],
        operating_conditions: Dict,
        objective: str = 'minimize_ntr',
        num_iterations: int = 20
    ) -> Dict:
        """
        Optimize parameters for bio-inspired features
        
        Uses simple grid search with random sampling for exploration
        
        Args:
            base_geometry: Base propeller geometry
            features: Bio-inspired features to optimize
            operating_conditions: Operating conditions
            objective: Optimization objective
            num_iterations: Number of optimization iterations
            
        Returns:
            Optimal design and parameters
        """
        best_design = None
        best_score = float('inf') if objective == 'minimize_ntr' else -float('inf')
        
        # Baseline evaluation
        baseline_eval = self.evaluator.evaluate_design(
            base_geometry,
            operating_conditions
        )
        baseline_ntr = baseline_eval['performance_metrics']['noise_to_thrust_ratio_dB_per_N']
        
        for iteration in range(num_iterations):
            # Generate random parameter variations
            custom_configs = self._generate_random_configs(features)
            
            # Evaluate design with these parameters
            evaluation = self.evaluator.evaluate_bio_inspired_design(
                base_geometry,
                features,
                operating_conditions,
                baseline_ntr
            )
            
            # Extract score based on objective
            if objective == 'minimize_ntr':
                score = evaluation['performance_metrics']['noise_to_thrust_ratio_dB_per_N']
                is_better = score < best_score
            elif objective == 'maximize_efficiency':
                score = evaluation['thrust_analysis']['efficiency']
                is_better = score > best_score
            else:  # maximize noise reduction
                score = evaluation['performance_metrics'].get('noise_reduction_percentage', 0)
                is_better = score > best_score
            
            # Update best design
            if is_better:
                best_score = score
                best_design = {
                    'geometry': evaluation['modified_geometry'],
                    'evaluation': evaluation,
                    'configs': custom_configs,
                    'iteration': iteration,
                    'score': score
                }
            
            # Store in history
            self.history.append({
                'iteration': iteration,
                'score': score,
                'ntr': evaluation['performance_metrics']['noise_to_thrust_ratio_dB_per_N']
            })
        
        # Calculate improvement over baseline
        if best_design:
            improvement_percentage = (
                (baseline_ntr - best_design['evaluation']['performance_metrics']['noise_to_thrust_ratio_dB_per_N'])
                / baseline_ntr * 100
            )
            best_design['improvement_over_baseline_percentage'] = improvement_percentage
            best_design['baseline_ntr'] = baseline_ntr
        
        return best_design
    
    def _generate_random_configs(self, features: List[str]) -> Dict:
        """
        Generate random configurations for bio-inspired features
        
        Args:
            features: List of features
            
        Returns:
            Dictionary of configurations
        """
        configs = {}
        
        if 'owl_serrations' in features:
            configs['owl_serrations'] = {
                'serration_depth_ratio': np.random.uniform(0.03, 0.08),
                'serration_wavelength_ratio': np.random.uniform(0.015, 0.04)
            }
        
        if 'humpback_tubercles' in features:
            configs['humpback_tubercles'] = {
                'amplitude_ratio': np.random.uniform(0.08, 0.14),
                'wavelength_ratio': np.random.uniform(0.20, 0.35)
            }
        
        if 'dragonfly_corrugations' in features:
            configs['dragonfly_corrugations'] = {
                'corrugation_depth_ratio': np.random.uniform(0.025, 0.045),
                'corrugation_wavelength_ratio': np.random.uniform(0.04, 0.07)
            }
        
        return configs
    
    def multi_objective_optimization(
        self,
        base_geometry: Dict,
        feature_combinations: List[List[str]],
        operating_conditions: Dict,
        weights: Optional[Dict] = None
    ) -> List[Dict]:
        """
        Multi-objective optimization across feature combinations
        
        Args:
            base_geometry: Base geometry
            feature_combinations: List of feature combination lists
            operating_conditions: Operating conditions
            weights: Weights for different objectives
            
        Returns:
            Pareto-optimal designs
        """
        if weights is None:
            weights = {
                'noise_reduction': 0.6,
                'efficiency': 0.3,
                'manufacturability': 0.1
            }
        
        results = []
        
        # Baseline
        baseline_eval = self.evaluator.evaluate_design(
            base_geometry,
            operating_conditions
        )
        baseline_ntr = baseline_eval['performance_metrics']['noise_to_thrust_ratio_dB_per_N']
        
        for features in feature_combinations:
            # Evaluate this combination
            evaluation = self.evaluator.evaluate_bio_inspired_design(
                base_geometry,
                features,
                operating_conditions,
                baseline_ntr
            )
            
            # Calculate multi-objective score
            noise_reduction = evaluation['performance_metrics'].get('noise_reduction_percentage', 0)
            efficiency = evaluation['thrust_analysis']['efficiency']
            
            # Manufacturability penalty (more features = harder to manufacture)
            manufacturability_score = 100 - len(features) * 15
            
            # Weighted score
            total_score = (
                weights['noise_reduction'] * noise_reduction +
                weights['efficiency'] * efficiency * 100 +
                weights['manufacturability'] * manufacturability_score
            )
            
            results.append({
                'features': features,
                'evaluation': evaluation,
                'noise_reduction_percentage': noise_reduction,
                'efficiency': efficiency,
                'manufacturability_score': manufacturability_score,
                'total_score': total_score
            })
        
        # Sort by total score
        results.sort(key=lambda x: x['total_score'], reverse=True)
        
        return results
    
    def get_optimization_history(self) -> List[Dict]:
        """
        Get optimization history
        
        Returns:
            List of iteration results
        """
        return self.history
    
    def clear_history(self):
        """Clear optimization history"""
        self.history = []
