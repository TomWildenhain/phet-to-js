from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('simulations/<str:sim_name>', views.simulation, name='simulations'),
]