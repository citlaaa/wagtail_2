from wagtail import hooks
from wagtail.admin.viewsets.model import ModelViewSet
from .models import EstimulosUser

class EstimulosUserViewSet(ModelViewSet):
    model = EstimulosUser
    menu_label = "Usuarios de Estímulos"
    menu_icon = "user"
    menu_order = 210  # para que aparezca debajo de Consejo
    add_to_admin_menu = True
    list_display = ["user", "rol", "activo", "creado"]
    search_fields = ["user__username", "user__email", "rol"]
    form_fields = ["user", "rol", "activo"]

@hooks.register("register_admin_viewset")
def register_viewset():
    return EstimulosUserViewSet("estimulos_user")
