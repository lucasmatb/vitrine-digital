from django.urls import path
from . import views

urlpatterns = [
    path('visualizar-produto/', views.retorna_visualizar_produto, name='visualizar-produto')
]