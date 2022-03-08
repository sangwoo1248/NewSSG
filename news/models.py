# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from pymysql import NULL

class N_Category(models.Model):
    c_id = models.AutoField(primary_key=True)
    c_name = models.CharField(unique=True, max_length=5)

    class Meta:
        managed = False
        db_table = 'N_category'


class N_CategoryDetail(models.Model):
    cd_id = models.AutoField(primary_key=True)
    c = models.ForeignKey(N_Category, models.DO_NOTHING)
    cd_name = models.CharField(unique=True, max_length=10)

    class Meta:
        managed = False
        db_table = 'N_category_detail'


class News(models.Model):
    n_id = models.AutoField(primary_key=True)
    p = models.ForeignKey('Press', models.DO_NOTHING, blank=True, null=True)
    cd = models.ForeignKey(N_CategoryDetail, models.DO_NOTHING, blank=True, null=True)
    n_title = models.CharField(max_length=1024)
    nd_img = models.CharField(max_length=1024, blank=True, null=True)
    n_input = models.DateTimeField(blank=True, null=True)
    o_link = models.CharField(unique=True, max_length=768, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'News'


class N_content(models.Model):
    nc_id = models.AutoField(primary_key=True)
    n = models.ForeignKey('News', models.DO_NOTHING, blank=True, null=True)
    n_content = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'N_content'

class N_summarization(models.Model):
    ns_id = models.AutoField(primary_key=True)
    n = models.ForeignKey('News', models.DO_NOTHING, blank=True, null=True)
    ns_content = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'N_summarization'


class Press(models.Model):
    p_id = models.AutoField(primary_key=True)
    p_name = models.CharField(unique=True, max_length=10)

    class Meta:
        managed = False
        db_table = 'Press'

class N_Viewcount(models.Model):
    v_id = models.AutoField(primary_key=True)
    hits = models.PositiveIntegerField(default=0)
    n = models.ForeignKey('News', models.DO_NOTHING, blank=True, null=True)
    id  = models.ForeignKey('Memberinfo', models.DO_NOTHING, blank=True, null=True, db_column='id')

# 2022-02-07 park-jong-won  add ScrollData,Log
class ScrollData(models.Model):
    ipaddr = models.CharField(max_length=15)
    acstime = models.DateTimeField(auto_now = True)
    url = models.CharField(db_column='URL', max_length=45)  # Field name made lowercase.
    staytime = models.IntegerField()
    scroll = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'Scroll_Data'

class Log(models.Model):
    user = models.ForeignKey('Memberinfo', models.DO_NOTHING, blank=True, null=True)
    ipaddr = models.CharField(db_column='IPaddr', max_length=15, db_collation='utf8_general_ci', blank=True, null=True)  # Field name made lowercase.
    acstime = models.DateTimeField(blank=True, null=True, auto_now = True)
    url = models.CharField(db_column='URL', max_length=45, blank=True, null=True)  # Field name made lowercase.
    user = models.ForeignKey('Memberinfo', models.DO_NOTHING, blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'Log'

class Memberinfo(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    password = models.CharField(max_length=30)
    name = models.CharField(max_length=10)
    birth = models.DateTimeField(blank=True, null=True)
    sex = models.CharField(max_length=5)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)

    class Meta:
        managed = False
        db_table = 'memberinfo'