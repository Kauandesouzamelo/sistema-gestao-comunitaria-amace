from django.contrib import admin
from .models import Beneficiario


@admin.register(Beneficiario)
class BeneficiarioAdmin(admin.ModelAdmin):
    list_display = (
        'nome_responsavel',
        'status',
        'data_cadastro',
    )

    list_filter = ('status',)

    search_fields = ('nome_responsavel',)
