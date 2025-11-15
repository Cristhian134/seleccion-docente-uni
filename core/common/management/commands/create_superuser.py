from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.common.models import EstadoEvaluador, Evaluador, Persona, TipoEvaluador


class Command(BaseCommand):
  help = "Crea un superusuario con su Persona asociada"

  def add_arguments(self, parser):
    # Permite pasar flags desde consola
    parser.add_argument("--nombre", type=str, help="Nombre del usuario")
    parser.add_argument("--apellido_pat", type=str, help="Apellido paterno")
    parser.add_argument("--apellido_mat", type=str, help="Apellido materno")
    parser.add_argument("--dni", type=str, help="DNI")
    parser.add_argument("--correo", type=str, help="Correo electrónico")
    parser.add_argument("--telefono", type=str, help="Teléfono")
    parser.add_argument("--genero", type=str, help="Género")

    parser.add_argument("--codigo", type=str, help="Código de usuario")
    parser.add_argument("--username", type=str, help="Nombre de usuario")
    parser.add_argument("--password", type=str, help="Contraseña")
    parser.add_argument("--facultad", type=str, help="Facultad")

    parser.add_argument(
        "--defaults",
        action="store_true",
        help="Usar valores por defecto (si no se pasan flags)"
    )

  def handle(self, *args, **options):

    # ==========================
    # VALORES POR DEFECTO
    # ==========================
    default_values = {
        "nombre": "root",
        "apellido_pat": "ap",
        "apellido_mat": "am",
        "dni": "12345678",
        "correo": "root@gmail.com",
        "telefono": "999999999",
        "genero": "M",

        "codigo": "root",
        "username": "root",
        "password": "root",
        "facultad": "FIIS"
    }

    def get_value(key):
      """
      Si viene una bandera --> úsala.
      Si no viene bandera --> si --defaults usar default.
      Si no usar default igual.
      (permite ambas formas).
      """
      if options.get(key):
        return options[key]
      return default_values[key]

    nombre = get_value("nombre")
    apellido_pat = get_value("apellido_pat")
    apellido_mat = get_value("apellido_mat")
    dni = get_value("dni")
    correo = get_value("correo")
    telefono = get_value("telefono")
    genero = get_value("genero")

    codigo_user = get_value("codigo")
    username = get_value("username")
    password = get_value("password")
    facultad = get_value("facultad")

    # =======================================
    # Crear Persona
    # =======================================
    persona, created_persona = Persona.objects.get_or_create(
        dni=dni,
        defaults={
            "nombre": nombre,
            "apellidoPaterno": apellido_pat,
            "apellidoMaterno": apellido_mat,
            "correo": correo,
            "telefono": telefono,
            "genero": genero,
        }
    )

    if created_persona:
      self.stdout.write(self.style.SUCCESS(f"Persona creada: {persona}"))
    else:
      self.stdout.write(self.style.WARNING(f"Persona ya existe: {persona}"))

    # =======================================
    # Crear Usuario
    # =======================================
    User = get_user_model()

    if User.objects.filter(codigoUsuario=codigo_user).exists():
      self.stdout.write(self.style.WARNING(f"Usuario con código {codigo_user} ya existe."))
      return

    if User.objects.filter(nombreUsuario=username).exists():
      self.stdout.write(self.style.WARNING(f"Usuario {username} ya existe."))
      return

    try:
      user = User.objects.create_superuser(
          codigoUser=codigo_user,
          nombreUser=username,
          claveUser=password,
          persona=persona,
          facultad=facultad,
          is_staff=True,
          is_superuser=True
      )

      Evaluador.objects.create(
          persona=persona,
          tipoEvaluador=TipoEvaluador.DOCENTE,
          estadoEvaluador=EstadoEvaluador.CONFIRMADO,
      )
      self.stdout.write(self.style.SUCCESS(f"Superusuario creado: {user}"))

    except Exception as e:
      self.stderr.write(self.style.ERROR(f"Error creando superusuario: {e}"))
