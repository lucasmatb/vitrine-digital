from django.shortcuts import render, redirect
from empresas.models import Empresa, Categoria_Empresa
from usuarios.models import Pedido_Lojista
from django.db.models import Count

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard_usuario')
    
    return render(request, 'home.html')

def retorna_dashboard_usuario(request):
    data = {}

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

    if request.user.has_perm('empresas.add_empresa'):
        usuario_tem_pedido_em_aguardo = 'lojista'
    elif Pedido_Lojista.objects.filter(
            id_usuario=request.user,
            status_pedido='Aguardando avaliação'
        ).exists():

        usuario_tem_pedido_em_aguardo = 'aguardando'
    else:
        usuario_tem_pedido_em_aguardo = 'usuario'

    data['usuario_tem_pedido_em_aguardo'] = usuario_tem_pedido_em_aguardo

    return render(request, 'dashboard-usuario.html', {'data': data, 'pedido_aguardo': usuario_tem_pedido_em_aguardo})

def retorna_dashboard_lojista(request):

    #data = {}
    #data['form'] = UsuarioRegistrationForm()
    return render(request, 'dashboard-lojista.html')#, data)