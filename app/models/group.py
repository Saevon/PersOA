from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models

from app.constants.database import MAX_CHAR_LENGTH
from app.models.abstract import AbstractPersOAModel

class TraitGroup(AbstractPersOAModel):
    """
    A grouping for Traits.
    """

    name = models.CharField(
    	max_length=MAX_CHAR_LENGTH,
        blank=False,
        unique=True)
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

    def __unicode__(self):
    	return unicode(self.name)

    @property
    def traits(self):
        """"
        Combines the list of Traits
        """
        return self.basic_traits + self.linear_traits

    @seeded(2)
    def generate(self, num=None, seed=None):
        """
        Returns a choice for each of the groupings traits
        """
        group = {}
        for trait in self.traits:
            group[trait.name] = trait.generate(num, seed)

        return group

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
