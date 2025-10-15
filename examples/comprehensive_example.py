"""
Comprehensive example demonstrating bio-inspired UAV propeller optimization
for achieving 15% noise reduction target
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from propeller_design import BaselinePropeller, PropellerDesign
from aeroacoustics import NoiseAnalyzer, ThrustCalculator, AeroacousticMetrics
from bio_inspired import BioInspiredDesignFactory
from optimization import PropellerOptimizer, DesignEvaluator


def main():
    """
    Main demonstration of the bio-inspired propeller optimization workflow
    """
    
    print("=" * 80)
    print("Bio-Inspired UAV Propeller Aeroacoustic Optimization")
    print("Target: Minimum 15% reduction in Noise-to-Thrust Ratio")
    print("=" * 80)
    print()
    
    # Step 1: Get baseline propeller design
    print("Step 1: Establishing Baseline")
    print("-" * 80)
    baseline_geometry = BaselinePropeller.get_standard_2_blade()
    operating_conditions = BaselinePropeller.get_typical_operating_conditions()
    
    print(f"Baseline Design: {baseline_geometry['name']}")
    print(f"  Blades: {baseline_geometry['num_blades']}")
    print(f"  Diameter: {baseline_geometry['diameter_m']*1000:.1f} mm")
    print(f"  Operating RPM: {operating_conditions['rpm']}")
    print()
    
    # Step 2: Evaluate baseline performance
    print("Step 2: Baseline Performance Evaluation")
    print("-" * 80)
    evaluator = DesignEvaluator()
    baseline_eval = evaluator.evaluate_design(baseline_geometry, operating_conditions)
    
    baseline_metrics = baseline_eval['performance_metrics']
    baseline_ntr = baseline_metrics['noise_to_thrust_ratio_dB_per_N']
    
    print(f"Baseline Results:")
    print(f"  Noise: {baseline_metrics['total_noise_spl_db']:.1f} dB")
    print(f"  Thrust: {baseline_metrics['thrust_N']:.2f} N")
    print(f"  Power: {baseline_metrics['power_W']:.1f} W")
    print(f"  Efficiency: {baseline_metrics['propulsive_efficiency']:.1%}")
    print(f"  Noise-to-Thrust Ratio: {baseline_ntr:.2f} dB/N")
    print()
    
    # Step 3: Generate bio-inspired design variants
    print("Step 3: Generating Bio-Inspired Design Variants")
    print("-" * 80)
    bio_factory = BioInspiredDesignFactory()
    variants = bio_factory.generate_design_variants(baseline_geometry, num_variants=5)
    
    print(f"Generated {len(variants)} design variants:")
    for variant in variants:
        print(f"  - {variant['name']}: {variant['features']}")
    print()
    
    # Step 4: Evaluate each variant
    print("Step 4: Evaluating Design Variants")
    print("-" * 80)
    
    results = []
    for variant in variants:
        name = variant['name']
        geometry = variant['geometry']
        features = variant['features']
        
        # Use appropriate evaluation method
        if features:
            evaluation = evaluator.evaluate_bio_inspired_design(
                baseline_geometry,
                features,
                operating_conditions, 
                baseline_ntr=baseline_ntr
            )
        else:
            evaluation = evaluator.evaluate_design(
                geometry, 
                operating_conditions, 
                baseline_ntr=baseline_ntr
            )
        
        metrics = evaluation['performance_metrics']
        ntr = metrics['noise_to_thrust_ratio_dB_per_N']
        noise_reduction = metrics.get('noise_reduction_percentage', 0)
        meets_target = metrics.get('meets_15_percent_target', False)
        
        results.append({
            'name': name,
            'features': features,
            'ntr': ntr,
            'noise_db': metrics['total_noise_spl_db'],
            'thrust_N': metrics['thrust_N'],
            'noise_reduction_pct': noise_reduction,
            'meets_target': meets_target,
            'evaluation': evaluation
        })
        
        print(f"\n{name}:")
        print(f"  Features: {', '.join(features) if features else 'None'}")
        print(f"  Noise: {metrics['total_noise_spl_db']:.1f} dB")
        print(f"  Thrust: {metrics['thrust_N']:.2f} N")
        print(f"  NTR: {ntr:.2f} dB/N")
        print(f"  Noise Reduction: {noise_reduction:.1f}%")
        print(f"  Meets 15% Target: {'YES ✓' if meets_target else 'NO'}")
    
    print()
    
    # Step 5: Find best design
    print("Step 5: Identifying Optimal Design")
    print("-" * 80)
    
    # Sort by noise reduction
    results.sort(key=lambda x: x['noise_reduction_pct'], reverse=True)
    best_result = results[0]
    
    print(f"\nBest Design: {best_result['name']}")
    print(f"  Noise Reduction: {best_result['noise_reduction_pct']:.1f}%")
    print(f"  NTR Improvement: {baseline_ntr - best_result['ntr']:.2f} dB/N")
    print(f"  Meets 15% Target: {'YES ✓' if best_result['meets_target'] else 'NO'}")
    print()
    
    # Step 6: Optimization for further improvement
    print("Step 6: Parameter Optimization for Best Features")
    print("-" * 80)
    
    if best_result['features']:
        optimizer = PropellerOptimizer()
        optimized = optimizer.optimize_bio_inspired_parameters(
            baseline_geometry,
            best_result['features'],
            operating_conditions,
            num_iterations=10
        )
        
        opt_metrics = optimized['evaluation']['performance_metrics']
        opt_ntr = opt_metrics['noise_to_thrust_ratio_dB_per_N']
        opt_reduction = opt_metrics.get('noise_reduction_percentage', 0)
        
        print(f"\nOptimized Design Results:")
        print(f"  Noise Reduction: {opt_reduction:.1f}%")
        print(f"  NTR: {opt_ntr:.2f} dB/N")
        print(f"  Improvement over baseline: {optimized['improvement_over_baseline_percentage']:.1f}%")
        print(f"  Meets 15% Target: {'YES ✓' if opt_reduction >= 15.0 else 'NO'}")
        print()
    
    # Step 7: Summary and recommendations
    print("=" * 80)
    print("Summary and Recommendations")
    print("=" * 80)
    print()
    print("Bio-Inspired Features Implemented:")
    print("  1. Owl Wing Serrations - Trailing edge modifications for noise reduction")
    print("  2. Humpback Whale Tubercles - Leading edge bumps for flow control")
    print("  3. Dragonfly Corrugations - Surface corrugations for structural rigidity")
    print()
    
    # Find designs meeting target
    successful_designs = [r for r in results if r['meets_target']]
    
    if successful_designs:
        print(f"✓ Success! {len(successful_designs)} design(s) meet the 15% noise reduction target:")
        for design in successful_designs:
            print(f"  - {design['name']}: {design['noise_reduction_pct']:.1f}% reduction")
    else:
        print("Note: Combined features approach the target. Further optimization recommended:")
        print("  - Fine-tune bio-inspired feature parameters")
        print("  - Combine with advanced materials")
        print("  - Consider additional nature-inspired modifications")
    
    print()
    print("Research Contributions:")
    print("  ✓ Nature-inspired modifications (not geometric parameters)")
    print("  ✓ Comprehensive aeroacoustic analysis framework")
    print("  ✓ Systematic evaluation of bio-inspired features")
    print("  ✓ Optimization framework for design space exploration")
    print()
    print("Next Steps:")
    print("  1. CFD validation of bio-inspired modifications")
    print("  2. Physical prototyping and testing")
    print("  3. Wind tunnel acoustic measurements")
    print("  4. Flight testing with real-world validation")
    print()
    print("=" * 80)


if __name__ == '__main__':
    main()
