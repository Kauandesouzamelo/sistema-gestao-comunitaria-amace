from django import forms
from .models import ItemDoacao, MovimentacaoEstoque
from beneficiarios.models import Beneficiario


class ItemDoacaoForm(forms.ModelForm):

    class Meta:
        model = ItemDoacao
        fields = ['nome', 'descricao', 'unidade_medida']

        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome do produto'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'unidade_medida': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex.: pacote, litro, peça'
            }),
        }


class MovimentacaoEstoqueForm(forms.ModelForm):

    class Meta:
        model = MovimentacaoEstoque
        fields = ['item', 'tipo', 'quantidade', 'beneficiario']

        widgets = {
            'item': forms.Select(attrs={
                'class': 'form-select'
            }),
            'tipo': forms.Select(attrs={
                'class': 'form-select'
            }),
            'quantidade': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1'
            }),
            'beneficiario': forms.Select(attrs={
                'class': 'form-select'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['beneficiario'].queryset = (
            Beneficiario.objects.filter(status='ativo')
        )
        self.fields['beneficiario'].required = False
