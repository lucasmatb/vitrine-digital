from django.urls import path
from . import views

urlpatterns = [
    path('cadastro-empresa/', views.retorna_cadastro_empresa, name='cadastrar_empresa'),
    path('valida-cadastro-empresa/', views.valida_cadastro_empresa, name='valida_cadastrar_empresa'),
    path('editar-empresa/<int:pk>/', views.retorna_editar_empresa, name='editar_empresa'),
    path('valida-editar-empresa/<int:pk>/', views.valida_editar_empresa, name='valida_editar_empresa'),
    path('visualizar-empresa/', views.retorna_visualizar_empresa_usuario, name='visualizar_empresa'),
    path('minhas-empresas-lojista/', views.retorna_minhas_empresas_lojista, name='minhas_empresas_lojista'),
    path('visualizar-empresa-lojista/', views.retorna_visualizar_empresa_lojista, name='visualizar_empresa_lojista'),
    path('verifica-cep/<str:cep>/', views.verifica_cep, name='verifica_cep'),  
]