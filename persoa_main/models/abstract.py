from django.db import models

class AbstractPersOAModel(models.Model):
    """
    A model made for the PersOA app
    """

    class Meta:
        abstract = True
        app_label = 'app'
