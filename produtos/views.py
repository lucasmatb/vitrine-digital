from django.shortcuts import render

def retorna_visualizar_produto(request):
    return render(request, 'visualizar-produto.html')