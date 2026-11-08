from django.test import TestCase
from .models import Beneficiario


class BeneficiarioModelTest(TestCase):

    def test_cadastrar_beneficiario(self):
        beneficiario = Beneficiario.objects.create(
            nome_responsavel='Maria da Silva'
        )

        self.assertEqual(beneficiario.nome_responsavel, 'Maria da Silva')
        self.assertEqual(beneficiario.status, 'ativo')

    def test_representacao_beneficiario(self):
        beneficiario = Beneficiario.objects.create(
            nome_responsavel='João Santos'
        )

        self.assertEqual(str(beneficiario), 'João Santos')
