"""
Propeller design class for managing and evaluating designs
"""

from typing import Dict, Optional
import copy


class PropellerDesign:
    """
    Main class for managing propeller designs and their evaluation
    """
    
    def __init__(self, geometry: Dict, name: Optional[str] = None):
        """
        Initialize propeller design
        
        Args:
            geometry: Dictionary with propeller geometry parameters
            name: Optional name for the design
        """
        self.geometry = copy.deepcopy(geometry)
        self.name = name or geometry.get('name', 'Unnamed Design')
        self.performance_data = {}
        self.noise_data = {}
        
    def get_geometry(self) -> Dict:
        """Get propeller geometry"""
        return copy.deepcopy(self.geometry)
    
    def update_geometry(self, updates: Dict):
        """
        Update geometry parameters
        
        Args:
            updates: Dictionary with parameters to update
        """
        self.geometry.update(updates)
    
    def set_performance_data(self, data: Dict):
        """
        Store performance evaluation results
        
        Args:
            data: Performance data dictionary
        """
        self.performance_data = copy.deepcopy(data)
    
    def set_noise_data(self, data: Dict):
        """
        Store noise evaluation results
        
        Args:
            data: Noise data dictionary
        """
        self.noise_data = copy.deepcopy(data)
    
    def get_summary(self) -> Dict:
        """
        Get summary of design and performance
        
        Returns:
            Dictionary with design summary
        """
        summary = {
            'name': self.name,
            'num_blades': self.geometry.get('num_blades', 2),
            'diameter_m': self.geometry.get('diameter_m', 0.254),
            'design_type': self.geometry.get('design_type', 'custom'),
            'bio_inspired_features': self.geometry.get('bio_inspired_features', [])
        }
        
        # Add performance metrics if available
        if self.performance_data:
            summary['thrust_N'] = self.performance_data.get('thrust_N', 0)
            summary['power_W'] = self.performance_data.get('power_W', 0)
            summary['efficiency'] = self.performance_data.get('efficiency', 0)
        
        # Add noise metrics if available
        if self.noise_data:
            summary['noise_spl_db'] = self.noise_data.get('total_spl_db', 0)
            summary['ntr_dB_per_N'] = self.noise_data.get('noise_to_thrust_ratio_dB_per_N', 0)
            summary['noise_reduction_percentage'] = self.noise_data.get('noise_reduction_percentage', 0)
        
        return summary
    
    def compare_to_baseline(self, baseline_ntr: float) -> Dict:
        """
        Compare this design to a baseline
        
        Args:
            baseline_ntr: Baseline noise-to-thrust ratio
            
        Returns:
            Comparison metrics
        """
        if not self.noise_data:
            return {'error': 'No noise data available'}
        
        current_ntr = self.noise_data.get('noise_to_thrust_ratio_dB_per_N', 0)
        
        if baseline_ntr <= 0:
            return {'error': 'Invalid baseline NTR'}
        
        reduction_percentage = ((baseline_ntr - current_ntr) / baseline_ntr) * 100
        meets_target = reduction_percentage >= 15.0
        
        return {
            'baseline_ntr': baseline_ntr,
            'current_ntr': current_ntr,
            'reduction_percentage': reduction_percentage,
            'meets_15_percent_target': meets_target,
            'improvement_db': baseline_ntr - current_ntr
        }
    
    def export_geometry(self, format: str = 'dict') -> Dict:
        """
        Export geometry in specified format
        
        Args:
            format: Export format ('dict', 'json', etc.)
            
        Returns:
            Exported geometry
        """
        if format == 'dict':
            return self.get_geometry()
        else:
            # Add other formats as needed
            return self.get_geometry()
    
    def __repr__(self) -> str:
        """String representation"""
        return f"PropellerDesign(name='{self.name}', blades={self.geometry.get('num_blades', '?')})"
    
    def __str__(self) -> str:
        """Human-readable string"""
        summary = self.get_summary()
        output = [f"Propeller Design: {self.name}"]
        output.append(f"  Blades: {summary.get('num_blades', 'N/A')}")
        output.append(f"  Diameter: {summary.get('diameter_m', 'N/A'):.3f} m")
        
        if summary.get('bio_inspired_features'):
            output.append(f"  Bio-inspired features: {', '.join(summary['bio_inspired_features'])}")
        
        if 'thrust_N' in summary:
            output.append(f"  Thrust: {summary['thrust_N']:.2f} N")
            output.append(f"  Power: {summary['power_W']:.1f} W")
            output.append(f"  Efficiency: {summary['efficiency']:.1%}")
        
        if 'noise_spl_db' in summary:
            output.append(f"  Noise: {summary['noise_spl_db']:.1f} dB")
            output.append(f"  NTR: {summary['ntr_dB_per_N']:.2f} dB/N")
            if 'noise_reduction_percentage' in summary:
                output.append(f"  Noise reduction: {summary['noise_reduction_percentage']:.1f}%")
        
        return '\n'.join(output)
