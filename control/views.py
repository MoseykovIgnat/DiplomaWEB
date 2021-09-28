from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import ScUsers, ScPaths, ScResults, ScConditions, ScConditionsResult, ScGraphName, ScGraphInfo, ScConditionsOnline
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.http import JsonResponse
from django.dispatch import receiver
from .forms import ScUsersForm, ScConditionsForm
from django.core.serializers import serialize
from django.core.serializers.json import Serializer
from django.contrib.auth import update_session_auth_hash
from django.views import generic
from django.http import HttpResponse
from . import models
from . import forms
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404, redirect, render
from background_task import background
from django.core.serializers.json import DjangoJSONEncoder
import re
import json
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth import models
from .utils import *
import time


# Create your views here.
@receiver(user_logged_in)
def got_online(sender, user, request, **kwargs):
    ScUsers.objects.filter(name=user).update(status='Online')


@receiver(user_logged_out)
def got_offline(sender, user, request, **kwargs):
    if request.user.groups.filter(name='Opers').exists():
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
    for i in range(len(x)):
        vars_formula.append(x[i][0])
    return vars_formula


def update_condition_results():
    ids_for_signal_alarm = list()
    global bool_result
    '''Время волшебства'''
    data = ScConditionsOnline.objects.all()
    for condition in data:
        formula = condition.formula
        vars_formula = get_vars_formula(formula)
        empty_values = list()
        for var_formula in vars_formula:
            formula = formula.replace(str(var_formula),
                                      str(ScResults.objects.filter(var_title=var_formula)[0].value))
            if str(ScResults.objects.filter(var_title=var_formula)[0].comment) == 'Empty':
                empty_values.append(str(ScResults.objects.filter(var_title=var_formula)[0].var_title))
        digit_formula = formula
        if empty_values:
            result_for_db = ScConditionsResult(cond_id=condition.cond_id, val_formula=formula,
                                               empty_values=str(empty_values), text_formula=condition.formula,
                                               time_calc=(datetime.now(tz=timezone.utc)))
            result_for_db.save()
        else:
            result = eval(digit_formula)
            if condition.cond_type == '7':
                if condition.cond_type == '7':
                    result_for_db = ScConditionsResult(cond_id=condition.cond_id, val_formula=formula,
                                                       bool_result=bool(result), text_formula=condition.formula,
                                                       time_calc=(datetime.now(tz=timezone.utc)))
                    result_for_db.save()
            if condition.cond_type == '1':
                result_for_db = ScConditionsResult(cond_id=condition.cond_id, val_formula=formula,
                                                   val_result=result,
                                                   text_formula=condition.formula,
                                                   time_calc=(datetime.now(tz=timezone.utc)))
                result_for_db.save()
            if condition.cond_type == '6':
                if not condition.max_val.isdigit():
                    formula = condition.max_val
                    vars_max_val = get_vars_formula(formula)
                    for var_max_val in vars_max_val:
                        formula = formula.replace(str(var_max_val),
                                                  str(ScResults.objects.filter(var_title=var_max_val)[
                                                          0].value))
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
                                                  str(ScResults.objects.filter(var_title=var_min_val)[
                                                          0].value))
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
                if not bool_result:
                    ids_for_signal_alarm.append(condition.cond_id)
                result_for_db = ScConditionsResult(cond_id=condition.cond_id, val_formula=val_formula,
                                                   bool_result=bool_result, text_formula=text_formula,
                                                   val_result=result, result_formula=result_formula,
                                                   time_calc=(datetime.now(tz=timezone.utc)))
                result_for_db.save()
            if condition.cond_type == '2' or condition.cond_type == '3' or condition.cond_type == '4' or condition.cond_type == '5':
                if not condition.limit_val.isdigit():
                    formula = condition.limit_val
                    vars_limit_val = get_vars_formula(formula)
                    for var_limit_val in vars_limit_val:
                        formula = formula.replace(str(var_limit_val),
                                                  str(ScResults.objects.filter(var_title=var_limit_val)[
                                                          0].value))
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
                    if not bool_result:
                        ids_for_signal_alarm.append(condition.cond_id)
                if condition.cond_type == '3':
                    val_formula = digit_formula + '>' + str(digit_limit_val)
                    text_formula = condition.formula + '>' + condition.limit_val
                    result_formula = str(eval(str(digit_formula))) + '>' + str(eval(str(digit_limit_val)))
                    bool_result = bool(result > limit_val)
                    if not bool_result:
                        ids_for_signal_alarm.append(condition.cond_id)
                if condition.cond_type == '4':
                    val_formula = digit_formula + '>=' + str(digit_limit_val)
                    text_formula = condition.formula + '>=' + condition.limit_val
                    result_formula = str(eval(str(digit_formula))) + '>=' + str(eval(str(digit_limit_val)))
                    bool_result = bool(result >= limit_val)
                    if not bool_result:
                        ids_for_signal_alarm.append(condition.cond_id)
                if condition.cond_type == '5':
                    val_formula = digit_formula + '<=' + str(digit_limit_val)
                    text_formula = condition.formula + '<=' + condition.limit_val
                    result_formula = str(eval(str(digit_formula))) + '<=' + str(eval(str(digit_limit_val)))
                    bool_result = bool(result <= limit_val)
                    if not bool_result:
                        ids_for_signal_alarm.append(condition.cond_id)
                    if not bool_result:
                        ids_for_signal_alarm.append(condition.cond_id)
                result_for_db = ScConditionsResult(cond_id=condition.cond_id, val_formula=val_formula,
                                                   bool_result=bool_result, text_formula=text_formula,
                                                   val_result=result, result_formula=result_formula,
                                                   time_calc=(datetime.now(tz=timezone.utc)))
                result_for_db.save()
    return ids_for_signal_alarm


def index(request):
    if not request.user.is_authenticated:
        return render(request, 'index_not_login.html')
    else:
        info = ScResults.objects.all()
        return render(
            request,
            'index.html',
            context={'info': info},
        )


def get_conditions(request):
    if request.method == 'GET' and request.is_ajax():
        result = list()
        data = ScConditions.objects.all()
        for i in data:
            condition_result = ScConditionsResult.objects.get(cond_id=i.cond_id)
            if condition_result.bool_result == 0 or condition_result.bool_result == 1:
                result.append(i.comment)
        result = json.dumps(result)
        return HttpResponse(result, content_type='application/json')


def update_leds(request):
    if request.method == 'GET' and request.is_ajax():
        result_conditions = list()
        conditions = ScConditionsResult.objects.all()
        for condition in conditions:
            if condition.bool_result == 0 or condition.bool_result == 1:
                cond_name = ScConditions.objects.get(cond_id=condition.cond_id)
                result_condition = {'cond_name': cond_name.comment, 'bool_result': condition.bool_result}
                result_conditions.append(result_condition)
        result_conditions = json.dumps(result_conditions)
        return HttpResponse(result_conditions, content_type='application/json')


def update_info_about_conditions(request):
    # condition = ScConditions.objects.get(cond_id=140)
    # condition_result = ScConditionsResult.objects.get(cond_id=140)
    # print((condition.time_create_or_alert + timedelta(hours=7)))
    if request.method == 'GET' and request.is_ajax():
        user = request.user.username
        user_id = ScUsers.objects.get(name=user)
        list_of_users = [user_id.id]
        group = models.Group.objects.get(name='Expert')
        query_users = group.user_set.all()
        for g in query_users:
            user_id_from_group = ScUsers.objects.get(name=g)
            list_of_users.append(user_id_from_group.id)
        condition_result = list()
        a = ScConditions.objects.filter(user_id__in=list_of_users)
        # group = models.Group.objects.get(name='Opers')
        # usersz = group.user_set.all()
        # print(usersz)
        for i in a:
            try:
                b = ScConditionsResult.objects.get(cond_id=i.cond_id)
                cond_data = {"name": i.comment, "val_result": b.val_result, "bool_result": b.bool_result,
                             "display_method": i.display_method,
                             "val_formula": b.val_formula, "text_formula": b.text_formula,
                             "cond_type": i.cond_type,
                             "value_result": b.val_result, "result_formula": b.result_formula,
                             "empty_values": b.empty_values, "time_calc": str(b.time_calc)}
                condition_result.append(cond_data)
            except:
                print("Condition isn't ready")
        data = json.dumps(condition_result)
        return HttpResponse(data, content_type='application/json')


# def update_info_about_variables(request):
#     if request.method == 'GET' and request.is_ajax():
#         data =[]
#         if is_expert(request.user):
#             data = serialize("json", ScResults.objects.all())
#             print('User is expert')
#         elif is_oper(request.user):
#             user = request.user.username
#             user_id = ScUsers.objects.get(name=user)
#             list_of_users = [user_id.id]
#             group = models.Group.objects.get(name='Expert')
#             query_users = group.user_set.all()
#             for g in query_users:
#                 user_id_from_group = ScUsers.objects.get(name=g)
#                 list_of_users.append(user_id_from_group.id)
#             print(list_of_users)
#             data = serialize("json", ScResults.objects.filter(user_id__in=list_of_users))
#         return HttpResponse(data, content_type='application/json')

def update_info_about_variables(request):
    if request.method == 'GET' and request.is_ajax():
        data = serialize("json", ScResults.objects.all())
        return HttpResponse(data, content_type='application/json')


def update_info_in_graphs(request):
    if request.method == 'GET' and request.is_ajax():
        queryset = ScGraphInfo.objects.values('dot_name', 'dot_condition', 'dot_id_in_graph', 'graph__graph_name')
        data = json.dumps(list(queryset), cls=DjangoJSONEncoder)
        return HttpResponse(data, content_type='application/json')


def is_SAM_working(request):
    if request.method == 'GET' and request.is_ajax():
        a = update_condition_results()
        data = {"Result": 'true'}
        return HttpResponse(json.dumps(data), content_type='application/json')


def del_exist_condition(request):
    cond_name = request.GET.get('cond_name')
    user = request.user.username
    user_id_for_del = ScUsers.objects.get(name=user)
    cond_id = ScConditions.objects.get(user_id=user_id_for_del, comment=cond_name)
    ScConditionsResult.objects.filter(cond_id=cond_id.cond_id).delete()
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


def save_new_graph_name(request):
    if request.method == "POST":
        print('ok i save new graph name')
        scgraphname_model = ScGraphName()
        scgraphname_model.graph_name = request.POST.get('new_graph_name')
        scgraphname_model.save()
        a = {'result': 'true'}
        print(request.POST.get('new_graph_name'))
        return HttpResponse(json.dumps(a), content_type='application/json')


def rename_dot_name(request):
    # ЗАКИДЫВАЕМ НОВОЕ ИМЯ ВМЕСТО СТАРОГО
    if request.method == "POST":
        obj, created = ScGraphInfo.objects.update_or_create(
            dot_id_in_graph=request.POST.get('dot_id_in_graph'),
            graph=ScGraphName.objects.get(graph_name=request.POST.get('dot_graph_name')),
            defaults={'dot_name': request.POST.get('new_name')}
        )
        a = {'result of change dot name': 'true'}
        return HttpResponse(json.dumps(a), content_type='application/json')


def change_dot_condition(request):
    if request.method == "POST":
        obj, created = ScGraphInfo.objects.update_or_create(
            dot_id_in_graph=request.POST.get('dot_id_in_graph'),
            graph=ScGraphName.objects.get(graph_name=request.POST.get('dot_graph_name')),
            defaults={'dot_condition': request.POST.get('new_dot_condition')}
        )
        a = {'result of change condition': 'true'}
        return HttpResponse(json.dumps(a), content_type='application/json')


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


def graph_editor(request):
    return render(request,
                  'graph_editor.html')


def condition_create(request):
    user = request.user
    username = request.user.username
    user_id = ScUsers.objects.get(name=username)
    if request.method == 'POST':
        print(request)
        if '0)' in request.POST['formula']:
            request.POST = request.POST.copy()
            request.POST['formula'] = request.POST['formula'].replace('0)', '0sec)')
        form = ScConditionsForm(user_id, request.POST)
        print(form)
        if form.is_valid():
            formula = request.POST.get('formula')
            formula = formula.replace('0)', '0sec)')
            vars_formula = get_vars_formula(formula)
            for new_var in vars_formula:
                obj, created = ScPaths.objects.update_or_create(
                    user_id=user_id.id,
                    path=new_var, interval_time=5, status='Online',
                    defaults={}
                )
            instance = form.save(commit=False)
            instance.user_id = user_id.id
            instance.isalert = 0
            instance.time_create_or_alert = datetime.now(tz=timezone.utc)
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
