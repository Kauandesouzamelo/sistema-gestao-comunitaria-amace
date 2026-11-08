from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group


class UsuarioForm(UserCreationForm):

    perfil = forms.ChoiceField(
        choices=[
            ('Coordenador', 'Coordenador'),
            ('Voluntário', 'Voluntário'),
        ],
        label='Perfil'
    )

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'perfil',
        ]

        labels = {
            'username': 'Nome de usuário',
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'email': 'E-mail',
        }

    def save(self, commit=True):
        usuario = super().save(commit=commit)

        if commit:
            grupo = Group.objects.get(name=self.cleaned_data['perfil'])
            usuario.groups.clear()
            usuario.groups.add(grupo)

        return usuario


class UsuarioEdicaoForm(forms.ModelForm):

    perfil = forms.ChoiceField(
        choices=[
            ('Coordenador', 'Coordenador'),
            ('Voluntário', 'Voluntário'),
        ],
        label='Perfil'
    )

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'perfil',
        ]

        labels = {
            'username': 'Nome de usuário',
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'email': 'E-mail',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            grupo = self.instance.groups.first()

            if grupo:
                self.fields['perfil'].initial = grupo.name

    def save(self, commit=True):
        usuario = super().save(commit=commit)

        if commit:
            grupo = Group.objects.get(
                name=self.cleaned_data['perfil']
            )
            usuario.groups.clear()
            usuario.groups.add(grupo)

        return usuario
