"""jerias_math_db URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from jerias_production import views

urlpatterns = [
    path('add-person/', views.add_person, name='add_person'),
    path('groups/', views.group_list, name='group_list'),
    path('people/', views.person_list, name='person_list'),
    path('app_users/', views.app_user_list, name='app_user_list'),
    path('group_people/', views.group_person_list, name='group_person_list'),
    path('create-group-person/', views.create_group_person,
         name='create_group_person'),
    path('group-event/search/', views.search_group_events,
         name='search_group_events'),
    path('group-event/add/', views.add_group_event, name='add_group_event'),
    path('group/upsert/', views.upsert_group, name='upsert_group'),
    path('create-student-attendance/', views.create_student_attendance,
         name='create_student_attendance'),
    path('get-student-attendance-by-group-event/', views.get_student_attendance_by_group_event,
         name='get_student_attendance_by_group_event'),

    path('search-student-attendance-by-student/', views.search_student_attendance_by_student,
         name='search_student_attendance_by_student'),

    path('admin/', admin.site.urls),
]
