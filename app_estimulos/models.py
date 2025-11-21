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

