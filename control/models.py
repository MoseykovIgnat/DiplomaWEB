from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class ScPaths(models.Model):
    path_id = models.AutoField(primary_key=True)
    path = models.CharField(max_length=100)
    interval_time = models.IntegerField()
    status = models.CharField(max_length=10)
    user = models.ForeignKey('ScUsers', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'sc_paths'

    def __str__(self):
        return "%s" % self.path


class ScUsers(models.Model):
    name = models.CharField(unique=True, max_length=150)
    status = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'sc_users'

    def __str__(self):
        return self.name


class ScConditions(models.Model):
    cond_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('ScUsers', models.DO_NOTHING)
    formula = models.CharField(max_length=250)
    cond_type = models.CharField(max_length=15, blank=True, null=True)
    max_val = models.CharField(max_length=250)
    min_val = models.CharField(max_length=250)
    limit_val = models.CharField(max_length=250)
    comment = models.CharField(max_length=100, blank=True, null=True)
    display_method = models.CharField(max_length=10, blank=True, null=False)

    class Meta:
        managed = False
        db_table = 'sc_conditions'


class ScresultsTest(models.Model):
    var_title = models.CharField(primary_key=True, max_length=100)
    value = models.FloatField(blank=True, null=True)
    flag = models.IntegerField(blank=True, null=True)
    submission_date = models.DateTimeField(blank=True, null=True)
    comment = models.CharField(max_length=70, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'scresults_test'