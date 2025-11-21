from django.shortcuts import render

def inicio_consejo(request):
    app_name = 'Consejo'
    
    # Si la solicitud es POST, es que se envió el formulario de login.
    if request.method == 'POST':
        # En una implementación real, aquí se procesaría el login.
        # Simulamos que el login es exitoso y mostramos la página "Hola mundo".
        context = {
            'app_name': app_name,
        }
        return render(request, 'app_home.html', context)
    
    # Si la solicitud es GET, mostramos el formulario de inicio de sesión.
    else:
        context = {
            'app_name': app_name,
        }
        return render(request, 'login.html', context)