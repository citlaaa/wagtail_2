from wagtail import hooks
from wagtail.admin.viewsets.model import ModelViewSet
from .models import DictaminadoraUser, DictaminadoraDocumento


class DictaminadoraUserViewSet(ModelViewSet):
    model = DictaminadoraUser
    menu_label = "Usuarios Dictaminadora"
    menu_icon = "user"
    menu_order = 220
    add_to_admin_menu = True
    list_display = ["user", "rol", "activo", "creado"]
    search_fields = ["user__username", "user__email", "rol"]
    form_fields = ["user", "rol", "activo"]


class DictaminadoraDocumentoViewSet(ModelViewSet):
    model = DictaminadoraDocumento
    menu_label = "Documentos Dictaminadora"
    menu_icon = "doc-full"
    menu_order = 221
    add_to_admin_menu = True
    list_display = ["descripcion", "visible", "subido_por", "creado"]
    search_fields = ["descripcion"]
    form_fields = ["descripcion", "archivo_pdf", "visible", "subido_por"]


@hooks.register("register_admin_viewset")
def register_dictaminadora_user_viewset():
    return DictaminadoraUserViewSet("dictaminadora_user")


@hooks.register("register_admin_viewset")
def register_dictaminadora_documento_viewset():
    return DictaminadoraDocumentoViewSet("dictaminadora_documento")
