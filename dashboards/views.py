from django.shortcuts import render
from django.shortcuts import redirect

# Create your views here.

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard_usuario')
    
    return render(request, 'home.html')