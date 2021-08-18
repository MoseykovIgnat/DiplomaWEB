from django.urls import path
from . import views

PREFIX = ''

urlpatterns = [
    path(PREFIX + '', views.index, name='home'),
    path(PREFIX + 'custom_settings/', views.custom_settings, name='custom_settings'),
    path(PREFIX + 'create_post/', views.create_post, name='create_post'),
    path(PREFIX + 'post/new', views.post_new, name='post_new'),
    path(PREFIX + 'add_new_variable/', views.add_new_variable, name='add_new_variable'),
    path(PREFIX + 'display/variables', views.update_info_about_variables, name='update_info_about_variables'),
    path(PREFIX + 'display/conditions', views.update_info_about_conditions, name='update_info_about_conditions'),
    path(PREFIX + 'display/leds', views.update_leds, name='update_leds'),
    path(PREFIX + 'get/all/conditions', views.get_conditions, name='get_conditions'),
    path(PREFIX + 'del_exist_variable/', views.del_exist_variable, name='del_exist_variable'),
    path(PREFIX + 'condition_create', views.condition_create, name='condition_create'),
    path(PREFIX + 'del_exist_condition/', views.del_exist_condition, name='del_exist_condition'),
]

