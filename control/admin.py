from django.contrib import admin
from .models import ScUsers, ScPaths, ScResults, ScConditions, ScConditionsResult, ScGraphName, ScGraphInfo


class ScConditionsResultAdmin(admin.ModelAdmin):
    list_display = ('cond_id', 'val_result', 'bool_result', 'val_formula', 'text_formula', 'result_formula',
                    'time_calc', 'empty_values')
    list_filter = ('cond_id', 'val_result')


class ScConditionsAdmin(admin.ModelAdmin):
    list_display = ('user', 'formula', 'max_val', 'min_val', 'limit_val', 'comment', 'display_method', 'priority',
                    'isalert', 'alert_interval', 'time_create_or_alert')
    list_filter = ('user', 'formula')


class ScGraphInfoAdmin(admin.ModelAdmin):
    list_display = ('dot_name', 'dot_condition', 'dot_id_in_graph', 'graph')
    list_filter = ('dot_name', 'dot_condition')


class ScGraphNameAdmin(admin.ModelAdmin):
    list_display = 'graph_name'
    list_filter = 'graph_name'


class ScPathsAdmin(admin.ModelAdmin):
    list_display = ('path', 'interval_time', 'status', 'user')
    list_filter = ('path', 'interval_time')


class ScResultsAdmin(admin.ModelAdmin):
    list_display = ('var_title', 'value', 'flag', 'submission_date', 'comment')
    list_filter = ('var_title', 'value')


class ScUsersAdmin(admin.ModelAdmin):
    list_display = ('name', 'status')
    list_filter = ('name', 'status')


admin.site.register(ScUsers, ScUsersAdmin)
admin.site.register(ScPaths, ScPathsAdmin)
admin.site.register(ScResults, ScResultsAdmin)
admin.site.register(ScConditionsResult, ScConditionsResultAdmin)
admin.site.register(ScConditions, ScConditionsAdmin)
admin.site.register(ScGraphInfo, ScGraphInfoAdmin)
admin.site.register(ScGraphName, ScGraphNameAdmin)

# Register your models here.
