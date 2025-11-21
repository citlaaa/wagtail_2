from wagtail import hooks
from wagtail.admin.viewsets.model import ModelViewSet
from .models import DictaminadoraUser

class DictaminadoraUserViewSet(ModelViewSet):
    model = DictaminadoraUser
    menu_label = "Usuarios Dictaminadora"
    menu_icon = "user"
    menu_order = 220
    add_to_admin_menu = True
    list_display = ["user", "rol", "activo", "creado"]
    search_fields = ["user__username", "user__email", "rol"]
    form_fields = ["user", "rol", "activo"]

@hooks.register("register_admin_viewset")
def register_viewset():
    return DictaminadoraUserViewSet("dictaminadora_user")
