from django.contrib import admin
from .models import ScUsers, ScPaths, ScresultsTest
admin.site.register(ScPaths)
admin.site.register(ScUsers)

class ScresultsTestAdmin(admin.ModelAdmin):
    list_display = ('var_title', 'value', 'flag', 'submission_date', 'comment')
    list_filter = ('value', 'submission_date')

admin.site.register(ScresultsTest, ScresultsTestAdmin)
# Register your models here.
