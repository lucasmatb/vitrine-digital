from django.shortcuts import render
from django.http import JsonResponse
from django.contrib import messages
from .forms import EmpresaRegistrationForm
from .models import Empresa, Endereco, Estado, Cidade
from django.shortcuts import redirect
import requests

def retorna_cadastro_empresa(request):
    data = {}
    data['form'] = EmpresaRegistrationForm()
    return render(request, 'cadastro-empresa.html', data)

def valida_cadastro_empresa(request):
    form = EmpresaRegistrationForm(request.POST, request.FILES or None)
    if form.is_valid():
        print(form.cleaned_data)
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

    return render(request, 'cadastro-empresa.html', {'form': form})

def retorna_model_estado_por_nome(nomeEstado):
    return Estado.objects.get(descricao=nomeEstado)

def retorna_model_cidade(estado, nomeCidade):
    return Cidade.objects.get(descricao=nomeCidade, id_estado=estado)

def retorna_editar_empresa(request):
    data = {}
    data['form'] = EmpresaRegistrationForm()
    return render(request, 'cadastro-empresa.html', data)

def valida_editar_empresa(request):
    form = EmpresaRegistrationForm(request.POST or None)
#    if form.is_valid():
#        usuario = Usuario.objects.create_user(
#            email       =  encriptarAESGCM(form.cleaned_data['email']),
#            password    =  form.cleaned_data['password'],
#            first_name  =  encriptarAESGCM(form.cleaned_data['first_name']),
#            last_name   =  encriptarAESGCM(form.cleaned_data['last_name']),
#            cpf         =  encriptarAESGCM(form.cleaned_data['cpf'])
#        )

#        grupo = Group.objects.get(name='Usuário')

#        usuario.groups.add(grupo)

#        messages.success(request, 'Cadastro realizado com sucesso!')
#        return redirect('login')
    
    return render(request, 'cadastro-empresa.html', {'form': form})

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