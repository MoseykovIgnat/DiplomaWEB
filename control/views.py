from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import ScUsers, ScPaths, ScresultsTest, ScConditions
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.http import JsonResponse
from django.dispatch import receiver
from .forms import ScUsersForm, ScConditionsForm
from django.core.serializers import serialize
from django.contrib.auth import update_session_auth_hash
from django.views import generic
from django.http import HttpResponse
from . import models
from . import forms
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404, redirect, render
import re


# Create your views here.
@receiver(user_logged_in)
def got_online(sender, user, request, **kwargs):
    ScUsers.objects.filter(name=user).update(status='Online')


@receiver(user_logged_out)
def got_offline(sender, user, request, **kwargs):
    ScUsers.objects.filter(name=user).update(status='Offline')


def formula_without_priority_staples(x):
    if x[0] == '(':
        x = x[1:]
    x = x.replace('-(', '-').replace('+(', '+').replace('*(', '*').replace('/(', '/').replace('**(', '**').replace('))',
                                                                                                                   ')').replace(
        'sec))', 'sec)').replace('min))', 'min)').replace('h))', 'h)').replace('d))', 'd)').replace('m))',
                                                                                                    'm)').replace('y))',
                                                                                                                  'y)')
    x = "".join(re.split(r'([:][a-z]+)[)]', x))
    return x


def get_vars_formula(formula):
    x = re.findall(
        "(([A-Za-z0-9_]+):((?:\\.|[A-Za-z0-9_.\-\/])+):([A-Za-z0-9_]+)(?:\(([+-]?\d+)([a-z]+)(?:,([+-]?\d+)([a-z]+))\))?)",
        formula)
    vars_formula = list()
    # print(x)
    for i in range(len(x)):
        vars_formula.append(x[i][0])
    # print(vars_formula)
    return vars_formula


def index(request):
    global bool_result
    if not request.user.is_authenticated:
        return render(request, 'index_not_login.html')
    else:
        info = ScresultsTest.objects.all()

        '''Время волшебства'''
        user = request.user.username
        user_id = ScUsers.objects.get(name=user)
        data = ScConditions.objects.filter(user_id=user_id)
        condition_result = list()
        for condition in data:
            formula = condition.formula
            vars_formula = get_vars_formula(formula)
            empty_values = list()
            for var_formula in vars_formula:
                formula = formula.replace(str(var_formula),
                                          str(ScresultsTest.objects.filter(var_title=var_formula)[0].value))
                if str(ScresultsTest.objects.filter(var_title=var_formula)[0].comment) == 'Empty':
                    empty_values.append(str(ScresultsTest.objects.filter(var_title=var_formula)[0].var_title))
            digit_formula = formula
            if empty_values:
                cond_data = {"name": condition.comment, "result": '0', "display_method": condition.display_method,
                             "val_formula": formula, "text_formula": condition.formula,
                             "cond_type": condition.cond_type, 'empty_values': empty_values}
                condition_result.append(cond_data)
            else:
                result = eval(digit_formula)
                if condition.cond_type == '1':
                    cond_data = {"name": condition.comment, "result": result, "display_method": condition.display_method,
                                 "val_formula": formula, "text_formula": condition.formula,
                                 "cond_type": condition.cond_type}
                    condition_result.append(cond_data)
                if condition.cond_type == '6':
                    if not condition.max_val.isdigit():
                        formula = condition.max_val
                        vars_max_val = get_vars_formula(formula)
                        for var_max_val in vars_max_val:
                            formula = formula.replace(str(var_max_val),
                                                      str(ScresultsTest.objects.filter(var_title=var_max_val)[0].value))
                        digit_max_val = formula
                        max_val = eval(formula)
                    else:
                        max_val = float(condition.max_val)
                        digit_max_val = max_val
                    if not condition.min_val.isdigit():
                        formula = condition.min_val
                        vars_min_val = get_vars_formula(formula)
                        for var_min_val in vars_min_val:
                            formula = formula.replace(str(var_min_val),
                                                      str(ScresultsTest.objects.filter(var_title=var_min_val)[0].value))
                        digit_min_val = formula
                        min_val = eval(formula)
                    else:
                        min_val = float(condition.min_val)
                        digit_min_val = min_val
                    val_formula = digit_formula + ' in ' + '[' + str(digit_min_val) + ' ; ' + str(
                        digit_max_val) + '] ?'
                    text_formula = condition.formula + ' in ' + '[' + str(condition.min_val) + ' ; ' + str(
                        condition.max_val) + '] ?'
                    result_formula = str(eval(str(digit_formula))) + ' in ' + '[' + str(
                        eval(str(digit_min_val))) + ' ; ' + str(eval(str(digit_max_val))) + '] ?'
                    bool_result = bool(max_val >= result >= min_val)
                    cond_data = {"name": condition.comment, "result": bool_result,
                                 "display_method": condition.display_method,
                                 "val_formula": val_formula, "text_formula": text_formula,
                                 "cond_type": condition.cond_type,
                                 "value_result": result, "result_formula": result_formula}
                    condition_result.append(cond_data)
                if condition.cond_type == '2' or condition.cond_type == '3' or condition.cond_type == '4' or condition.cond_type == '5':
                    if not condition.limit_val.isdigit():
                        formula = condition.limit_val
                        vars_limit_val = get_vars_formula(formula)
                        for var_limit_val in vars_limit_val:
                            formula = formula.replace(str(var_limit_val),
                                                      str(ScresultsTest.objects.filter(var_title=var_limit_val)[0].value))
                        digit_limit_val = formula
                        limit_val = eval(formula)
                    else:
                        limit_val = float(condition.limit_val)
                        digit_limit_val = limit_val
                    if condition.cond_type == '2':
                        val_formula = digit_formula + '<' + str(digit_limit_val)
                        text_formula = condition.formula + '<' + condition.limit_val
                        result_formula = str(eval(str(digit_formula))) + '<' + str(eval(str(digit_limit_val)))
                        bool_result = bool(result < limit_val)
                    if condition.cond_type == '3':
                        val_formula = digit_formula + '>' + str(digit_limit_val)
                        text_formula = condition.formula + '>' + condition.limit_val
                        result_formula = str(eval(str(digit_formula))) + '>' + str(eval(str(digit_limit_val)))
                        bool_result = bool(result > limit_val)
                    if condition.cond_type == '4':
                        val_formula = digit_formula + '>=' + str(digit_limit_val)
                        text_formula = condition.formula + '>=' + condition.limit_val
                        result_formula = str(eval(str(digit_formula))) + '>=' + str(eval(str(digit_limit_val)))
                        bool_result = bool(result >= limit_val)
                    if condition.cond_type == '5':
                        val_formula = digit_formula + '<=' + str(digit_limit_val)
                        text_formula = condition.formula + '<=' + condition.limit_val
                        result_formula = str(eval(str(digit_formula))) + '<=' + str(eval(str(digit_limit_val)))
                        bool_result = bool(result <= limit_val)
                    cond_data = {"name": condition.comment, "result": bool_result,
                                 "display_method": condition.display_method,
                                 "val_formula": val_formula, "text_formula": text_formula,
                                 "cond_type": condition.cond_type,
                                 "value_result": result, "result_formula": result_formula}
                    condition_result.append(cond_data)
                if condition.display_method == 'Text+Siren':
                    if not bool_result:
                        print("!!!!!!СИРЕНА!!!!!!!")

        return render(
            request,
            'index.html',
            context={'info': info, 'condition_result': condition_result},
        )


def del_exist_condition(request):
    cond_name = request.GET.get('cond_name')
    user = request.user.username
    user_id_for_del = ScUsers.objects.get(name=user)
    data = ScConditions.objects.filter(user_id=user_id_for_del)
    conditions = ScConditions.objects.filter(user_id=user_id_for_del, comment=cond_name)
    for condition in conditions:
        vars_formula = get_vars_formula(condition.formula)
        for var_formula in vars_formula:
            counter = 0
            for formula_check in data:
                if var_formula in formula_check.formula:
                    counter += 1
            if counter == 1:
                ScPaths.objects.filter(path=var_formula).delete()
        ScConditions.objects.filter(user_id=user_id_for_del, comment=cond_name).delete()
        data = serialize("json", ScConditions.objects.filter(user_id=user_id_for_del.id))
    return HttpResponse(data, content_type='application/json')



def display_data(request):
    if request.method == 'GET' and request.is_ajax():
        response_data = {}
        current_user = request.user.username
        data = serialize("json", ScresultsTest.objects.all())
        return HttpResponse(data, content_type='application/json')


def add_new_variable(request):
    if request.method == "POST":
        scpaths_model = models.ScPaths()
        user = request.user.username
        user_id = ScUsers.objects.get(name=user)
        scpaths_model.user_id = user_id.id
        scpaths_model.path = request.POST.get('var_path')
        scpaths_model.interval_time = 5
        scpaths_model.source = request.POST.get('source')
        scpaths_model.status = request.POST.get('status')
        scpaths_model.save()
        data = serialize("json", ScPaths.objects.filter(user_id=user_id.id))
        return HttpResponse(data, content_type='application/json')


def del_exist_variable(request):
    var_path = request.GET.get('var_path')
    user = request.user.username
    user_id_for_del = ScUsers.objects.get(name=user)
    ScPaths.objects.filter(path=var_path, user_id=user_id_for_del.id).delete()
    data = serialize("json", ScPaths.objects.filter(user_id=user_id_for_del.id))
    return HttpResponse(data, content_type='application/json')


def custom_settings(request):
    user = request.user.username
    user_id = ScUsers.objects.get(name=user)
    your_variables = ScPaths.objects.filter(user_id=user_id.id)
    your_conditions = ScConditions.objects.filter(user_id=user_id.id)
    return render(
        request,
        'custom_settings.html',
        context={'your_variables': your_variables, 'your_conditions': your_conditions},
    )


def condition_create(request):
    user = request.user
    username = request.user.username
    user_id = ScUsers.objects.get(name=username)
    if request.method == 'POST':
        if '0)' in request.POST['formula']:
            request.POST = request.POST.copy()
            request.POST['formula'] = request.POST['formula'].replace('0)', '0sec)')
        # print(request.POST)
        form = ScConditionsForm(user_id, request.POST)
        if form.is_valid():
            formula = request.POST.get('formula')
            formula = formula.replace('0)', '0sec)')
            vars_formula = get_vars_formula(formula)
            for new_var in vars_formula:
                if not ScPaths.objects.filter(path=new_var):
                    scpaths_model = models.ScPaths()
                    scpaths_model.user_id = user_id.id
                    scpaths_model.path = new_var
                    scpaths_model.interval_time = 5
                    scpaths_model.status = 'Online'
                    scpaths_model.save()
            instance = form.save(commit=False)
            instance.user_id = user_id.id
            instance.save()
            return redirect('custom_settings')
    else:
        form = ScConditionsForm(user_id)
    return render(request,
                  'custom_setting_condition_form.html',
                  context={'form': form}
                  )


def create_post(request):
    response_data = {}
    if request.POST.get('action') == 'post':
        path = request.POST.get('path')
        interval_time = request.POST.get('interval_time')
        user = request.user.username
        response_data['path'] = path
        response_data['interval_time'] = interval_time
        return JsonResponse(response_data)


def post_new(request):
    form = ScUsersForm()
    return JsonResponse(form)
