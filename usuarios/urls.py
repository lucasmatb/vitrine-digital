from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .customResetPassword import PasswordResetView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('auth/cadastro/', views.cadastro, name='cadastro'),
    path('auth/login/', views.login, name='login'),
    path('auth/valida-cadastro/', views.valida_cadastro, name='valida_cadastro'),
    path('auth/valida-login/', views.valida_login, name='valida_login'),
    path('auth/logout/', auth_views.LogoutView.as_view(), name='logout'),
    #exemplo de substituição apenas da view
    #    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name="password_reset"),
    path('auth/password_reset/', PasswordResetView.as_view(), name="password_reset"),
    #login_required(views.indexLogadoAreaCliente)
    path('dashboard-usuario/', login_required(views.retorna_dashboard_usuario), name='dashboard_usuario'),
    path('lojas-favoritas-usuario/', login_required(views.retorna_lojas_favoritas_usuario), name='lojas_favoritas_usuario'),
    path('meus-dados-usuario/', login_required(views.retorna_meus_dados_usuario), name='meus_dados_usuario'),
    path('produtos-salvos-usuario/', login_required(views.retorna_produtos_salvos_usuario), name='produtos_salvos_usuario'),

    path('minhas-empresas-lojista/', views.retorna_minhas_lojas_lojista, name='minhas_empresas_lojista'),
]