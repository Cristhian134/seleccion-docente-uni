from core.common.models import Decano, EncargadoConsejo, EstadoDecano, EstadoEncargadoConsejo, Evaluador
from core.roles import ROLES


def get_user_rol(user):
  if not user.is_authenticated:
    return "Anonimo"

  persona = getattr(user, "persona", None)
  if not persona:
    return "Usuario"

  if user.is_superuser:
    return ROLES.ADMINISTRADOR

  if Decano.objects.filter(persona=persona, estadoDecano=EstadoDecano.ACTIVO).exists():
    return ROLES.DECANO

  if EncargadoConsejo.objects.filter(persona=persona, estadoEncargadoConsejo=EstadoEncargadoConsejo.ACTIVO).exists():
    return ROLES.ENCARGADO_CONSEJO

  if Evaluador.objects.filter(persona=persona).exists():
    return ROLES.EVALUADOR

  return "Usuario"
