from django.urls import path
from . import views

urlpatterns = [
    path('visualizar-produto/', views.retorna_visualizar_produto, name='visualizar_produto'),
    path('criar-produto/', views.criar_produto, name='criar_produto'),
    path('editar-produto/<int:pk>/', views.editar_produto, name='editar_produto'),
    path('excluir-produto/<int:pk>/', views.excluir_produto, name='excluir_produto'),
]