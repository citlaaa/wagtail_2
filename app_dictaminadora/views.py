from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
import os
from .models import DictaminadoraUser, DictaminadoraDocumento


def validar_archivo_pdf(archivo):
    """Valida que el archivo sea realmente un PDF"""
    # Validar extensión
    ext = os.path.splitext(archivo.name)[1].lower()
    if ext != '.pdf':
        raise ValidationError('Solo se permiten archivos PDF')

    # Validar tipo MIME
    if archivo.content_type != 'application/pdf':
        raise ValidationError('El archivo debe ser un PDF válido')


    return True


def get_dictaminadora_user(user):
    """Obtiene el DictaminadoraUser activo para un usuario Django"""
    try:
        return DictaminadoraUser.objects.get(user=user, activo=True)
    except DictaminadoraUser.DoesNotExist:
        return None


def inicio_dictaminadora(request):
    """Vista de login para la aplicación Dictaminadora"""
    app_name = 'Dictaminadora'
    context = {'app_name': app_name, 'error_message': None}

    if request.user.is_authenticated:
        dictaminadora_user = get_dictaminadora_user(request.user)
        if dictaminadora_user:
            return redirect('dictaminadora_home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            try:
                dictaminadora_user = DictaminadoraUser.objects.get(user=user, activo=True)
                login(request, user)
                return redirect('dictaminadora_home')

            except DictaminadoraUser.DoesNotExist:
                context[
                    'error_message'] = f"El usuario '{username}' no está registrado o activo en la aplicación {app_name}."
                return render(request, 'app_dictaminadora/login.html', context)
        else:
            context['error_message'] = "Credenciales incorrectas. Por favor, inténtelo de nuevo."
            return render(request, 'app_dictaminadora/login.html', context)

    return render(request, 'app_dictaminadora/login.html', context)


def logout_dictaminadora(request):
    """Cerrar sesión"""
    logout(request)
    return redirect('inicio_dictaminadora')


@login_required(login_url='inicio_dictaminadora')
def dictaminadora_home(request):
    """Página principal después del login"""
    dictaminadora_user = get_dictaminadora_user(request.user)
    if not dictaminadora_user:
        messages.error(request, "No tienes acceso a esta aplicación.")
        return redirect('inicio_dictaminadora')

    context = {
        'app_name': 'Dictaminadora',
        'app_user': dictaminadora_user,
        'user': request.user,
    }
    return render(request, 'app_dictaminadora/home.html', context)


@login_required(login_url='inicio_dictaminadora')
def dictaminadora_consultor(request):
    """Vista de consulta de documentos"""
    dictaminadora_user = get_dictaminadora_user(request.user)
    if not dictaminadora_user or not dictaminadora_user.puede_consultar():
        messages.error(request, "No tienes permiso para acceder a esta sección.")
        return redirect('inicio_dictaminadora')

    documentos = DictaminadoraDocumento.objects.filter(visible=True).order_by('-creado')

    context = {
        'app_name': 'Dictaminadora',
        'app_user': dictaminadora_user,
        'documentos': documentos,
    }
    return render(request, 'app_dictaminadora/consultor.html', context)


@login_required(login_url='inicio_dictaminadora')
def dictaminadora_gestor(request):
    """Vista de gestión de documentos"""
    dictaminadora_user = get_dictaminadora_user(request.user)
    if not dictaminadora_user or not dictaminadora_user.puede_crear():
        messages.error(request, "No tienes permiso para acceder al gestor de documentos.")
        return redirect('dictaminadora_home')

    documentos = DictaminadoraDocumento.objects.all().order_by('-creado')

    context = {
        'app_name': 'Dictaminadora',
        'app_user': dictaminadora_user,
        'documentos': documentos,
    }
    return render(request, 'app_dictaminadora/gestor.html', context)


@login_required(login_url='inicio_dictaminadora')
def dictaminadora_guardar(request):
    """Guardar nuevo documento"""
    dictaminadora_user = get_dictaminadora_user(request.user)
    if not dictaminadora_user or not dictaminadora_user.puede_crear():
        messages.error(request, "No tienes permiso para subir documentos.")
        return redirect('dictaminadora_home')

    if request.method == 'POST':
        try:
            descripcion = request.POST.get("descripcion")
            archivo_pdf = request.FILES.get("archivo_pdf")
            visible = 'visible' in request.POST

            if not descripcion or not archivo_pdf:
                messages.error(request, "Debes proporcionar una descripción y un archivo PDF.")
                return redirect('dictaminadora_gestor')

            # VALIDAR QUE SEA PDF
            try:
                validar_archivo_pdf(archivo_pdf)
            except ValidationError as e:
                messages.error(request, str(e))
                return redirect('dictaminadora_gestor')

            documento = DictaminadoraDocumento(
                descripcion=descripcion,
                archivo_pdf=archivo_pdf,
                visible=visible,
                subido_por=request.user
            )
            documento.save()
            messages.success(request, "Documento guardado exitosamente.")
        except Exception as e:
            messages.error(request, f"Error al guardar el documento: {e}")

    return redirect('dictaminadora_gestor')


@login_required(login_url='inicio_dictaminadora')
def dictaminadora_detalle(request, id):
    """Ver detalle/editar documento"""
    dictaminadora_user = get_dictaminadora_user(request.user)
    if not dictaminadora_user or not dictaminadora_user.puede_editar():
        messages.error(request, "No tienes permiso para editar documentos.")
        return redirect('dictaminadora_home')

    documento = get_object_or_404(DictaminadoraDocumento, pk=id)

    context = {
        'app_name': 'Dictaminadora',
        'app_user': dictaminadora_user,
        'documento': documento,
    }
    return render(request, 'app_dictaminadora/editar.html', context)


@login_required(login_url='inicio_dictaminadora')
def dictaminadora_editar(request, id):
    """Procesar edición de documento"""
    dictaminadora_user = get_dictaminadora_user(request.user)
    if not dictaminadora_user or not dictaminadora_user.puede_editar():
        messages.error(request, "No tienes permiso para editar documentos.")
        return redirect('dictaminadora_home')

    if request.method == 'POST':
        try:
            documento = get_object_or_404(DictaminadoraDocumento, pk=id)
            documento.descripcion = request.POST.get("descripcion")
            documento.visible = 'visible' in request.POST

            if 'archivo_pdf' in request.FILES:
                # VALIDAR QUE SEA PDF
                try:
                    validar_archivo_pdf(request.FILES["archivo_pdf"])
                except ValidationError as e:
                    messages.error(request, str(e))
                    return redirect('dictaminadora_detalle', id=id)

                documento.archivo_pdf.delete(save=False)
                documento.archivo_pdf = request.FILES["archivo_pdf"]

            documento.save()
            messages.success(request, "Documento actualizado exitosamente.")
        except Exception as e:
            messages.error(request, f"Error al actualizar el documento: {e}")

    return redirect('dictaminadora_gestor')


@login_required(login_url='inicio_dictaminadora')
def dictaminadora_eliminar(request, id):
    """Eliminar documento (solo admin)"""
    dictaminadora_user = get_dictaminadora_user(request.user)
    if not dictaminadora_user or not dictaminadora_user.puede_eliminar():
        messages.error(request, "No tienes permiso para eliminar documentos.")
        return redirect('dictaminadora_home')

    try:
        documento = get_object_or_404(DictaminadoraDocumento, pk=id)
        documento.archivo_pdf.delete(save=False)
        documento.delete()
        messages.success(request, "Documento eliminado exitosamente.")
    except Exception as e:
        messages.error(request, f"Error al eliminar el documento: {e}")

    return redirect('dictaminadora_gestor')