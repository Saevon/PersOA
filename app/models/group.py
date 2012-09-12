from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models

from app.constants.database import MAX_CHAR_LENGTH
from app.models.abstract import AbstractPersOAModel
from itertools import chain
from utils.decorators import seeded

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
        return chain(self.basic_traits.all(), self.linear_traits.all())

    @seeded(2)
    def generate(self, num=None, seed=None, include=None):
        """
        Returns a choice for each of the groupings traits
        """
        if num is None:
            num = 1

        groups = []

        for i in range(num):
            group = {}
            for trait in self.traits:
                group[trait.name] = [
                    i.details(include)
                    for i in trait.generate(seed=seed)
                ]

            groups.append(group)

        return group

    def details(self, include=None):
        """
        Returns a dict with the choice's details
        """
        details = self.data()

        if include is None:
            pass
        elif include['group_name']:
            return self.name
        elif include['group_desc']:
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
