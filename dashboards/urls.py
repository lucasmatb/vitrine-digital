from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('area-cliente/', login_required(views.indexLogadoAreaCliente), name='home-area-cliente')
]