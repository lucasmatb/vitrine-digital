from django.shortcuts import render
from django.http import JsonResponse
from django.contrib import messages
from .forms import EmpresaForm
from .models import Empresa, Endereco, Estado, Cidade
from produtos.models import Produto
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
import requests

def retorna_cadastro_empresa(request):
    data = {}
    data['form'] = EmpresaForm()
    return render(request, 'formulario-empresa.html', data)

def valida_cadastro_empresa(request):
    empresa_count = Empresa.objects.filter(id_usuario=request.user).count()
    if empresa_count >= 10:
        messages.error(request, 'Você chegou no limite de empresas para sua conta, o limite é 10.')
        return redirect('minhas_empresas_lojista')

    form = EmpresaForm(request.POST, request.FILES or None)
    if form.is_valid():
        estado = retorna_model_estado_por_nome(form.cleaned_data['estado'])
        cidade = retorna_model_cidade(estado, form.cleaned_data['cidade'])

        if estado is None or cidade is None:
            messages.error(request, 'Problema na resolução do endereço, tente novamente mais tarde')
        else:
            empresa = Empresa.objects.create(
                nome_fantasia   =  form.cleaned_data['nome_fantasia'],
                razao_social    =  form.cleaned_data['razao_social'],
                cnpj            =  form.cleaned_data['cnpj_alterado'],
                telefone        =  form.cleaned_data['telefone'],
                email           =  form.cleaned_data['email'],
                imagem_capa     =  form.cleaned_data['imagem_capa'],
                imagem_perfil   =  form.cleaned_data['imagem_perfil'],
                id_usuario      =  request.user
            )

            empresa.empresa_categoria.add(*form.cleaned_data['categorias'])

            Endereco.objects.create(
                cep         =  form.cleaned_data['cep'],
                logradouro  =  form.cleaned_data['logradouro'],
                numero      =  form.cleaned_data['numero'],
                complemento =  form.cleaned_data['complemento'],
                bairro      =  form.cleaned_data['bairro'],
                id_cidade   =  cidade,
                id_empresa  =  empresa
            )

            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('minhas_empresas_lojista')

    return render(request, 'formulario-empresa.html', {'form': form})

def retorna_model_estado_por_nome(nomeEstado):
    return Estado.objects.get(descricao=nomeEstado)

def retorna_model_cidade(estado, nomeCidade):
    return Cidade.objects.get(descricao=nomeCidade, id_estado=estado)

def retorna_editar_empresa(request, pk):
    data = {}
    empresa = Empresa.objects.get(pk=pk)
    endereco = Endereco.objects.get(id_empresa=empresa)

    if validacao_usuario_possui_empresa(request.user, pk) == False:
        messages.error(request, 'Esta empresa não pertence ao usuário logado')
        return redirect('minhas_empresas_lojista')

    data['form'] = EmpresaForm(instance=empresa)
    data['form'].fields['cnpj_alterado'].initial = empresa.cnpj
    data['form'].fields['cep'].initial = endereco.cep
    data['form'].fields['logradouro'].initial = endereco.logradouro
    data['form'].fields['numero'].initial = endereco.numero
    data['form'].fields['complemento'].initial = endereco.complemento
    data['form'].fields['bairro'].initial = endereco.bairro
    data['form'].fields['cidade'].initial = endereco.id_cidade
    data['form'].fields['estado'].initial = endereco.id_cidade.id_estado
    data['form'].fields['categorias'].initial = empresa.empresa_categoria.all()
    data['imagem_capa'] = empresa.imagem_capa
    data['imagem_perfil'] = empresa.imagem_perfil
    data['id_empresa'] = empresa.id

    return render(request, 'formulario-empresa.html', data)

def valida_editar_empresa(request, pk):
    data = {}
    empresa = Empresa.objects.get(pk=pk)

    if validacao_usuario_possui_empresa(request.user, pk) == False:
        messages.error(request, 'Esta empresa não pertence ao usuário logado')
        return redirect('minhas_empresas_lojista')

    data['id_empresa'] = empresa.id
    data['imagem_capa'] = empresa.imagem_capa
    data['imagem_perfil'] = empresa.imagem_perfil
    endereco = Endereco.objects.get(id_empresa=empresa)
    form = EmpresaForm(request.POST, request.FILES or None, instance=empresa)
    if form.is_valid():
        estado = retorna_model_estado_por_nome(form.cleaned_data['estado'])
        cidade = retorna_model_cidade(estado, form.cleaned_data['cidade'])

        if estado is None or cidade is None:
            messages.error(request, 'Problema na resolução do endereço, tente novamente mais tarde')
        else:

            if form.cleaned_data['imagem_capa'] is None:
                form.cleaned_data['imagem_capa'] = empresa.imagem_capa
            if form.cleaned_data['imagem_perfil'] is None:
                form.cleaned_data['imagem_perfil'] = empresa.imagem_perfil

            empresa.nome_fantasia   =  form.cleaned_data['nome_fantasia']
            empresa.razao_social    =  form.cleaned_data['razao_social']
            empresa.cnpj            =  form.cleaned_data['cnpj_alterado']
            empresa.telefone        =  form.cleaned_data['telefone']
            empresa.email           =  form.cleaned_data['email']
            empresa.imagem_capa     =  form.cleaned_data['imagem_capa']
            empresa.imagem_perfil   =  form.cleaned_data['imagem_perfil']
            empresa.save()
            
            empresa.empresa_categoria.set(form.cleaned_data['categorias'])

            endereco.cep         =  form.cleaned_data['cep']
            endereco.logradouro  =  form.cleaned_data['logradouro']
            endereco.numero      =  form.cleaned_data['numero']
            endereco.complemento =  form.cleaned_data['complemento']
            endereco.bairro      =  form.cleaned_data['bairro']
            endereco.id_cidade   =  cidade
            endereco.save()

            messages.success(request, 'Edição realizada com sucesso!')
            return redirect('minhas_empresas_lojista')

    data['form'] = form
    return render(request, 'formulario-empresa.html', data)

def retorna_visualizar_empresa_usuario(request):
    return render(request, 'visualizar-empresa-usuario.html')

def retorna_minhas_empresas_lojista(request):
    data = {}
    data['empresas'] = Empresa.objects.filter(id_usuario=request.user).prefetch_related('empresa_categoria')
    return render(request, 'minhas-empresas-lojista.html', data)

def verifica_cep(request, cep):
    cep_formatado = cep.replace("-", "")

    url = f'https://viacep.com.br/ws/{cep_formatado}/json/'

    try:
        response = requests.get(url)
        response.raise_for_status()

        dados = response.json()

        if "erro" in dados:
            return JsonResponse({'erro': 'CEP não encontrado'}, status=404)

        return JsonResponse(dados, content_type='application/json')

    except requests.RequestException as e:
        return JsonResponse({'erro': 'Erro ao buscar CEP'}, status=500)
    
def excluir_empresa(request, pk):

    if validacao_usuario_possui_empresa(request.user, pk) == False:
        messages.error(request, 'Esta empresa não pertence ao usuário logado')
        return redirect('minhas_empresas_lojista')

    empresa = get_object_or_404(Empresa, pk=pk)
    empresa.delete()
    messages.success(request, 'Empresa excluída com sucesso')
    return redirect('minhas_empresas_lojista')

def validacao_usuario_possui_empresa(usuario, id_empresa):
    empresa = Empresa.objects.get(pk=id_empresa)
    if empresa.id_usuario != usuario:
        return False
    return True

def favorita_nao_favorita_empresa(request, id_empresa):
    try:
        if request.user.favorito_empresa.filter(id=id_empresa).exists():
            request.user.favorito_empresa.remove(Empresa.objects.get(pk=id_empresa))
            like_string = 'unlike'
        else:
            like_string = 'like'
            request.user.favorito_empresa.add(Empresa.objects.get(pk=id_empresa))
        return JsonResponse({'status': 'success', 'message': like_string})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

def salva_nao_salva_produto(request, id_produto):
    try:
        if request.user.favorito_produto.filter(id=id_produto).exists():
            request.user.favorito_produto.remove(Produto.objects.get(pk=id_produto))
            like_string = 'unlike'
        else:
            like_string = 'like'
            request.user.favorito_produto.add(Produto.objects.get(pk=id_produto))

        return JsonResponse({'status': 'success', 'message': like_string})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
