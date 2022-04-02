from django.urls import path
from . import views

PREFIX = ''

urlpatterns = [
    path(PREFIX + '', views.index, name='home'),
    path(PREFIX + 'alert/', views.load_alert_data, name='alert'),
    path(PREFIX + 'custom_settings/', views.custom_settings, name='custom_settings'),
    path(PREFIX + 'graph_editor/', views.graph_editor, name='graph_editor'),
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
    path(PREFIX + 'is_SAM_working/', views.is_SAM_working, name='is_SAM_working'),
    path(PREFIX + 'is_user_still_online/', views.is_user_still_online, name='is_user_still_online'),
    path(PREFIX + 'rename_dot_name/', views.rename_dot_name, name='rename_dot_name'),
    path(PREFIX + 'change_dot_condition/', views.change_dot_condition, name='change_dot_condition'),
    path(PREFIX + 'save_new_graph_name/', views.save_new_graph_name, name='save_new_graph_name'),
    path(PREFIX + 'update_info_in_graphs/', views.update_info_in_graphs, name='update_info_in_graphs'),
    path(PREFIX + 'search_info_for_autocomplite/', views.search_info_for_autocomplete, name='search_info_for_autocomplete'),
    path(PREFIX + 'change_condition_display_method/', views.change_condition_display_method, name='change_condition_display_method'),
    path(PREFIX + 'get_new_alert_sound/', views.get_new_alert_sound, name='get_new_alert_sound'),

]

