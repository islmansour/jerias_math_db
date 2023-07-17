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
from jerias_production.views.general_view import get_lookup_table_data
from jerias_production.views.payments_view import get_purchase_payments
from jerias_production.views.person_view import add_person, app_user_list, person_list
from jerias_production.views.group_view import group_list, upsert_group, group_person_list, create_group_person
from jerias_production.views.event_view import search_group_events, add_group_event
from jerias_production.views.attendance_view import create_student_attendance, get_student_attendance_by_group_event, search_student_attendance_by_student
from jerias_production.views.purchases_view import create_update_purchase, purchases_by_student

urlpatterns = [
    # Existing URL patterns
    path('add-person/', add_person, name='add_person'),
    path('groups/', group_list, name='group_list'),
    path('people/', person_list, name='person_list'),
    path('app_users/', app_user_list, name='app_user_list'),
    path('group_people/', group_person_list, name='group_person_list'),
    path('create-group-person/', create_group_person, name='create_group_person'),
    path('group-event/search/', search_group_events, name='search_group_events'),
    path('group-event/add/', add_group_event, name='add_group_event'),
    path('group/upsert/', upsert_group, name='upsert_group'),
    path('create-student-attendance/', create_student_attendance,
         name='create_student_attendance'),
    path('get-student-attendance-by-group-event/', get_student_attendance_by_group_event,
         name='get_student_attendance_by_group_event'),
    path('search-student-attendance-by-student/', search_student_attendance_by_student,
         name='search_student_attendance_by_student'),
    path('purchases/search/', purchases_by_student, name='purchases_by_student'),
    path('purchase/<int:purchase_id>/payments/',
         get_purchase_payments, name='purchase_payments'),
    path('lookup-table-data/', get_lookup_table_data,
         name='lookup_table_data'),
    path('purchase/upsert/', create_update_purchase,
         name='create_update_purchase'),
    path('admin/', admin.site.urls),
    # Other URL patterns
]
