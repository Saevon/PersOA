"""
models relating to personality
"""

from app.models.choice import BasicChoice, LinearChoice, SubChoice
from app.models.group import TraitGroup
from app.models.trait import BasicTrait, LinearTrait

__all__ = [
    BasicChoice,
    LinearChoice,
    SubChoice,
    TraitGroup,
    BasicTrait,
    LinearTrait,
]
