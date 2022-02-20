from django.contrib import admin
from .models import ScUsers, ScPaths, ScResults, ScConditions, ScConditionsResult, ScGraphName, ScGraphInfo,\
    ScVariableAutoCompletion, ScPostfixAutoCompletion, ScAlertHistory


class ScConditionsResultAdmin(admin.ModelAdmin):
    list_display = ('cond_id', 'val_result', 'bool_result', 'val_formula', 'text_formula', 'result_formula',
                    'time_calc', 'empty_values')
    list_filter = ('cond_id', 'val_result')


class ScAlertHistoryAdmin(admin.ModelAdmin):
    list_display = ('comment', 'creator', 'time_calc', 'is_required_condition', 'text_formula', 'val_formula',
                    'bool_result', 'val_result')
    list_filter = ('cond_id', 'val_result')


class ScConditionsAdmin(admin.ModelAdmin):
    list_display = ('user','cond_id', 'formula', 'cond_type', 'max_val', 'min_val', 'limit_val', 'comment', 'display_method', 'priority',
                    'isalert', 'alert_interval', 'time_create_or_alert', 'is_required_condition')
    list_filter = ('user', 'formula')


class ScGraphInfoAdmin(admin.ModelAdmin):
    list_display = ('dot_name', 'dot_condition', 'dot_id_in_graph', 'graph')
    list_filter = ('dot_name', 'dot_condition')


class ScPathsAdmin(admin.ModelAdmin):
    list_display = ('path', 'interval_time', 'status', 'user')
    list_filter = ('path', 'interval_time')


class ScResultsAdmin(admin.ModelAdmin):
    list_display = ('var_title', 'value', 'flag', 'submission_date', 'comment')
    list_filter = ('var_title', 'value')


class ScUsersAdmin(admin.ModelAdmin):
    list_display = ('name', 'status')
    list_filter = ('name', 'status')


class ScVariableAutoCompletionAdmin(admin.ModelAdmin):
    list_display = ('name', 'comment', 'postfix_id')
    list_filter = ('name', 'comment', 'postfix_id')


class ScPostfixAutoCompletionAdmin(admin.ModelAdmin):
    list_display = ('name', 'comment', 'postfix_id')
    list_filter = ('name', 'comment', 'postfix_id')


admin.site.register(ScUsers, ScUsersAdmin)
admin.site.register(ScAlertHistory, ScAlertHistoryAdmin)
admin.site.register(ScPaths, ScPathsAdmin)
admin.site.register(ScResults, ScResultsAdmin)
admin.site.register(ScConditionsResult, ScConditionsResultAdmin)
admin.site.register(ScConditions, ScConditionsAdmin)
admin.site.register(ScGraphInfo, ScGraphInfoAdmin)
admin.site.register(ScPostfixAutoCompletion, ScPostfixAutoCompletionAdmin)
admin.site.register(ScVariableAutoCompletion, ScVariableAutoCompletionAdmin)
admin.site.register(ScGraphName)

# Register your models here.
