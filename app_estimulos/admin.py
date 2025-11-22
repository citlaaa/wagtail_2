from django.contrib import admin
from .models import EstimulosUser, EstimulosDocumento


@admin.register(EstimulosUser)
class EstimulosUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'rol', 'activo', 'creado')
    list_filter = ('rol', 'activo')
    search_fields = ['user__username', 'user__email']


@admin.register(EstimulosDocumento)
class EstimulosDocumentoAdmin(admin.ModelAdmin):
    list_display = ('descripcion', 'visible', 'subido_por', 'creado', 'modificado')
    list_filter = ('visible', 'creado')
    search_fields = ['descripcion']
    readonly_fields = ('creado', 'modificado')
