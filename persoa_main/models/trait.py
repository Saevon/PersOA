from django.db import models

from persoa_main.constants.database import MAX_CHAR_LENGTH
from persoa_main.models.abstract import AbstractPersOAModel

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
    	max_length=MAX_CHAR_LENGTH,
        blank=True)

    def __unicode__(self):
        return unicode(self.name)

    def generate(self, *args, **kwargs):
        """
        Returns a choice from this trait
        """
        return NotImplemented

    def details(self, include=None):
        """
        Returns a dict with the trait's details
        """
        details = self.data()
        if include is not None:
            if 'choices' in include:
                include.remove('choices')
                details.update({
                    'choices': [choice.details(include=include) for choice in self.choices],
                })
            if 'groups' in include:
                details.update({
                    'groups': [group.data() for group in self.groups],
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

class BasicTrait(AbstractTrait):
    """
    A trait which has a list of choices, and is chosen X times
    """

    default_num = models.PositiveSmallIntegerField(blank=False, null=False)

    def data(self):
        details = super(BasicTrait, self).data()
        details.update({
            'type': 'basic',
            'default_num': self.def_num
        })
        return details

class LinearTrait(AbstractTrait):
    """
    A trait with its choices on a scale
    """

    neg_name = models.CharField(
    	max_length=MAX_CHAR_LENGTH,
        blank=False)
    pos_name = models.CharField(
    	max_length=MAX_CHAR_LENGTH,
        blank=False)

    def data(self):
        details = super(LinearTrait, self).data()
        details.update({
            'type': 'scale',
            'neg': self.neg_name,
            'pos': self.pos_name,
        })
        return details
