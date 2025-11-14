from django.urls import include, path
from django.contrib.auth.views import LogoutView

urlpatterns = [
  path("", include("core.autenticacion.login.urls")),
  path("logout/", LogoutView.as_view(), name="logout"),
]
