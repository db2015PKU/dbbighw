# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models


class Cinema(models.Model):
    cinema_name = models.CharField(primary_key=True, max_length=40)
    district = models.CharField(max_length=20)
    road = models.CharField(max_length=20)
    busstation = models.CharField(db_column='busStation', max_length=20)  # Field name made lowercase.
    phone = models.CharField(max_length=50)
    businesshours = models.TimeField(db_column='businessHours')  # Field name made lowercase.
    estimate = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    movie_name = models.CharField(max_length=40, blank=True, null=True)
    room = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cinema'
