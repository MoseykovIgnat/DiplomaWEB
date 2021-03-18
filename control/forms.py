from django import forms
from .models import ScUsers, ScPaths, ScresultsTest
from django.core.exceptions import ValidationError


class ScUsersForm(forms.ModelForm):

    class Meta:
        model = ScUsers
        fields = ('name', 'status')


# class ScPathsForm(forms.ModelForm):
#     path = forms.CharField(label='path', max_length=40)
#     source = forms.CharField(label='source', max_length=10)
#     interval_time = forms.IntegerField(label='interval_time')
#     class Meta:
#         model = ScPaths
#         fields = ('path', 'source', 'interval_time')

# class PostCondition(forms.ModelForm):
#     new_date = forms.DateField(help_text='Inter data', required=True)
#
#     def clean_new_date(self):
#         data = self.cleaned_data['new_date']
#         if data:
#             print(data)
#         else:
#             raise ValidationError(_('Invalid date - renewal in past'))
#     class Meta:
#         model = ScresultsTest  # Какая одель будет использоваться для создания формы
#         fields = ('name1', 'name2') # Какие поля должны присутствовать в форме


