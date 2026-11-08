from django.test import TestCase
from django.contrib.auth.models import User, Group
from django.urls import reverse


class GestaoUsuariosTest(TestCase):

    def setUp(self):
        self.voluntario = User.objects.create_user(
            username='voluntario_teste',
            password='senha123'
        )

        grupo, criado = Group.objects.get_or_create(
            name='Voluntário'
        )

        self.voluntario.groups.add(grupo)

    def test_voluntario_nao_pode_acessar_usuarios(self):
        self.client.force_login(self.voluntario)

        resposta = self.client.get(reverse('listar_usuarios'))

        self.assertEqual(resposta.status_code, 302)

    def test_coordenador_pode_acessar_usuarios(self):
        coordenador = User.objects.create_user(
            username='coordenador_teste',
            password='senha123'
        )

        grupo, criado = Group.objects.get_or_create(
            name='Coordenador'
        )

        coordenador.groups.add(grupo)

        self.client.force_login(coordenador)

        resposta = self.client.get(reverse('listar_usuarios'))

        self.assertEqual(resposta.status_code, 200)
