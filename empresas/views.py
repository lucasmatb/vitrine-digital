from django.shortcuts import render
from django.http import JsonResponse
from django.contrib import messages
from .forms import EmpresaForm
from .models import Empresa, Endereco, Estado, Cidade
from django.shortcuts import redirect
import requests

def retorna_cadastro_empresa(request):
    data = {}
    data['form'] = EmpresaForm()
    return render(request, 'formulario-empresa.html', data)

def valida_cadastro_empresa(request):
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

def retorna_visualizar_empresa_lojista(request):
    return render(request, 'visualizar-empresa-lojista.html')

def retorna_minhas_empresas_lojista(request):
    data = {}
    data['empresas'] = Empresa.objects.filter(id_usuario=request.user).prefetch_related('empresa_categoria')
    return render(request, 'minhas-empresas-lojista.html', data)

def verifica_cep(request, cep):
    # Formatar o CEP removendo possíveis caracteres extras (se necessário)
    cep_formatado = cep.replace("-", "")

    # URL da API ViaCEP
    url = f'https://viacep.com.br/ws/{cep_formatado}/json/'

    try:
        # Fazer a requisição GET para a API externa
        response = requests.get(url)
        response.raise_for_status()  # Levanta exceções para erros HTTP

        # Converter a resposta para JSON
        dados = response.json()

        # Verificar se houve erro na resposta da API
        if "erro" in dados:
            return JsonResponse({'erro': 'CEP não encontrado'}, status=404)

        # Retornar os dados como JSON
        return JsonResponse(dados, content_type='application/json')

    except requests.RequestException as e:
        # Em caso de erro na requisição externa, retornar erro
        return JsonResponse({'erro': 'Erro ao buscar CEP'}, status=500)