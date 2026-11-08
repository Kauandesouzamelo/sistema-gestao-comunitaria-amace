from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UsuarioForm, UsuarioEdicaoForm


def eh_coordenador(usuario):
    return (
        usuario.is_superuser
        or usuario.groups.filter(name='Coordenador').exists()
    )


@login_required
@user_passes_test(eh_coordenador)
def cadastrar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário cadastrado com sucesso!')
            return redirect('listar_usuarios')
    else:
        form = UsuarioForm()

    return render(
        request,
        'gestao_usuarios/cadastrar.html',
        {'form': form}
    )


@login_required
@user_passes_test(eh_coordenador)
def listar_usuarios(request):
    usuarios = User.objects.prefetch_related('groups').order_by('username')

    return render(
        request,
        'gestao_usuarios/listar.html',
        {'usuarios': usuarios}
    )


@login_required
@user_passes_test(eh_coordenador)
def editar_usuario(request, usuario_id):
    usuario = get_object_or_404(User, pk=usuario_id)

    if request.method == 'POST':
        form = UsuarioEdicaoForm(request.POST, instance=usuario)

        if form.is_valid():
            # Impede que o Coordenador retire o próprio perfil
            if (
                usuario.pk == request.user.pk
                and form.cleaned_data['perfil'] != 'Coordenador'
            ):
                messages.error(
                    request,
                    'Você não pode retirar seu próprio perfil de Coordenador.'
                )
            else:
                form.save()
                messages.success(request, 'Usuário atualizado com sucesso!')
                return redirect('listar_usuarios')
    else:
        form = UsuarioEdicaoForm(instance=usuario)

    return render(
        request,
        'gestao_usuarios/editar.html',
        {'form': form, 'usuario': usuario}
    )


@login_required
@user_passes_test(eh_coordenador)
def alternar_status_usuario(request, usuario_id):
    if request.method != 'POST':
        return redirect('listar_usuarios')

    usuario = get_object_or_404(User, pk=usuario_id)

    if usuario.pk == request.user.pk:
        messages.error(
            request,
            'Você não pode desativar sua própria conta.'
        )
        return redirect('listar_usuarios')

    usuario.is_active = not usuario.is_active
    usuario.save(update_fields=['is_active'])

    if usuario.is_active:
        messages.success(request, 'Usuário ativado com sucesso!')
    else:
        messages.success(request, 'Usuário desativado com sucesso!')

    return redirect('listar_usuarios')
