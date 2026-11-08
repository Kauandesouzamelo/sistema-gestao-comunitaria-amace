from django.db import models
from beneficiarios.models import Beneficiario


class ItemDoacao(models.Model):

    nome = models.CharField(
        max_length=150,
        verbose_name='Nome do produto'
    )

    descricao = models.TextField(
        blank=True,
        verbose_name='Descrição'
    )

    unidade_medida = models.CharField(
        max_length=30,
        verbose_name='Unidade de medida'
    )

    quantidade_estoque = models.PositiveIntegerField(
        default=0,
        verbose_name='Quantidade em estoque'
    )

    data_cadastro = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data de cadastro'
    )

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Item de doação'
        verbose_name_plural = 'Itens de doação'
        ordering = ['nome']


class MovimentacaoEstoque(models.Model):

    TIPO_CHOICES = [
        ('entrada', 'Entrada'),
        ('saida', 'Saída'),
    ]

    item = models.ForeignKey(
        ItemDoacao,
        on_delete=models.PROTECT,
        verbose_name='Produto'
    )

    beneficiario = models.ForeignKey(
        Beneficiario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Beneficiário'
    )

    tipo = models.CharField(
        max_length=10,
        choices=TIPO_CHOICES,
        verbose_name='Tipo de movimentação'
    )

    quantidade = models.PositiveIntegerField(
        verbose_name='Quantidade'
    )

    data_movimentacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data da movimentação'
    )

    def __str__(self):
        return f'{self.get_tipo_display()} - {self.item.nome} ({self.quantidade})'

    class Meta:
        verbose_name = 'Movimentação de estoque'
        verbose_name_plural = 'Movimentações de estoque'
        ordering = ['-data_movimentacao']
