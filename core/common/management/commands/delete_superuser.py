from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction
from core.common.models import Evaluador


class Command(BaseCommand):
  help = "Elimina un superusuario y sus modelos asociados (Persona, Evaluador)"

  def add_arguments(self, parser):
    parser.add_argument(
        "username",
        type=str,
        help="Nombre de usuario (nombreUsuario) o código (codigoUsuario) del superusuario a eliminar",
    )

  @transaction.atomic
  def handle(self, *args, **options):
    User = get_user_model()
    identifier = options["username"]

    # ——————————————————————————
    # Buscar por username o codigoUsuario
    # ——————————————————————————
    user = (
        User.objects.filter(nombreUsuario=identifier).first()
        or User.objects.filter(codigoUsuario=identifier).first()
    )

    if not user:
      self.stderr.write(self.style.ERROR(f"No existe un usuario '{identifier}'."))
      return

    if not user.is_superuser:
      self.stderr.write(
          self.style.ERROR(f"El usuario '{identifier}' no es un superusuario.")
      )
      return

    persona = getattr(user, "persona", None)

    # ——————————————————————————
    # Eliminar Evaluador
    # ——————————————————————————
    if persona:
      deleted_eval = Evaluador.objects.filter(persona=persona).delete()
      if deleted_eval[0] > 0:
        self.stdout.write(
            self.style.WARNING(f"Evaluador eliminado ({deleted_eval[0]} registros).")
        )

    # ——————————————————————————
    # Eliminar Persona
    # ——————————————————————————
    if persona:
      persona.delete()
      self.stdout.write(
          self.style.WARNING(f"Persona eliminada: {persona.dni}")
      )

    # ——————————————————————————
    # Eliminar Usuario
    # ——————————————————————————
    username_display = user.nombreUsuario
    user.delete()
    self.stdout.write(
        self.style.SUCCESS(f"Superusuario eliminado correctamente: {username_display}")
    )
