from django.urls import include, path

urlpatterns = [
  path("", include("core.protegido.home.urls")),
  # path("", include("core.protegido.listar_docentes.urls")),
  # path("", include("core.protegido.crear_convocatoria.urls")),
  # path("", include("core.protegido.ver_convocatorias.urls")),
]
