from django.urls import path
from . import views

urlpatterns = [
    path('checkin/', views.daily_checkin, name='daily_checkin'),
]

urlpatterns += [
    path('dashboard/', views.analytics_dashboard, name='analytics_dashboard'),
]
