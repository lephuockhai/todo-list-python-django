from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.log_in, name='login'),
    path('logout/', views.log_out, name='logout'),
    path('home/', views.home, name='home'),
    path('changepassword/', views.change_password, name='changepassword'),
    path('profile/', views.profile, name='profile'),
    path('change-profile/', views.change_profile, name='change-profile'),
    path('createtask/', views.createtask, name= 'createtask'),
    path('createlist', views.createlist, name='createlist'),
    path('creategroup', views.creategroup, name='creategroup'),
    path('update-task-status/<int:task_id>/', views.update_task_status, name='update-task-status'),
    path('delete-task/<int:task_id>/', views.delete_task, name='delete-task'),
    path('assigns-to-list/', views.assigns_to_list, name='assigns-to-list'),
    path('delete-list/<int:list_id>/', views.delete_list, name='delete-list'),
    path('delete-group/<int:group_id>/', views.delete_group, name='delete-group'),
    path('assign_user_to_task', views.assigns_to_task, name='assign_user_to_task'),
]