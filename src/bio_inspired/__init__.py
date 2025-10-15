"""
Bio-inspired design patterns module
Implements nature-inspired modifications for noise reduction
"""

from .owl_serrations import OwlWingSerrations
from .humpback_tubercles import HumpbackWhaleTubercles
from .dragonfly_corrugations import DragonflyCorrugations
from .design_factory import BioInspiredDesignFactory

__all__ = [
    'OwlWingSerrations',
    'HumpbackWhaleTubercles', 
    'DragonflyCorrugations',
    'BioInspiredDesignFactory'
]
