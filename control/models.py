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


class ScPathsOnline(models.Model):
    path_id = models.AutoField(primary_key=True)
    path = models.CharField(max_length=100)
    interval_time = models.IntegerField()
    status = models.CharField(max_length=10)
    user = models.ForeignKey('ScUsers', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'sc_paths_online'

    def __str__(self):
        return "%s" % self.path


class ScUsers(models.Model):
    name = models.CharField(unique=True, max_length=150)
    status = models.CharField(max_length=10)
    last_activity = models.DateTimeField(blank=True, null=True)

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
    priority = models.IntegerField(blank=True, null=True)
    isalert = models.IntegerField(blank=True, null=True)
    alert_interval = models.IntegerField(blank=True, null=True)
    time_create_or_alert = models.DateTimeField(blank=True, null=True)
    is_required_condition = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sc_conditions'


class ScResults(models.Model):
    var_title = models.CharField(primary_key=True, max_length=100)
    value = models.FloatField(blank=True, null=True)
    flag = models.IntegerField(blank=True, null=True)
    submission_date = models.DateTimeField(blank=True, null=True)
    comment = models.CharField(max_length=70, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'scresults_test'


class ScConditionsResult(models.Model):
    cond_id = models.IntegerField(primary_key=True)
    val_result = models.FloatField(blank=True, null=True)
    bool_result = models.IntegerField(blank=True, null=True)
    val_formula = models.CharField(max_length=1500, blank=True, null=True)
    text_formula = models.CharField(max_length=1500, blank=True, null=True)
    result_formula = models.CharField(max_length=1000, blank=True, null=True)
    time_calc = models.DateTimeField(blank=True, null=True)
    empty_values = models.CharField(max_length=1500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sc_conditions_result'


class ScConditionsOnline(models.Model):
    cond_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('ScUsers', models.DO_NOTHING)
    formula = models.CharField(max_length=250)
    cond_type = models.CharField(max_length=15, blank=True, null=True)
    max_val = models.CharField(max_length=250)
    min_val = models.CharField(max_length=250)
    limit_val = models.CharField(max_length=250)
    comment = models.CharField(max_length=100, blank=True, null=True)
    display_method = models.CharField(max_length=10, blank=True, null=False)
    priority = models.IntegerField(blank=True, null=True)
    isalert = models.IntegerField(blank=True, null=True)
    alert_interval = models.IntegerField(blank=True, null=True)
    time_create_or_alert = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sc_conditions_onlweb'


class ScGraphInfo(models.Model):
    dot_id = models.AutoField(primary_key=True)
    dot_name = models.CharField(max_length=100)
    dot_condition = models.CharField(max_length=100, blank=True, null=True)
    dot_id_in_graph = models.IntegerField()
    graph = models.ForeignKey('ScGraphName', models.DO_NOTHING)



    class Meta:
        managed = False
        db_table = 'sc_graph_info'


class ScGraphName(models.Model):
    graph_id = models.AutoField(primary_key=True)
    graph_name = models.CharField(max_length=100)

    def natural_key(self):
        return self.graph_name

    class Meta:
        managed = False
        db_table = 'sc_graph_name'


class ScVariableAutoCompletion(models.Model):
    name = models.CharField(primary_key=True, max_length=100)
    comment = models.CharField(max_length=200, blank=True, null=True)
    postfix_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sc_variable_auto_completion'


class ScPostfixAutoCompletion(models.Model):
    name = models.CharField(max_length=100)
    postfix_id = models.IntegerField()
    comment = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sc_postfix_auto_completion'


class ScConditionsTags(models.Model):
    cond = models.ForeignKey(ScConditions, models.DO_NOTHING)
    tag = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sc_conditions_tags'


class ScAlertHistory(models.Model):
    comment = models.CharField(max_length=200, blank=True, null=True)
    creator = models.CharField(max_length=150, blank=True, null=True)
    time_calc = models.DateTimeField(blank=True, null=True)
    is_required_condition = models.IntegerField(blank=True, null=True)
    text_formula = models.CharField(max_length=1500, blank=True, null=True)
    val_formula = models.CharField(max_length=1500, blank=True, null=True)
    bool_result = models.IntegerField(blank=True, null=True)
    val_result = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sc_alert_history'
