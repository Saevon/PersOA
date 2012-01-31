from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models

from persoa_main.constants.database import MAX_CHAR_LENGTH
from persoa_main.models.abstract import AbstractPersOAModel

class TraitGroup(AbstractPersOAModel):
    """
    A grouping for Traits.
    """

    name = models.CharField(
    	max_length=MAX_CHAR_LENGTH,
        blank=False)
    desc = models.TextField(blank=True)
    basic_traits = models.ManyToManyField(
        'BasicTrait',
        related_name='groups',
        blank=True,
        null=True)
    linear_traits = models.ManyToManyField(
        'LinearTrait',
        related_name='groups',
        blank=True,
        null=True)

    @property
    def traits(self)):
        """"
        Combines the list of Traits
        """
        return self.basic_traits + self.linear_traits

    def generate(self, *args, **kwargs):
        """
        Returns a choice from this trait
        """
        return NotImplemented

    def details(self, include=None):
        """
        Returns a dict with the choice's details
        """
        details = self.data()
        if include is not None and 'traits' in include:
            details.remove('traits')
            details.update({
                'traits': [trait.details(include) for trait in self.traits]
            })
        return details

    def data(self):
        """
        Returns a dict with the basic details
        """
        return {
            'name': self.name,
            'desc': self.desc,
        }
