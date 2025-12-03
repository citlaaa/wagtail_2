from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
import os
from .models import EstimulosUser, EstimulosDocumento


def validar_archivo_pdf(archivo):
    """Valida que el archivo sea realmente un PDF"""

    ext = os.path.splitext(archivo.name)[1].lower()
    if ext != '.pdf':
        raise ValidationError('Solo se permiten archivos PDF')

    # Validar tipo MIME Esto evita tener ataques
    if archivo.content_type != 'application/pdf':
        raise ValidationError('El archivo debe ser un PDF válido')
    return True


def get_estimulos_user(user):
    try:
        return EstimulosUser.objects.get(user=user, activo=True)
    except EstimulosUser.DoesNotExist:
        return None


def inicio_estimulos(request):
    """Vista de login para la aplicación Estímulos"""
    app_name = 'Estímulos'
    context = {'app_name': app_name, 'error_message': None}

    if request.user.is_authenticated:
        estimulos_user = get_estimulos_user(request.user)
        if estimulos_user:
            return redirect('estimulos_home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            try:
                estimulos_user = EstimulosUser.objects.get(user=user, activo=True)
                login(request, user)
                return redirect('estimulos_home')

            except EstimulosUser.DoesNotExist:
                context[
                    'error_message'] = f"El usuario '{username}' no está registrado o activo en la aplicación {app_name}."
                return render(request, 'app_estimulos/login.html', context)
        else:
            context['error_message'] = "Credenciales incorrectas. Por favor, inténtelo de nuevo."
            return render(request, 'app_estimulos/login.html', context)

    return render(request, 'app_estimulos/login.html', context)


def logout_estimulos(request):
    """Cerrar sesión"""
    logout(request)
    return redirect('inicio_estimulos')


@login_required(login_url='inicio_estimulos')
def estimulos_home(request):
    """Página principal después del login"""
    estimulos_user = get_estimulos_user(request.user)
    if not estimulos_user:
        messages.error(request, "No tienes acceso a esta aplicación.")
        return redirect('inicio_estimulos')

    context = {
        'app_name': 'Estímulos',
        'app_user': estimulos_user,
        'user': request.user,
    }
    return render(request, 'app_estimulos/home.html', context)


@login_required(login_url='inicio_estimulos')
def estimulos_consultor(request):
    """Vista de consulta de documentos"""
    estimulos_user = get_estimulos_user(request.user)
    if not estimulos_user or not estimulos_user.puede_consultar():
        messages.error(request, "No tienes permiso para acceder a esta sección.")
        return redirect('inicio_estimulos')

    documentos = EstimulosDocumento.objects.filter(visible=True).order_by('-creado')

    context = {
        'app_name': 'Estímulos',
        'app_user': estimulos_user,
        'documentos': documentos,
    }
    return render(request, 'app_estimulos/consultor.html', context)


@login_required(login_url='inicio_estimulos')
def estimulos_gestor(request):
    #"""Vista de gestión de documentos"""
    estimulos_user = get_estimulos_user(request.user)
    if not estimulos_user or not estimulos_user.puede_crear():
        messages.error(request, "No tienes permiso para acceder al gestor de documentos.")
        return redirect('estimulos_home')

    documentos = EstimulosDocumento.objects.all().order_by('-creado')

    context = {
        'app_name': 'Estímulos',
        'app_user': estimulos_user,
        'documentos': documentos,
    }
    return render(request, 'app_estimulos/gestor.html', context)


@login_required(login_url='inicio_estimulos')
def estimulos_guardar(request):
    """Guardar nuevo documento"""
    estimulos_user = get_estimulos_user(request.user)
    if not estimulos_user or not estimulos_user.puede_crear():
        messages.error(request, "No tienes permiso para subir documentos.")
        return redirect('estimulos_home')

    if request.method == 'POST':
        try:
            descripcion = request.POST.get("descripcion")
            archivo_pdf = request.FILES.get("archivo_pdf")
            visible = 'visible' in request.POST

            if not descripcion or not archivo_pdf:
                messages.error(request, "Debes proporcionar una descripción y un archivo PDF.")
                return redirect('estimulos_gestor')

            # VALIDAR QUE SEA PDF
            try:
                validar_archivo_pdf(archivo_pdf)
            except ValidationError as e:
                messages.error(request, str(e))
                return redirect('estimulos_gestor')

            documento = EstimulosDocumento(
                descripcion=descripcion,
                archivo_pdf=archivo_pdf,
                visible=visible,
                subido_por=request.user
            )
            documento.save()
            messages.success(request, "Documento guardado exitosamente.")
        except Exception as e:
            messages.error(request, f"Error al guardar el documento: {e}")

    return redirect('estimulos_gestor')


@login_required(login_url='inicio_estimulos')
def estimulos_detalle(request, id):
    """Ver detalle/editar documento"""
    estimulos_user = get_estimulos_user(request.user)
    if not estimulos_user or not estimulos_user.puede_editar():
        messages.error(request, "No tienes permiso para editar documentos.")
        return redirect('estimulos_home')

    documento = get_object_or_404(EstimulosDocumento, pk=id)

    context = {
        'app_name': 'Estímulos',
        'app_user': estimulos_user,
        'documento': documento,
    }
    return render(request, 'app_estimulos/editar.html', context)


@login_required(login_url='inicio_estimulos')
def estimulos_editar(request, id):
    """Procesar edición de documento"""
    estimulos_user = get_estimulos_user(request.user)
    if not estimulos_user or not estimulos_user.puede_editar():
        messages.error(request, "No tienes permiso para editar documentos.")
        return redirect('estimulos_home')

    if request.method == 'POST':
        try:
            documento = get_object_or_404(EstimulosDocumento, pk=id)
            documento.descripcion = request.POST.get("descripcion")
            documento.visible = 'visible' in request.POST

            if 'archivo_pdf' in request.FILES:
                # VALIDAR QUE SEA PDF
                try:
                    validar_archivo_pdf(request.FILES["archivo_pdf"])
                except ValidationError as e:
                    messages.error(request, str(e))
                    return redirect('estimulos_detalle', id=id)

                documento.archivo_pdf.delete(save=False)
                documento.archivo_pdf = request.FILES["archivo_pdf"]

            documento.save()
            messages.success(request, "Documento actualizado exitosamente.")
        except Exception as e:
            messages.error(request, f"Error al actualizar el documento: {e}")

    return redirect('estimulos_gestor')


@login_required(login_url='inicio_estimulos')
def estimulos_eliminar(request, id):
    """Eliminar documento (solo admin)"""
    estimulos_user = get_estimulos_user(request.user)
    if not estimulos_user or not estimulos_user.puede_eliminar():
        messages.error(request, "No tienes permiso para eliminar documentos.")
        return redirect('estimulos_home')

    try:
        documento = get_object_or_404(EstimulosDocumento, pk=id)
        documento.archivo_pdf.delete(save=False)
        documento.delete()
        messages.success(request, "Documento eliminado exitosamente.")
    except Exception as e:
        messages.error(request, f"Error al eliminar el documento: {e}")

    return redirect('estimulos_gestor')
