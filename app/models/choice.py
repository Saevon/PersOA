from django.db import models

from app.constants.database import MAX_CHAR_LENGTH, MAX_DEFN_LENGTH
from app.models.abstract import AbstractPersOAModel
from utils.decorators import seeded

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
        max_length=MAX_DEFN_LENGTH,
        blank=True)

    def __unicode__(self):
        return unicode(self.name)

    @seeded(1)
    def generated_data(self, seed=None):
        """
        Returns data that is shown if this was generated
            Note: if this choice has subchoices, then one is generated in this function
            and a ' :: ' is used to seperate the choice from the subchoice
            e.g. 'Phobia :: Pyrophobia'
        """
        if len(self.sub_choices):
            num = seed() % len(self.sub_choices)
            return '%(choice)s :: %(name)s' % {
                'choice': self.name,
                'name': self.sub_choices[num].generated_data(),
            }

        return self.name

    def details(self, include=None):
        """
        Returns a dict with the choice's details
            Note: For this to work the sub-class needs to have a trait property
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
        Is made to allow groupings with a depth of 2
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

    def generated_data(self):
        """
        Returns data that is shown if this was generated
        """
        return self.name
