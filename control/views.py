from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import ScUsers, ScVariableAutoCompletion, ScPostfixAutoCompletion, ScPaths, ScResults, ScConditions, \
    ScConditionsResult, ScGraphName, ScGraphInfo, ScConditionsTags, ScConditionsOnline, ScAlertHistory, ScAlertSoundPlayer
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
from django.db.models import Q


# Create your views here.
@receiver(user_logged_in)
def got_online(sender, user, request, **kwargs):
    ScUsers.objects.filter(name=user).update(status='Online')


@receiver(user_logged_out)
def got_offline(sender, user, request, **kwargs):
    if request.user.groups.filter(name='Opers').exists():
        ScUsers.objects.filter(name=user).update(status='Offline')


def is_user_still_online(request):
    if request.method == 'GET' and request.is_ajax():
        user = request.user.username
        ScUsers.objects.filter(name=user).update(last_activity=datetime.strptime(request.GET.get("current_datetime"), '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc))
        data = {"Result": 'true'}
        return HttpResponse(json.dumps(data), content_type='application/json')


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
        "(([A-Za-z0-9_]+):((?:\\.|[A-Za-z0-9_.\%\-\/\ ])+):([A-Za-z0-9_]+)(?:\(([+-]?\d+)([a-z]+)(?:,([+-]?\d+)([a-z]+))\))?)",
        formula)
    vars_formula = list()
    for i in range(len(x)):
        vars_formula.append(x[i][0])
    return vars_formula


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


def load_alert_data(request) -> render:
    user = request.user.username
    # user_id = ScUsers.objects.get(name=user)
    # your_conditions = ScAlertHistory.objects.filter(creator=user, is_required_condition=0).order_by('-time_calc')
    # required_conditions = ScAlertHistory.objects.filter(is_required_condition=1).order_by('-time_calc')
    all_conditions = ScAlertHistory.objects.filter((Q(creator=user) & Q(is_required_condition=0)) | Q(is_required_condition=1)).order_by('-time_calc')
    return render(
        request,
        'alert.html',
        context={'conditions': all_conditions},
    )


def get_new_alert_sound(request):
    if request.method == 'GET' and request.is_ajax():
        user = request.user.username
        user_id = ScUsers.objects.get(name=user)
        new_alerts_to_play = ScAlertSoundPlayer.objects.filter(user_id=user_id).values()
        result = {'alerts': [], 'most_primary_alert': None}
        most_primary_alert_id = 0
        for element in new_alerts_to_play:
            alert = ScAlertHistory.objects.get(id=element['alert_id'])
        print(new_alerts_to_play)
        return HttpResponse(new_alerts_to_play, content_type='application/json')


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
    def insert_information_about_conditions(query_of_conditions, conditions_information_dict, is_required):
        for elem in query_of_conditions:
            try:
                condition_info_from_sc_results = ScConditionsResult.objects.get(cond_id=elem.cond_id)
                condition_tags = list(ScConditionsTags.objects.filter(cond_id=elem.cond_id))
                tags = [tag.tag for tag in condition_tags]
                cond_data = {"name": elem.comment, "val_result": condition_info_from_sc_results.val_result,
                             "bool_result": condition_info_from_sc_results.bool_result,
                             "display_method": elem.display_method,
                             "val_formula": condition_info_from_sc_results.val_formula,
                             "text_formula": condition_info_from_sc_results.text_formula,
                             "cond_type": elem.cond_type,
                             "value_result": condition_info_from_sc_results.val_result,
                             "result_formula": condition_info_from_sc_results.result_formula,
                             "empty_values": condition_info_from_sc_results.empty_values,
                             "time_calc": str(condition_info_from_sc_results.time_calc),
                             "creator_of_the_condition": str(elem.user),
                             "condition_tags": '; '.join(tags),
                             "alert_interval": elem.alert_interval,
                             "priority": elem.priority}
                conditions_information_dict[is_required].append(cond_data)
            except:
                print("Condition isn't ready")

    if request.method == 'GET' and request.is_ajax():
        user = request.user.username
        user_id = ScUsers.objects.get(name=user)
        conditions_information = {'required': [], 'unrequired': []}

        # Получаем необязательные условия пользователя
        unrequired_conditions_of_this_user = ScConditions.objects.filter(user_id=user_id, is_required_condition=False)
        insert_information_about_conditions(unrequired_conditions_of_this_user, conditions_information, 'unrequired')

        # Получаем обязательные условия
        required_conditions = ScConditions.objects.filter(is_required_condition=True)
        insert_information_about_conditions(required_conditions, conditions_information, 'required')

        conditions_information['required'].sort(key=lambda k: k['display_method'], reverse=True)
        conditions_information['unrequired'].sort(key=lambda k: k['display_method'], reverse=True)
        data = json.dumps(conditions_information)
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
        data = {"Result": 'true'}
        return HttpResponse(json.dumps(data), content_type='application/json')


def del_exist_condition(request):
    cond_name = request.GET.get('cond_name')
    user = request.user.username
    user_id_for_del = ScUsers.objects.get(name=user)
    cond_id = ScConditions.objects.get(user_id=user_id_for_del, comment=cond_name)
    ScConditionsResult.objects.filter(cond_id=cond_id.cond_id).delete()
    ScConditionsTags.objects.filter(cond_id=cond_id.cond_id).delete()
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


def search_info_for_autocomplete(request):
    if request.method == 'GET' and request.is_ajax():
        data = []
        print(request.GET.get('nameStartsWith'))
        limit = int(request.GET.get('maxRows'))
        # Фильтр либо в комментарии, либо в имени
        qs_var = ScVariableAutoCompletion.objects.filter(name__icontains=request.GET.get('nameStartsWith')).order_by(
            'name')[:limit]
        for name in qs_var:
            qs_postfix = ScPostfixAutoCompletion.objects.filter(postfix_id=name.postfix_id).order_by('name')
            for postfix in qs_postfix:
                data.append({'value': name.name + postfix.name, 'desc': name.comment + ' (' + postfix.comment + ').'})
        return JsonResponse(data, safe=False)


def change_condition_display_method(request):
    query = ScConditions.objects.get(user__name=request.POST.get('creator'), comment=request.POST.get('cond_name'))
    ScConditions.objects.filter(user__name=request.POST.get('creator'), comment=request.POST.get('cond_name')).update(display_method='Text+Siren') if query.display_method == 'Text' else ScConditions.objects.filter(user__name=request.POST.get('creator'), comment=request.POST.get('cond_name')).update(display_method='Text')
    a = {'result of change dot name': 'true'}
    return HttpResponse(json.dumps(a), content_type='application/json')


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
        scpaths_model = ScPaths()
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
    username = request.user.username
    user_id = ScUsers.objects.get(name=username)
    if request.method == 'POST':
        if '0)' in request.POST['formula']:
            request.POST = request.POST.copy()
            request.POST['formula'] = request.POST['formula'].replace('0)', '0sec)')
        form = ScConditionsForm(user_id, request.POST)
        if form.is_valid():
            formula = request.POST.get('formula')
            formula = formula.replace('0)', '0sec)')
            vars_formula = get_vars_formula(formula)
            print(vars_formula)
            tags_in_condition = re.findall(r'\w+', request.POST['tags'])
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
            instance.is_required_condition = request.POST['is_required_condition']
            instance.save()
            for tag in tags_in_condition:
                obj, created = ScConditionsTags.objects.update_or_create(
                    cond_id=instance.cond_id,
                    tag=tag,
                    defaults={}
                )
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
