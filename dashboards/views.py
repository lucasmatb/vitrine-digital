from django.shortcuts import render, redirect
from empresas.models import Empresa, Categoria_Empresa
from django.db.models import Count

# Create your views here.

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard_usuario')
    
    return render(request, 'home.html')

def retorna_dashboard_usuario(request):
    data = {}

    # Filtrar categorias que têm pelo menos uma empresa associada
    categorias = Categoria_Empresa.objects.annotate(
        num_empresas=Count('empresa')
    ).filter(num_empresas__gt=0)

    for categoria in categorias:
        empresas = Empresa.objects.filter(empresa_categoria=categoria).annotate(
            favoritos=Count('favoritos_empresas')
        )

        empresas_com_favoritos = [
            {
                'id': empresa.id,
                'nome_fantasia': empresa.nome_fantasia,
                'cnpj': empresa.cnpj,
                'imagem_perfil': empresa.imagem_perfil,
                'imagem_capa': empresa.imagem_capa,
                'categorias': empresa.empresa_categoria.all(),
                'favorito_usuario': empresa.favoritos_empresas.filter(id=request.user.id).exists(),
                'favoritos': empresa.favoritos
            }
            for empresa in empresas
        ]

        data[categoria.descricao] = empresas_com_favoritos

    return render(request, 'dashboard-usuario.html', {'data': data})

def retorna_dashboard_lojista(request):

    #data = {}
    #data['form'] = UsuarioRegistrationForm()
    return render(request, 'dashboard-lojista.html')#, data)