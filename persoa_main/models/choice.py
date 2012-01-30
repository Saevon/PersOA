from django.db import models

from persoa_main.constants.database import MAX_CHAR_LENGTH
from persoa_main.models.abstract import AbstractPersOAModel

class AbstractChoice(AbstractPersOAModel):
    """
    A basic choice for a Trait
    """

    class Meta(AbstractPersOAModel.Meta):
        abstract = True

    name = models.CharField(
    	max_length=MAX_CHAR_LENGTH,
        blank=False)
    desc = models.TextField(blank=True)
    defn = models.CharField(
    	max_length=MAX_CHAR_LENGTH,
        blank=True)

    def details(self, *args, **kwargs):
        """
        Returns a dict with the choice's details
        """
        details = {
            'name': self.name,
            'desc': self.desc,
            'defn': self.defn,
        }
        return details

class BasicChoice(AbstractChoice):
    """
    A standard Choice
    """

class ScaleChoice(AbstractChoice):
    """
    A choice that is set on a scale
    """

    side = models.SmallIntegerField(blank=False, null=False)

    def details(self, *args, **kwargs):
        details = super(ScaleChoice, self).details()
        details.update({
            'pos': self.side
        })
        return details
