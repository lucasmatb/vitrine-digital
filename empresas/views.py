from django.shortcuts import render
from .forms import EmpresaRegistrationForm

def retorna_cadastro_empresa(request):
    data = {}
    data['form'] = EmpresaRegistrationForm()
    return render(request, 'cadastro-empresa.html', data)

def valida_cadastro_empresa(request):
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
    #data = {}
    #data['form'] = UsuarioRegistrationForm()
    return render(request, 'minhas-empresas-lojista.html')#, data)