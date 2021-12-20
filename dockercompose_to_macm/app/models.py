from django.db import models
from django.contrib.postgres.fields import ArrayField


# Create your models here.


class MACM(models.Model):
    appId = models.IntegerField(null=True)
    application = models.CharField(max_length=100)
    #i seguenti saranno liste di liste:
    components = models.CharField(max_length=100)
    primaries = models.CharField(max_length=100)
    secondaries = models.CharField(max_length=100)
    asset_types = models.CharField(max_length=100)
    dev_types = models.CharField(max_length=100)
    custom_types = models.CharField(max_length=100)

class Asset_Type(models.Model):
    asset_type = models.CharField(max_length=100)


