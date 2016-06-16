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
    def generate(self, seed=None):
        return self

    def details(self, include=None):
        """
        Returns a dict with the choice's details
            Note: For this to work the sub-class needs to have a trait property
        """
        details = self.data()
        if include is None:
            return details
        elif include['choice_name']:
            return self.name
        include['choice'] = False

        if include['trait']:
            details['trait'] = self.trait.details(include)
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
        on_delete=models.CASCADE,
        related_name='choices',
        blank=False,
        null=False)

    @seeded(1)
    def generate(self, seed=None):
        """
        Returns a choice or a sub_choice
        """
        if len(self.sub_choices.all()):
            num = seed() % len(self.sub_choices.all())
            return self.sub_choices.all()[num]
        return self

    def details(self, include=None):
        details = super(BasicChoice, self).details(include)

        if include is None:
            return details
        elif include['choice_desc']:
            details['sub'] = [i.details(include) for i in self.sub_choices.all()]
        return details

class LinearChoice(AbstractChoice):
    """
    A choice that is set on a scale
    """

    side = models.SmallIntegerField(blank=False, null=False)
    trait = models.ForeignKey(
        'LinearTrait',
        on_delete=models.CASCADE,
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
        on_delete=models.CASCADE,
        related_name='sub_choices',
        blank=False,
        null=False)

    def details(self, include=None):
        """
        Returns data that is shown if this was generated
        """
        details = self.data()
        if include is None:
            pass
        elif include['choice_name']:
            return '%(choice)s :: %(name)s' % {
                'choice': self.choice.name,
                'name': self.name,
            }
        return details

    def data(self):
        """
        Returns a dict with the basic details
        """
        return {
            'name': '%(choice)s :: %(name)s' % {
                'choice': self.choice.name,
                'name': self.name,
            },
            'defn': self.defn,
        }
