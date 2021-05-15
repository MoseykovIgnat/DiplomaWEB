from django import forms
from .models import ScUsers, ScPaths, ScresultsTest, ScConditions
from django.core.exceptions import ValidationError

type_cond_choices = (
    (1, "Result of formula"),
    (2, "<"),
    (3, ">"),
    (4, ">="),
    (5, "<="),
    (6, "Result in interval"),
)
display_method_choices = (
    ('Text', "Text"),
    # ('Image', "Image"),
    # ('Siren', "Siren"),
    ('Text+Siren', "Text+Siren"),
)


class ScConditionsForm(forms.ModelForm):
    def __init__(self, form_user_id, *args, **kwargs):
        super(ScConditionsForm, self).__init__(*args, **kwargs)

    comment = forms.CharField(label='Name of your condition')
    cond_type = forms.TypedChoiceField(choices=type_cond_choices, coerce=str, label='Conditional type')
    min_val = forms.CharField(required=False, label='Minimum value',
                              widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}))
    max_val = forms.CharField(required=False, label='Maximum value',
                              widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}))
    limit_val = forms.CharField(required=False, label='Limit value',
                                widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}))
    display_method = forms.TypedChoiceField(choices=display_method_choices, label='Display method', coerce=str)
    formula = forms.CharField(label='Formula', widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}))
    priority = forms.IntegerField(required=False, min_value=0, max_value=10,
                                  label='Condition priority for signal alert')
    alert_interval = forms.IntegerField(required=False, min_value=30, max_value=600,
                                        label='Interval for condition signal alert')

    class Meta:
        model = ScConditions
        fields = ['comment', 'formula', 'cond_type', 'min_val', 'max_val', 'limit_val', 'display_method', 'priority',
                  'alert_interval']


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
