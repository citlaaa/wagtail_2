from django.db import models
from django.contrib.auth.models import User

class DictaminadoraUser(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Administrador'),
        ('miembro', 'Miembro'),
        ('consulta', 'Consulta'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='dictaminadora_users'
    )
    rol = models.CharField(max_length=30, choices=ROLE_CHOICES)
    activo = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user',)
        verbose_name = 'Usuario (Dictaminadora)'
        verbose_name_plural = 'Usuarios (Dictaminadora)'

    def __str__(self):
        return f"{self.user.username} — {self.rol} ({'Activo' if self.activo else 'Inactivo'})"

    # Métodos de permisos (miembro = editor)
    def puede_consultar(self):
        return self.activo and self.rol in ['admin', 'miembro', 'consulta']

    def puede_crear(self):
        return self.activo and self.rol in ['admin', 'miembro']

    def puede_editar(self):
        return self.activo and self.rol in ['admin', 'miembro']

    def puede_eliminar(self):
        return self.activo and self.rol == 'admin'


class DictaminadoraDocumento(models.Model):
    descripcion = models.CharField(max_length=300, verbose_name="Descripción")
    archivo_pdf = models.FileField(upload_to="dictaminadora/pdf/", verbose_name="Archivo PDF")
    visible = models.BooleanField(default=True, verbose_name="Visible")
    creado = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    modificado = models.DateTimeField(auto_now=True, verbose_name="Última modificación")
    subido_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='dictaminadora_documentos',
        verbose_name="Subido por"
    )

    class Meta:
        verbose_name = 'Documento (Dictaminadora)'
        verbose_name_plural = 'Documentos (Dictaminadora)'
        ordering = ['-creado']

    def __str__(self):
        return self.descripcion
