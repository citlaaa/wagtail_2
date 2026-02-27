from django.db import models
from django.contrib.auth.models import User

class ConsejoUser(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Administrador'),
        ('editor', 'Editor'),
        ('consulta', 'Consulta'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='consejo_users',
        limit_choices_to={'is_active': True}
        
    )
    rol = models.CharField(max_length=30, choices=ROLE_CHOICES)
    activo = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user',)  # opcional: asegura una fila por user en esta app
        verbose_name = 'Usuario (Consejo)'
        verbose_name_plural = 'Usuarios (Consejo)'

    def __str__(self):
        return f"{self.user.username} — {self.rol} ({'Activo' if self.activo else 'Inactivo'})"

    def puede_consultar(self):
        return self.activo and self.rol in ['admin', 'editor', 'consulta']

    def puede_crear(self):
        return self.activo and self.rol in ['admin', 'editor']

    def puede_editar(self):
        return self.activo and self.rol in ['admin', 'editor']

    def puede_eliminar(self):
        return self.activo and self.rol == 'admin'

class ConsejoDocumento(models.Model):
    descripcion = models.CharField(max_length=300, verbose_name="Descripción")
    archivo_pdf = models.FileField(upload_to="consejo/pdf/", verbose_name="Archivo PDF")
    visible = models.BooleanField(default=True, verbose_name="Visible")
    creado = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    modificado = models.DateTimeField(auto_now=True, verbose_name="Última modificación")
    subido_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='consejo_documentos',
        verbose_name="Subido por"
        )

    class Meta:
        verbose_name = 'Documento (Consejo)'
        verbose_name_plural = 'Documentos (Consejo)'
        ordering = ['-creado']

    def __str__(self):
            return self.descripcion
