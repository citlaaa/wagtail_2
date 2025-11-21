from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .models import ConsejoUser # Importamos el modelo específico

def inicio_consejo(request):
    app_name = 'Consejo'
    context = {'app_name': app_name, 'error_message': None} # Inicializamos el mensaje de error

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # 1. Autenticar el usuario con las credenciales estándar de Django
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # El usuario existe en User, ahora validamos si es un usuario de Consejo activo
            try:
                # Intenta obtener el registro de ConsejoUser para este usuario (y que esté activo)
                consejo_user = ConsejoUser.objects.get(user=user, activo=True)
                
                # Inicia la sesión de Django y procede a la página de inicio de la app
                login(request, user)
                context['rol'] = consejo_user.rol
                return render(request, 'app_home.html', context)
            
            except ConsejoUser.DoesNotExist:
                # El usuario existe, pero no tiene perfil activo en ConsejoUser
                context['error_message'] = f"El usuario **{username}** no está registrado o activo en la aplicación **{app_name}**."
                return render(request, 'login.html', context)
        else:
            # Autenticación de Django fallida
            context['error_message'] = "Credenciales incorrectas. Por favor, inténtelo de nuevo."
            return render(request, 'login.html', context)
    
    # Si la solicitud es GET, muestra el formulario de inicio de sesión.
    return render(request, 'login.html', context)