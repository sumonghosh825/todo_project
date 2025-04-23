from django.urls import path
from .views import (
    register, user_login, user_logout, home, 
    task_management, add_task, edit_task, delete_task, 
    profile, update_profile, load_security_content, update_security, 
    load_tasks_by_category,load_tasks_by_status, load_profile_content
)

urlpatterns = [
    # **Authentication Routes**
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),

    # **Profile Routes**
    path('profile/', profile, name='profile'),
    path('load_profile_content/', load_profile_content, name='load_profile_content'),
    path('update_profile/', update_profile, name='update_profile'),

    # **Security Routes**
    path('load_security_content/', load_security_content, name='load_security_content'),
    path('update_security/', update_security, name='update_security'),

    # **Task Management**
    path('tasks/', task_management, name='task_management'),
    path('tasks/add/', add_task, name='add_task'),
    path('tasks/edit/<int:task_id>/', edit_task, name='edit_task'),
    path('tasks/delete/<int:task_id>/', delete_task, name='delete_task'),

    # **Category-Based Task Loading**
    path('tasks/load/<str:category>/', load_tasks_by_category, name='load_tasks_by_category'),
    path('tasks/status/<str:status>/', load_tasks_by_status, name='load_tasks_by_status'),
]
