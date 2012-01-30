import json

from persoa_main.constants.database import MAX_CHAR_LENGHT
from persoa_main.models.abstract import AbstractPersOAModel

class AbstractTrait(AbstractPersOAModel):
    """
    Part of a person's personality
    """

    class Meta(AbstractPersOAModel.Meta):
        abstract = True

    name = models.CharField(
    	max_length=MAX_CHAR_LENGTH,
        blank=False)
    desc = models.TextField(blank=True)
    defn = models.CharField(
    	max_length=Max_CHAR_LENGTH,
        blank=True)

    def generate(self, *args, **kwargs):
        """
        Returns a choice from this trait
        """
        return NotImplemented

    def details(self, *args, **kwargs):
        """
        Returns a dict with the trait's details
        """
        details = {
            'type': NotImplemented,
            'name': self.name,
            'desc': self.desc,
            'defn': self.defn,
        }
        includes = kwargs.get('includes', None)
        if includes != None and 'choices' in includes:
            choices = [choice.details()]
            details.update({'choices': choices})
        return details

class BasicTrait(AbstractTrait):
    """
    A trait which has a list of choices
    """

class LinearTrait(AbstractTrait):
    """
    A trait with its choices on a scale
    """

    neg_name = models.CharField(
    	max_length=MAX_CHAR_LENGHT,
        blank=False)
    pos_name = models.CharField(
    	max_length=MAX_CHAR_LENGHT,
        blank=False)

    def details(self, *args, **kwargs):
        details = super(LinearTrait, self).details(*args, **kwargs)
        details.update({
            'type': 'scale',
            'neg': self.neg_name,
            'pos': self.pos_name,
        })
        return details

class MultiTrait(AbstractTrait):
    """
    A trait which can be selected multiple times
    """

    def_num = models.PositiveSmallIntegerField(blank=False, null=False)

    def details(self, *args, **kwargs):
        details = super(LinearTrait, self).details()
        details.update({
            'type': 'multi_choice',
            'default_num': self.def_num
        })
        return details
