from django.conf import settings
from django.urls import include, path
from django.contrib import admin

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from search import views as search_views

# Importar las vistas de cada app
from app_consejo import views as consejo_views
from app_estimulos import views as estimulos_views
from app_dictaminadora import views as dictaminadora_views

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("search/", search_views.search, name="search"),

    # URLs de la aplicación CONSEJO
    path("consejo/iniciar-sesion/", consejo_views.inicio_consejo, name="inicio_consejo"),
    path("consejo/cerrar-sesion/", consejo_views.logout_consejo, name="logout_consejo"),
    path("consejo/", consejo_views.consejo_home, name="consejo_home"),
    path("consejo/consulta/", consejo_views.consejo_consultor, name="consejo_consultor"),
    path("consejo/gestor/", consejo_views.consejo_gestor, name="consejo_gestor"),
    path("consejo/gestor/guardar/", consejo_views.consejo_guardar, name="consejo_guardar"),
    path("consejo/gestor/detalle/<int:id>/", consejo_views.consejo_detalle, name="consejo_detalle"),
    path("consejo/gestor/editar/<int:id>/", consejo_views.consejo_editar, name="consejo_editar"),
    path("consejo/gestor/eliminar/<int:id>/", consejo_views.consejo_eliminar, name="consejo_eliminar"),

    # URLs de la aplicación ESTÍMULOS
    path("estimulos/iniciar-sesion/", estimulos_views.inicio_estimulos, name="inicio_estimulos"),
    path("estimulos/cerrar-sesion/", estimulos_views.logout_estimulos, name="logout_estimulos"),
    path("estimulos/", estimulos_views.estimulos_home, name="estimulos_home"),
    path("estimulos/consulta/", estimulos_views.estimulos_consultor, name="estimulos_consultor"),
    path("estimulos/gestor/", estimulos_views.estimulos_gestor, name="estimulos_gestor"),
    path("estimulos/gestor/guardar/", estimulos_views.estimulos_guardar, name="estimulos_guardar"),
    path("estimulos/gestor/detalle/<int:id>/", estimulos_views.estimulos_detalle, name="estimulos_detalle"),
    path("estimulos/gestor/editar/<int:id>/", estimulos_views.estimulos_editar, name="estimulos_editar"),
    path("estimulos/gestor/eliminar/<int:id>/", estimulos_views.estimulos_eliminar, name="estimulos_eliminar"),

    # URLs de la aplicación DICTAMINADORA

    path("dictaminadora/iniciar-sesion/", dictaminadora_views.inicio_dictaminadora, name="inicio_dictaminadora"),
    path("dictaminadora/cerrar-sesion/", dictaminadora_views.logout_dictaminadora, name="logout_dictaminadora"),
    path("dictaminadora/", dictaminadora_views.dictaminadora_home, name="dictaminadora_home"),
    path("dictaminadora/consulta/", dictaminadora_views.dictaminadora_consultor, name="dictaminadora_consultor"),
    path("dictaminadora/gestor/", dictaminadora_views.dictaminadora_gestor, name="dictaminadora_gestor"),
    path("dictaminadora/gestor/guardar/", dictaminadora_views.dictaminadora_guardar, name="dictaminadora_guardar"),
    path("dictaminadora/gestor/detalle/<int:id>/", dictaminadora_views.dictaminadora_detalle, name="dictaminadora_detalle"),
    path("dictaminadora/gestor/editar/<int:id>/", dictaminadora_views.dictaminadora_editar, name="dictaminadora_editar"),
    path("dictaminadora/gestor/eliminar/<int:id>/", dictaminadora_views.dictaminadora_eliminar, name="dictaminadora_eliminar"),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = urlpatterns + [
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    path("", include(wagtail_urls)),
]
