from django.shortcuts import render

def inicio_estimulos(request):
    app_name = 'Estímulos'
    
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