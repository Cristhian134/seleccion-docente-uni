from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
  help = "Lista todos los superusuarios creados en el sistema"

  def handle(self, *args, **kwargs):
    User = get_user_model()
    su_list = User.objects.filter(is_superuser=True)

    if not su_list.exists():
      self.stdout.write(self.style.WARNING("No existen superusuarios."))
      return

    self.stdout.write(self.style.SUCCESS("=== SUPERUSUARIOS ==="))

    for u in su_list:
      persona = getattr(u, "persona", None)
      nombre = f"{persona.nombre} {persona.apellidoPaterno} {persona.apellidoMaterno}" if persona else "—"

      self.stdout.write(
          f"- ID: {u.id} | Usuario: {u.nombreUsuario} | Código: {u.codigoUsuario} | Nombre: {nombre}"
      )
