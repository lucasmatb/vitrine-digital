from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .customResetPassword import PasswordResetView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    #rotas de autenticação
    
    path('auth/cadastro/', views.cadastro, name='cadastro'),
    path('auth/login/', views.login, name='login'),
    path('auth/valida-cadastro/', views.valida_cadastro, name='valida_cadastro'),
    path('auth/valida-login/', views.valida_login, name='valida_login'),
    path('auth/logout/', auth_views.LogoutView.as_view(), name='logout'),

    #rotas de recuperação de senha

    path('auth/password_reset/', PasswordResetView.as_view(template_name='recuperar-senha/recuperar-senha.html'), name="password_reset"),
    path('auth/password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='recuperar-senha/email-enviado.html'), name="password_reset_done"),
    path('auth/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='recuperar-senha/registrar-senha.html'), name='password_reset_confirm'),
    path('auth/reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='recuperar-senha/confirmacao-senha.html'), name='password_reset_complete'),

    #rotas de usuários

    path('empresas-favoritas-usuario/', login_required(views.retorna_empresas_favoritas_usuario), name='empresas_favoritas_usuario'),
    path('produtos-salvos-usuario/', login_required(views.retorna_produtos_salvos_usuario), name='produtos_salvos_usuario'),
    path('pesquisar-empresas-usuario/', login_required(views.retorna_pesquisar_empresas_usuario), name='pesquisar_empresas_usuario'),
    path('meus-dados-usuario/', login_required(views.retorna_meus_dados_usuario), name='meus_dados_usuario'),
    path('pedido-lojista/', login_required(views.cria_pedido_lojista_por_usuario), name='pedido_lojista')
]