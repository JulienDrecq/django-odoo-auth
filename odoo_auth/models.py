from django.db import models
from django.contrib.auth.models import User


class OdooUser(models.Model):
    user = models.OneToOneField(User)
    odoo_id = models.BigIntegerField(primary_key=True)
    username = models.CharField(max_length=256)
