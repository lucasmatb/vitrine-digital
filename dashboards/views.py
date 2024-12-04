from django.shortcuts import render
from django.shortcuts import redirect

# Create your views here.

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard_usuario')
    
    return render(request, 'home.html')

def retorna_dashboard_usuario(request):
    #data = {}
    #data['form'] = UsuarioRegistrationForm()
    return render(request, 'dashboard-usuario.html')#, data)

def retorna_dashboard_lojista(request):
    #data = {}
    #data['form'] = UsuarioRegistrationForm()
    return render(request, 'dashboard-lojista.html')#, data)