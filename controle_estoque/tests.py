from django.test import TestCase
from django.core.exceptions import ValidationError
from django.urls import reverse
from beneficiarios.models import Beneficiario
from .models import ItemDoacao, MovimentacaoEstoque
from django.contrib.auth.models import User, Permission


class EstoqueModelTest(TestCase):

    def setUp(self):
        self.produto = ItemDoacao.objects.create(
            nome='Arroz',
            unidade_medida='Pacote',
            quantidade_estoque=10
        )

        self.beneficiario = Beneficiario.objects.create(
            nome_responsavel='Maria da Silva'
        )

    def test_cadastro_produto(self):
        self.assertEqual(self.produto.nome, 'Arroz')
        self.assertEqual(self.produto.quantidade_estoque, 10)

    def test_registro_movimentacao(self):
        movimentacao = MovimentacaoEstoque.objects.create(
            item=self.produto,
            tipo='saida',
            quantidade=3,
            beneficiario=self.beneficiario
        )

        self.assertEqual(movimentacao.quantidade, 3)
        self.assertEqual(movimentacao.tipo, 'saida')

    def test_bloquear_saida_maior_que_estoque(self):
        usuario = User.objects.create_user(
            username='coordenador_teste',
            password='senha123'
        )
        usuario.user_permissions.add(
            Permission.objects.get(codename='add_movimentacaoestoque')
        )

        self.client.force_login(usuario)

        resposta = self.client.post(
            reverse('registrar_movimentacao'),
            {
                'item': self.produto.pk,
                'tipo': 'saida',
                'quantidade': 11,
                'beneficiario': self.beneficiario.pk,
            }
        )

        self.produto.refresh_from_db()

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(self.produto.quantidade_estoque, 10)
        self.assertEqual(MovimentacaoEstoque.objects.count(), 0)
        self.assertContains(resposta, 'Estoque insuficiente')

    def test_registrar_entrada_estoque(self):
        usuario = User.objects.create_user(
            username='coordenador_entrada',
            password='senha123'
        )
        usuario.user_permissions.add(
            Permission.objects.get(codename='add_movimentacaoestoque'),
            Permission.objects.get(codename='view_itemdoacao')
        )

        self.client.force_login(usuario)

        resposta = self.client.post(
            reverse('registrar_movimentacao'),
            {
                'item': self.produto.pk,
                'tipo': 'entrada',
                'quantidade': 5,
                'beneficiario': '',
            }
        )

        self.produto.refresh_from_db()

        self.assertRedirects(resposta, reverse('listar_produtos'))
        self.assertEqual(self.produto.quantidade_estoque, 15)
        self.assertEqual(MovimentacaoEstoque.objects.count(), 1)
