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


class AuthGroup(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    group = models.ForeignKey(AuthGroup)
    permission = models.ForeignKey('AuthPermission')

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group_id', 'permission_id'),)


class AuthPermission(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    content_type = models.ForeignKey('DjangoContentType')
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type_id', 'codename'),)


class AuthUser(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    username = models.CharField(unique=True, max_length=30)

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser)
    group = models.ForeignKey(AuthGroup)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user_id', 'group_id'),)


class AuthUserUserPermissions(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser)
    permission = models.ForeignKey(AuthPermission)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user_id', 'permission_id'),)


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


class DjangoAdminLog(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', blank=True, null=True)
    user = models.ForeignKey(AuthUser)
    action_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Movie(models.Model):
    movie_id = models.TextField(primary_key=True)  # This field type is a guess.
    movie_name = models.CharField(max_length=40)
    show_date = models.DateField()
    show_time = models.TimeField()
    runtime = models.TextField()  # This field type is a guess.
    director = models.CharField(max_length=40)
    actors = models.CharField(max_length=40)
    movie_type = models.CharField(max_length=40, blank=True, null=True)
    movie_language = models.CharField(max_length=20, blank=True, null=True)
    price = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'movie'


class Movieshow(models.Model):
    cinema_id = models.TextField(primary_key=True)  # This field type is a guess.
    movie_id = models.TextField(primary_key=True)  # This field type is a guess.
    show_date = models.DateField(primary_key=True)
    show_time = models.TimeField(primary_key=True)
    room_no = models.TextField(primary_key=True)  # This field type is a guess.
    price = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'movieShow'
        unique_together = (('cinema_id', 'movie_id', 'show_date', 'show_time', 'room_no'),)


class Room(models.Model):
    room_no = models.TextField(primary_key=True)  # This field type is a guess.
    seatx_max = models.TextField()  # This field type is a guess.
    seaty_max = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'room'


class RoomOfCinema(models.Model):
    cinema_id = models.TextField(primary_key=True)  # This field type is a guess.
    room_no = models.TextField(primary_key=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'room_of_cinema'
        unique_together = (('cinema_id', 'room_no'),)


class Selltickets(models.Model):
    ticket_id = models.IntegerField(primary_key=True, blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    cinema_id = models.TextField()  # This field type is a guess.
    movie_id = models.TextField()  # This field type is a guess.
    show_date = models.DateField()
    show_time = models.TimeField()
    room_no = models.TextField()  # This field type is a guess.
    seatx = models.TextField()  # This field type is a guess.
    seaty = models.TextField()  # This field type is a guess.
    price = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'sellTickets'
        unique_together = (('seatx', 'seaty', 'show_date', 'show_time', 'room_no'),)


class Useraccount(models.Model):
    user_id = models.IntegerField(primary_key=True, blank=True, null=True)
    user_email = models.CharField(max_length=40)
    user_name = models.CharField(max_length=40)
    user_password = models.CharField(max_length=30)
    user_phone = models.CharField(max_length=20)
    user_permissions = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'userAccount'
