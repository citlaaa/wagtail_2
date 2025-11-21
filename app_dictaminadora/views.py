from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .models import DictaminadoraUser # Importamos el modelo específico

def inicio_dictaminadora(request):
    app_name = 'Dictaminadora'
    context = {'app_name': app_name, 'error_message': None}
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            try:
                # Intenta obtener el registro de DictaminadoraUser para este usuario (y que esté activo)
                dictaminadora_user = DictaminadoraUser.objects.get(user=user, activo=True)
                
                login(request, user)
                context['rol'] = dictaminadora_user.rol
                return render(request, 'app_home.html', context)
            
            except DictaminadoraUser.DoesNotExist:
                context['error_message'] = f"El usuario **{username}** no está registrado o activo en la aplicación **{app_name}**."
                return render(request, 'login.html', context)
        else:
            context['error_message'] = "Credenciales incorrectas. Por favor, inténtelo de nuevo."
            return render(request, 'login.html', context)
    
    return render(request, 'login.html', context)