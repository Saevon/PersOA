"""
models relating to personality
"""

from persoa_main.models.choice import BasicChoice, LinearChoice, MultiChoice
from persoa_main.models.trait import BasicTrait, LinearTrait, MultiTrait

__all__ = [
    BasicChoice,
    ScaleChoice,
    BasicTrait,
    LinearTrait,
    MultiTrait,
]