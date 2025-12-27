from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('equipment/', views.equipment_list, name='equipment_list'),
    path('equipment/new/', views.equipment_create, name='equipment_create'),
    path('equipment/<int:pk>/', views.equipment_detail, name='equipment_detail'),
    path('requests/', views.request_list, name='request_list'),
    path('requests/new/', views.request_create, name='request_create'),
    path('requests/<int:pk>/edit/', views.request_update, name='request_update'),
    path('api/requests/<int:pk>/stage/', views.update_request_stage, name='update_request_stage'),
    path('api/equipment/<int:pk>/', views.get_equipment_details, name='get_equipment_details'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('api/events/', views.request_events, name='request_events'),
]
