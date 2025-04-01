from django.urls import path
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('painel-usuario/', login_required(views.retorna_dashboard_usuario), name='dashboard_usuario'),
    path(
        'painel-lojista/<int:id_empresa>/',
        permission_required('empresas.view_empresa')(views.retorna_dashboard_lojista),
        name='dashboard_lojista'
    )
]