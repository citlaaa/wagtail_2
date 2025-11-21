# from wagtail import hooks
# from django.contrib import admin
# from django.contrib.auth import get_user_model

# User = get_user_model()

# @hooks.register("register_admin_viewset")
# def register_user_admin_viewset():
#     pass

from wagtail import hooks
from wagtail.admin.viewsets.model import ModelViewSet
from .models import ConsejoUser


class ConsejoUserViewSet(ModelViewSet):
    model = ConsejoUser
    menu_label = "Usuarios del Consejo"
    menu_icon = "user"
    menu_order = 200
    add_to_admin_menu = True
    list_display = ["user", "rol", "activo", "creado"]
    search_fields = ["user__username", "user__email", "rol"]
    form_fields = ["user", "rol", "activo"]


@hooks.register("register_admin_viewset")
def register_viewset():
    return ConsejoUserViewSet("consejo_user")
