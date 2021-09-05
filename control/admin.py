from django.contrib import admin
from .models import ScUsers, ScPaths, ScResults, ScConditions, ScConditionsResult, ScGraphName, ScGraphInfo

admin.site.register(ScPaths)
admin.site.register(ScUsers)
admin.site.register(ScConditions)
admin.site.register(ScConditionsResult)


class ScResultsAdmin(admin.ModelAdmin):
    list_display = ('var_title', 'value', 'flag', 'submission_date', 'comment')
    list_filter = ('value', 'submission_date')


admin.site.register(ScResults, ScResultsAdmin, ScGraphName, ScGraphInfo)
# Register your models here.
