from django.db import models

from app.constants.database import MAX_CHAR_LENGTH, MAX_DEFN_LENGTH
from app.models.abstract import AbstractPersOAModel
from utils.decorators import seeded

class AbstractTrait(AbstractPersOAModel):
    """
    Part of a person's personality
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

    def details(self, include=None):
        """
        Returns a dict with the trait's details
        """
        details = self.data()
        if include is None:
            return details
        elif include['trait_name']:
            return self.name
        include['trait'] = False

        if include['choice']:
            details.update({
                'choices': [choice.details(include) for choice in self.choices.all()],
            })
        if include['group']:
            details.update({
                'groups': [group.details(include) for group in self.groups.all()],
            })
        return details

    def data(self):
        """
        Returns a dict with the basic details
        """
        return {
            'type': None,
            'name': self.name,
            'desc': self.desc,
            'defn': self.defn,
        }

    @seeded(2)
    def generate(self, num=None, seed=None):
        """
        Returns num choices from this trait using the given seed
        """
        return NotImplemented

class BasicTrait(AbstractTrait):
    """
    A trait which has a list of choices, and is chosen X times
    """

    default_num = models.PositiveSmallIntegerField(blank=False, null=False)

    def data(self):
        """
        Returns a dict with the basic details
        """
        details = super(BasicTrait, self).data()
        details.update({
            'type': 'basic',
            'default_num': self.default_num
        })
        return details

    @seeded(2)
    def generate(self, num=None, seed=None):
        """
        Returns num choices from this trait using the given seed
        """
        if num is None:
            num = self.default_num

        length = len(self.choices.all())

        choices = []
        for i in range(num):
            num = seed() % length
            choice = self.choices.all()[num]

            choices.append(choice.generate(seed))

        return choices
        

class LinearTrait(AbstractTrait):
    """
    A trait with its choices on a scale with only +1/-1 choices
    """

    neg_name = models.CharField(
        max_length=MAX_CHAR_LENGTH,
        blank=False)
    pos_name = models.CharField(
        max_length=MAX_CHAR_LENGTH,
        blank=False)

    def data(self):
        """
        Returns a dict with the basic details
        """
        details = super(LinearTrait, self).data()
        details.update({
            'type': 'scale',
            'neg': self.neg_name,
            'pos': self.pos_name,
        })
        return details

    @seeded(2)
    def generate(self, num=None, seed=None):
        """
        Returns num choices from this trait using the given seed
        """
        if num is None:
            num = 1

        length = len(self.choices.all())

        choices = []
        for i in range(num):
            num = seed() % length
            choice = self.choices.all()[num]

            choices.append(choice.generate(seed))

        return choices
