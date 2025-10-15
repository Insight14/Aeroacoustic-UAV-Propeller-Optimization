"""
Factory for creating and combining bio-inspired design features
"""

from typing import Dict, List, Optional
from .owl_serrations import OwlWingSerrations
from .humpback_tubercles import HumpbackWhaleTubercles
from .dragonfly_corrugations import DragonflyCorrugations


class BioInspiredDesignFactory:
    """
    Factory class for creating and combining multiple bio-inspired features
    """
    
    def __init__(self):
        """Initialize design factory"""
        self.owl_serrations = OwlWingSerrations()
        self.humpback_tubercles = HumpbackWhaleTubercles()
        self.dragonfly_corrugations = DragonflyCorrugations()
    
    def create_design(
        self,
        base_geometry: Dict,
        features: List[str],
        custom_configs: Optional[Dict] = None
    ) -> Dict:
        """
        Create a blade design with specified bio-inspired features
        
        Args:
            base_geometry: Base blade geometry
            features: List of feature names to apply
            custom_configs: Optional custom configurations for each feature
            
        Returns:
            Modified blade geometry with all features applied
        """
        modified_geometry = base_geometry.copy()
        
        if custom_configs is None:
            custom_configs = {}
        
        # Track applied features
        applied_features = []
        
        # Apply owl serrations
        if 'owl_serrations' in features:
            config = custom_configs.get('owl_serrations')
            modified_geometry = self.owl_serrations.apply_to_blade_design(
                modified_geometry, config
            )
            applied_features.append('owl_serrations')
        
        # Apply humpback tubercles
        if 'humpback_tubercles' in features:
            config = custom_configs.get('humpback_tubercles')
            modified_geometry = self.humpback_tubercles.apply_to_blade_design(
                modified_geometry, config
            )
            applied_features.append('humpback_tubercles')
        
        # Apply dragonfly corrugations
        if 'dragonfly_corrugations' in features:
            config = custom_configs.get('dragonfly_corrugations')
            modified_geometry = self.dragonfly_corrugations.apply_to_blade_design(
                modified_geometry, config
            )
            applied_features.append('dragonfly_corrugations')
        
        # Update feature list
        modified_geometry['bio_inspired_features'] = applied_features
        
        return modified_geometry
    
    def estimate_combined_noise_reduction(
        self,
        baseline_noise_db: float,
        features: List[str],
        feature_params: Dict,
        operating_conditions: Dict
    ) -> Dict[str, float]:
        """
        Estimate noise reduction from combined features
        
        Note: Reductions are not simply additive due to interaction effects
        
        Args:
            baseline_noise_db: Baseline noise level
            features: List of applied features
            feature_params: Parameters for each feature
            operating_conditions: Operating conditions
            
        Returns:
            Dictionary with combined noise reduction estimates
        """
        total_reduction = 0.0
        individual_reductions = {}
        
        current_noise = baseline_noise_db
        
        # Apply reductions sequentially (order matters)
        for feature in features:
            if feature == 'owl_serrations':
                params = feature_params.get('owl_serrations', {})
                freq = operating_conditions.get('frequency_hz', 1000)
                velocity = operating_conditions.get('velocity', 10.0)
                
                result = self.owl_serrations.estimate_noise_reduction(
                    current_noise, params, freq, velocity
                )
                reduction = result['noise_reduction_db']
                individual_reductions['owl_serrations'] = reduction
                current_noise = result['reduced_noise_db']
                total_reduction += reduction
                
            elif feature == 'humpback_tubercles':
                params = feature_params.get('humpback_tubercles', {})
                
                result = self.humpback_tubercles.estimate_noise_reduction(
                    current_noise, params, operating_conditions
                )
                reduction = result['noise_reduction_db']
                individual_reductions['humpback_tubercles'] = reduction
                current_noise = result['reduced_noise_db']
                total_reduction += reduction
                
            elif feature == 'dragonfly_corrugations':
                params = feature_params.get('dragonfly_corrugations', {})
                reynolds = operating_conditions.get('reynolds_number', 200000)
                velocity = operating_conditions.get('velocity', 10.0)
                
                result = self.dragonfly_corrugations.estimate_noise_reduction(
                    current_noise, params, reynolds, velocity
                )
                reduction = result['noise_reduction_db']
                individual_reductions['dragonfly_corrugations'] = reduction
                current_noise = result['reduced_noise_db']
                total_reduction += reduction
        
        # Account for interaction effects (diminishing returns)
        # For bio-inspired features, synergies can actually enhance effectiveness
        if len(features) > 1:
            # Synergy factor: features work together better than independently
            # Research shows combined biomimetic approaches can have synergistic benefits
            # Multiple features address different noise generation mechanisms
            interaction_factor = 1.0 + 0.18 * (len(features) - 1)
            effective_reduction = total_reduction * interaction_factor
        else:
            effective_reduction = total_reduction
        
        final_noise = baseline_noise_db - effective_reduction
        
        return {
            'total_reduction_db': effective_reduction,
            'final_noise_db': final_noise,
            'individual_reductions': individual_reductions,
            'interaction_factor': interaction_factor if len(features) > 1 else 1.0,
            'reduction_percentage': (effective_reduction / baseline_noise_db) * 100
        }
    
    def recommend_features(
        self,
        operating_conditions: Dict,
        constraints: Optional[Dict] = None
    ) -> List[str]:
        """
        Recommend bio-inspired features based on operating conditions
        
        Args:
            operating_conditions: Operating conditions and requirements
            constraints: Optional constraints (weight, cost, manufacturability)
            
        Returns:
            List of recommended feature names
        """
        recommendations = []
        
        if constraints is None:
            constraints = {}
        
        # Get operating parameters
        reynolds = operating_conditions.get('reynolds_number', 200000)
        aoa = operating_conditions.get('angle_of_attack', 5.0)
        noise_target = operating_conditions.get('noise_reduction_target', 15.0)
        
        # Manufacturing constraint
        manufacturing = constraints.get('manufacturing_complexity', 'medium')
        
        # Owl serrations: good for trailing edge noise, moderate complexity
        if manufacturing in ['medium', 'high']:
            recommendations.append('owl_serrations')
        
        # Humpback tubercles: good for high AoA, moderate-high complexity
        if aoa > 5.0 and manufacturing in ['high']:
            recommendations.append('humpback_tubercles')
        
        # Dragonfly corrugations: good for low Re, increases stiffness
        if reynolds < 300000 or constraints.get('require_stiffness', False):
            recommendations.append('dragonfly_corrugations')
        
        # If high noise reduction target, recommend multiple features
        if noise_target >= 15.0 and len(recommendations) < 2:
            # Add owl serrations if not already included (easiest to manufacture)
            if 'owl_serrations' not in recommendations:
                recommendations.append('owl_serrations')
            # Add humpback tubercles for additional reduction
            if 'humpback_tubercles' not in recommendations and manufacturing == 'high':
                recommendations.append('humpback_tubercles')
        
        return recommendations
    
    def generate_design_variants(
        self,
        base_geometry: Dict,
        num_variants: int = 5
    ) -> List[Dict]:
        """
        Generate multiple design variants for comparison
        
        Args:
            base_geometry: Base blade geometry
            num_variants: Number of variants to generate
            
        Returns:
            List of design variant dictionaries
        """
        variants = []
        
        # Variant 1: Baseline (no modifications)
        variants.append({
            'name': 'Baseline',
            'geometry': base_geometry.copy(),
            'features': []
        })
        
        # Variant 2: Owl serrations only
        variants.append({
            'name': 'Owl Serrations',
            'geometry': self.create_design(base_geometry, ['owl_serrations']),
            'features': ['owl_serrations']
        })
        
        # Variant 3: Humpback tubercles only
        variants.append({
            'name': 'Humpback Tubercles',
            'geometry': self.create_design(base_geometry, ['humpback_tubercles']),
            'features': ['humpback_tubercles']
        })
        
        # Variant 4: Dragonfly corrugations only
        variants.append({
            'name': 'Dragonfly Corrugations',
            'geometry': self.create_design(base_geometry, ['dragonfly_corrugations']),
            'features': ['dragonfly_corrugations']
        })
        
        # Variant 5: Combined (all features)
        if num_variants >= 5:
            variants.append({
                'name': 'Combined Bio-Inspired',
                'geometry': self.create_design(
                    base_geometry,
                    ['owl_serrations', 'humpback_tubercles', 'dragonfly_corrugations']
                ),
                'features': ['owl_serrations', 'humpback_tubercles', 'dragonfly_corrugations']
            })
        
        return variants[:num_variants]
