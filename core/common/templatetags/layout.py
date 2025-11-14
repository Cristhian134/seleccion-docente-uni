from django import template
from django.contrib.auth.models import AnonymousUser

from core.common.utils import get_user_rol
from core.roles import MODULOS, ROLES

register = template.Library()


@register.inclusion_tag("layout.html", takes_context=True)
def render_layout(context):
  """
  Renderiza TODO el layout: header + sidenav + datos de usuario en un solo tag.
  """
  request = context.get("request")
  user = getattr(request, "user", AnonymousUser())

  # Datos de usuario
  if user.is_authenticated:
    persona = getattr(user, "persona", None)
    nombre_completo = (
        f"{persona.nombre} {persona.apellidoPaterno} {persona.apellidoMaterno}"
        if persona else user.codigoUsuario
    )
    facultad = getattr(user, "facultad", None)
    codigo = user.codigoUsuario
  else:
    nombre_completo = "Invitado"
    facultad = None
    codigo = None

  rol = get_user_rol(user)
  admin = rol == ROLES.ADMINISTRADOR

  # Filtrado de módulos según rol
  modulos_permitidos = [
      modulo for modulo in MODULOS
      if rol in modulo.get("roles", [])
  ]

  url_volver = context.get("url_volver", "/home")

  return {
      # HEADER
      "usuario": nombre_completo,
      "rol": rol,
      "facultad": facultad,
      "codigo": codigo,
      "admin": admin,

      # SIDENAV
      "modulos": modulos_permitidos,
      "url_volver": url_volver,
  }
