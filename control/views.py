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
from django.shortcuts import get_object_or_404, redirect, render


# Create your views here.
@receiver(user_logged_in)
def got_online(sender, user, request, **kwargs):
    ScUsers.objects.filter(name=user).update(status='Online')


@receiver(user_logged_out)
def got_offline(sender, user, request, **kwargs):
    ScUsers.objects.filter(name=user).update(status='Offline')


def index(request):
    if not request.user.is_authenticated:
        return render(request, 'index_not_login.html')
    else:
        info = ScresultsTest.objects.all()
        return render(
            request,
            'index.html',
            context={'info': info},
        )


def display_data(request):
    if request.method == 'GET' and request.is_ajax():
        response_data = {}
        current_user = request.user.username
        data = serialize("json", ScresultsTest.objects.all())
        print(current_user)
        print(serialize("json", ScresultsTest.objects.all()))
        return HttpResponse(data, content_type='application/json')


def add_new_variable(request):
    if request.method == "POST":
        scpaths_model = models.ScPaths()
        user = request.user.username
        user_id = ScUsers.objects.get(name=user)
        scpaths_model.user_id = user_id.id
        scpaths_model.path = request.POST.get('var_path')
        scpaths_model.interval_time = request.POST.get('interval_time')
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
        form = ScConditionsForm(user_id, request.POST)
        if form.is_valid():
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
        print(response_data)
        return JsonResponse(response_data)
    return print('dsfg')





def post_new(request):
    form = ScUsersForm()
    return JsonResponse(form)





