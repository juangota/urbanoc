########################### import django ###########################
from django.db import models


class ModelsCommons(models.Model):
    """
    Translation abstract model
    <2018-09-28 JAF> creation
    """
    creation_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
