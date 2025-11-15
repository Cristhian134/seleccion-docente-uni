from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from core.common.models import Persona

User = get_user_model()


class DNIOrEmailBackend(ModelBackend):

  def authenticate(self, request, username=None, password=None, **kwargs):
    """
    Permite iniciar sesión con:
    - correo
    - dni
    """
    user = None

    # Buscar persona por DNI o correo
    try:
      persona = Persona.objects.filter(dni=username).first()

      if not persona:
        persona = Persona.objects.filter(correo=username).first()

      if persona:
        user = User.objects.filter(persona=persona).first()

      # fallback legacy: codigoUsuario
      if not user:
        user = User.objects.filter(codigoUsuario=username).first()

    except Exception as e:
      return None

    if user and user.check_password(password):
      return user

    return None
