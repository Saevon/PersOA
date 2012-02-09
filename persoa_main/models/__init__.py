"""
models relating to personality
"""

from persoa_main.models.choice import BasicChoice, LinearChoice, SubChoice
from persoa_main.models.group import TraitGroup
from persoa_main.models.trait import BasicTrait, LinearTrait

__all__ = [
    BasicChoice,
    LinearChoice,
    SubChoice,
    TraitGroup,
    BasicTrait,
    LinearTrait,
]
