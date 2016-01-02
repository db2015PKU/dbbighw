from __future__ import unicode_literals

from django.db import models

class Cinema(models.Model):
    cinema_id = models.TextField(primary_key=True)  # This field type is a guess.
    cinema_name = models.CharField(max_length=40)
    district = models.CharField(max_length=20)
    road = models.CharField(max_length=20)
    busstation = models.CharField(db_column='busStation', max_length=20)  # Field name made lowercase.
    phone = models.CharField(max_length=50)
    businesshoursbegin = models.TimeField(db_column='businessHoursBegin')  # Field name made lowercase.
    businesshoursend = models.TimeField(db_column='businessHoursEnd')  # Field name made lowercase.
    estimate = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'cinema'
    def __unicode__(self):  # __str__ on Python 3
        return self.cinema_name