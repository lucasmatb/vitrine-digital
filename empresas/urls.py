from django.urls import path
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from . import views

urlpatterns = [
    path('cadastro-empresa/', permission_required('empresas.add_empresa')(views.retorna_cadastro_empresa), name='cadastrar_empresa'),
    path('valida-cadastro-empresa/', permission_required('empresas.add_empresa')(views.valida_cadastro_empresa), name='valida_cadastrar_empresa'),

    path('editar-empresa/<int:pk>/', permission_required('empresas.change_empresa')(views.retorna_editar_empresa), name='editar_empresa'),
    path('valida-editar-empresa/<int:pk>/', permission_required('empresas.change_empresa')(views.valida_editar_empresa), name='valida_editar_empresa'),

    path('verifica-cep/<str:cep>/', permission_required('empresas.add_empresa')(views.verifica_cep), name='verifica_cep'),

    path('excluir-empresa/<int:pk>/', permission_required('empresas.delete_empresa')(views.excluir_empresa), name='excluir_empresa'),

    path('minhas-empresas-lojista/', permission_required('empresas.view_empresa')(views.retorna_minhas_empresas_lojista), name='minhas_empresas_lojista'),

    path('visualizar-empresa/<int:id_empresa>/', login_required(views.retorna_visualizar_empresa_usuario), name='visualizar_empresa'),

    path('favorita-nao-favorita-empresa/<int:id_empresa>/', login_required(views.favorita_nao_favorita_empresa), name='favorita_nao_favorita_empresa'),
    path('salva-nao-salva-produto/<int:id_produto>/', login_required(views.salva_nao_salva_produto), name='salva_nao_salva_produto')
]