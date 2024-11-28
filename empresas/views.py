from django.shortcuts import render

def retorna_cadastro_empresa(request):
    return render(request, 'cadastro-empresas.html')

def retorna_visualizar_empresa_lojista(request):
    return render(request, 'visualizar-empresa-lojista.html')