from django.db import models
from django.contrib.auth.models import User


class EstimulosUser(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Administrador'),
        ('evaluador', 'Evaluador'),
        ('consulta', 'Consulta'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='estimulos_users'
    )
    rol = models.CharField(max_length=30, choices=ROLE_CHOICES)
    activo = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user',)
        verbose_name = 'Usuario (Estímulos)'
        verbose_name_plural = 'Usuarios (Estímulos)'

    def __str__(self):
        return f"{self.user.username} — {self.rol} ({'Activo' if self.activo else 'Inactivo'})"

    # Métodos de permisos (evaluador = editor)
    def puede_consultar(self):
        return self.activo and self.rol in ['admin', 'evaluador', 'consulta']

    def puede_crear(self):
        return self.activo and self.rol in ['admin', 'evaluador']

    def puede_editar(self):
        return self.activo and self.rol in ['admin', 'evaluador']

    def puede_eliminar(self):
        return self.activo and self.rol == 'admin'


class EstimulosDocumento(models.Model):
    descripcion = models.CharField(max_length=300, verbose_name="Descripción")
    archivo_pdf = models.FileField(upload_to="estimulos/pdf/", verbose_name="Archivo PDF")
    visible = models.BooleanField(default=True, verbose_name="Visible")
    creado = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    modificado = models.DateTimeField(auto_now=True, verbose_name="Última modificación")
    subido_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='estimulos_documentos',
        verbose_name="Subido por"
    )

    class Meta:
        db_table = 'estimulos_documentos'
        verbose_name = 'Documento (Estímulos)'
        verbose_name_plural = 'Documentos (Estímulos)'
        ordering = ['-creado']

    def __str__(self):
        return self.descripcion
