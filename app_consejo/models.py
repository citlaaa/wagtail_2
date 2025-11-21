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
        related_name='consejo_users'
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
