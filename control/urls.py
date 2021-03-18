from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('custom_settings/', views.custom_settings, name='custom_settings'),
    path('create_post/', views.create_post, name='create_post'),
    path('post/new', views.post_new, name='post_new'),
    path('add_new_variable/', views.add_new_variable, name='add_new_variable'),
    path('display/data', views.display_data, name='display_data')
]