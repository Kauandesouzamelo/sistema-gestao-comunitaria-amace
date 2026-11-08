from django.db import models


class Beneficiario(models.Model):

    STATUS_CHOICES = [
        ('ativo', 'Ativo'),
        ('inativo', 'Inativo'),
    ]

    nome_responsavel = models.CharField(
        max_length=150,
        verbose_name='Nome do responsável'
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='ativo',
        verbose_name='Status'
    )

    data_cadastro = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data de cadastro'
    )

    def __str__(self):
        return self.nome_responsavel

    class Meta:
        verbose_name = 'Beneficiário'
        verbose_name_plural = 'Beneficiários'
        ordering = ['nome_responsavel']
