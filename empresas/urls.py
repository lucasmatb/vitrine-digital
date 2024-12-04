from django.urls import path
from . import views

urlpatterns = [
    path('cadastro-empresa/', views.retorna_cadastro_empresa, name='cadastro_empresa'),
    path('valida-cadastro-empresa/', views.valida_cadastro_empresa, name='valida_cadastro_empresa'),
    path('visualizar-empresa/', views.retorna_visualizar_empresa_lojista, name='retorna_visualizar_empresa_lojista'),
    path('minhas-empresas-lojista/', views.retorna_minhas_empresas_lojista, name='minhas_empresas_lojista')
]