from wagtail import hooks
from wagtail.admin.viewsets.model import ModelViewSet
from .models import ConsejoUser, ConsejoDocumento


class ConsejoUserViewSet(ModelViewSet):
    model = ConsejoUser
    menu_label = "Usuarios del Consejo"
    menu_icon = "user"
    menu_order = 200
    add_to_admin_menu = True
    list_display = ["user", "rol", "activo", "creado"]
    search_fields = ["user__username", "user__email", "rol"]
    form_fields = ["user", "rol", "activo"]


class ConsejoDocumentoViewSet(ModelViewSet):
    model = ConsejoDocumento
    menu_label = "Documentos Consejo"
    menu_icon = "doc-full"
    menu_order = 201
    add_to_admin_menu = True
    list_display = ["descripcion", "visible", "subido_por", "creado"]
    search_fields = ["descripcion"]
    form_fields = ["descripcion", "archivo_pdf", "visible", "subido_por"]


@hooks.register("register_admin_viewset")
def register_consejo_user_viewset():
    return ConsejoUserViewSet("consejo_user")


@hooks.register("register_admin_viewset")
def register_consejo_documento_viewset():
    return ConsejoDocumentoViewSet("consejo_documento")
