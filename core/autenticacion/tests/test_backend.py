from django.contrib.auth import get_user_model
from django.test import TestCase

from core.autenticacion.backend import DNIOrEmailBackend
from core.common.models import Facultad, Persona


User = get_user_model()


class DNIOrEmailBackendTests(TestCase):

  def setUp(self):
    self.persona = Persona.objects.create(
        nombre="Carlos",
        apellidoPaterno="Perez",
        apellidoMaterno="Diaz",
        dni="55554444",
        correo="carlos@example.com",
        telefono="900111222",
        genero="masculino",
    )
    self.user = User.objects.create_user(
        codigoUser="carlos01",
        nombreUser="Carlos",
        claveUser="strongpass",
        facultad=Facultad.FIM,
        persona=self.persona,
    )
    self.backend = DNIOrEmailBackend()

  def test_authenticate_by_dni(self):
    authenticated = self.backend.authenticate(None, username=self.persona.dni, password="strongpass")
    self.assertEqual(authenticated, self.user)

  def test_authenticate_by_email(self):
    authenticated = self.backend.authenticate(None, username=self.persona.correo, password="strongpass")
    self.assertEqual(authenticated, self.user)

  def test_authenticate_by_codigo_usuario_fallback(self):
    authenticated = self.backend.authenticate(None, username=self.user.codigoUsuario, password="strongpass")
    self.assertEqual(authenticated, self.user)

  def test_authenticate_invalid_password_returns_none(self):
    authenticated = self.backend.authenticate(None, username=self.persona.dni, password="wrong")
    self.assertIsNone(authenticated)
