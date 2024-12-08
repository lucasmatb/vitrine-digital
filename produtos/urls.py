from django.urls import path
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from . import views

urlpatterns = [
    path('visualizar-produto/', login_required(views.retorna_visualizar_produto), name='visualizar_produto'),

    path('listagem-produtos/<int:id_empresa>/', permission_required('produtos.view_produto')(views.retorna_listagem_produtos_por_empresa), name='listagem_produto_por_empresa'),
    path('criar-produto/', permission_required('produtos.add_produto')(views.criar_produto), name='criar_produto'),
    path('editar-produto/<int:pk>/', permission_required('produtos.change_produto')(views.editar_produto), name='editar_produto'),
    path('excluir-produto/<int:pk>/', permission_required('produtos.delete_produto')(views.excluir_produto), name='excluir_produto'),
]
