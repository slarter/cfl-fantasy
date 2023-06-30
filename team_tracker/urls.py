from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='tracker-home'),
    path('standings/', views.standings, name='tracker-standings')
]