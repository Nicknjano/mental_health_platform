from django.urls import path
from . import views

urlpatterns = [
    path('recommendations/', views.resource_recommendations, name='resource_recommendations'),
]
