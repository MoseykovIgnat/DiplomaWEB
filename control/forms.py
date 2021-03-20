from django import forms
from .models import ScUsers, ScPaths, ScresultsTest, ScConditions
from django.core.exceptions import ValidationError

GEEKS_CHOICES = (
    (1, "Result of formula"),
    (2, "<"),
    (3, ">"),
    (4, ">="),
    (5, "<="),
    (6, "Result in interval"),
)


class ScConditionsForm(forms.ModelForm):
    def __init__(self, form_user_id, *args, **kwargs):
        super(ScConditionsForm, self).__init__(*args, **kwargs)
        self.fields['v1'] = forms.ModelChoiceField(queryset=ScPaths.objects.filter(user_id=form_user_id))
        self.fields['v2'] = forms.ModelChoiceField(required=False, queryset=ScPaths.objects.filter(user_id=form_user_id))
        self.fields['v3'] = forms.ModelChoiceField(required=False, queryset=ScPaths.objects.filter(user_id=form_user_id))
        self.fields['v4'] = forms.ModelChoiceField(required=False, disabled=False, queryset=ScPaths.objects.filter(user_id=form_user_id))
        self.fields['v5'] = forms.ModelChoiceField(required=False, queryset=ScPaths.objects.filter(user_id=form_user_id))
        self.fields['cond_type'] = forms.TypedChoiceField(choices=GEEKS_CHOICES, initial='Your formula (Example (v1+v2)/v3)', coerce=str)
        self.fields['min_val'] = forms.FloatField(disabled=True, required=False)
        self.fields['max_val'] = forms.FloatField(disabled=True, required=False)
        self.fields['limit_val'] = forms.FloatField(disabled=True, required=False)

    # def save(self, user_name, *args, **kwargs):
    #     super(ScConditionsForm, self).save(*args, **kwargs)
    #     ScConditions.user = user_name

    class Meta:
        model = ScConditions
        fields = ['comment', 'v1', 'v2', 'v3', 'v4', 'v5', 'formula', 'cond_type', 'max_val', 'min_val', 'limit_val']


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
