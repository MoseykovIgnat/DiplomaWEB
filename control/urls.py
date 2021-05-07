from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('custom_settings/', views.custom_settings, name='custom_settings'),
    path('create_post/', views.create_post, name='create_post'),
    path('post/new', views.post_new, name='post_new'),
    path('add_new_variable/', views.add_new_variable, name='add_new_variable'),
    path('display/variables', views.update_info_about_variables, name='update_info_about_variables'),
    path('display/conditions', views.update_info_about_conditions, name='update_info_about_conditions'),
    path('display/leds', views.update_leds, name='update_leds'),
    path('get/all/conditions', views.update_leds, name='get_conditions'),
    path('del_exist_variable/', views.del_exist_variable, name='del_exist_variable'),
    path('condition_create', views.condition_create, name='condition_create'),
    path('del_exist_condition/', views.del_exist_condition, name='del_exist_condition'),
]
