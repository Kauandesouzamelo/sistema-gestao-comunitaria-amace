from django import forms
from .models import Beneficiario


class BeneficiarioForm(forms.ModelForm):

    class Meta:
        model = Beneficiario
        fields = ['nome_responsavel', 'status']

        widgets = {
            'nome_responsavel': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o nome do responsável'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
        }
