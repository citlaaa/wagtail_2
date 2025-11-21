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
