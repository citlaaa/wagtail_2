from django.contrib import admin
from .models import ConsejoUser


@admin.register(ConsejoUser)
class ConsejoUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'rol', 'activo', 'creado')
    list_filter = ('rol', 'activo')
    search_fields = ['user__username', 'user__email']