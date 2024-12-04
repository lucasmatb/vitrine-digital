from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('painel-usuario/', login_required(views.retorna_dashboard_usuario), name='dashboard_usuario'),
    path('painel-lojista/', login_required(views.retorna_dashboard_usuario), name='dashboard_lojista'),
]