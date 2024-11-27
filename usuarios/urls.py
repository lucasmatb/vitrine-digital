from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .customResetPassword import PasswordResetView

urlpatterns = [
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.login, name='login'),
    path('valida_cadastro/', views.valida_cadastro, name='valida_cadastro'),
    path('valida_login/', views.valida_login, name='valida_login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    #exemplo de substituição apenas da view
    #    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name="password_reset"),
    path('password_reset/', PasswordResetView.as_view(), name="password_reset"),
]