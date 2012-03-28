from django.db import models

from app.constants.database import MAX_CHAR_LENGTH
from app.models.abstract import AbstractPersOAModel

class AbstractChoice(AbstractPersOAModel):
    """
    A basic choice for a Trait
    """

    class Meta(AbstractPersOAModel.Meta):
        abstract = True

    name = models.CharField(
        max_length=MAX_CHAR_LENGTH,
        blank=False,
        unique=True)
    desc = models.TextField(blank=True)
    defn = models.CharField(
        max_length=MAX_CHAR_LENGTH,
        blank=True)

    def __unicode__(self):
        return unicode(self.name)

    def generated_data(self):
        """
        Returns data that is shown if this was generate
        """
        return self.name

    def details(self, include=None):
        """
        Returns a dict with the choice's details
        """
        details = self.data()
        if include is not None and 'traits' in include:
            details.update({
                'trait': self.trait.data(),
            })
        return details

    def data(self):
        """
        Returns a dict with the basic details
        """
        return {
            'name': self.name,
            'desc': self.desc,
            'defn': self.defn,
        }

class BasicChoice(AbstractChoice):
    """
    A standard Choice
    """
    trait = models.ForeignKey(
        'BasicTrait',
        related_name='choices',
        blank=False,
        null=False)

class LinearChoice(AbstractChoice):
    """
    A choice that is set on a scale
    """

    side = models.SmallIntegerField(blank=False, null=False)
    trait = models.ForeignKey(
        'LinearTrait',
        related_name='choices',
        blank=False,
        null=False)

    def data(self):
        details = super(LinearChoice, self).data()
        details.update({
            'pos': self.side,
        })
        return details

class SubChoice(AbstractPersOAModel):
    """
    A secondary level of a choice
    """

    name = models.CharField(
        max_length=MAX_CHAR_LENGTH,
        blank=False,
        unique=True)
    defn = models.CharField(
        max_length=MAX_CHAR_LENGTH,
        blank=True)
    choice = models.ForeignKey(
        'BasicChoice',
        related_name='sub_choices',
        blank=False,
        null=False)
