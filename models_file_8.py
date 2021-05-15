# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class BackgroundTask(models.Model):
    task_name = models.CharField(max_length=190)
    task_params = models.TextField()
    task_hash = models.CharField(max_length=40)
    verbose_name = models.CharField(max_length=255, blank=True, null=True)
    priority = models.IntegerField()
    run_at = models.DateTimeField()
    repeat = models.BigIntegerField()
    repeat_until = models.DateTimeField(blank=True, null=True)
    queue = models.CharField(max_length=190, blank=True, null=True)
    attempts = models.IntegerField()
    failed_at = models.DateTimeField(blank=True, null=True)
    last_error = models.TextField()
    locked_by = models.CharField(max_length=64, blank=True, null=True)
    locked_at = models.DateTimeField(blank=True, null=True)
    creator_object_id = models.PositiveIntegerField(blank=True, null=True)
    creator_content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'background_task'


class BackgroundTaskCompletedtask(models.Model):
    task_name = models.CharField(max_length=190)
    task_params = models.TextField()
    task_hash = models.CharField(max_length=40)
    verbose_name = models.CharField(max_length=255, blank=True, null=True)
    priority = models.IntegerField()
    run_at = models.DateTimeField()
    repeat = models.BigIntegerField()
    repeat_until = models.DateTimeField(blank=True, null=True)
    queue = models.CharField(max_length=190, blank=True, null=True)
    attempts = models.IntegerField()
    failed_at = models.DateTimeField(blank=True, null=True)
    last_error = models.TextField()
    locked_by = models.CharField(max_length=64, blank=True, null=True)
    locked_at = models.DateTimeField(blank=True, null=True)
    creator_object_id = models.PositiveIntegerField(blank=True, null=True)
    creator_content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'background_task_completedtask'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
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


class ScConditions(models.Model):
    cond_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('ScUsers', models.DO_NOTHING)
    formula = models.CharField(max_length=250)
    cond_type = models.CharField(max_length=15, blank=True, null=True)
    max_val = models.CharField(max_length=250, blank=True, null=True)
    min_val = models.CharField(max_length=250, blank=True, null=True)
    limit_val = models.CharField(max_length=250, blank=True, null=True)
    comment = models.CharField(max_length=100, blank=True, null=True)
    display_method = models.CharField(max_length=10, blank=True, null=True)
    priority = models.IntegerField(blank=True, null=True)
    isalert = models.IntegerField(blank=True, null=True)
    alert_interval = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sc_conditions'


class ScConditionsResult(models.Model):
    cond_id = models.IntegerField(primary_key=True)
    val_result = models.FloatField(blank=True, null=True)
    bool_result = models.IntegerField(blank=True, null=True)
    val_formula = models.CharField(max_length=1500, blank=True, null=True)
    result_formula = models.CharField(max_length=1000, blank=True, null=True)
    time_calc = models.DateTimeField(blank=True, null=True)
    empty_values = models.CharField(max_length=1500, blank=True, null=True)
    text_formula = models.CharField(max_length=1500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sc_conditions_result'


class ScPaths(models.Model):
    path_id = models.AutoField(primary_key=True)
    path = models.CharField(max_length=100)
    interval_time = models.IntegerField()
    status = models.CharField(max_length=10)
    user = models.ForeignKey('ScUsers', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'sc_paths'


class ScUsers(models.Model):
    name = models.CharField(unique=True, max_length=150)
    status = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'sc_users'


class ScresultsTest(models.Model):
    var_title = models.CharField(primary_key=True, max_length=100)
    value = models.FloatField(blank=True, null=True)
    flag = models.IntegerField(blank=True, null=True)
    submission_date = models.DateTimeField(blank=True, null=True)
    comment = models.CharField(max_length=70, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'scresults_test'
