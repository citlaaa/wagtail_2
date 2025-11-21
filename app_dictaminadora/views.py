from django.shortcuts import render

def inicio_dictaminadora(request):
    app_name = 'Dictaminadora'
    
    if request.method == 'POST':
        context = {
            'app_name': app_name,
        }
        return render(request, 'app_home.html', context)
    
    else:
        context = {
            'app_name': app_name,
        }
        return render(request, 'login.html', context)