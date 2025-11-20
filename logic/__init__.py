"""
Logic module for Wumpus World
Propositional logic and resolution inference
"""

from .propositional import PropositionalKB
from .resolution import ResolutionEngine

__all__ = ['PropositionalKB', 'ResolutionEngine']