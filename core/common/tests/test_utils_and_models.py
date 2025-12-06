from datetime import time

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase

from core.common.models import (
  Curso,
  Decano,
  EncargadoConsejo,
  EstadoDecano,
  EstadoEncargadoConsejo,
  EstadoSeccion,
  Evaluador,
  Facultad,
  Horario,
  Persona,
  Seccion,
)
from core.common.utils import get_user_rol
from core.roles import ROLES


User = get_user_model()


class UserRoleTests(TestCase):

  def setUp(self):
    self.persona = Persona.objects.create(
        nombre="Ana",
        apellidoPaterno="García",
        apellidoMaterno="Lopez",
        dni="12345678",
        correo="ana@example.com",
        telefono="999999999",
        genero="femenino",
    )
    self.usuario = User.objects.create_user(
        codigoUser="u001",
        nombreUser="Usuario base",
        claveUser="password123",
        facultad=Facultad.FIIS,
        persona=self.persona,
    )

  def test_anonymous_user_returns_anonimo(self):
    rol = get_user_rol(AnonymousUser())
    self.assertEqual(rol, "Anonimo")

  def test_user_without_persona_attribute_returns_usuario(self):
    class DummyUser:
      is_authenticated = True
      is_superuser = False

    rol = get_user_rol(DummyUser())
    self.assertEqual(rol, "Usuario")

  def test_superuser_takes_priority(self):
    admin_persona = Persona.objects.create(
        nombre="Admin",
        apellidoPaterno="Admin",
        apellidoMaterno="User",
        dni="87654321",
        correo="admin@example.com",
        telefono="888888888",
        genero="masculino",
    )

    admin_user = User.objects.create_superuser(
        codigoUser="admin01",
        nombreUser="Superuser",
        claveUser="adminpass",
        facultad=Facultad.FC,
        persona=admin_persona,
    )

    rol = get_user_rol(admin_user)
    self.assertEqual(rol, ROLES.ADMINISTRADOR)

  def test_decano_role_detected(self):
    Decano.objects.create(persona=self.persona, estadoDecano=EstadoDecano.ACTIVO)

    rol = get_user_rol(self.usuario)
    self.assertEqual(rol, ROLES.DECANO)

  def test_encargado_consejo_role_detected(self):
    EncargadoConsejo.objects.create(
        persona=self.persona,
        estadoEncargadoConsejo=EstadoEncargadoConsejo.ACTIVO,
    )

    rol = get_user_rol(self.usuario)
    self.assertEqual(rol, ROLES.ENCARGADO_CONSEJO)

  def test_evaluador_role_detected(self):
    Evaluador.objects.create(
        persona=self.persona,
        tipoEvaluador="docente",
        estadoEvaluador="confirmado",
    )

    rol = get_user_rol(self.usuario)
    self.assertEqual(rol, ROLES.EVALUADOR)


class SeccionHorarioTests(TestCase):

  def setUp(self):
    self.curso = Curso.objects.create(
        nombreCurso="Cálculo I",
        codigoCurso="CAL101",
        creditosCurso=4,
        facultad=Facultad.FIIS,
    )
    self.seccion = Seccion.objects.create(
        curso=self.curso,
        codigoSeccion="A1",
        estadoSeccion=EstadoSeccion.ACTIVO,
    )

  def test_total_horas_sums_all_horarios(self):
    Horario.objects.create(
        seccion=self.seccion,
        dia="lunes",
        horaInicio=time(8, 0),
        horaFin=time(10, 0),
    )
    Horario.objects.create(
        seccion=self.seccion,
        dia="miercoles",
        horaInicio=time(14, 30),
        horaFin=time(16, 0),
    )

    self.assertEqual(self.seccion.total_horas, 4)
