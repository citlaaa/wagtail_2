from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ConsejoUser, ConsejoDocumento


def get_consejo_user(user):
    """Obtiene el ConsejoUser activo para un usuario Django"""
    try:
        return ConsejoUser.objects.get(user=user, activo=True)
    except ConsejoUser.DoesNotExist:
        return None


def inicio_consejo(request):
    """Vista de login para la aplicación Consejo"""
    app_name = 'Consejo'
    context = {'app_name': app_name, 'error_message': None}

    # Si ya está logueado y es usuario de Consejo, redirigir al home
    if request.user.is_authenticated:
        consejo_user = get_consejo_user(request.user)
        if consejo_user:
            return redirect('consejo_home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            try:
                consejo_user = ConsejoUser.objects.get(user=user, activo=True)
                login(request, user)
                return redirect('consejo_home')

            except ConsejoUser.DoesNotExist:
                context[
                    'error_message'] = f"El usuario '{username}' no está registrado o activo en la aplicación {app_name}."
                return render(request, 'app_consejo/login.html', context)
        else:
            context['error_message'] = "Credenciales incorrectas. Por favor, inténtelo de nuevo."
            return render(request, 'app_consejo/login.html', context)

    return render(request, 'app_consejo/login.html', context)


def logout_consejo(request):
    """Cerrar sesión"""
    logout(request)
    return redirect('inicio_consejo')


@login_required(login_url='inicio_consejo')
def consejo_home(request):
    """Página principal después del login"""
    consejo_user = get_consejo_user(request.user)
    if not consejo_user:
        messages.error(request, "No tienes acceso a esta aplicación.")
        return redirect('inicio_consejo')

    context = {
        'app_name': 'Consejo',
        'consejo_user': consejo_user,
        'user': request.user,
    }
    return render(request, 'app_consejo/home.html', context)


@login_required(login_url='inicio_consejo')
def consejo_consultor(request):
    """Vista de consulta de documentos (todos los roles pueden ver)"""
    consejo_user = get_consejo_user(request.user)
    if not consejo_user or not consejo_user.puede_consultar():
        messages.error(request, "No tienes permiso para acceder a esta sección.")
        return redirect('inicio_consejo')

    documentos = ConsejoDocumento.objects.filter(visible=True).order_by('-creado')

    context = {
        'app_name': 'Consejo',
        'consejo_user': consejo_user,
        'documentos': documentos,
    }
    return render(request, 'app_consejo/consultor.html', context)


@login_required(login_url='inicio_consejo')
def consejo_gestor(request):
    """Vista de gestión de documentos (admin y editor)"""
    consejo_user = get_consejo_user(request.user)
    if not consejo_user or not consejo_user.puede_crear():
        messages.error(request, "No tienes permiso para acceder al gestor de documentos.")
        return redirect('consejo_home')

    documentos = ConsejoDocumento.objects.all().order_by('-creado')

    context = {
        'app_name': 'Consejo',
        'consejo_user': consejo_user,
        'documentos': documentos,
    }
    return render(request, 'app_consejo/gestor.html', context)


@login_required(login_url='inicio_consejo')
def consejo_guardar(request):
    """Guardar nuevo documento"""
    consejo_user = get_consejo_user(request.user)
    if not consejo_user or not consejo_user.puede_crear():
        messages.error(request, "No tienes permiso para subir documentos.")
        return redirect('consejo_home')

    if request.method == 'POST':
        try:
            descripcion = request.POST.get("descripcion")
            archivo_pdf = request.FILES.get("archivo_pdf")
            visible = 'visible' in request.POST

            if not descripcion or not archivo_pdf:
                messages.error(request, "Debes proporcionar una descripción y un archivo PDF.")
                return redirect('consejo_gestor')

            documento = ConsejoDocumento(
                descripcion=descripcion,
                archivo_pdf=archivo_pdf,
                visible=visible,
                subido_por=request.user
            )
            documento.save()
            messages.success(request, "Documento guardado exitosamente.")
        except Exception as e:
            messages.error(request, f"Error al guardar el documento: {e}")

    return redirect('consejo_gestor')


@login_required(login_url='inicio_consejo')
def consejo_detalle(request, id):
    """Ver detalle/editar documento"""
    consejo_user = get_consejo_user(request.user)
    if not consejo_user or not consejo_user.puede_editar():
        messages.error(request, "No tienes permiso para editar documentos.")
        return redirect('consejo_home')

    documento = get_object_or_404(ConsejoDocumento, pk=id)

    context = {
        'app_name': 'Consejo',
        'consejo_user': consejo_user,
        'documento': documento,
    }
    return render(request, 'app_consejo/editar.html', context)


@login_required(login_url='inicio_consejo')
def consejo_editar(request, id):
    """Procesar edición de documento"""
    consejo_user = get_consejo_user(request.user)
    if not consejo_user or not consejo_user.puede_editar():
        messages.error(request, "No tienes permiso para editar documentos.")
        return redirect('consejo_home')

    if request.method == 'POST':
        try:
            documento = get_object_or_404(ConsejoDocumento, pk=id)
            documento.descripcion = request.POST.get("descripcion")
            documento.visible = 'visible' in request.POST

            if 'archivo_pdf' in request.FILES:
                # Eliminar archivo anterior
                documento.archivo_pdf.delete(save=False)
                documento.archivo_pdf = request.FILES["archivo_pdf"]

            documento.save()
            messages.success(request, "Documento actualizado exitosamente.")
        except Exception as e:
            messages.error(request, f"Error al actualizar el documento: {e}")

    return redirect('consejo_gestor')


@login_required(login_url='inicio_consejo')
def consejo_eliminar(request, id):
    """Eliminar documento (solo admin)"""
    consejo_user = get_consejo_user(request.user)
    if not consejo_user or not consejo_user.puede_eliminar():
        messages.error(request, "No tienes permiso para eliminar documentos.")
        return redirect('consejo_home')

    try:
        documento = get_object_or_404(ConsejoDocumento, pk=id)
        documento.archivo_pdf.delete(save=False)
        documento.delete()
        messages.success(request, "Documento eliminado exitosamente.")
    except Exception as e:
        messages.error(request, f"Error al eliminar el documento: {e}")

    return redirect('consejo_gestor')
