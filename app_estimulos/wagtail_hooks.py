from wagtail import hooks
from wagtail.admin.viewsets.model import ModelViewSet
from .models import EstimulosUser, EstimulosDocumento


class EstimulosUserViewSet(ModelViewSet):
    model = EstimulosUser
    menu_label = "Usuarios de Estímulos"
    menu_icon = "user"
    menu_order = 210
    add_to_admin_menu = True
    list_display = ["user", "rol", "activo", "creado"]
    search_fields = ["user__username", "user__email", "rol"]
    form_fields = ["user", "rol", "activo"]


class EstimulosDocumentoViewSet(ModelViewSet):
    model = EstimulosDocumento
    menu_label = "Documentos Estímulos"
    menu_icon = "doc-full"
    menu_order = 211
    add_to_admin_menu = True
    list_display = ["descripcion", "visible", "subido_por", "creado"]
    search_fields = ["descripcion"]
    form_fields = ["descripcion", "archivo_pdf", "visible", "subido_por"]


@hooks.register("register_admin_viewset")
def register_estimulos_user_viewset():
    return EstimulosUserViewSet("estimulos_user")


@hooks.register("register_admin_viewset")
def register_estimulos_documento_viewset():
    return EstimulosDocumentoViewSet("estimulos_documento")
